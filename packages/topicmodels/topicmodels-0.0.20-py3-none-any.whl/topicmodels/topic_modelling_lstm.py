import tensorflow
import torch
import keras
from tensorflow.keras.callbacks import LambdaCallback
import eval_measure
from corpus import DocData,DocDatalstm
import ldann
from ldann import Doc2Topic,Logger,data_feeder,Doc2Topiclstm
from eval_measure import custom_evaluator
import os
import collections
import numpy as np
import random
import json
import pandas as pd
import fasttext
from scipy import spatial


def topicmodelinglstm(file_name,weight_dir,epochs=1,no_topic=10,topic_word=5,column_name='clean_text'):
#     datapathlstm=os.path.join(path_name)
#     weight_dir=weight_dir
    datalstm = DocDatalstm(file_name, ns_rate=1, min_count=1,column_name=column_name)
    datalstm.count_cooccs(os.path.join(r"stt_lemmas_lstm.json"))
    datalstm.load_cooccs(os.path.join(r"stt_lemmas_lstm.json"))
    f=8
    lr=0.015
    modellstm = Doc2Topiclstm(datalstm, n_topics=no_topic, batch_size=1024*f, n_epochs=epochs, lr=lr, l1_doc=0.0000002, l1_word=0.000000015)
    topicwordnn=modellstm.get_topic_words(top_n=topic_word)
    
    totalsum=0.0
    finaltopics=[]
    for i in range(no_topic):
        tmptopic=''
        for j in range(topic_word):
            totalsum+=topicwordnn[i][j][1]
            tmptopic+=topicwordnn[i][j][0]
            if j<(topic_word-1):
                tmptopic+=' ,'
#         print(tmptopic)
        finaltopics.append(tmptopic)
    totalsum/=no_topic
    score=totalsum
#     totalsum/=topic_word
    finaltopics=pd.DataFrame({'topic':finaltopics})
    return finaltopics,score