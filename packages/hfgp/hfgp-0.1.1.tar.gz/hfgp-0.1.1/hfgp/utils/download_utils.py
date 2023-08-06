# -*- coding: utf-8 -*-
# @Date    : 2021/9/27 16:23
# @Author  : stellahong (stellahong@fuzhi.ai)
# @Desc    :

import os

def download(MODEL_HUB_PATH, model_name):
    model_dir = os.path.join(MODEL_HUB_PATH, model_name)
    os.makedirs(model_dir)
    os.system(f"wget -P {model_dir} 192.168.50.198/{model_name}/config.json")
    os.system(f"wget -P {model_dir} 192.168.50.198/{model_name}/tokenizer.json")
    os.system(f"wget -P {model_dir} 192.168.50.198/{model_name}/tokenizer_config.json")
    os.system(f"wget -P {model_dir} 192.168.50.198/{model_name}/vocab.txt")
    os.system(f"wget -P {model_dir} 192.168.50.198/{model_name}/pytorch_model.bin")