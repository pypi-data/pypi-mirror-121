# -*- coding: utf-8 -*-
# @Date    : 2020/4/7 11:01
# @Author  : stellahong (stellahong@fuzhi.ai)
# @Desc    :
import os
import sys
import numpy as np
import traceback
import psutil


def show_layer_info(layer_name, layer_out):
    print('[layer]: %s\t[shape]: %s \n%s' % (layer_name, str(layer_out.get_shape().as_list()), show_memory_use()))


def show_memory_use():
    used_memory_percent = psutil.virtual_memory().percent
    strinfo = '{}% memory has been used'.format(used_memory_percent)
    return strinfo


def import_class(import_str):
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str,
                           traceback.format_exception(*sys.exc_info())))


def import_object(import_str, *args, **kwargs):
    return import_class(import_str)(*args, **kwargs)


def import_module(import_str):
    __import__(import_str)
    return sys.modules[import_str]

def color_msg(msg, color="red"):
    if color == "red":
        return '\033[31m{}\033[0m'.format(msg)

    elif color == "blue":
        return '\033[34m{}\033[0m'.format(msg)

    elif color == "yellow":
        return '\033[33m{}\033[0m'.format(msg)

    elif color == "green":
        return '\033[36m{}\033[0m'.format(msg)


# onhot encode to category
def ohe2cat(label):
    return np.argmax(label, axis=1)

def cat2oht(y, num_class):
    array = np.zeros((y.shape[0], num_class))
    for id, idx in enumerate(y):
        array[id][idx - 1] = 1
    return array
print(cat2oht(np.array([1,0,2,1,0,1]),3))