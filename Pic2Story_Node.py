# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def tensor_to_image(tensor):
    image_np = tensor.squeeze().mul(255).clamp(0, 255).byte().numpy()
    image = Image.fromarray(image_np, mode='RGB')
    return image

class Pic2Story_Loader:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "repo_id": ("STRING",{"default": "abhijit2111/Pic2Story"}),
                "inference_mode": (["gpu_float16", "gpu", "cpu"],),
            }
        }
    
    RETURN_TYPES = ("PICMODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_main"
    CATEGORY = "Pic2Story"
    
    def load_main(self, repo_id, inference_mode):
        if not repo_id:
            raise ValueError("need a repo_id or local_model_path ")
        if "Pic2Story" in repo_id:
            mode="story"
        else:
            mode = "paligemma"
        if mode=="story":
            if inference_mode == "gpu_float16":
                model = BlipForConditionalGeneration.from_pretrained(repo_id,
                                                                     torch_dtype=torch.float16).to("cuda")
            elif inference_mode == "gpu":
                model = BlipForConditionalGeneration.from_pretrained(repo_id).to("cuda")
            else:
                model = BlipForConditionalGeneration.from_pretrained(repo_id)
            processor = BlipProcessor.from_pretrained(repo_id)
        else:
            from transformers import PaliGemmaForConditionalGeneration, PaliGemmaProcessor
            
            #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            device = "cpu" if "cpu" in inference_mode else "cuda"
            model = PaliGemmaForConditionalGeneration.from_pretrained(
                repo_id,
                torch_dtype=torch.bfloat16,
                local_files_only=True
            ).to(device)
            processor = PaliGemmaProcessor.from_pretrained(repo_id, local_files_only=True)
        model={"model":model,"processor":processor,"inference_mode":inference_mode,"mode":mode}
            
        return (model,)
        

class Pic2Story_Sampler:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": ("PICMODEL",),
                "prompt": ("STRING", {"default": "a photography of"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "pic_to_story"
    CATEGORY = "Pic2Story"

   
    def pic_to_story(self, image,model, prompt):
        processor=model.get("processor")
        mode=model.get("mode")
        inference_mode=model.get("inference_mode")
        model=model.get("model")
        pil_image = tensor_to_image(image)
        if mode=="story":
            if inference_mode == "gpu_float16":
                if not prompt:
                    # unconditional image captioning
                    inputs = processor(pil_image, return_tensors="pt").to("cuda", torch.float16)
                    print("processor image without prompt")
                else:
                    # conditional image captioning
                    inputs = processor(pil_image, prompt, return_tensors="pt").to("cuda", torch.float16)
                out = model.generate(**inputs)
                story_out = processor.decode(out[0], skip_special_tokens=True)
                print(type(story_out))
                
                return (story_out,)
            elif inference_mode == "gpu":
                if not prompt:
                    # unconditional image captioning
                    inputs = processor(pil_image, return_tensors="pt").to("cuda")
                    print("processor image without prompt")
                else:
                    # conditional image captioning
                    inputs = processor(pil_image, prompt, return_tensors="pt").to("cuda")
                out = model.generate(**inputs)
                story_out = processor.decode(out[0], skip_special_tokens=True)
                return (story_out,)
            else:
                if not prompt:
                    # unconditional image captioning
                    inputs = processor(pil_image, return_tensors="pt")
                    print("processor image without prompt")
                else:
                    # conditional image captioning
                    inputs = processor(pil_image, prompt, return_tensors="pt")
                out = model.generate(**inputs)
                
                story_out = processor.decode(out[0], skip_special_tokens=True)
        else:
            device ="cpu" if "cpu" in inference_mode else "cuda"
            
            if not prompt:
                prompt= "describe en\n"
            inputs = processor(text=prompt, images=pil_image,
                               padding="longest", do_convert_rgb=True, return_tensors="pt").to(device)
            inputs = inputs.to(dtype=model.dtype)
            
            with torch.no_grad():
                output = model.generate(**inputs, max_new_tokens=128)
            
            story_out = processor.decode(output[0], skip_special_tokens=True)
            
            story_out=story_out.splitlines()[-1]
        return (story_out,)


NODE_CLASS_MAPPINGS = {
    "Pic2Story_Loader":Pic2Story_Loader,
    "Pic2Story_Sampler": Pic2Story_Sampler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Pic2Story_Loader":"Pic2Story_Loader",
    "Pic2Story_Sampler": "Pic2Story_Sampler"

}
