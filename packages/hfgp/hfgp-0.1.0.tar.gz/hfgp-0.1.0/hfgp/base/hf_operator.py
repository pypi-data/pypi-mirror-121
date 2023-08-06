import os

import gin

from transformers import AutoConfig, AutoTokenizer

from hfgp.conf.config import MODEL_HUB_PATH
from hfgp.base.cls_model_op import SentenceEncoder


@gin.configurable
class BaseTrainer():
    """
    预训模型训练基类
    预训练模型算子基类，加载Huggingface Models Repository中的模型
    定义对应具体模型可调参数
    """
    
    def __init__(self,
                 lr=2e-5,
                 epoch=5,
                 warmup_steps=1000,
                 weight_decay=0.01,
                 train_batch_size=16,
                 max_length=128
                 ):
        self.epoch = epoch
        self.lr = lr
        self.warmup_steps = warmup_steps
        self.weight_decay = weight_decay
        self.train_batch_size = train_batch_size
        self.max_length = max_length
        
        self.model_hub_path = MODEL_HUB_PATH  # 预训练模型加载文件夹路径
        self.best_score = -9999999
    
    def load(self, task_model, model_name):
        self.model_name = model_name
        self.config = AutoConfig.from_pretrained(MODEL_HUB_PATH + os.sep + model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_HUB_PATH + os.sep + model_name)
        self.ptm = task_model  # ptm: pre-train-model
    
    def build(self, num_classes, max_length, device=None):
        self.model = SentenceEncoder(self.ptm,
                                     self.tokenizer,
                                     self.config,
                                     num_labels=num_classes,
                                     max_length=max_length,
                                     device=device)
    
    def fit(self, train_dataloader, evaluator, output_path):
        self.model.fit(train_dataloader=train_dataloader,
                       evaluator=evaluator,
                       epochs=self.epoch,
                       evaluation_steps=100,
                       optimizer_params={"lr": self.lr},
                       callback=self.show_score_callback,
                       save_best_model=True,
                       output_path=output_path)
        self.best_score = self.model.best_score
        
    def predict(self, test_data):
        sentneces = [[" ".join(x[0].split(" "))[:]] for x in test_data]
        predictions = self.model.predict(sentences=sentneces, batch_size=32, convert_to_numpy=True, apply_softmax=True)
        return predictions
    
    @staticmethod
    def show_score_callback(score, epoch, steps):
        print(score, epoch, steps)
