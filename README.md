# ComfyUI_Pic2Story

ComfyUI simple node based on BLIP method, with the function of "Image to Txt " .   

Original model: [link](https://huggingface.co/Salesforce/blip-image-captioning-large)    
Using model: [link](https://huggingface.co/abhijit2111/Pic2Story)    

1.Installation
-----
  1.1 In the .\ComfyUI \ custom_node directory, run the following:  
  
  ```
  git clone https://github.com/smthemex/ComfyUI_Pic2Story.git
  ```
 
  1.2 using repo_id or offline   
  
  repo_id:  abhijit2111/Pic2Story   [link](https://huggingface.co/abhijit2111/Pic2Story/tree/main)   
  repo_id:  google/paligemma2-3b-pt-896  [link](https://huggingface.co/google/paligemma2-3b-pt-896/tree/main)  


2.Example
---
Prompt is not necessary! 提示词不是必须的,可以去掉.   
 ![](https://github.com/smthemex/ComfyUI_Pic2Story/blob/main/example.png)
 


4.Citation
------

``` python  
@misc{https://doi.org/10.48550/arxiv.2201.12086,
  doi = {10.48550/ARXIV.2201.12086},
  
  url = {https://arxiv.org/abs/2201.12086},
  
  author = {Li, Junnan and Li, Dongxu and Xiong, Caiming and Hoi, Steven},
  
  keywords = {Computer Vision and Pattern Recognition (cs.CV), FOS: Computer and information sciences, FOS: Computer and information sciences},
  
  title = {BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation},
  
  publisher = {arXiv},
  
  year = {2022},
  
  copyright = {Creative Commons Attribution 4.0 International}
}
```
