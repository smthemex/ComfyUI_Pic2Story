# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class Pic2Story:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True, "default": "a photography of"}),
                "repo_id": ("STRING",
                               {"default": "abhijit2111/Pic2Story"}),
                "inference_mode": (["gpu_float16", "gpu", "cpu"],),
                "get_model_online": ("BOOLEAN", {"default": True},)
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "pic_to_story"
    CATEGORY = "Pic2Story"

    def tensor_to_image(self, tensor):
        tensor = tensor.cpu()
        image_np = tensor.squeeze().mul(255).clamp(0, 255).byte().numpy()
        image = Image.fromarray(image_np, mode='RGB')
        return image

    def pic_to_story(self, image, prompt, repo_id, inference_mode, get_model_online):
        if image == None:
            raise ValueError("need a picture")
        if not repo_id:
            raise ValueError("need a repo_id or local_model_path ")
        else:
            if not get_model_online:
                os.environ['TRANSFORMERS_OFFLINE'] = "1"
                
            processor = BlipProcessor.from_pretrained(repo_id)

            pil_image = self.tensor_to_image(image)

            try:
                if inference_mode == "gpu_float16":
                    model = BlipForConditionalGeneration.from_pretrained(repo_id,
                                                                         torch_dtype=torch.float16).to("cuda")
                    if not prompt:
                        # unconditional image captioning
                        inputs = processor(pil_image, return_tensors="pt").to("cuda", torch.float16)
                    else:
                        # conditional image captioning
                        inputs = processor(pil_image, prompt, return_tensors="pt").to("cuda", torch.float16)
                    out = model.generate(**inputs)
                    story_out = processor.decode(out[0], skip_special_tokens=True)
                    print(type(story_out))

                    return (story_out,)
                elif inference_mode == "gpu":
                    model = BlipForConditionalGeneration.from_pretrained(repo_id).to("cuda")
                    if not prompt:
                        # unconditional image captioning
                        inputs = processor(pil_image, return_tensors="pt").to("cuda")
                    else:
                        # conditional image captioning
                        inputs = processor(pil_image, prompt, return_tensors="pt").to("cuda")
                    out = model.generate(**inputs)
                    story_out = processor.decode(out[0], skip_special_tokens=True)
                    return (story_out,)
                else:
                    model = BlipForConditionalGeneration.from_pretrained(repo_id)
                    if not prompt:
                        # unconditional image captioning
                        inputs = processor(pil_image, return_tensors="pt")
                    else:
                        # conditional image captioning
                        inputs = processor(pil_image, prompt, return_tensors="pt")
                    out = model.generate(**inputs)

                    story_out = processor.decode(out[0], skip_special_tokens=True)
                    return (story_out,)
            except Exception as e:
                print(e)


NODE_CLASS_MAPPINGS = {
    "Pic2Story": Pic2Story
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Pic2Story": "Pic2Story"

}
