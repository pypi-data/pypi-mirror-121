import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import gin
import torch
import numpy as np

from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, AutoModelForQuestionAnswering, \
    AutoModelForTokenClassification
from torch.utils.data.dataloader import DataLoader

from hfgp.base.hf_operator import BaseTrainer
from hfgp.evaluator.sentence_transformer_evaluator import CEAucEvaluator
from hfgp.conf.config import MODEL_SAVE_PATH, MODEL_HUB_PATH

from hfgp.utils.data_utils import convert2clssample
from hfgp.utils.download_utils import download

@gin.configurable
class HFTaskModel():
    # Constructor parameters become configurable.
    def __init__(self,
                 task='',
                 model_name='',
                 backbone=None):
        self.task = task
        self.model_name = model_name
        self.backbone = backbone
        self.__load__()
    
    def __load__(self):
        """
        根据定义的任务类型加载HF模型，目前只支持文本分类，问答匹配，文本序列
        :return:
        """
        if not os.path.exists(MODEL_HUB_PATH + os.sep + self.model_name):
            try:
                download(MODEL_HUB_PATH, self.model_name)
            except:
                raise ValueError("Download Error!")
        if self.task == "text_classification":
            model = AutoModelForSequenceClassification.from_pretrained(MODEL_HUB_PATH + os.sep + self.model_name)
        elif self.task == "token_classification":
            model = AutoModelForTokenClassification.from_pretrained(MODEL_HUB_PATH + os.sep + self.model_name)
        elif self.task == "question_and_answer":
            model = AutoModelForQuestionAnswering.from_pretrained(MODEL_HUB_PATH + os.sep + self.model_name)
        else:
            model = None
            raise NotImplementedError
        self.backbone.load(model, self.model_name)


@gin.configurable
class HFOp(BaseTrainer):
    def __init__(self, meta_data, hf_model):
        """
        HFGP类，实现统一HF模型接入
        :param metadata: a dict formed like:
            {"class_num": 10,
             "language": ZH,
             "num_train_instances": 10000,
             "num_test_instances": 1000,
             "time_budget": 300}
 
        """
        super().__init__()
        self.meta_data = meta_data
        self.hf_model = hf_model
        self.train_dataloader = None
        self.eval_dataloader = None
        self.best_score = 0.0
        self.output_path = MODEL_SAVE_PATH  # 训练模型存储文件夹路径
    
    def fit(self, x_train, y_train, remaining_time_budget=None, **kwargs):
        y_train = y_train.astype(int)
        
        num_class = kwargs["label_num"]
        max_length = kwargs["max_length"]
    
        print(y_train.shape)
        self._init_data_loader(x_train, y_train, num_class=num_class)
        self.hf_model.backbone.build(num_class, max_length)
        
        # fit
        self.hf_model.backbone.fit(train_dataloader=self.train_dataloader,
                                   evaluator=self.evaluator,
                                   output_path=self.output_path)
        
        print("best val auc is {}".format(self.hf_model.backbone.best_score))
        
        self.best_score = self.hf_model.backbone.best_score
        best_predictions = self.predict(self.evaluator.sentence_pairs)
        print("best_predictions", best_predictions)
        return best_predictions
    
    def predict(self, x_test, remaining_time_budget=None):
        return self.hf_model.backbone.predict(x_test)
    
    def save(self, path="./"):
        pass
    
    def load_weights(self, checkpoint):
        """
        实际加载权重，权重更新到GPU，赋值到实际attr
        :param checkpoint:
        :return:
        """
        checkpoint_model = os.path.join(checkpoint, "pytorch_model.bin")
        device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        
        model_state_dict = torch.load(checkpoint_model, map_location=device)
        self.hf_model.model.load_state_dict(model_state_dict)
        self.hf_model.tokenizer.from_pretrained(checkpoint)
    
    def _init_data_loader(self, x_train, y_train, num_class):
        train_x, valid_x, train_y, valid_y = train_test_split(x_train, y_train, test_size=0.2, random_state=42)
        train_data_y = np.argmax(train_y, axis=1)
        train_samples = convert2clssample(train_x, train_data_y)
        self.train_dataloader = DataLoader(train_samples, shuffle=True,
                                           batch_size=self.hf_model.backbone.train_batch_size)
        dev_samples = convert2clssample(valid_x, valid_y)
        self.evaluator = CEAucEvaluator.from_input_examples(dev_samples, name='dev', num_class=num_class)
    
    def load(self, path="./"):
        """
        加载训练好的模型权重
        :param path: 待加载的模型权重文件夹路径
        :return:
        """
        self.load_weights(checkpoint=path)


if __name__ == "__main__":
    import os
    
    code_dir = os.path.dirname(__file__)
    meta_data = {"class_num": 10,
                 "language": 'ZH',
                 "num_train_instances": 10000,
                 "num_test_instances": 1000,
                 "time_budget": 300}
    print(code_dir)
    if (os.path.exists(os.path.join(code_dir, 'hf_gp.gin'))):
        gin.parse_config_file(os.path.join(code_dir, 'hf_gp.gin'))
    
    model = HFOp(meta_data)
    print(model.hf_model.backbone.model_name)
