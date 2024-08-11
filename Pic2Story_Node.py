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
    
    RETURN_TYPES = ("MODEL","MODEL","STRING",)
    RETURN_NAMES = ("model","processor","info")
    FUNCTION = "load_main"
    CATEGORY = "Pic2Story"
    
    def load_main(self, repo_id, inference_mode):
        if not repo_id:
            raise ValueError("need a repo_id or local_model_path ")
        if inference_mode == "gpu_float16":
            model = BlipForConditionalGeneration.from_pretrained(repo_id,
                                                                 torch_dtype=torch.float16).to("cuda")
        elif inference_mode == "gpu":
            model = BlipForConditionalGeneration.from_pretrained(repo_id).to("cuda")
        else:
            model = BlipForConditionalGeneration.from_pretrained(repo_id)
        processor = BlipProcessor.from_pretrained(repo_id)
        return (model,processor,inference_mode,)
        

class Pic2Story_Sampler:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": ("MODEL",),
                "processor": ("MODEL",),
                "info": ("STRING", {"forceInput": True, "default": ""}),
                "prompt": ("STRING", {"default": "a photography of"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "pic_to_story"
    CATEGORY = "Pic2Story"

   

    def pic_to_story(self, image,model,processor,info, prompt):

        pil_image = tensor_to_image(image)

        if info == "gpu_float16":
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
        elif info == "gpu":
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
            return (story_out,)


NODE_CLASS_MAPPINGS = {
    "Pic2Story_Loader":Pic2Story_Loader,
    "Pic2Story_Sampler": Pic2Story_Sampler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Pic2Story_Loader":"Pic2Story_Loader",
    "Pic2Story_Sampler": "Pic2Story_Sampler"

}
