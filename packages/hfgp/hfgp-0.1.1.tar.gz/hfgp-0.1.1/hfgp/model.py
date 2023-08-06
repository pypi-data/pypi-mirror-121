# -*- coding: utf-8 -*-

import re
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

import os

os.system('pip install jieba')
os.system("pip install transformers==4.9.1")
os.system("pip install gin-config==0.3.0")
import jieba
import gin

from hf_gp import HFOp

MAX_VOCAB_SIZE = 20000


# code form https://towardsdatascience.com/multi-class-text-classification-with-lstm-1590bee1bd17
def clean_en_text(dat):
    REPLACE_BY_SPACE_RE = re.compile('["/(){}\[\]\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-zA-Z #+_]')
    
    ret = []
    for line in dat:
        # text = text.lower() # lowercase text
        line = REPLACE_BY_SPACE_RE.sub(' ', line)
        line = BAD_SYMBOLS_RE.sub('', line)
        line = line.strip()
        ret.append(line)
    return ret


def clean_zh_text(dat):
    REPLACE_BY_SPACE_RE = re.compile('[“”【】/（）：！～「」、|，；。"/(){}\[\]\|@,\.;]')
    
    ret = []
    for line in dat:
        line = REPLACE_BY_SPACE_RE.sub(' ', line)
        line = line.strip()
        ret.append(line)
    return ret


def _tokenize_chinese_words(text):
    return ' '.join(jieba.cut(text, cut_all=False))


def vectorize_data(x_train, x_val=None):
    vectorizer = TfidfVectorizer(ngram_range=(1, 1), max_features=MAX_VOCAB_SIZE)
    if x_val:
        full_text = x_train + x_val
    else:
        full_text = x_train
    vectorizer.fit(full_text)
    train_vectorized = vectorizer.transform(x_train)
    if x_val:
        val_vectorized = vectorizer.transform(x_val)
        return train_vectorized, val_vectorized, vectorizer
    return train_vectorized, vectorizer


# onhot encode to category
def ohe2cat(label):
    return np.argmax(label, axis=1)


class model(object):
    """ model of SVM baseline """
    
    def __init__(self, metadata):
        """ Initialization for model
        :param metadata: a dict formed like:
            {"class_num": 10,
             "language": ZH,
             "num_train_instances": 10000,
             "num_test_instances": 1000,
             "time_budget": 300}
        """
        self.done_training = False
        self.metadata = metadata
        self.train_output_path = './'
        self.test_input_path = './'
        self.model = LinearSVC(random_state=0, tol=1e-5, max_iter=500)
        code_dir = os.path.dirname(__file__)
        if (os.path.exists(os.path.join(code_dir, 'hf_gp.gin'))):
            gin.parse_config_file(os.path.join(code_dir, 'hf_gp.gin'))
        self.op = HFOp(metadata)
        print("load HF Op!")
        
        self.tokenizer = TfidfVectorizer()
    
    def fit(self, x_train, y_train, remaining_time_budget=None):
        
        """model training on train_dataset.
        
        :param train_dataset: tuple, (x_train, y_train)
            x_train: list of str, input training sentences.
            y_train: A `numpy.ndarray` matrix of shape (sample_count, class_num).
                     here `sample_count` is the number of examples in this dataset as train
                     set and `class_num` is the same as the class_num in metadata. The
                     values should be binary.
        :param remaining_time_budget:
        """
        if self.done_training:
            return
        # tokenize Chinese words
        if self.metadata['language'] == 'ZH':
            print(x_train.shape)
            
            x_train = clean_zh_text(x_train)
            x_train = list(map(_tokenize_chinese_words, x_train))
            print(x_train)
        else:
            x_train = clean_en_text(x_train)
        
        # x_train, self.tokenizer = vectorize_data(x_train)
        # model = LinearSVC(random_state=0, tol=1e-5, max_iter=500)
        print(str(type(x_train)) + " " + str(y_train.shape))
        
        kwargs = {"label_num": self.metadata["class_num"],
                  "max_length": 128}
       
        self.op.fit(x_train, y_train, remaining_time_budget,  **kwargs)
        self.model = self.op
        # with open(self.train_output_path + 'model.pickle', 'wb') as handle:
        #     pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        # with open(self.train_output_path + 'tokenizer.pickle', 'wb') as handle:
        #     pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        self.done_training=True
    
    def predict(self, x_test, remaining_time_budget=None):
        """
        :param x_test: list of str, input test sentences.
        :param remaining_time_budget:
        :return: A `numpy.ndarray` matrix of shape (sample_count, class_num).
                 here `sample_count` is the number of examples in this dataset as test
                 set and `class_num` is the same as the class_num in metadata. The
                 values should be binary or in the interval [0,1].
        """
        # with open(self.test_input_path + 'model.pickle', 'rb') as handle:
        #     model = pickle.load(handle, encoding='iso-8859-1')
        # with open(self.test_input_path + 'tokenizer.pickle', 'rb') as handle:
        #     tokenizer = pickle.load(handle, encoding='iso-8859-1')
        
        train_num, test_num = self.metadata['train_num'], self.metadata['test_num']
        class_num = self.metadata['class_num']
        
        # tokenizing Chinese words
        if self.metadata['language'] == 'ZH':
            x_test = clean_zh_text(x_test)
            x_test = list(map(_tokenize_chinese_words, x_test))
        else:
            x_test = clean_en_text(x_test)

        result = self.model.predict(x_test)
        print(result)
        return result
        # return y_test
    
    def save(self, path="./"):
        '''
        Save a trained model.
        '''
        pass
    
    def load(self, path="./"):
        '''
        Load a trained model.
        '''
        pass
