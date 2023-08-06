from transformers import BertTokenizer
import onnxruntime
import onnx,os
import numpy as np
# import os
# # tokenizer = BertTokenizer.from_pretrained("out/")
# # tokenizer.save_pretrained("out")
# # print(dir(tokenizer))

# path =os.path.dirname(tkitSeg.__file__)
# print(path)
def to_numpy(tensor):
    """[summary]
    生成np数据
    Args:
        tensor ([type]): [description]

    Returns:
        [type]: [description]
    """
    # return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()
    return np.array(tensor)
# def softmax(x):

#     f_x = np.exp(x) / np.sum(np.exp(x))
#     return f_x


def softmax(x):
    """[summary]
    
    转化成为概率

    Args:
        x ([type]): [description]

    Returns:
        [type]: [description]
    """

    # returns max of each row and keeps same dims
    max = np.max(x, axis=-1, keepdims=True)
    e_x = np.exp(x - max)  # subtracts each row with its max value
    # returns sum of each row and keeps same dims
    sum = np.sum(e_x, axis=-1, keepdims=True)
    f_x = e_x / sum
    max = np.max(x, axis=-1, keepdims=True)
    return f_x, np.argmax(x, axis=-1)


# def bulidToken_type_ids(attention_mask, Token_type=99):
#     """
#     构建新的类型矩阵
#     Pytorch 替换tensor中大于某个值的所有元素
#     https://blog.csdn.net/lxb206/article/details/103893961

#     """
#     b = torch.full(list(attention_mask.size()), 99)
#     out = torch.where(attention_mask > 0, b, attention_mask)
#     return out





# np 批量修改
# https://blog.csdn.net/lxb206/article/details/103893961


class tkitSeg:
    """[summary]
    
    分词和词性标注
    
    """
    def __init__(self,path="./"):
        self.labels = ['zzz','n','t',
            's',
            'f',
            'm',
            'q',
            'b',
            'r',
            'v',
            'a',
            'z',
            'd',
            'p',
            'c',
            'u',
            'y',
            'e',
            'o',
            'i',
            'l',
            'j',
            'h',
            'k',
            'g',
            'x',
            'w',
            'nr',
            'ns',
            'nt',
            'nx',
            'nz',
            'vd',
            'vn',
            'vx',
            'ad',
            'an']
        # path =os.path.dirname(tkitSeg.__file__)
        
        if os.path.exists(os.path.join(path,"model_troch_export.onnx")):
            self.path=path
            
        else:
            # print(os.path.dirname(__file__))
            self.path=os.path.dirname(__file__)
            
        # print("self.path",self.path)
        self.model_path=os.path.join(self.path,"model_troch_export.onnx")
            
        self.tokenizer=BertTokenizer.from_pretrained(self.path)
        self.loadModel()
        pass
    def loadModel(self):
        """[summary]
        
        加载训练的模型
        
        """
        
        self.ort_session = onnxruntime.InferenceSession(self.model_path)
        self.ort_session.get_providers()
        onnx_model = onnx.load(self.model_path)
        onnx.checker.check_model(onnx_model)
    def prediction(self,textLIst):
        """[summary]
        
        批量标注词性和分词

        Args:
            textLIst ([type]): [description]

        Returns:
            [type]: [description]
        """
        inputData = self.tokenizer(textLIst, padding="max_length",
                            max_length=128, truncation=True)
        # print("out",out)
        # compute ONNX Runtime output prediction

        token_type_ids = to_numpy(inputData["attention_mask"])
        # print()
        token_type_ids[token_type_ids > 0] = 1

        ort_inputs = {self.ort_session.get_inputs()[0].name: to_numpy(inputData["input_ids"]), self.ort_session.get_inputs(
        )[1].name: token_type_ids, self.ort_session.get_inputs()[2].name: to_numpy(inputData["attention_mask"])}

        # print(ort_inputs)
        ort_outs = self.ort_session.run(None, ort_inputs)
        return ort_outs, inputData
    
    
    def autoSeg(self,textLIst):
        """[summary]
        
        自动批量标注词性，分词，最大同时处理24条

        Args:
            textLIst ([type]): [description]

        Returns:
            [type]: [description]
        """
        datas = []
        orlen = len(textLIst)
        textLIst = (textLIst*24)[:24]
        ort_outs, inputData = self.prediction(textLIst)

        # onnx推理结果
        out = ort_outs[0]
        outType = ort_outs[1]

        for indexp, typeList, wd, attention_mask, text in zip(out.argmax(axis=-1), outType.argmax(axis=-1), inputData["input_ids"], inputData["attention_mask"], textLIst[:orlen]):
            # print(indexp,typeList,wd,attention_mask )
            one = []
            words = self.tokenizer.convert_ids_to_tokens(wd)
            # print(indexp)
            wordList=[]
            p=0
            for i, (pi, t, w, mask) in enumerate(zip(indexp.tolist(), typeList.tolist(), words, attention_mask)):
                
                if mask > 0:
                    
                    if i<p:
                        # print("漏掉")
                        continue
                        pass
                    else:
                        # print("漏掉")
                        pass
                    # print(i,i+pi,p)
                    # print(words[i:i+pi])

                    p=i+pi
                    

                    outword = []
                    for ww in words[i:i+pi]:
                        outword.append(ww.replace("##", '').replace(
                            "[PAD]", ' ').replace("[SEP]", ' \n'))

                    if len(outword) > 0:
                        one.append({"word": "".join(outword), "wtype": self.labels[t]})
                        wordList.append("".join(outword))
                elif mask == 0:
                    break
            datas.append(({"text": text, "pos": one,"seg":wordList}))
        return datas


# # 使用示例

# text = [" 张杨，男，汉族，黑龙江双城人，1988年2月6日生于贵州省贵阳市", " 自学习结合部分句法分析的汉语词性标注"]

# Seg=tkitSeg()
# datas = Seg.autoSeg(text)
# print(datas)

