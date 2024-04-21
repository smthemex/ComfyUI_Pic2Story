# ComfyUI_Pic2Story

ComfyUI simple node based on BLIP method, with the function of "Image to Txt " .   

Original model: [link](https://huggingface.co/Salesforce/blip-image-captioning-large)    
Using model: [link](https://huggingface.co/abhijit2111/Pic2Story)    

1.Installation
-----
  1.1 In the .\ComfyUI \ custom_node directory, run the following:  
  
  ``` python 
  git clone https://github.com/smthemex/ComfyUI_Pic2Story.git
  ```
  1.2 using it

  1.3 Download the model 
  
  Model download method 1: Use model_path(repo_id) download directly   
  ----
  
  ![](https://github.com/smthemex/ComfyUI_Pic2Story/blob/main/example/example.png)
    
  Model download method 2：如果无法直连huggingface  
  ---
  
 方法a,直接浏览器下载模型：   
    
 下载[link](https://huggingface.co/abhijit2111/Pic2Story/tree/main)所有文件到一个你喜欢的的路径，路径名不要有中文，路径所有“\”要换成“/”，在model_path填写你的路径，例如 X:/XX/XXX,关闭get_model_online,即可使用。  

 方法B,用我做的另一个模型下载节点：（比如你懒得去浏览器下载）  

 把主节点的model_path转为输入，然后链接模型下载节点，模型默认下载至comfyUI的diffuse目录下（你也可以改成任何你喜欢的），其他参数不要动，注意hf_mirror是开启的，不然下载速度会很慢或者直接下载不了。 等下载完成即可使用，下次再用也不用再使用改模型下载节点，直接用模型保存路径以及开启离线使用即可。  

Citation
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
