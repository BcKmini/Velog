---
title: "8/2 Attention Mechanism"
date: 2024-08-02 12:52:26
source: "https://velog.io/@mi_nini/82-Attention-Mechanism"
---

📝목차


T- he Meaning of Tensors in RNN




Attention Mechanisms


Sequence to Sequence


Transformer


Attention is all you need!










📌
보너스 - Embedding layer


Embedding in NN




NLP 첫 레이어로 활용

Lookup Table로 구성










공식 문서 참고


Official Docs

PyTorch: 
https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html

TensorFlow: 
https://www.tensorflow.org/api_docs/python/tf/keras/layers/Embedding
 






📌
RNN Tensors 의미


텐서 (Tensor) 의미


사전적 의미 (온라인 위키, 
https://ko.wikipedia.org/wiki/텐서
)

19세기에 카를 프리드리히 가우스가 곡면에 대한 미분 기하학을 만들면서 도입하였다. 기본적인 예는 내적과 선형 변환이 있으며 미분 기하학에서 자주 등장한다. 텐서는 기저를 선택하여 다차원 배열로 나타낼 수 있으며, 기저를 바꾸는 변환 법칙이 존재한다. 




쉽게, 3차원 벡터를 텐서로 생각하면 편리하다.




참고

블로그: 
https://rekt77.tistory.com/102

유튜브: 
https://www.youtube.com/watch?v=m0qwxNA7IzI
 








이미지(Image)에서의 텐서

흑백 이미지 -> 3차원 텐서

컬러 이미지 -> 4차원 텐서








동영상(Video)에서의 텐서








Tensor in NLP


입출력 텐서 in Fully Connected Layer






Tensor in NLP




앞쪽 Padding 하는 경우








뒤쪽 Padding 하는 경우








📌
Attention Mechanism


Tokenizer 및 Embedding 개념




한글의 경우 형태소분석 과정 추가

Okt.morphs(phrase, norm=False, stem=False)

Parse phrase to morphemes.




💻파이썬 사전(Dictionary) 구조


>>
>
 score 
=
 
{
}


>>
>
 score
[
'sonic'
]
 
=
 
80


>>
>
 score
[
'dante'
]
 
=
 
70


>>
>
 score
[
'kim'
]
 
=
 
99


>>
>
 
print
(
score
[
'kim'
]
)


99


Query: 질의, 찾고자 하는 대상 (내가 찾고자 하는 것을 포함하는 질문)

Key: 찾을 값을 참조하는 값

Value: 저장된 데이터 (Query를 통해 찾을 값)

Dictionary: Python 자료구조 (key: value 쌍으로 이루어진 집합)




Attention MechanismAttention Score


Softmax를 통해 Attention Distribution 계산


각 인코더의 Feature와 Attention 가중치를 가중합(weighted sum)하여 Attention Value 계산






Query에 대하여 어떤 Key가 유사한지를 찾는다


Query와 Key의 유사도 값을 반영하여 Value 값들을 합성한다.






사전에서 질의(Query)에 대한 값을 찾는 과정




Attention Mechanism




Attention Score 구하기






Attention Mechanism




Attention Score


Softmax를 통해 Attention Distribution 계산






Attention Score






Softmax를 통해 Attention Distribution 계산






각 인코더의 Feature와 Attention 가중치를 가중합(weighted sum)하여 Attention Value 계산








Attention Score






Softmax를 통해 Attention Distribution 계산






각 인코더의 Feature와 Attention 가중치를 가중합(weighted sum)하여 Attention Value 계산






Attention Value를 현재시점(t)에 연결(concatenate)








Attention Score






Softmax를 통해 Attention Distribution 계산






각 인코더의 Feature와 Attention 가중치를 가중합(weighted sum)하여 Attention Value 계산






Attention Value를 현재시점(t)에 연결(concatenate)






- 출력층 연산의 입력이 되는 값 계산






📌
Sequence to Sequence(seq2seq)


Sequence to Sequence (Seq2Sec)

인공지능을 활용한 번역 모델에서 많이 사용






대부분의 Attention Network: Key, Value를 동일하게 사용


Seq2Sec: Encoder의 Hidden Layer들을 key, value로 사용




Seq2Sec: Key-Value 생성




Seq2Sec: Query




Attention Value 계산






Attention 신경망_seq2seq 실습


https://github.com/bentrevett/pytorch-seq2seq
 






📌
Transformer


2016년 구글은 GNMT (Google Neural Machine Translation) 시스템 발표




Seq2Seq + Attention + 강화학습(Reinforce Learning)




논문 링크: 
https://arxiv.org/pdf/1609.08144.pdf
 




기계번역 성능평가(metric) – PPL


PPL (Perplexity):

확률의 역수, 헷갈리는 정도

예측 확률이 높으면 좋음 따라서  PPL 낮을수록 좋은 모델

각 time-step별 실제 정답에 얼마나 가까운지 만 채점




번역1이 잘된 번역이지만, 오히려 맞춘 개수가 많아 확률이 Hit 확률이 높은 번역2가 PPL이 낮다.

번역 품질 평가 metric으로 사용하기에는 한계점


기계번역 성능평가(metric) – BLEU


BLEU (Bi-Lingual Evaluation Understudy)

정답과 예측 문장 사이에서 일치하는 n-gram 별 precision의 가중(기하) 평균  높을수록 좋음

n-gram별 정밀도의 평균을 백분률로 나타낸 것






2017년 페이스북, Fully Convolutional Seq2Seq 발표






논문 링크: 
https://arxiv.org/pdf/1705.03122.pdf
 




Seq2Seq와 비슷한 구조, Attention 기술만 적용






논문 링크: 
https://arxiv.org/pdf/1706.03762.pdf
 






Multi-head Attenttion


Multi-head Attenttion

좋은 검색 결과를 얻기 위한 것 --> 최적의 질의 (Query)를 만드는 것

좋은 Query 만드는 방법을 학습하는 것 --> Attention 학습




만약 다양하게 할 수 있다면 좀 더 좋은 결과를 얻을 수 있을 것

Attention을 동시에 여러개 생성하여 종합 --> Multi-Head Attention


Transformer




Attention is all you need! -> 논문제목 


CNN, RNN 사용을 배제하고, 오직 Attention Mechanism만을 사용하여 최고의 성능


현재 SOTA 기술에 속함 (State – of – the - Art)


논문 링크: 
https://papers.nips.cc/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf
 






모델 특징




Scaled Dot-product Attention


Multi-head Attention이 핵심 알고리즘


RNN의 BPTT 없음  병렬계산 가능


Positional Encoding (입력 단어 위치 표시): 병렬연산 지원








📌전체적 구조_Transformer






빨강색: 인코더 (입력, Input)

파랑색: 디코더 (출력, Output)

주황색: 인코더에서 Self-Attention이 일어나는 부분

하늘색: 디코더에서 Self-Attention이 일어나는 부분

노란색: 인코더와 디코더의 Attention이 일어나는 부분




입출력 구조




Word Embedding




Positional Encoding




예) “I love you but not love him.”


앞의 love와 뒤의 love은 일반적인 임베딩만을 거쳤을 때 동일한 값을 가짐


Positional Encoding 이라는 주기함수에 의한 위치에 따른 다른 임베딩을 거치면 같은 단어여도 문장에서 쓰인 위치에 따라 다른 임베딩 값을 됨.


Scaled Dot-product Attention




Multi-head Attention






Linear 연산(Matrix Mult) 이용해 Q, K, V 차원 감소


h개의 Attention Layer를 병렬 계산


계산된 h개를 Concatenate


필요에 따라 Linear 연산을 통해 차원을 변경


병렬처리에 매우 유리한 구조




Attention 신경망_Transformer 실습




Github Transformer 구현

- 독일어-영어 번역: 
https://github.com/hyunwoongko/transformer

- 영어-한국어 번역: 
https://github.com/nawnoes/pytorch-transformer

Transformer 참고 블로그
https://rubikscode.net/2019/08/05/transformer-with-python-and-tensorflow-2-0-attention-layers/
