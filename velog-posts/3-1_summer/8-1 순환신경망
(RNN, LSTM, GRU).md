<blockquote>
<h2 id="목차">목차</h2>
</blockquote>
<ul>
<li>RNN Ideas
Sequential Data
Vanilla RNN
BPTT</li>
<li>LSTM (Long Short-term Memory)</li>
<li>GRU (Gated Recurrent Unit)</li>
</ul>
<hr />
<h2 id="📌span-stylecolorindianredrnn-ideasspan">📌<span style="color: indianred;">RNN Ideas</span></h2>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/25fd9351-aa2f-433b-ad21-bc2268e01544/image.png" /></p>
<table>
<thead>
<tr>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/6c1e5061-6423-4e24-a57b-ce191fd485a6/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/43021bb5-3d4c-4a26-851e-f4254a016870/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/7078d214-8811-4465-908f-8dadc0ea1e37/image.png" /></th>
</tr>
</thead>
</table>
<hr />
<h2 id="time-related-data">Time-related Data</h2>
<ul>
<li>Sequential Data Types</li>
</ul>
<table>
<thead>
<tr>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/f04f8816-8b67-48ee-9f6a-eacc3123b350/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/8c15f56c-7968-4411-81aa-5076d2129dd0/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/1a2acef0-a94d-4e0e-b049-9fc5355bc841/image.png" /></th>
</tr>
</thead>
</table>
<ol>
<li>Sequential Data: 순서가 의미 있는 데이터, 순서가 바뀌면 의미 상실</li>
<li>Temporal Sequence: sequential data + 시간 개념</li>
<li>Time Series: temporal sequenc에서 일정 간격으로 샘플링한 data</li>
</ol>
<hr />
<h2 id="sequential-data-with-dnn">Sequential Data with DNN</h2>
<ul>
<li>Deep Neural Network 
<img alt="" src="https://velog.velcdn.com/images/mi_nini/post/bf5af31f-f0a0-46d9-aed4-70edabb26a37/image.png" /></li>
<li>음성신호: 초당 44,000개 샘플이 있어야 함</li>
<li>4.4만개를 다 입력으로 넣을 수 있는가?
너무나 긴 input layer</li>
<li>음성의 길이는 매번 변하는데…
항상 변하는 input layer</li>
</ul>
<hr />
<ul>
<li><h3 id="various-input--output--multiple-input---singlemultiple-output">Various Input / Output – multiple input -&gt; single/multiple output</h3>
</li>
<li>다중입력 -&gt; 단일출력</li>
</ul>
<table>
<thead>
<tr>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/28304d17-8d2d-4b53-88fd-0d712a1d3464/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/07811bf1-894c-4616-86e0-6c011a635d01/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/97d5f800-3832-4cf6-bb06-b31cf25efdb5/image.png" /></th>
</tr>
</thead>
</table>
<ul>
<li>다중 입력 -&gt; 다중 출력</li>
</ul>
<table>
<thead>
<tr>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/3fd684e5-9fc9-4aed-98f3-dad7ce6d0686/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/33a13829-5407-41c8-9559-6326768f8f76/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/eda718a4-1027-4873-8333-fd3bb3a5a239/image.png" /></th>
</tr>
</thead>
</table>
<ul>
<li>단일 입력 -&gt; 다중 출력 </li>
</ul>
<table>
<thead>
<tr>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/ae6bb20e-3e6b-48b4-9331-e348462b7d2c/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/c3141062-2435-468d-8689-150547f2655a/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/d42393e8-c434-4b44-bebe-f9c6e826c3b4/image.png" /></th>
</tr>
</thead>
</table>
<hr />
<h2 id="📌span-stylecolorindianred기본-순환-신경망-vanilla-recurrent-networkspan">📌<span style="color: indianred;">기본 순환 신경망 (Vanilla Recurrent Network)</span></h2>
<ul>
<li><p>기본 순환 신경망</p>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/b70e610b-03d7-4b11-a8ea-a811650fb455/image.png" /> | <img alt="" src="https://velog.velcdn.com/images/mi_nini/post/e935c402-a0ea-4d64-a02e-090a09af8c96/image.png" /></p>
</li>
<li><p>-| --|</p>
</li>
<li><p>다층 순환 깅경망
<img alt="" src="https://velog.velcdn.com/images/mi_nini/post/6a87156d-43c1-4795-9257-609c9808331b/image.png" /></p>
</li>
<li><p>순환 신경망도 심층 신경망처럼 쌓아 올릴 수 있다.</p>
</li>
<li><p>하지만 신경망 구조가 복잡해지고 학습이 잘 되지 않아 깊게 쌓지는 않는다
(일반적으로 3~4계층을 사용하는 것으로 알려짐)</p>
</li>
</ul>
<hr />
<table>
<thead>
<tr>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/e8100c33-a587-4a1b-b39b-dfac4cef2aa8/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/d71d0d33-b74a-469c-9233-ee3aa6cd7e1e/image.png" /></th>
</tr>
</thead>
<tbody><tr>
<td>- 기울기 소실 문제 (Gradient Vanishing Problem)</td>
<td></td>
</tr>
<tr>
<td><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/efd2df71-46e2-4ad1-bbbe-80a5fbc8216a/image.png" /></td>
<td></td>
</tr>
<tr>
<td>- 시그모이드 함수를 사용하면 입력의 절대값이 클 경우에 시그모이드 함수의 출력값이 0 또는 1에 수렴하면서 기울기가 0에 가까워짐</td>
<td></td>
</tr>
<tr>
<td>- 역전파 과정에서 전파시킬 기울기가 점차 사라져서 입력층 방향으로 갈 수록 제대로 역전파가 되지 않는 기울기 소실 문제가 발생.</td>
<td></td>
</tr>
</tbody></table>
<p>@차근차근 딥러닝
<img alt="" src="https://velog.velcdn.com/images/mi_nini/post/c9a62465-9637-417d-9bec-cc8ff0f78446/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/b10c574d-b8b2-48a2-a225-17eaa21c436d/image.png" /></p>
<hr />
<h2 id="sequential-data의-구조">Sequential Data의 구조</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/14da770f-412e-4f29-8a7c-61c6d83e4fad/image.png" /></p>
<hr />
<h2 id="📌span-stylecolorindianredbpttspan">📌<span style="color: indianred;">BPTT</span></h2>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/363828e0-31f1-429a-8229-3c5d84054a62/image.png" /></p>
<h2 id="truncated-bptt">Truncated BPTT</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/716a6927-27ab-4c2c-abd9-defc9858ac14/image.png" /></p>
<h2 id="단순-rnn의-작동">단순 RNN의 작동</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/5cb054c4-4ef4-4497-81e4-4a01367c9e2f/image.png" /></p>
<hr />
<h2 id="📌span-stylecolorindianredlstm--gruspan">📌<span style="color: indianred;">LSTM &amp; GRU</span></h2>
<h3 id="lstm-long-short-term-memory">LSTM (Long Short-Term Memory)</h3>
<ul>
<li>유명한 알고리즘</li>
<li>Vanilla RNN 개선<ul>
<li>설계 철학
오래 기억할 것은 오래 기억하자.
잊을 것은 빨리 잊어버리자.
<img alt="" src="https://velog.velcdn.com/images/mi_nini/post/a4e553b8-c97c-44fc-9375-b55464f2110e/image.png" /></li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/a6ec37b8-eb2c-48ff-a0fb-847e79ac1599/image.png" /></p>
<ul>
<li><p>Cell state: Long-term 기억 학습
(새로운 기억을 덧셈으로 업데이트)</p>
</li>
<li><p>Hidden state: 은닉계층 정보를 다음
계층으로 넘기는 정보</p>
</li>
<li><p>3개의 Gate로 설계됨: <span style="color: indianred;"><strong>Forget Gate, Input Gate, Output Gate</span></strong></p>
</li>
<li><p>Sigmoid 함수로 이루어진 3개의 Gate를 통해 정보를 통과시킬지 여부를 결정해 셀 상태(기억, 메모리)를 보호하거나 제어함</p>
</li>
</ul>
<hr />
<h2 id="--forget-gate">- Forget Gate</h2>
<p>얼마만큼 잊을지 결정
<img alt="" src="https://velog.velcdn.com/images/mi_nini/post/4532cd6c-c29a-4887-bc9b-d79cd97a2783/image.png" /></p>
<h2 id="--input-gate">- Input Gate</h2>
<p>새로운 정보를 Cell State (기억)에 얼마만큼 더해줄 것인지 결정
<img alt="" src="https://velog.velcdn.com/images/mi_nini/post/2cba7981-6f0a-42f1-ab6c-40385ad2c2c2/image.png" /></p>
<h2 id="--output-gate">- Output Gate</h2>
<p>Cell State (기억)을 얼마나 출력해 줄 지 결정</p>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/f5514fb3-66f6-4c09-a7ee-19c3cbf358cf/image.png" /></p>
<hr />
<hr />
<h2 id="--all-in-one-by-math">- All in One by Math</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/9a76bc8a-cd6a-4d7a-86f0-07660cffc726/image.png" /></p>
<ul>
<li>하다마드 곱 (Hadamard product) 연산자
(element-wise 곱)</li>
</ul>
<hr />
<hr />
<h2 id="📌span-stylecolorindianredgruspan">📌<span style="color: indianred;">GRU</span></h2>
<ul>
<li>GRU (Gated Recurrent Unit)<ul>
<li>LSTM의 간소화 버전</li>
<li>Cell State (기억)이 없어짐</li>
<li>Forget Gate와 Input Gate를 
하나로 합침</li>
<li>Reset Gate 추가
<img alt="" src="https://velog.velcdn.com/images/mi_nini/post/677cfb1b-a98e-403e-a004-d7d5594aabc3/image.png" /></li>
</ul>
</li>
</ul>
<h2 id="reset-gate">Reset Gate</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/0ffca05d-fa51-42b6-9266-aba163c3b78f/image.png" /></p>
<h2 id="forget--input-gate">Forget + Input Gate</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/83441b7b-4fd8-423c-8ad2-d6a291c395cd/image.png" /></p>
<h2 id="hidden-state-최종-업데이트-방식">Hidden State 최종 업데이트 방식</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/851a1c8c-86f8-449d-8e8a-31dd4aef7e76/image.png" /></p>
<hr />
<h2 id="📌span-stylecolorindianred-rnn-종류별-특징span">📌<span style="color: indianred;"> RNN 종류별 특징</span></h2>
<p><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/86e7cbdb-8d53-4cad-9f3b-11bf86f70ece/image.png" /></p>
<table>
<thead>
<tr>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/8c8a2e3b-575e-4098-ae21-cd38fb158db9/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/a6193a4c-af70-4b57-b494-42bfde718db0/image.png" /></th>
<th><img alt="" src="https://velog.velcdn.com/images/mi_nini/post/f4a19e66-d050-4839-b381-8336edb720b1/image.png" /></th>
</tr>
</thead>
</table>
<h2 id="1-rnn">1. RNN</h2>
<p>1) 핵심 개념<br />입력 갯수 출력 갯수에 따라서 one to many, many to one, many to many 로 나눠지지만 </p>
<p> 핵심은 이전 hidden state 의 아웃풋과 현시점의 인풋이 함께 연산 된다는 것</p>
<p> 2) 문제  입력 시퀀스의 길이가 너무 길면 (Long sequence)</p>
<p> --&gt;  그레디언트 주는 편미분 과정에서 (Back Propagation Through Time)
그레디언트가 사라지거나 폭발하는 문제가 생김 (Gradient Vanishing , Gradient Exploding) </p>
<p><span style="color: indianred;">문제점은 many to many 와 같은 구조에서 초반부에 입력된 것이 후반부에 잊혀지는 것이다</span>
-&gt; 예전 기억도 계속 리마인드 시켜주는 학습 방법이 필요하다 -&gt;LSTM</p>
<h2 id="2-lstm">2. LSTM</h2>
<p>LSTM 셀에서는 상태(state)가 두 개의 벡터 ​와 ​로 나누어 진다는 것을 알 수 있다. </p>
<p>ht ​를 단기 상태(short-term state), ​Ct를 장기 상태(long-term state)라고 볼 수 있다.각 게이트를 정말 간단하게만 정리하자면 컨셉,</p>
<p>input gate : 이번 입력을 얼마나 반영할지 </p>
<p>output gate : 이번 정보를 얼마나 내보낼지 </p>
<p>forget gate : 과거 정보를 얼마나 까먹을지 </p>
<p>그리고 이 모든 장기기억이 ct에 담김으로써 RNN의 문제를 해결</p>
<h2 id="3-gru">3. GRU</h2>
<p>복잡한 구조를 간단히 시킨게 GRU</p>
<ul>
<li>GRU는 게이트가 2개, LSTM은 3개</li>
<li>GRU는 내부 메모리 값 ( ct )이 외부에서 보게되는 hidden state 값과 다르지 않음. LSTM에 있는 출력 게이트가 없음 ! </li>
<li>입력 게이트와 까먹음 게이트가 업데이트 게이트 z로 합쳐졌고, 리셋 게이트 r은 이전 hidden state 값에 바로 적용</li>
</ul>
<p>따라서, LSTM의 까먹음 게이트의 역할이 r과 z 둘 다에 나눠졌다고 생각할 수 있음
    출력값을 계산할 때 추가적인 비선형 함수를 적용하지 않음 </p>
<h2 id="tmi">TMI</h2>
<blockquote>
<p>1) Rt : reset gate (지난 정보를 얼마나 버릴지) 
현재 시점의 입력값 (xt)가 입력되면 그 시점의 가중치 Wr 와 내적 
전 시점의 hiddenstate ht-1는 그시점의 가중치 Ur 와 내적 
마지막으로 두 계산이 더해져 sigmoid 함수에 입력 --&gt; 결과는 0~1사이값 </p>
</blockquote>
<blockquote>
<p>2) Zt : update gate  (이번 정보를 얼마나 반영할지) 
현재 시점의 입력값 (xt)가 입력되면 그 시점의 가중치 Wz 와 내적 
전 시점의 hiddenstate ht-1는 그시점의 가중치 Uz 와 내적 
마지막으로 두 계산이 더해져 sigmoid 함수에 입력 --&gt; 결과는 0~1사이값 </p>
</blockquote>
<blockquote>
<p>3) ~h : 현재 시점에 과거의 메모리를 얼마나 사용할거냐 
현재 시점의 입력값 (xt)가 입력되면 그 시점의 가중치 Wh 와 내적 
전 시점의 hiddenstate ht-1는 그시점의 가중치 Uh 와 내적하고 Rt(지난 정보 버림값)와 성분 곱
마지막으로 두 계산이 더해져 tanh 함수에 입력</p>
</blockquote>
<blockquote>
<p>4) h : 최종 메모리 정보 
update gate 출력값 Zt (이전정보 얼마나 반영) 와 이전시점 hidden state  ht-1를 성분 곱
update gate 에서 버리는 값인 1-Zt (이전정보 얼마나 안반영) 와 현재시점 hidden state ht 을 성분 곱 </p>
</blockquote>
<blockquote>
<h2 id="깃허브-코드-참고-">깃허브 코드 참고 :</h2>
<p><a href="https://github.com/BcKmini/Ai_Python">https://github.com/BcKmini/Ai_Python</a> 
6주차/7/30</p>
</blockquote>