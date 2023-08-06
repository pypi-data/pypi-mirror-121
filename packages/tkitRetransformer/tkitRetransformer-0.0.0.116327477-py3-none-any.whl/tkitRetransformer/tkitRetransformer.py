# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel,BertConfig,AutoModel,AutoConfig
import os
class tkitRetransformer:
    """
    tkitRetransformer
    用来修改transformers模型
    
    """
    def __init__(self,from_pretrained,tokenizer):
        """[模块说明]
        """
        MODEL_NAME=from_pretrained
        self.tokenizer=tokenizer


        self.config = AutoConfig.from_pretrained(MODEL_NAME)
        # tokenizer = BertTokenizer.from_pretrained(tokenizer_MODEL_NAME)

        self.model = AutoModel.from_pretrained(MODEL_NAME)
        pass
    def edit(self):
        """Edit
        基本的模型编辑示例

        """
        self.config.position_embedding_type="relative_key_query"
        self.config.vocab_size=tokenizer.vocab_size
        self.config.type_vocab_size=100
        # tokenizer
        self.model.embeddings.word_embeddings=nn.Embedding(self.tokenizer.vocab_size, self.model.embeddings.word_embeddings.embedding_dim, padding_idx=self.tokenizer.pad_token_id)
        # 修改嵌入类型
        # help(model.embeddings.token_type_embeddings)

        self.model.embeddings.token_type_embeddings=nn.Embedding(self.config.type_vocab_size, self.model.embeddings.token_type_embeddings.embedding_dim)
    def save(self, path='./model'):
        """Save the model

        path：为保存模型的目录

        """
        self.config.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        PATH=os.path.join(path,"pytorch_model.bin")
        torch.save(self.model.state_dict(), PATH)
        print("model save to:",path)


if __name__ == "__main__":
    print("测试保存模型")
    MODEL_NAME="uer/chinese_roberta_L-2_H-512"
    tokenizer_MODEL_NAME="clue/roberta_chinese_clue_tiny"
    tokenizer = BertTokenizer.from_pretrained(tokenizer_MODEL_NAME)
    trt=tkitRetransformer(MODEL_NAME,tokenizer)
    trt.save()