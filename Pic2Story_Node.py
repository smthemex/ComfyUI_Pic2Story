# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class DownloadModel:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "repo_id": ("STRING",
                            {"default": "abhijit2111/Pic2Story"}),
                "model_local_dir": ("STRING",
                                    {"default": "./models/diffusers"}),
                "max_workers": ("INT", {"default": 4, "min": 1, "max": 8, "step": 1, "display": "slider"}),
                "local_dir_use_symlinks": ("BOOLEAN", {"default": True},),
                "use_hf_mirror": ("BOOLEAN", {"default": True},)
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_path",)
    FUNCTION = "download_model"
    CATEGORY = "Pic2Story"

    def hf_mirror(self, use_hf_mirror):
        if use_hf_mirror:
            os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        else:
            os.environ['HF_ENDPOINT'] = 'https://huggingface.co'
        return os.environ['HF_ENDPOINT']

    def download_model(self, repo_id, model_local_dir, max_workers, local_dir_use_symlinks, use_hf_mirror):
        self.hf_mirror(use_hf_mirror)
        from huggingface_hub import snapshot_download

        model_path = f"{model_local_dir}/{repo_id.split('/')[-1]}"  # 本地模型存储的地址
        # 开始下载
        snapshot_download(
            repo_id=repo_id,
            local_dir=model_path,
            local_dir_use_symlinks=local_dir_use_symlinks,  # 为false时，但是本地模型使用文件保存，而非blob形式保存，但是每次使用得重新下载。
            max_workers=max_workers
            # token=token,“在hugging face上生成的 自己的access token， 否则模型下载可能会中断”
            # proxies = {"https": "http://localhost:7890"},  # 可选代理端口
        )
        return (model_path,)


class Pic2Story:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True, "default": "a photography of"}),
                "model_path": ("STRING",
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

    def get_model(self, get_model_online):
        if get_model_online:
            os.environ['TRANSFORMERS_OFFLINE'] = "0"
        else:
            os.environ['TRANSFORMERS_OFFLINE'] = "1"
        return os.environ['TRANSFORMERS_OFFLINE']

    def pic_to_story(self, image, prompt, model_path, inference_mode, get_model_online):
        if image == None:
            raise ValueError("need a picture")
        if not model_path:
            raise ValueError("need a model_path")
        else:
            self.get_model(get_model_online)

            processor = BlipProcessor.from_pretrained(model_path)

            pil_image = self.tensor_to_image(image)

            try:
                if inference_mode == "gpu_float16":
                    model = BlipForConditionalGeneration.from_pretrained(model_path,
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
                    model = BlipForConditionalGeneration.from_pretrained(model_path).to("cuda")
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
                    model = BlipForConditionalGeneration.from_pretrained(model_path)
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
                e = ("Notice: When using \'use_model_offline\', the model path must be the path of existing "
                     "pre downloaded models.\n 注意： 使用\'use_model_offline\'模式时，模型路径必须是已有预下载模型的路径")
                print(e)


NODE_CLASS_MAPPINGS = {
    "DownloadModel": DownloadModel,
    "Pic2Story": Pic2Story
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DownloadModel": "DownloadModel",
    "Pic2Story": "Pic2Story"

}
