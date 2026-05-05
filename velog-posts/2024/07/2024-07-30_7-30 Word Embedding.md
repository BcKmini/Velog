---
title: "7/30 Word Embedding"
date: 2024-07-30 12:13:53
source: "https://velog.io/@mi_nini/730-Word-Embedding"
---

📝목차




Text 처리 특징


단어의 의미


WordNet


TF-IDF


Word2Vec

Skip-gram

Glove

FastText


Word Embedding 응용분야








📌Text 처리 특징


단어(words)의 특징






단어는 눈으로 보면…

이산적 기호 (discrete symbol)

분류적 값 (Categorical Value)




하지만 사람의 머릿속에는…

어휘는 계층적

단어 사이에도 유사성 존재

보라색은 파랑과 검정 중에서 어디에 가까운가?




단어의 표현

One-hot encoding ㅠㅠ

-> One-hot encoding은 단어 집합의 크기를 벡터의 차원으로 하고, 표현하고 싶은 단어의 인덱스에 1의 값을 부여하고, 다른 인덱스에는 0을 부여하는 단어의 벡터 표현 방식








📌
Feature 벡터






Feature

데이터셋을 잘 설명할 수 있는 특징(변수)

Feature를 통해 특정 데이터를 수치화 가능

Feature Vector: Feature를 모아서 하나의 벡터로 만든 것








단어의 Feature Vector는 무엇인가?

단어의 의미와 연관관계를 학습할 수 있는 무언가 필요하다.






좋은 Feature를 생성해야 하는 이유




데이터(언어, 영상, 음성 등)는 반드시 숫자로 표현해야 한다!


이왕이면 데이터를 잘 표현할 수 있는 숫자로 만들어야 한다!








특히, 언어의 경우 다양한 난관들이 있기 때문에 특별히 주의를 기울여야 한다!






📌
Word one-hot vector








단어를 표현하는 가장 단순한 방법

One-hot vector로 표현하면 가장 편리






Word One-hot Vector

크기는 의미 없음

하나의 1과 나머지는 0으로 구성된 n차원 벡터






단점

Very Sparse

유사성(Similarity)을 구할 수 없음








반대로 지나간다 -> -1

만나서 직각이 생긴다 -> 0

같은방향으로 지나간다 -> 1






📌
신경망에서의 학습 원리




인공신경망에서의 학습이란?

입력 X와 출력 Y의 관계를 학습

X의 feature 값을 추출하는 방법을 학습

중간 계층(Hidden Layer)에서 출력 Y값을 표현하기 위해 입력 X로부터 중요한 정보만을 반복적으로 추출


Auto Encoder ->

오토인코더(Auto Encoder)란 입력이 들어왔을 때, 해당 입력 데이터를 최대한 compression 시킨 후, compressed data를 다시 본래의 입력 형태로 복원 시키는 신경망이다.


데이터를 압축하는 부분을 Encoder라고 하고, 복원하는 부분을 Decoder라고 부른다.




딥러닝: 단어를 연속적으로 표현하여 학습




Deep Learning에 필요한 단어 특성




단어를 연속적으로 표현하여 학습하고자 함

단어를 연속적인 값들로 채울 수 있다면…

One-hot vector보다 Dense Vector를 얻을 수 있음

단어간 유사도, Feature 특성을 보다 쉽게 학습 가능






📌단어의 의미




외부적으로 다르게 보일지라도,

내부적으로 다양하게 해석 가능

상호 연관성 존재






다의어(多義語) ,                                                동형어(同型語)






단어의 의미를 정확히 추출하는 데 어려움, 동형어의 경우 큰 문제….

해결책

- 주변 단어를 고려: RNN

- 동형어: WSD (Word Sense Disambiguation) 기법 적용






동의어 nbsp;                                      상위어/하위어






단어의 다양한 구조, 관계 등은 One-hot Encoding을 통해 해결하기는 사실상 불가능하다.

다른 대안이 필요하다.

전통적 방법: WordNet, TF-IDF

Deep Learning 관점: Word2Vec






📌
WordNet이란?


WordNet




어휘분류사전 (시소러스, Thesaurus)


프린스턴대학 George Artitage Miller 교수 주도하에 1985년부터 만들고 있는 사전


상위어, 하위어, 동의어 집합을 구축: Directed Acyclic Graph (유방향 비순환 그래프)






자연어처리에서 WordNet 활용








단어 사이의 거리(Distance)를 구할 수 있다.






두 단어의 유사도를 구할 수 있다.

𝑠𝑖𝑚𝑖𝑙𝑎𝑟𝑖𝑡𝑦(𝑤, 𝑤^′ )=−log⁡〖𝑑𝑖𝑠𝑡𝑎𝑛𝑐𝑒(𝑤, 𝑤^′)〗






(Training Set 없이도 유사도를

구할 수 있다는 것은 매력적)






WordNet의 장단점






장점

단어간 계층구조 파악 가능

동의어 집합 찾을 수 있음

단어 사이의 유사도 계산 가능






단점

사전 작성자(사람)의 주관적 판단이 개입될 수 있음

일반 도메인(General Domain)에만 적용 가능

특정 도메인(예: 게임, 코딩, 여행)에서 성능이 안 좋을 수 있음.






해결책: 고전적 Word Embedding인 TF-IDF 방식 등장








📌
TF-IDF






TF-IDF

Term Frequency – Inverse Document Frequency의 약어

사전 기반 방식이 특정 도메인에서 작동하지 않는 상황을 극복하기 위한 하나의 방법

어떤 단어(w)가 문서(d)에서 얼마나 중요한지를 나타내는 수치






TF (Term Frequency)

단어 w가 문서 d에 출현한 횟수

자주 등장하면 중요하다고 가정

하지만 the/a/an/is 와 같은 단어는

중요하지 않아도 많이 등장






IDF (Inverse Document Frequency)

단어 w가 전체 문서에서 등장한 횟수의 역수

값이 클수록 대부분의 문서에서 많이 쓰이는 단어






(수학 연산자의 특성)




+와 X의 차이 -> X는 비례성이 있다. 식을 생각해보기.








TF-IDF: 자연어처리에서 활용




문서에서 단어 W가 얼마나 중요한지를 수치화


문서간, 혹은 단어간 유사도를 구할 수 있을지도…


각 문서에서의 중요도를 feature vector로 고려






벡터들을 가지고 k-means를 돌릴 수 있다.

distancd -> 유사도의 역수


유사한 개념… 동시출현빈도




동시출현빈도 (Co-occurrence Frequency)


함께 등장하는 단어를 이용하여 Feature Vector 구성


가정

의미가 비슷하면 쓰임새도 비슷

쓰임새가 비슷하면 비슷한 문장에 등장

그러므로 함께 나타나는 단어들은 유사할 것


일반적으로 Window를 사용함

Context windowing 수행

Window size는 Hyper-parameter








아직도 해결되지 않은 문제들






사전방식에 비해 도메인이 특화된 것을 잘 표현 가능






Feature로 선택하는 문서, 단어도 어차피 Hyper--parameter






Hyper--parameter -> 학습을 할 때 컴퓨터 스스로 X 사람이 지정해줘야 함 






여전히 Sparse Matrix










해결책: Deep Learning을 지원할 수 있는 Feature Vector를 만들자!






📌
Word2Vec




Insight

Context Window 주변에 나타나는 단어일수록 비슷한 벡터를 가질 것이다.

문장의 문맥에 따라 정해지는 것은 아님  window size에 따라 다른 의미도 가능


Strategy

주변 단어를 예측하는 과정에서 정보 압축

예측 값 𝑦 ̂ 을 위해 필요한 정보만 압축

Dense Vector를 얻을 수 있음






📌Skip-gram




중심 단어로부터 좌,우 거리에 있는 단어를 추출






Skip-gram 아키텍처




장점: 직관적이고 이해하기 쉽다.


단점: 출현빈도가 적을 경우 벡터가 정확하지 않을 수 있다.










📌
GloVe




GloVe

Global Vectors for Word representation

skip-gram이 window를 반복적으로 이동하면서 단어를 예측하도록 학습하는 반면

GloVe는 window 내에 있는 단어의 출현빈도를 예측하도록 학습




-> 예측하도록 학습시킴




장점: 빠르다. 출현빈도 적은 단어도 비교적 잘 처리












📌
FastText


Skip-gram의 업그레이드 버전




기존 skip-gram은 OoV (Out of Vocabulary) 대응이 어려움


단어를 subword로 분할


Skip-gram을 이용하여 embedding을 수행하고 sub-word에 대한 embedding vector에 주변 단어의 context vector를 곱한 이후 더한다.


이 값이 최대화 되도록 학습


최종적으로 각 subword에 대한 embedding vecto의 합이 word embedding vector








📌
Word Embedding 응용분야 


응용분야 1. 자연어 처리 (Natural Language Processing)




쳇봇, 번역, 요약…


Word Embedding은 DNN에 입력하기 위한 중간단계


Word Embedding을 최종 목표 모델로 사용하기에는 부족


자연어 처리에서는 최초 입력 Linear Layer에 포함되는 경우도 많음




Word Embedding을 수행하지 않고 One-hot Vector로 입력하는 것도 가능






첫번째 Linear Layer에 Word Embedding Layer를 포함하는 방법도 가능




Dataset이 적을 경우 대규모로 훈련된(Pre-trained) 모델을 Tunning 하기 위해 적용 가능




응용분야 2. 추천시스템




다양한 상품의 Event(클릭, 조회 등)Sequence를 파악할 수 있는 경우,




Event Sequence를 단어로 가정하고 Embedding 가능




예) 클릭 순서 (Click event history)에 따른 Embedding










코드참고 :


Github
 - 6주차/7.29~
