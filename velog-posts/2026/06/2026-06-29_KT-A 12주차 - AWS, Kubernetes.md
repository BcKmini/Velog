---
title: "KT-A 12주차 / AWS, Kubernetes"
date: 2026-06-29 03:06:14
source: "https://velog.io/@mi_nini/KT-A-12주차-AWS-Kubernetes"
---

## 들어가며

11주차는 동원예비군 훈련에 참여하면서 미니 프로젝트를 진행하지 못해 곧바로 12주차 학습을 진행하게 되었다. 원래는 이전에 프론트엔드로 구현했던 프로젝트를 Spring을 활용하여 데이터베이스와 연동하고, json-server 기반의 임시 백엔드를 실제 서버 환경으로 대체하는 내용을 다룰 예정이었다. 하지만 일정상 해당 프로젝트를 진행하지 못했기 때문에 이번 글에서는 프로젝트 대신 학습한 내용을 정리하고자 한다.  
이번 글은 클라우드 환경에서 자주 사용되는 핵심 서비스와 k8s, 그리고 AWS 기반 CI/CD 파이프라인을 중심으로 정리한 학습 기록이다. 

**다루는 범위:**

  * **AWS 인프라** : EC2, S3, EBS, VPC, ELB, Auto Scaling, Route53, CloudFront
  * **AWS 데이터베이스** : RDS, Aurora, DynamoDB, ElastiCache
  * **AWS 보안·네트워크** : IAM, Organizations, VPN, Direct Connect
  * **컨테이너** : Docker, VM vs Container, MSA
  * **Kubernetes** : 클러스터 구성, Pod/RS/Deployment/Service/Ingress/HPA, ConfigMap/Secret, Volume
  * **CI/CD on AWS** : CodePipeline, CodeBuild, CodeDeploy, 배포 전략 7가지
  * **고가용성·DR** : ELB+Auto Scaling, Route53 Failover, 재해복구 전략



* * *

## 1\. 클라우드의 등장 배경과 AWS 글로벌 인프라

### 1.1 왜 클라우드가 필요했나?

예전 On-Premise 방식을 생각해보자. 서비스를 운영하려면 서버를 직접 구매해야 했다. 서버는 최대 트래픽 기준으로 사야 했기 때문에, 평소에는 비싼 장비가 놀고 있었다. 반대로 예상치 못한 트래픽 폭증이 오면 서버가 터졌다.

항목| On-Premise| Cloud  
---|---|---  
서버 구매| 직접 구매, 설치| 필요할 때 빌림  
초기 투자 비용| 매우 높음| 거의 없음  
확장 속도| 수 주 ~ 수 개월| 수 분 이내  
유지보수| 직접 담당| CSP(클라우드 제공업체) 담당  
요금 방식| 선불 자본 지출| 종량제 (쓴 만큼 지불)  
  
클라우드의 핵심 이점은 세 가지로 요약된다.

  * **민첩성** : 새 기능/서비스를 빠르게 출시할 수 있음
  * **비용 최적화** : 사용한 만큼만 지불, 불필요한 서버 유지 비용 없음
  * **보안 취약성 최소화** : AWS가 물리적 인프라 보안을 직접 담당



### 1.2 AWS vs Azure 비교

구분| AWS (Amazon Web Services)| Microsoft Azure  
---|---|---  
출시| 2006년 (클라우드 시장 선두)| 2010년 (후발주자, 빠른 성장)  
시장 점유율| 1위 (약 30% 이상)| 2위 (약 25% 내외)  
강점| 광범위한 서비스, 글로벌 인프라| Microsoft 제품 통합 (Windows Server, AD, Office 365)  
가상 머신| EC2| Azure Virtual Machine  
스토리지| S3| Blob Storage  
DB| RDS, DynamoDB| Azure SQL, Cosmos DB  
AI/ML| SageMaker, Rekognition| Azure AI, Cognitive Services  
주요 고객층| 스타트업, 기술 기업, 글로벌 서비스| 기존 Microsoft 고객, 공공기관, 대기업  
  
### 1.3 AWS 글로벌 인프라 — 리전, 가용 영역, 엣지

AWS 글로벌 인프라는 리전 → 가용 영역 → 엣지 로케이션의 3단계 계층 구조로 구성된다.
[code] 
    리전 (Region)
    ├── 가용 영역 AZ-1 (데이터 센터 × n)
    ├── 가용 영역 AZ-2 (데이터 센터 × n)
    └── 가용 영역 AZ-3 (데이터 센터 × n)
    
    엣지 로케이션 (전 세계 수백 곳)
    Local Zone (대도시 근처 mini 리전)
[/code]

**리전(Region)**

  * AWS가 전 세계에서 데이터 센터를 클러스터링하는 물리적 위치
  * 각 리전은 완전히 독립적 — 서울 리전 장애가 도쿄 리전에 영향 없음
  * 서울 리전 코드: `ap-northeast-2`



리전 선택 시 4가지 고려사항:  
1\. **거버넌스** : 금융, 의료 데이터는 국내 데이터센터에 보관해야 하는 법적 요건이 있음  
2\. **지연 시간** : 사용자와 가까울수록 응답이 빠름  
3\. **서비스 가용성** : 모든 AWS 서비스가 모든 리전에 출시되지 않음  
4\. **비용** : 리전마다 EC2 요금이 다름

**가용 영역(AZ, Availability Zone)**

  * 리전 내에서 서로 격리된 물리적 데이터 센터 그룹
  * 화재, 정전, 자연재해로부터 독립 운영
  * AZ끼리는 고속 프라이빗 전용 링크로 연결됨
  * 한 AZ가 다운돼도 다른 AZ가 서비스 지속 → **고가용성(HA)** 의 핵심



**엣지 로케이션**

  * 전 세계 주요 도시에 배치된 캐싱 거점 (200개 이상)
  * CloudFront(CDN), Route53에서 사용
  * 사용자 가장 가까운 곳에서 콘텐츠를 서빙해 지연 시간을 최소화



**Local Zone**

  * 리전을 사용자 근처로 확장한 소형 인프라
  * 실시간 게임, 라이브 스트리밍, AR/VR 같은 지연 시간에 민감한 워크로드용



* * *

## 2\. 클라우드 네이티브 — DevOps와 CI/CD

### 2.1 Cloud Native란?

클라우드 네이티브는 단순히 "클라우드에서 실행한다"는 의미가 아니다. **처음부터 클라우드 환경을 최대한 활용할 수 있게 설계·개발·운영하는 방법론** 이다.

기존 앱을 클라우드에 그냥 옮기는 건 **Lift & Shift**(이전·재호스팅). 클라우드 네이티브의 핵심 요소 4가지:

요소| 설명  
---|---  
**DevOps**|  개발(Dev)과 운영(Ops)의 협업 문화  
**Container**|  이식 가능한 경량 실행 환경  
**CI/CD**|  빌드·테스트·배포 자동화 파이프라인  
**Micro Services (MSA)**|  기능별로 분리된 독립 서비스 구조  
  
### 2.2 DevOps — 개발팀과 운영팀의 벽을 허물다

DevOps 이전의 전통적인 개발 환경에는 구조적인 충돌이 있었다.

관점| 목표| 갈등 요인  
---|---|---  
개발팀(Dev)| 기능을 빠르게 배포| 변경이 많을수록 좋음  
운영팀(Ops)| 시스템 안정성 유지| 변경이 적을수록 좋음  
  
이 구조적 갈등으로 배포 주기가 길어지고, 장애 발생 시 책임 소재가 불분명해진다. DevOps는 **자동화와 협업 문화** 를 통해 이 문제를 해결한다.

### 2.3 CI/CD — 자동화된 배포 파이프라인
[code] 
    Code → Build → Test → Release → Deploy → Monitor
      ↑                                             |
      └──────────── 피드백 루프 ────────────────────┘
[/code]

**CI (Continuous Integration, 지속적 통합)**

  * 코드 변경 사항을 주기적으로(매일 또는 여러 번) 빈번하게 merge
  * merge 시 자동으로 빌드와 테스트 실행
  * 통합 문제를 조기에 발견



**CD (Continuous Delivery/Deployment, 지속적 배포)**

  * 테스트를 통과한 코드를 자동으로 스테이징 또는 운영 환경에 배포
  * Continuous Delivery: 운영 배포 전 수동 승인 포함
  * Continuous Deployment: 완전 자동화, 승인 없이 즉시 배포



CI/CD 도구 예시: Jenkins, GitLab CI/CD, GitHub Actions, AWS CodePipeline, ArgoCD

CI/CD 도입 효과: 배포 주기 단축, 버그 조기 발견, 팀 생산성 향상, 릴리즈 위험 감소

* * *

## 3\. 클라우드 서비스 모델 — IaaS, PaaS, SaaS
[code] 
    온프레미스 (모두 직접 관리)
      Networking / Storage / Server / OS / Middleware / Runtime / Application
    
    IaaS (OS부터 직접 관리)
      CSP 제공: Networking / Storage / Server
      직접 관리: OS / Middleware / Runtime / Application
    
    PaaS (애플리케이션만 관리)
      CSP 제공: Networking / Storage / Server / OS / Middleware / Runtime
      직접 관리: Application
    
    SaaS (관리 없음, 사용만)
      CSP 제공: 전부
[/code]

모델| AWS 대표 서비스| 사용 예시  
---|---|---  
IaaS| EC2, VPC, S3| 가상 서버, 네트워크 직접 구성  
PaaS| Elastic Beanstalk, RDS| 코드만 올리면 자동 배포  
SaaS| Amazon Chime, WorkDocs| 그냥 쓰면 됨  
  
**AWS 컴퓨팅 서비스 출시 연표** :

  * 2006년: EC2 — 가상화 기반 IaaS (AWS 최초 서비스)
  * 2014년: ECS — 컨테이너 오케스트레이션 (re:Invent 2014)
  * 2014년: Lambda — 서버리스 Function-as-a-Service (re:Invent 2014)
  * 2016년: Lightsail — 단순화된 VPS 서비스
  * 2017년: Fargate — 서버리스 컨테이너 실행 (re:Invent 2017)
  * 2018년: EKS — 관리형 Kubernetes (re:Invent 2017 발표, 2018 GA)



* * *

## 4\. AWS EC2 — 클라우드의 가상 서버

![AWS EC2 Instance Types — 각 패밀리와 용도 분류](https://media.geeksforgeeks.org/wp-content/uploads/20250529181702162572/Aws-EC2-instance-types.webp)

### 4.1 EC2란?

EC2(Elastic Compute Cloud)는 AWS의 핵심 컴퓨팅 서비스다. 클라우드에서 안전하고 크기 조정 가능한 컴퓨팅 용량을 제공한다. 트래픽 변화에 따라 수초 만에 인스턴스를 추가하거나 제거할 수 있다.

### 4.2 EC2 인스턴스 생성 시 결정사항

항목| 설명| 예시  
---|---|---  
**이름 및 태그**|  리소스 식별·관리용 태그 부여| `Name: web-server-01`, `Env: production`  
**AMI**|  인스턴스의 OS 이미지 템플릿| Ubuntu 24.04 LTS, Amazon Linux 2023  
**인스턴스 유형**|  CPU/메모리 조합| `t3.medium` (2vCPU, 4GB)  
**키 페어**|  SSH 접속을 위한 공개키/프라이빗키| `user-key.pem`  
**네트워크/보안**|  VPC, 서브넷, 보안 그룹 설정| default VPC, port 22/80/443 허용  
**스토리지**|  EBS 볼륨 크기와 타입| 20GB gp3  
**사용자 데이터**|  인스턴스 최초 시작 시 실행할 스크립트| Nginx 자동 설치  
  
### 4.3 AMI (Amazon Machine Image)

AMI는 EC2 인스턴스의 템플릿이다. 한 번 설정한 환경을 AMI로 저장해두면, 동일한 환경을 여러 인스턴스로 즉시 복제할 수 있다.

AMI 구성요소:

  * **루트 볼륨 템플릿** : OS, 앱 서버, 애플리케이션
  * **시작 권한** : 어느 AWS 계정이 이 AMI로 인스턴스를 시작할 수 있는지
  * **블록 디바이스 매핑** : 인스턴스 시작 시 어떤 볼륨을 연결할지



AMI를 얻는 방법:  
1\. **AWS 제공 AMI** : Ubuntu, Amazon Linux, Windows Server 등 공식 이미지  
2\. **AWS Marketplace** : 상용 소프트웨어가 사전 설치된 이미지  
3\. **직접 생성** : 기존 인스턴스에서 커스텀 AMI 생성

AMI의 장점: **반복 가능(Repeatable)** , **재사용 가능(Reusable)** , **복구 가능(Recoverable)**

### 4.4 인스턴스 유형 이름 읽기

인스턴스 유형 이름은 규칙이 있다.
[code] 
    c  7  g  n  .  2xlarge
    │  │  │  │     └─── 인스턴스 크기
    │  │  │  └──────── 옵션 (n = 네트워크 최적화)
    │  │  └─────────── 프로세서 (g = AWS Graviton ARM)
    │  └────────────── 세대 (숫자 높을수록 최신)
    └───────────────── 인스턴스 패밀리
[/code]

**인스턴스 패밀리 상세** :

패밀리| 특징| 사용 케이스  
---|---|---  
**T (버스트 가능 범용)**|  평소 낮은 CPU, 필요 시 버스트| 개발/테스트, 소규모 웹서버  
**M (범용)**|  CPU:메모리 = 1:4 균형| 웹/앱 서버, 중간 규모 DB  
**C (컴퓨팅 최적화)**|  CPU:메모리 = 1:2| 배치 처리, HPC, 게임 서버, ML 추론  
**R (메모리 최적화)**|  CPU:메모리 = 1:8 이상| 대용량 인메모리 DB, 실시간 빅데이터  
**I (스토리지 최적화)**|  고성능 NVMe SSD| NoSQL, 데이터웨어하우스  
**P/G (가속 컴퓨팅)**|  GPU 탑재| ML 훈련, 영상 렌더링, 과학 계산  
  
최신 세대 인스턴스를 쓰는 게 유리하다 — 이전 세대 대비 성능 향상, 비용 절감, 더 나은 확장성.

### 4.5 테넌시와 배치 그룹

**테넌시(Tenancy)** — EC2가 어느 물리 서버에서 실행되는지 결정

테넌시| 설명| 비용  
---|---|---  
공유 테넌시| 다른 고객과 하드웨어 공유| 가장 저렴  
전용 인스턴스| 전용 하드웨어, 하지만 AWS가 배치| 비쌈  
전용 호스트| 특정 물리 서버를 통째로 점유, 소켓 단위 제어| 가장 비쌈  
  
**배치 그룹(Placement Group)**

유형| 배치 방식| 사용 케이스  
---|---|---  
클러스터| 서로 인접하게| HPC — 낮은 지연시간, 높은 처리량  
분산형| 여러 랙에 분산| 의료 기록 시스템 — 내결함성  
파티션| 논리 그룹으로 분할| Kafka, Hadoop — 대규모 분산 워크로드  
  
### 4.6 사용자 데이터 (User Data)

인스턴스가 최초로 시작될 때 루트 권한으로 자동 실행되는 스크립트다. Kubernetes 설치, 웹서버 초기화 등에 활용한다.
[code] 
    #!/bin/bash
    # Ubuntu 예시: 인스턴스 시작 시 Nginx 자동 설치
    apt update -y
    apt install -y nginx
    systemctl start nginx
    systemctl enable nginx
[/code]

### 4.7 EC2 구매 옵션 — 비용 최적화

옵션| 할인율| 약정| 특징  
---|---|---|---  
**온디맨드**|  기준가| 없음| 언제든 시작/종료, 단기 임시 워크로드  
**Compute Savings Plans**|  최대 66%| 1/3년| EC2, Fargate, Lambda에 유연 적용  
**EC2 Instance Savings Plans**|  최대 72%| 1/3년| 특정 리전·패밀리 고정, 가장 저렴  
**스팟 인스턴스**|  최대 90%| 없음| AWS 여유 용량 사용, 중단 가능성 있음  
  
실전 조합 전략: **온디맨드(베이스) + Savings Plans(예측 가능한 부분) + Spot(내결함성 워크로드)**

### 4.8 서버리스 컴퓨팅 — AWS Lambda

서버를 프로비저닝·관리할 필요 없이 코드만 올리면 이벤트 발생 시 자동 실행된다.
[code] 
    이벤트 소스 (S3 업로드, API Gateway 요청, DynamoDB 변경 등)
        ↓
    Lambda 함수 실행 (코드)
        ↓ (선택적)
    응답 반환
[/code]

**Lambda 특징** :

  * 지원 런타임: Python, Node.js, Java, Go, Ruby, C# 등
  * 최대 실행 시간: **15분**
  * 최대 메모리: **10GB**
  * 요금: 요청 수 + 실행 시간 기준 (밀리초 단위)



**Lambda 활용 예시** :

  * API Gateway + Lambda = 서버리스 REST API
  * S3 업로드 이벤트 + Lambda = 이미지 리사이징 자동화
  * CloudWatch 스케줄 + Lambda = 주기적 배치 작업



* * *

## 5\. Amazon S3 — 객체 스토리지

### 5.1 S3 개념과 구조

Amazon S3(Simple Storage Service)는 **무제한 용량의 객체 스토리지 서비스** 다. 파일 시스템이 아닌 Key-Value 방식으로 데이터를 저장한다.
[code] 
    버킷(Bucket): 최상위 컨테이너. 이름은 전 세계에서 유일해야 함.
    └── 객체(Object): 실제 데이터
        ├── Key   : 객체의 전체 경로 (예: images/2024/photo.jpg)
        ├── Value : 파일 데이터 (최대 5TB)
        └── Metadata: Content-Type, ETag, 사용자 정의 태그 등
[/code]

S3 주요 특성:

항목| 내용  
---|---  
**내구성**|  99.999999999% (11 nines) — 데이터 자동 3중 복제  
**가용성**|  Standard 기준 99.99% SLA  
**용량**|  무제한 (단일 객체 최대 5TB)  
**버킷 이름**|  전 세계 고유, 소문자·숫자·하이픈만 허용  
**범위**|  특정 리전에 버킷 생성, 리전 내 여러 AZ에 자동 복제  
  
S3 URL 형식:
[code] 
    https://버킷이름.s3.리전코드.amazonaws.com/키이름
    https://my-app.s3.ap-northeast-2.amazonaws.com/images/profile.jpg
[/code]

### 5.2 S3 스토리지 클래스

데이터 접근 빈도에 따라 최적의 클래스를 선택해 비용을 절감한다.

클래스| 가용성| 최소 보존| 복구 시간| 사용 케이스  
---|---|---|---|---  
**Standard**|  99.99%| 없음| 즉시| 자주 접근 (웹 서빙, 분석)  
**Intelligent-Tiering**|  99.9%| 없음| 즉시| 접근 패턴 불규칙  
**Standard-IA**|  99.9%| 30일| 즉시| 월 1회 미만 접근, DR 백업  
**One Zone-IA**|  99.5%| 30일| 즉시| 재생성 가능한 데이터, 저비용  
**Glacier Instant Retrieval**|  99.9%| 90일| 밀리초| 분기별 접근  
**Glacier Flexible Retrieval**|  99.99%| 90일| 1분~12시간| 연간 접근, 아카이브  
**Glacier Deep Archive**|  99.99%| 180일| 12~48시간| 7~10년 장기 보관, 규정 준수  
  
### 5.3 S3 버전 관리 (Versioning)

버전 관리 활성화 시 같은 Key에 파일을 덮어써도 이전 버전이 모두 보존된다.
[code] 
    버전 관리 비활성: 업로드 → 덮어쓰기 → 이전 파일 영구 삭제
    
    버전 관리 활성:
      photo.jpg 업로드   → ID: ver-001
      photo.jpg 재업로드 → ID: ver-002  (ver-001 유지)
      삭제 요청          → 삭제 마커(Delete Marker) 추가, 실제 파일 보존
      특정 버전 삭제     → 해당 ID만 삭제, 나머지 유지
[/code]

  * CodePipeline S3 소스 트리거에 버전 관리 활성화 **필수**
  * 각 버전마다 별도 과금



### 5.4 수명 주기 정책 (Lifecycle Policy)

시간 경과에 따라 데이터를 자동으로 더 저렴한 클래스로 전환하거나 삭제한다.
[code] 
    업로드 → S3 Standard
        ↓ 30일 후 자동 전환
    S3 Standard-IA
        ↓ 60일 후 자동 전환
    S3 Glacier Flexible Retrieval
        ↓ 270일 후
    자동 삭제
[/code]

### 5.5 주요 기능

**정적 웹사이트 호스팅** : HTML, CSS, JS 파일을 S3에서 직접 서빙. 별도 웹 서버 불필요.

**Presigned URL** : 프라이빗 버킷 객체에 대한 시간 제한 접근 URL 생성.
[code] 
    import boto3
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'my-bucket', 'Key': 'report.pdf'},
        ExpiresIn=3600  # 1시간 유효
    )
[/code]

**S3 Transfer Acceleration** : CloudFront 엣지 로케이션 경유로 업로드 속도 최적화. 지리적으로 먼 클라이언트에서 대용량 업로드 시 유용.

**교차 리전 복제 (CRR)** : 다른 리전 버킷에 객체를 자동 복제. DR, 지연 시간 감소, 데이터 주권 준수 목적.

* * *

## 6\. Amazon EBS — EC2 블록 스토리지

### 6.1 EBS 개념

EBS(Elastic Block Store)는 EC2 인스턴스에 연결하는 **네트워크 기반 블록 스토리지** 다.
[code] 
    EC2 인스턴스 ←── 네트워크 ──→ EBS 볼륨 (독립적으로 존재)
[/code]

EBS 특성:

  * **독립적 생존** : EC2가 종료돼도 볼륨은 유지됨 (Delete on Termination 설정에 따라)
  * **AZ 범위** : 동일 AZ 내 EC2에만 연결 가능
  * **스냅샷** : S3에 증분 백업. 다른 AZ/리전으로 복사해 활용 가능
  * **기본 연결** : 하나의 EBS는 하나의 EC2에만 연결 (io1/io2 Multi-Attach는 예외)



### 6.2 EBS 볼륨 타입

타입| 분류| 최대 IOPS| 최대 처리량| 특징 및 사용 케이스  
---|---|---|---|---  
**gp3**|  SSD 범용| 16,000| 1,000 MB/s| **신규 기본값**. 용량과 IOPS 독립 설정 가능  
**gp2**|  SSD 범용| 16,000| 250 MB/s| 구형. IOPS = 용량(GB) × 3 자동 결정 (gp3 권장)  
**io2 Block Express**|  프로비저닝 IOPS SSD| 256,000| 4,000 MB/s| 최고 성능 DB (SAP HANA, Oracle RAC)  
**io1**|  프로비저닝 IOPS SSD| 64,000| 1,000 MB/s| 고성능 DB, 지연 시간 민감 워크로드  
**st1**|  처리량 최적화 HDD| 500| 500 MB/s| Hadoop, Kafka, 로그 처리 (순차 읽기/쓰기)  
**sc1**|  콜드 HDD| 250| 250 MB/s| 접근 빈도 낮은 아카이브 데이터 (최저 비용)  
  
> **gp3 vs gp2** : gp3는 용량과 IOPS/처리량을 각각 독립적으로 설정 가능. 동일 성능 대비 gp3가 최대 20% 저렴하며 AWS 권장 타입.

### 6.3 EBS 스냅샷

스냅샷은 EBS 볼륨의 특정 시점 백업. S3에 저장되며 증분(Incremental) 방식으로 변경된 블록만 저장한다.
[code] 
    첫 번째 스냅샷: 전체 볼륨 저장
    두 번째 스냅샷: 첫 번째 이후 변경 블록만 저장
    세 번째 스냅샷: 두 번째 이후 변경 블록만 저장
    (각 스냅샷은 독립적으로 복원 가능)
[/code]

활용:

  * 볼륨을 다른 AZ로 이동: 스냅샷 생성 → 대상 AZ에서 볼륨 복원
  * 다른 리전 복사: 스냅샷 복사(Copy) → 복사된 스냅샷으로 볼륨 생성
  * AMI 생성의 기반: EC2 인스턴스 상태를 AMI로 저장 시 EBS 스냅샷이 함께 생성



* * *

## 7\. AWS 데이터베이스 서비스

### 7.1 관계형 vs 비관계형 — 어떤 DB를 선택할까?

특성| 관계형(SQL)| 비관계형(NoSQL)  
---|---|---  
데이터 구조| 행과 열로 이뤄진 테이블| 키-값, 문서, 와이드 컬럼, 그래프  
스키마| 고정됨 (변경이 어려움)| 동적 (자유롭게 변경 가능)  
확장 방식| 수직 확장 (서버 업그레이드)| 수평 확장 (서버 추가)  
일관성| 강력한 일관성 (ACID)| 최종적 일관성 (BASE) 지원  
AWS 서비스| RDS, Aurora| DynamoDB, ElastiCache  
선택 기준| 엄격한 스키마, 트랜잭션 필요| 유연한 데이터, 초고속 읽기/쓰기 필요  
  
### 7.2 Amazon RDS — 관리형 관계형 데이터베이스

RDS는 MySQL, PostgreSQL, Oracle, SQL Server, MariaDB, IBM Db2를 관리형으로 제공한다. 설치·패치·백업·복제·모니터링을 AWS가 담당한다.

**관리형 서비스의 장점** :

항목| EC2에 직접 설치| Amazon RDS  
---|---|---  
OS 설치/패치| 직접| AWS  
DB 소프트웨어 패치| 직접| AWS  
백업| 직접| AWS (자동)  
고가용성 구성| 직접| Multi-AZ 클릭 한 번  
스케일링| 직접| 콘솔에서 변경  
  
**Multi-AZ 배포 — 고가용성**

![RDS Multi-AZ and Read Replica diagram](https://media.geeksforgeeks.org/wp-content/uploads/20231209123630/Blank-diagram.jpeg)
[code] 
    가용 영역 1                가용 영역 2
    ┌──────────────────┐      ┌──────────────────┐
    │  프라이머리 DB   │      │  대기 DB (Standby) │
    │  (읽기/쓰기)     │←───→│  (평상시 미사용)   │
    └──────────────────┘  동기식   └──────────────────┘
           ↑                복제
        장애 발생
           ↓
      대기 DB 자동 승격
      (수분 내 복구)
[/code]

  * 프라이머리 DB에서 대기 DB로 **동기식 복제**
  * 프라이머리 장애 시 → 대기 DB가 자동으로 프라이머리로 승격
  * 애플리케이션은 같은 DNS 엔드포인트를 계속 사용 → 코드 변경 불필요
  * 대기 DB는 읽기에 사용되지 않음 (순수 대기 목적)



**읽기 전용 복제본 — 읽기 성능 향상**
[code] 
    프라이머리 DB
    (읽기/쓰기)
         │
         └── 비동기 복제
              ↓
      읽기 전용 복제본 #1  ← 리포트, 통계 쿼리
      읽기 전용 복제본 #2  ← 분석 작업
      읽기 전용 복제본 #3  ← 다른 리전 (교차 리전 복제)
[/code]

  * RDS당 최대 **5개** , Aurora는 최대 **15개** 읽기 전용 복제본
  * 비동기 복제 — 프라이머리와 약간의 지연(lag) 존재
  * Multi-AZ + 읽기 복제본을 동시에 사용 가능



### 7.3 Amazon Aurora — 클라우드 전용 고성능 DB

Aurora는 AWS가 처음부터 클라우드용으로 설계한 관계형 DB다. MySQL과 PostgreSQL과 호환된다.

**Aurora가 특별한 이유** :

항목| MySQL on RDS| Aurora  
---|---|---  
성능| 기준| MySQL 대비 최대 5배  
데이터 복사본| 2개 (Multi-AZ)| 3개 AZ × 2 = **6개 복사본**  
읽기 복제본| 최대 5개| 최대 15개  
스토리지| 수동 확장| **자동 확장** (최대 128TB)  
  
Aurora DB 클러스터 구조:
[code] 
    클러스터 엔드포인트 (읽기/쓰기)
        │
    프라이머리 인스턴스 (읽기/쓰기)
        │
        ├── Aurora 복제본 1 (읽기 전용, AZ-1)
        ├── Aurora 복제본 2 (읽기 전용, AZ-2)
        └── Aurora 복제본 3 (읽기 전용, AZ-3)
    
    클러스터 볼륨 (3개 AZ × 2 = 6개 복사본, 자동 복구)
[/code]

### 7.4 Amazon DynamoDB — 완전 관리형 NoSQL

서버 관리가 전혀 필요 없는 완전 관리형 키-값/문서 NoSQL 데이터베이스다.

**DynamoDB 기본 구조** :
[code] 
    테이블: Gamers
    ┌──────────────┬──────────────┬───────┬────────┬──────────┐
    │  GamerTag    │  GameID      │ Level │ Score  │ TopScore │
    │ (파티션 키)  │ (정렬 키)   │       │        │          │
    ├──────────────┼──────────────┼───────┼────────┼──────────┤
    │ "Hammer57"   │ "PuzzleGame" │  21   │  4050  │  483610  │
    │ "FluffyDuffy"│ "MysteryGame"│   5   │  1123  │   10863  │
    └──────────────┴──────────────┴───────┴────────┴──────────┘
[/code]

  * **파티션 키(Partition Key)** : 데이터 분산의 기준. 고르게 분산될수록 성능이 좋음
  * **정렬 키(Sort Key)** : 선택적. 파티션 키 + 정렬 키 = 복합 기본 키
  * **속성** : 나머지 데이터. 행마다 다른 속성을 가질 수 있음 (스키마 유연성)



**용량 모드** :

모드| 설명| 사용 시점  
---|---|---  
온디맨드| 요청 당 과금| 트래픽 예측 불가, 스파이크 워크로드  
프로비저닝| RCU/WCU 사전 설정| 트래픽 예측 가능, 비용 최적화  
  
  * **RCU (읽기 용량 단위)** : 최대 4KB 항목 1회 읽기
  * **WCU (쓰기 용량 단위)** : 최대 1KB 항목 1회 쓰기



**읽기 일관성** :

유형| RCU 소비| 설명  
---|---|---  
강력한 읽기 일관성| 1 RCU| 가장 최신 데이터 보장  
최종적 읽기 일관성| 0.5 RCU| 약간의 지연 가능, 비용 절감  
  
### 7.5 캐싱 전략 — ElastiCache

DB에 반복적으로 같은 쿼리를 날리는 건 낭비다. **자주 읽히는 데이터를 메모리에 캐싱** 해두면 응답 시간을 대폭 단축할 수 있다.

ElastiCache는 Redis와 Memcached를 관리형으로 제공한다.

**어떤 데이터를 캐싱해야 할까?**

  * 쿼리가 느리고 비용이 많이 드는 데이터
  * 자주 읽히지만 자주 바뀌지 않는 데이터 (상품 목록, 사용자 프로필 등)



**캐싱 전략 1 — Lazy Loading (지연 로딩)**
[code] 
    1. 요청 → 캐시 확인
    2. 캐시 HIT → 즉시 반환 (빠름)
       캐시 MISS → DB 조회 → 캐시에 저장 → 반환 (느림, but 다음엔 빠름)
[/code]

장점: 캐시에는 실제로 요청된 데이터만 저장됨  
단점: 첫 번째 요청은 항상 느림 (Cache Miss)

**캐싱 전략 2 — Write-Through (쓰기 시 동기화)**
[code] 
    쓰기 요청
        → DB에 저장
        → 캐시에도 즉시 저장
[/code]

장점: 캐시 데이터가 항상 최신  
단점: 모든 쓰기 작업에서 캐시도 업데이트 (오버헤드)

**캐시 만료 — TTL (Time To Live)**
[code] 
    # Redis 예시: 1시간 후 자동 만료
    cache.set("user:123", user_data, ex=3600)
[/code]

캐시 메모리가 가득 차면 **제거 정책(Eviction Policy)** 적용:

  * **LRU (Least Recently Used)** : 가장 오래 사용되지 않은 데이터 제거
  * **LFU (Least Frequently Used)** : 사용 빈도가 가장 낮은 데이터 제거
  * **TTL 기반** : TTL이 가장 짧은 데이터 제거



* * *

## 8\. AWS 네트워크 — VPC 완전 이해

![AWS VPC Architecture — 퍼블릭/프라이빗 서브넷, NAT 게이트웨이, 보안 그룹 구조](https://media.geeksforgeeks.org/wp-content/uploads/20230919120127/Screenshot-2023-09-19-120048-768.png)

### 8.1 VPC (Virtual Private Cloud)

VPC는 **AWS 클라우드 안에 사용자가 직접 정의하는 격리된 가상 네트워크** 다. 단일 AWS 리전에 연결된다.

VPC 특징:

  * 워크로드를 논리적으로 격리
  * 리소스에 사용자 정의 액세스 제어와 보안 설정 적용
  * 기본 VPC가 이미 리전마다 생성되어 있음



### 8.2 IP 주소와 CIDR

**CIDR(Classless Inter-Domain Routing)** — IP 주소 범위를 지정하는 표기법
[code] 
    10.22.0.0/16
    │         └── 앞 16비트를 네트워크 주소로 예약
    └──────────── IPv4 주소
    
    범위: 10.22.0.0 ~ 10.22.255.255 (65,536개 IP)
[/code]

CIDR| IP 개수| 사용 예시  
---|---|---  
`/16`| 65,536| VPC  
`/20`| 4,096| 대형 서브넷  
`/24`| 256| 일반 서브넷  
`/28`| 16| 소형 서브넷  
  
> AWS는 각 서브넷에서 5개의 IP를 예약한다 (네트워크 주소, VPC 라우터, DNS, 미래 사용, 브로드캐스트).

### 8.3 서브넷 — 퍼블릭과 프라이빗

서브넷은 VPC CIDR 블록의 하위 집합이다. 각 서브넷은 하나의 가용 영역에 속한다.
[code] 
    VPC: 172.31.0.0/16 (서울 리전)
    ├── AZ-1 (ap-northeast-2a)
    │   ├── 퍼블릭 서브넷: 172.31.0.0/20   ← 웹 서버, ALB
    │   └── 프라이빗 서브넷: 172.31.32.0/20 ← 앱 서버, DB
    └── AZ-2 (ap-northeast-2b)
        ├── 퍼블릭 서브넷: 172.31.16.0/20
        └── 프라이빗 서브넷: 172.31.48.0/20
[/code]

**퍼블릭 서브넷** : 인터넷에서 직접 접근 가능 → 웹 서버, Load Balancer  
**프라이빗 서브넷** : 인터넷에서 직접 접근 불가 → 앱 서버, 데이터베이스

### 8.4 인터넷 게이트웨이 (IGW)

인터넷 게이트웨이는 VPC와 인터넷 사이의 관문이다. 퍼블릭 서브넷의 인스턴스가 인터넷과 통신하려면 반드시 필요하다.

IGW 역할:  
1\. VPC 리소스와 인터넷 간의 통신 허용  
2\. NAT(Network Address Translation) 수행 — 프라이빗 IP ↔ 퍼블릭 IP 변환

**퍼블릭 서브넷 조건** (세 가지 모두 필요):  
1\. VPC에 IGW 연결  
2\. 라우팅 테이블에 `0.0.0.0/0 → IGW` 경로 추가  
3\. 인스턴스에 퍼블릭 IP 할당

### 8.5 라우팅 테이블

라우팅 테이블은 네트워크 트래픽 경로를 결정하는 규칙 집합이다.

**퍼블릭 서브넷 라우팅 테이블** :
[code] 
    Destination      Target
    172.31.0.0/16    local          ← VPC 내부 통신
    0.0.0.0/0        igw-xxxxx      ← 모든 외부 트래픽 → IGW로
[/code]

**프라이빗 서브넷 라우팅 테이블** (기본):
[code] 
    Destination      Target
    172.31.0.0/16    local          ← VPC 내부 통신만 가능
[/code]

**프라이빗 서브넷 라우팅 테이블** (NAT 추가 시):
[code] 
    Destination      Target
    172.31.0.0/16    local
    0.0.0.0/0        nat-xxxxx      ← 외부 트래픽 → NAT GW로
[/code]

### 8.6 NAT 게이트웨이

프라이빗 서브넷의 인스턴스가 인터넷에 **아웃바운드(나가는) 통신** 이 필요할 때 사용한다 (소프트웨어 업데이트, 외부 API 호출 등). 단, **인바운드(들어오는) 직접 접속은 차단** 된다.
[code] 
    프라이빗 인스턴스 (172.31.32.75)
        │ 소스 IP: 172.31.32.75
        ▼
    NAT 게이트웨이 (퍼블릭 서브넷에 위치)
        │ 소스 IP를 탄력적 IP(203.0.133.15)로 변환
        ▼
    인터넷 게이트웨이
        │
        ▼
    인터넷
[/code]

NAT GW는 반드시 **퍼블릭 서브넷** 에 위치하고, **탄력적 IP(EIP)** 를 부여해야 한다.

**탄력적 IP(Elastic IP)** : 인스턴스를 재시작해도 변하지 않는 고정 공인 IP.

### 8.7 보안 그룹 vs 네트워크 ACL

AWS에는 두 가지 방화벽 계층이 있다.

항목| 보안 그룹 (Security Group)| 네트워크 ACL (NACL)  
---|---|---  
**적용 단위**|  인스턴스 (ENI 수준)| 서브넷 수준  
**규칙 유형**|  허용 규칙만| 허용 + 거부 규칙  
**상태**| **Stateful** — 응답 트래픽 자동 허용| **Stateless** — 인바운드/아웃바운드 각각 설정  
**규칙 평가**|  모든 규칙을 동시 평가| 번호 순서대로 평가, 첫 번째 매칭에서 종료  
**기본 규칙**|  모든 인바운드 차단, 모든 아웃바운드 허용| 모든 트래픽 허용  
  
**트래픽 흐름** :
[code] 
    인터넷
      ↓
    NACL 인바운드 규칙 (서브넷 경계에서 1차 필터링)
      ↓
    보안 그룹 인바운드 규칙 (인스턴스 바로 앞에서 2차 필터링)
      ↓
    EC2 인스턴스
      ↓
    보안 그룹 아웃바운드 규칙
      ↓
    NACL 아웃바운드 규칙 (Stateless라서 명시적으로 설정 필요)
      ↓
    인터넷
[/code]

**보안 그룹 실전 설정 예시** :
[code] 
    웹 서버 보안 그룹 인바운드:
    - HTTPS 443 / 0.0.0.0/0   ← 모든 곳에서 HTTPS 허용
    - HTTP 80  / 0.0.0.0/0    ← 모든 곳에서 HTTP 허용
    - SSH 22   / 내 IP만       ← 관리자 접속만 허용
    
    앱 서버 보안 그룹 인바운드:
    - TCP 8080 / 웹 서버 보안 그룹 ID  ← 웹 서버에서만 접근 허용
    
    DB 서버 보안 그룹 인바운드:
    - TCP 3306 / 앱 서버 보안 그룹 ID  ← 앱 서버에서만 MySQL 접근 허용
[/code]

이렇게 보안 그룹을 **서로 참조** 하면 IP 대신 리소스 단위로 접근을 제어할 수 있다.

* * *

## 9\. ELB — Elastic Load Balancer

### 9.1 로드 밸런서 개념

ELB(Elastic Load Balancer)는 들어오는 트래픽을 여러 대상(EC2, 컨테이너, Lambda 등)에 자동 분산시키는 완전 관리형 서비스다.
[code] 
    클라이언트 요청
        ↓
    ELB (단일 진입점 — DNS 이름 고정)
        ↓ 트래픽 분산 (라운드 로빈, 최소 연결 등)
    ┌───────┬───────┬───────┐
    │ EC2-1 │ EC2-2 │ EC2-3 │
    └───────┴───────┴───────┘
[/code]

ELB 제공 기능:

  * **헬스 체크** : 비정상 대상을 자동으로 라우팅에서 제외 (설정한 간격마다 HTTP/TCP 확인)
  * **고가용성** : 여러 AZ에 걸쳐 자동 분산 (Cross-Zone Load Balancing)
  * **SSL/TLS 종료** : ELB에서 인증서 처리, EC2는 HTTP만 처리하면 됨
  * **고정 세션(Sticky Session)** : 동일 클라이언트를 동일 대상으로 지속 라우팅



### 9.2 ELB 유형 4가지

유형| OSI 계층| 라우팅 기준| 주요 프로토콜| 사용 케이스  
---|---|---|---|---  
**ALB** (Application)| 7계층| URL 경로, 헤더, 메서드, 쿼리 파라미터| HTTP/HTTPS, gRPC, WebSocket| 웹 앱, MSA, API Gateway 앞단  
**NLB** (Network)| 4계층| IP + 포트| TCP, UDP, TLS| 초저지연, 고성능, 고정 IP 필요 시  
**CLB** (Classic)| 4/7계층 혼합| 기본 HTTP/TCP| HTTP, HTTPS, TCP| 구형 (신규 사용 비권장)  
**GWLB** (Gateway)| 3계층| IP 패킷 전체| IP (GENEVE 캡슐화)| 방화벽·IDS/IPS 어플라이언스 투명 삽입  
  
### 9.3 ALB — Application Load Balancer

L7 레벨에서 동작하므로 **URL 경로** , **호스트 헤더** , **HTTP 메서드** 등으로 트래픽을 세밀하게 분기할 수 있다.
[code] 
    ALB 리스너 (HTTPS:443)
        │
        ├── 규칙 1: Host = api.example.com       → Target Group A (API 서버)
        ├── 규칙 2: Path = /images/*              → Target Group B (이미지 서버)
        ├── 규칙 3: Path = /admin/* + IP 조건    → Target Group C (관리 서버)
        └── 기본 규칙                             → Target Group D (웹 서버)
[/code]

**Target Group** : ALB가 트래픽을 전달할 대상들의 집합

  * 대상 유형: EC2 인스턴스, IP 주소, Lambda 함수, 다른 ALB
  * Target Group 단위로 헬스 체크, 포트, 프로토콜 설정
  * **하나의 ALB로 여러 MSA 서비스 라우팅** → 로드밸런서 비용 절감



### 9.4 NLB — Network Load Balancer

L4(TCP/UDP) 레벨 동작. 초당 수백만 요청을 밀리초 수준 지연으로 처리.

NLB 선택 기준:

  * 극도로 낮은 지연 시간이 필요한 실시간 서비스 (게임, 금융 트랜잭션)
  * HTTP가 아닌 TCP/UDP 프로토콜 직접 처리
  * **고정 IP 주소 필요** (NLB는 AZ마다 고정 IP 제공, ALB는 IP가 변함)
  * AWS PrivateLink 기반 서비스 노출



* * *

## 10\. EC2 Auto Scaling

### 10.1 Auto Scaling 개념

Auto Scaling은 애플리케이션 부하에 따라 EC2 인스턴스 수를 자동으로 조절하는 서비스다. **수평 확장(Scale Out/In)** 을 자동화한다.
[code] 
    트래픽 급증 → CPU 70% 초과 감지 → 인스턴스 추가 (Scale Out)
    트래픽 감소 → CPU 30% 미만 유지 → 인스턴스 제거 (Scale In)
[/code]

**Auto Scaling Group(ASG) 핵심 설정값** :

설정| 설명| 예시  
---|---|---  
**최소 용량 (Min)**|  항상 유지할 인스턴스 최솟값| 2  
**최대 용량 (Max)**|  절대 초과하지 않을 상한선| 10  
**희망 용량 (Desired)**|  현재 목표 인스턴스 수| 4  
**시작 템플릿**|  신규 인스턴스 생성 명세 (AMI, 유형, SG 등)| lt-0abc1234  
  
### 10.2 Auto Scaling 정책 4가지

**① 목표 추적 조정 (Target Tracking)** — 권장  
지정 지표를 목표값으로 자동 유지. 설정이 가장 간단하고 효과적이다.
[code] 
    설정: "ALB RequestCountPerTarget = 1000"
    → 대상당 요청이 1000을 초과 → 인스턴스 자동 추가
    → 요청이 감소 → 인스턴스 자동 제거
[/code]

사용 가능 지표: `CPUUtilization`, `ALBRequestCountPerTarget`, `NetworkIn/Out`

**② 단계 조정 (Step Scaling)**  
지표 수치 구간별로 단계적으로 다른 크기 조정.
[code] 
    CPU 60~70% → +1개
    CPU 70~85% → +3개
    CPU 85% 이상 → +5개
[/code]

**③ 단순 조정 (Simple Scaling)**  
CloudWatch 알람 하나에 고정 수량 조정. (현재는 Step Scaling으로 대체 추세)

**④ 예약 조정 (Scheduled Scaling)**  
특정 시간대에 미리 용량 조정.
[code] 
    매일 오전 08:00 → 인스턴스 10개 (업무 시작 대비)
    매일 자정 00:00 → 인스턴스 2개 (야간 최소 운영)
[/code]

### 10.3 ELB + Auto Scaling 통합 동작
[code] 
    인터넷
      ↓
    ALB (헬스 체크, 트래픽 분산)
      ↓
    Auto Scaling Group
      ├── EC2 인스턴스 1  ← ASG가 ALB Target Group에 자동 등록
      ├── EC2 인스턴스 2
      └── EC2 인스턴스 3  (부하 증가 시 자동 추가)
[/code]

  * 신규 인스턴스 기동 → ALB Target Group에 **자동 등록** → 헬스 체크 통과 후 트래픽 수신
  * 인스턴스 제거 전 **Connection Draining**(기존 요청 처리 완료) 후 제거
  * 헬스 체크 실패 인스턴스 → ASG가 자동 **종료 후 새 인스턴스 교체**



* * *

## 11\. Route53 + CloudFront

### 11.1 Amazon Route53 — DNS 서비스

Route53은 AWS의 완전 관리형 DNS(Domain Name System) 서비스다.
[code] 
    사용자: "www.example.com" 입력
        ↓
    Route53 DNS 조회
        ↓
    IP 주소 반환 (예: 52.95.110.1)
        ↓
    해당 IP로 실제 연결
[/code]

Route53 3가지 기능:  
1\. **도메인 등록** : Route53에서 직접 도메인 구매 가능  
2\. **DNS 레코드 관리** : A, AAAA, CNAME, MX, TXT, NS, SOA 레코드 관리  
3\. **트래픽 라우팅 + 헬스 체크** : 엔드포인트 상태를 모니터링해 자동 장애 전환

### 11.2 Route53 라우팅 정책 6가지

**① 단순 라우팅 (Simple)**

  * 도메인 → 단일 IP 반환
  * 헬스 체크 불가, 레코드 하나에 여러 IP 등록 시 무작위 반환



**② 가중치 기반 라우팅 (Weighted)**
[code] 
    api.example.com
      ├── 서울 ALB (가중치 70) → 전체 트래픽의 70%
      └── 도쿄 ALB (가중치 30) → 전체 트래픽의 30%
[/code]

카나리 배포(신버전에 일부 트래픽 먼저 전송), 부하 분산에 활용.

**③ 지연 시간 기반 라우팅 (Latency)**  
사용자와 각 AWS 리전 간 네트워크 지연 시간을 측정해 **가장 빠른 리전** 의 엔드포인트를 반환.  
글로벌 서비스에서 사용자 경험 최적화에 사용.

**④ 장애 조치 라우팅 (Failover)**
[code] 
    Primary: 서울 리전 ALB  ← 헬스 체크 정상 시 100% 트래픽
        ↓ 헬스 체크 실패
    Secondary: 도쿄 리전 ALB  ← 자동 전환 (Active-Passive DR)
[/code]

**⑤ 지리 위치 라우팅 (Geolocation)**  
클라이언트의 **물리적 위치**(국가, 대륙)를 기반으로 라우팅.
[code] 
    한국 → 서울 리전 엔드포인트
    미국 → us-east-1 엔드포인트
    EU → eu-west-1 엔드포인트
    기타 → 기본 레코드
[/code]

데이터 주권, 콘텐츠 현지화, GDPR 준수 등에 활용.

**⑥ 다중값 응답 (Multivalue Answer)**  
최대 8개의 정상 레코드를 무작위로 반환. 헬스 체크와 연동 가능.  
ELB 대체용이 아닌 클라이언트 측 단순 분산 보조 수단.

### 11.3 Amazon CloudFront — CDN

CloudFront는 AWS의 콘텐츠 전송 네트워크(CDN) 서비스다. 전 세계 **450개 이상의 엣지 로케이션** 에서 콘텐츠를 캐싱해 지연 시간을 줄인다.
[code] 
    오리진 서버 (S3 / ALB / EC2 / API Gateway)
        ↑ 캐시 MISS 시에만 요청 (오리진 부하 감소)
    CloudFront 배포 (Distribution)
        ↑ 캐시 HIT 시 엣지에서 즉시 반환
    엣지 로케이션 (사용자와 가장 가까운 곳)
        ↑
    사용자
[/code]

**CloudFront 주요 개념** :

용어| 설명  
---|---  
**Distribution**|  CloudFront 배포 단위. 오리진과 동작(Behavior) 설정 포함  
**Origin**|  원본 콘텐츠 위치 (S3, ALB, 커스텀 HTTP 서버)  
**OAC (Origin Access Control)**|  S3 버킷을 퍼블릭으로 열지 않고 CloudFront만 접근 허용  
**TTL**|  캐시 유지 시간 (기본 24시간, `Cache-Control` 헤더로 제어)  
**Invalidation**|  특정 경로의 캐시를 강제 삭제 (`/images/*` 패턴 지원)  
**Behavior**|  경로 패턴별 오리진, 캐시 정책, 허용 HTTP 메서드 분리 설정  
  
**CloudFront + S3 정적 웹사이트 구성** :
[code] 
    사용자 → CloudFront (HTTPS 자동 적용, 전 세계 엣지 캐싱)
                  ↑ 캐시 MISS 시만
             S3 버킷 (OAC로 접근, 버킷 자체는 프라이빗 유지)
[/code]

**캐시 정책 예시** :
[code] 
    Behavior 1: /api/*      → ALB 오리진, TTL=0 (캐시 없음, 항상 오리진 요청)
    Behavior 2: /static/*   → S3 오리진, TTL=86400 (1일 캐시)
    Behavior 3: *.jpg, *.png → S3 오리진, TTL=604800 (7일 캐시)
    기본           → ALB 오리진, TTL=0
[/code]

* * *

## 12\. 하이브리드 네트워크 — VPN vs Direct Connect

### 12.1 클라우드 배포 모델 4가지

모델| 설명| 장단점  
---|---|---  
**Public Cloud**|  AWS/Azure/GCP 단독 사용| 저비용, 빠른 시작, 유지보수 불필요  
**Private Cloud**|  기업 전용 인프라 (온프레미스)| 높은 보안/제어권, 고비용  
**Hybrid Cloud**|  Public + Private 조합| 민감 데이터는 Private, 나머지는 Public  
**Multi Cloud**|  여러 CSP 동시 사용| 벤더 종속 탈피, 복잡한 운영  
  
실제 기업들이 가장 많이 쓰는 패턴: **Hybrid Cloud** — 기존 온프레미스 인프라를 단번에 클라우드로 옮기기 어렵기 때문.

### 12.2 AWS Site-to-Site VPN

회사 데이터 센터(온프레미스)와 AWS VPC를 인터넷을 통해 **암호화 터널** 로 연결한다.
[code] 
    기업 데이터 센터
    └── 고객 게이트웨이 디바이스 (VPN 장비)
             ↕ 암호화 터널 2개 (이중화)
    └── 가상 프라이빗 게이트웨이 (AWS 측)
             └── VPC
[/code]

특징:

  * 최대 속도: **1.25Gbps**
  * 구성이 빠름 (수 시간 ~ 수 일)
  * 비활성 시 요금 없음
  * 데이터가 퍼블릭 인터넷을 경유 (암호화됨)
  * 정적(Static) 또는 동적(BGP) 라우팅 지원



### 12.3 AWS Direct Connect

데이터 센터에서 AWS까지 전용 **광 케이블** 로 직접 연결한다.
[code] 
    기업 데이터 센터
        → Direct Connect 파트너 시설 (코로케이션)
            → AWS 전용 회선
                → 가상 프라이빗 게이트웨이
                    → VPC
[/code]

특징:

  * 속도: 50Mbps(Hosted Connection 최소) ~ **100Gbps**(Dedicated Connection 최대)
  * 낮은 지연 시간, 일관된 네트워크 성능 (인터넷 혼잡 없음)
  * 데이터 기본 암호화 없음 (VPN 레이어 별도 추가 가능)
  * 특수 계약 필요, 설치에 수 주 ~ 수 개월 소요
  * 연결이 비활성 상태여도 포트 시간 비용 발생



**VPN vs Direct Connect 언제 쓸까?**

기준| VPN 선택| Direct Connect 선택  
---|---|---  
구성 속도| 빠르게 필요| 충분히 준비 시간 있음  
대역폭| 1.25Gbps 이하| 대용량 데이터 전송  
비용| 저비용| 전용 회선 비용 감수  
암호화| 기본 제공| 별도 구성 필요  
인터넷 경유| Yes (암호화됨)| No (전용 회선)  
  
* * *

## 13\. AWS IAM — 보안과 권한 관리

![AWS IAM Components — User, Group, Role, Policy 구조](https://media.geeksforgeeks.org/wp-content/uploads/20260608171005181833/IAMCOMP.webp)

### 13.1 루트 사용자의 위험성

AWS 계정을 생성하면 **루트 사용자** 가 만들어진다. 루트 사용자는 모든 AWS 서비스에 대한 전체 접근 권한을 가진다. 이 계정이 탈취되면 전체 인프라가 위험하다.

**루트 사용자로 해야 할 일** :  
1\. 결제 정보 관리  
2\. 초기 IAM 관리자 계정 생성  
3\. AWS 계정 해지

그 외 모든 일상 작업은 **IAM 사용자** 로 해야 한다.

### 13.2 IAM 핵심 구성 요소

![AWS IAM Architecture](https://media.geeksforgeeks.org/wp-content/uploads/20260608163749217807/IAM-aws.webp)

**IAM 사용자 (User)**

  * 사람이나 애플리케이션을 대표하는 엔터티
  * 고유한 자격 증명 (비밀번호, 액세스 키) 보유
  * 콘솔 접근 또는 프로그래밍 방식 접근 설정 가능



**IAM 그룹 (Group)**

  * IAM 사용자들의 집합
  * 그룹에 정책을 연결하면 모든 구성원에게 일괄 적용
  * 신규 팀원 온보딩 시 그룹에 추가하기만 하면 됨


[code] 
    그룹: Developers
    ├── 정책: AmazonEC2FullAccess
    ├── 정책: AmazonS3ReadOnly
    │
    ├── 사용자: Alice
    ├── 사용자: Bob
    └── 사용자: Charlie  ← 이 세 명 모두 위 정책 적용됨
[/code]

**IAM 역할 (Role)**

  * 임시 자격 증명을 사용하여 특정 권한을 위임
  * 사람이 아닌 **서비스** 나 **다른 계정** 에 권한 부여 시 사용
  * EC2 인스턴스, Lambda, ECS 태스크 등이 역할을 수임


[code] 
    예시: EC2 인스턴스가 S3에 파일을 업로드해야 할 때
    → EC2에 "S3 쓰기 권한" 역할을 부여
    → EC2가 역할을 수임 → 임시 자격 증명 발급 → S3 접근
    → 장기 자격 증명(액세스 키)을 코드에 하드코딩할 필요 없음
[/code]

**IAM 정책 (Policy)**

  * JSON 형식으로 권한을 정의하는 문서
  * 사용자, 그룹, 역할에 연결


[code] 
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "ec2:StartInstances",
            "ec2:StopInstances"
          ],
          "Resource": "arn:aws:ec2:*:*:instance/*",
          "Condition": {
            "StringEquals": {
              "ec2:ResourceTag/Owner": "${aws:username}"
            }
          }
        }
      ]
    }
[/code]

정책 요소:

  * **Effect** : `Allow` 또는 `Deny`
  * **Action** : 허용/거부할 작업 (예: `ec2:StartInstances`)
  * **Resource** : 대상 리소스 ARN (특정 EC2 또는 `*` 전체)
  * **Condition** : 선택적 조건 (IP, 태그, MFA 등)



**정책 유형** :

유형| 설명| 예시  
---|---|---  
AWS 관리형| AWS가 만들고 유지| `AmazonEC2FullAccess`  
고객 관리형| 직접 만든 커스텀 정책| `MyCustomPolicy`  
인라인 정책| 특정 사용자/역할에 직접 포함| 재사용 안 함  
리소스 기반 정책| 리소스에 직접 연결| S3 버킷 정책  
  
### 13.3 역할 수임 (Assume Role) 작동 방식
[code] 
    1. IAM 사용자/서비스 → STS에 역할 수임 요청
    2. AWS STS → 임시 보안 자격 증명 반환
               (Access Key + Secret Key + Session Token, 유효시간 제한)
    3. 임시 자격 증명으로 → AWS 리소스 접근
[/code]

역할은 한 번 수임하면 **일시적으로만** 유효하다. 장기 자격 증명 노출 위험이 없다.

### 13.4 AWS Organizations — 다중 계정 관리

대기업이나 성장하는 스타트업은 계정을 여러 개로 분리해 운영한다. 이유:

  * 팀별·환경별(개발/스테이징/운영) 청구 분리
  * 보안 경계 강화 (한 계정의 오류가 다른 계정에 영향 없음)
  * 규정 준수 요구사항



Organizations를 쓰면 이 계정들을 **계층 구조(OU)** 로 관리하고, 통합 결제도 가능하다.
[code] 
    관리 계정 (Root)
    └── OU: 개발
    │   ├── 계정: dev-frontend
    │   └── 계정: dev-backend
    └── OU: 스테이징
    │   └── 계정: staging
    └── OU: 운영
        ├── 계정: prod-kr
        └── 계정: prod-us
[/code]

**SCP(서비스 제어 정책)** — OU 또는 계정 수준의 최대 권한 제한
[code] 
    예시: 운영 OU에 SCP 적용
    SCP: "EC2, S3, RDS만 허용"
    → 이 OU 안의 계정들은 아무리 IAM 정책을 넓게 줘도 허용된 서비스만 사용 가능
[/code]

IAM 정책과 SCP의 교집합만 실제로 허용된다.

* * *

## 14\. VM vs Container vs MSA

![VM과 Container 아키텍처 비교](https://media.geeksforgeeks.org/wp-content/uploads/20200103130309/Capture36633.png)

### 14.1 세 가지 실행 환경 비교

**Bare Metal Server** : 물리 서버를 통째로 하나의 OS가 사용

**Virtual Machine (VM)** : 하이퍼바이저가 물리 서버를 논리적으로 분할, 각 VM이 독자적인 OS 보유

**Container** : 호스트 OS의 커널을 공유하되 프로세스 격리, 애플리케이션과 의존성만 패키징
[code] 
    Bare Metal          Virtual Machine        Container
    ┌──────────┐       ┌──┐ ┌──┐ ┌──┐       ┌──┐ ┌──┐ ┌──┐
    │    App   │       │A1│ │A2│ │A3│       │A1│ │A2│ │A3│
    ├──────────┤       │OS│ │OS│ │OS│       │Lib│ │Lib│ │Lib│
    │    OS    │       └──┘ └──┘ └──┘       └──┘ └──┘ └──┘
    ├──────────┤       ┌──────────────┐      ┌──────────────┐
    │ Hardware │       │  Hypervisor  │      │Container Engine│
    └──────────┘       ├──────────────┤      ├──────────────┤
                       │   Hardware   │      │     Host OS   │
                       └──────────────┘      ├──────────────┤
                                             │   Hardware   │
                                             └──────────────┘
[/code]

**상세 비교표** :

항목| Bare Metal| VM| Container  
---|---|---|---  
OS| 단일 OS| VM마다 별도 OS| 호스트 OS 공유  
크기| -| 수 GB| 수 MB ~ 수백 MB  
부팅 속도| 수 분| 수 분| **수 초 이내**  
격리 수준| 물리적 완전 격리| 하드웨어 수준 격리| 프로세스 수준 격리  
이식성| 낮음| 중간| **매우 높음**  
성능| 최고| 오버헤드 있음| 거의 Native에 가까움  
대표 기술| -| VMware, Hyper-V, KVM| **Docker** , containerd, Podman  
  
**상황별 선택 가이드** :

상황| 추천| 이유  
---|---|---  
초고성능 DB 서버| Bare Metal| 가상화 오버헤드 없이 최대 I/O 성능  
지연에 민감한 금융 트랜잭션| Bare Metal| 낮은 지연(latency), 안정적 성능  
개발/테스트 환경 다수| VM| 다양한 OS 시뮬레이션 가능  
고가용성 필요한 웹 서비스| VM| 스냅샷, Auto Scaling, HA 기본 지원  
마이크로서비스 운영| **Container**|  경량, 빠른 배포, 환경 일관성  
ML 워크로드| GPU VM / Container| GPU 탑재 VM, 또는 컨테이너로 이식성 확보  
  
### 14.2 Container의 핵심 특성

컨테이너는 애플리케이션과 그 실행에 필요한 **모든 요소(코드, 런타임, 라이브러리, 설정)** 를 하나로 패키징한 경량 실행 환경이다.

4가지 핵심 특성:

특성| 설명  
---|---  
**Lightweight**|  OS를 포함하지 않아 가볍고 빠름  
**Portable**|  "내 맥북에서 되는 게 서버에서도 된다"  
**Isolated**|  컨테이너끼리 독립 실행, 서로 영향 없음  
**Scalable**|  필요에 따라 즉시 수평 확장/축소  
  
### 14.3 MSA (Micro Service Architecture)

**Monolithic(모놀리식)** : 모든 기능이 하나의 배포 단위에 묶임

문제점:

  * 작은 수정도 전체 재배포
  * 한 기능의 장애가 전체 시스템에 영향
  * 특정 기능만 스케일 아웃 불가 (전체를 스케일 아웃해야 함)
  * 기술 스택 통일 강제



**MSA** : 기능별로 독립적인 서비스로 분리
[code] 
    Monolithic 주문 앱                   MSA 주문 앱
    ┌─────────────────────┐             
    │ 주문 UI             │             [주문 UI]  ─────────────────────┐
    │ 주문 기록            │     →                                       │
    │ 인벤토리             │             ALB (Application Load Balancer) │
    │ 이메일 발송          │               │                             │
    │ 영업 기록            │         ┌────┴──┬──────┬──────┐           │
    └─────────────────────┘         │       │      │      │           │
                                 [주문]  [인벤]  [이메] [영업]         │
                                  서비스   토리   일     기록           │
                                        서비스  서비스  서비스          │
[/code]

각 서비스:

  * 독립적으로 배포 가능
  * 독립적으로 확장 가능 (주문이 몰리면 주문 서비스만 스케일 아웃)
  * 서비스별 장애 격리 (이메일 서비스가 죽어도 주문은 처리됨)
  * 서비스별 기술 스택 자유 (Python AI 서비스 + Java 주문 서비스 혼용 가능)



컨테이너 + MSA + Kubernetes = 현대 클라우드 아키텍처의 핵심

* * *

## 15\. Kubernetes — 컨테이너 오케스트레이션

![Kubernetes Architecture — Master Node와 Worker Node 구성](https://media.geeksforgeeks.org/wp-content/uploads/20260406154006746759/k8s-arch.webp)

컨테이너가 늘어나면 직접 관리가 한계에 부딪힌다. "이 컨테이너가 죽었는데?", "트래픽이 몰리는데 더 띄워야 하는데?", "서버 A가 꽉 찼는데 서버 B에는 올려도 되나?" — 이 모든 걸 자동화해주는 것이 **Kubernetes(쿠버네티스, k8s)** 다.

### 15.1 Kubernetes 아키텍처

**Control Plane (마스터 노드)** — 클러스터 전체를 관리·감독

컴포넌트| 역할  
---|---  
**API Server**|  클러스터의 프론트엔드. kubectl 명령어, 대시보드, CI/CD 파이프라인이 여기로 요청  
**etcd**|  클러스터의 모든 상태 정보를 저장하는 고가용성 Key-Value DB. "Source of Truth"  
**Scheduler**|  새 Pod를 어느 Worker Node에 배치할지 결정. 리소스 가용량, 제약 조건, 정책 고려  
**Controller Manager**|  현재 상태와 원하는 상태의 차이를 감지하고 수렴시킴 (ReplicaSet 컨트롤러, 노드 컨트롤러 등)  
  
**Worker Node** — 실제 컨테이너가 실행되는 곳

컴포넌트| 역할  
---|---  
**kubelet**|  API Server와 통신하며 컨테이너 실행 명령을 수행. 노드의 상태를 API Server에 보고  
**kube-proxy**|  네트워크 라우팅 관리. Service의 가상 IP로 들어오는 트래픽을 실제 Pod로 전달  
**Container Runtime**|  컨테이너 실제 실행 엔진 (containerd, CRI-O 등)  
  
### 15.2 Kubernetes 클러스터 구축 실습

실습에서는 AWS EC2 인스턴스 3개로 클러스터를 구성했다:

  * Master Node: `t3.medium` (2vCPU, 4GB RAM) × 1
  * Worker Node: `t3.small` × 2



최소 요건: 2GB 이상 RAM, 2개 이상 CPU, swap 비활성화

**설치 전체 흐름** :
[code] 
    # ① 모든 노드: 스왑 비활성화 (k8s 필수 사전 조건)
    sudo swapoff -a
    sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
    
    # ② 모든 노드: 커널 모듈 로드
    sudo tee /etc/modules-load.d/containerd.conf <<EOF
    overlay
    br_netfilter
    EOF
    sudo modprobe overlay
    sudo modprobe br_netfilter
    
    # ③ 모든 노드: 커널 파라미터 설정 (Pod 간 네트워크 통신)
    sudo tee /etc/sysctl.d/kubernetes.conf <<EOF
    net.bridge.bridge-nf-call-ip6tables = 1
    net.bridge.bridge-nf-call-iptables = 1
    net.ipv4.ip_forward = 1
    EOF
    sudo sysctl --system
    
    # ④ 모든 노드: containerd 설치
    sudo apt install -y containerd.io
    containerd config default | sudo tee /etc/containerd/config.toml >/dev/null 2>&1
    sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
    sudo systemctl restart containerd
    sudo systemctl enable containerd
    
    # ⑤ 모든 노드: Kubernetes 구성 요소 설치
    sudo apt install -y kubelet kubeadm kubectl
    sudo apt-mark hold kubelet kubeadm kubectl  # 자동 업그레이드 방지
    
    # ⑥ 마스터 노드에서만: 클러스터 초기화
    sudo kubeadm init
    
    # ⑦ 마스터 노드: kubeconfig 설정
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
    
    # ⑧ 마스터 노드: 네트워크 플러그인 설치 (Calico)
    kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.2/manifests/calico.yaml
    
    # ⑨ 워커 노드에서: 클러스터에 조인
    sudo kubeadm join 172.31.x.x:6443 --token <토큰> \
        --discovery-token-ca-cert-hash sha256:<해시>
    
    # ⑩ 마스터 노드: 전체 노드 상태 확인
    kubectl get nodes
[/code]

왜 swap을 비활성화해야 할까?  
Kubernetes는 메모리 관리를 직접 한다. swap이 활성화되어 있으면 k8s가 실제 메모리 사용량을 정확히 파악하기 어렵고, 스케줄링 결정이 부정확해진다.

왜 네트워크 플러그인이 필요할까?  
k8s 자체는 Pod 간 통신 방법을 명세(CNI)만 정의한다. 실제 구현은 Calico, Flannel, Weave 등의 플러그인이 담당한다.

### 15.3 Pod — 가장 작은 배포 단위

Pod는 Kubernetes에서 배포 가능한 **가장 작은 단위** 다. 하나 이상의 컨테이너가 같은 네트워크와 스토리지를 공유하며 하나의 단위로 실행된다.
[code] 
    # po/pod.yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: pod-test2
    spec:
      containers:
      - name: test-nginx-container
        image: nginx:latest
        ports:
        - containerPort: 80
          protocol: TCP
[/code]

**자주 쓰는 Pod 관련 명령어** :
[code] 
    # Pod 생성 (명령어 방식)
    kubectl run nginx-pod --image=nginx --port=80
    
    # Pod 생성 (YAML 방식)
    kubectl apply -f po/pod.yaml
    
    # Pod 목록 확인
    kubectl get pods
    kubectl get pods -o wide   # IP, 배치된 노드도 표시
    
    # Pod 상세 정보 (이벤트, 컨테이너 상태 등)
    kubectl describe pods pod-test2
    
    # Pod 내부 접속
    kubectl exec -it pod-test2 -- bash
    
    # Pod에 명령어 전달
    kubectl exec pod-test2 -- env
    
    # 로그 확인
    kubectl logs pod-test2
    kubectl logs -f pod-test2   # 실시간 로그 스트리밍
    
    # Pod 삭제
    kubectl delete pod pod-test2
    kubectl delete -f po/pod.yaml
[/code]

**Pod의 한계** : Pod를 직접 만들면, Pod가 죽었을 때 아무도 되살려주지 않는다. 이걸 해결하는 것이 ReplicaSet이다.

### 15.4 ReplicaSet — Pod를 N개 유지

ReplicaSet은 **"이 Pod를 항상 N개 유지해줘"** 라고 선언하는 리소스다.
[code] 
    # rs/rs-nginx.yaml
    apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
      name: replicaset-nginx
    spec:
      replicas: 3                    # 항상 3개 유지
      selector:
        matchLabels:
          app: test-nginx-pods-label # 이 레이블의 Pod를 관리
      template:
        metadata:
          name: test-nginx-pod
          labels:
            app: test-nginx-pods-label
        spec:
          containers:
          - name: nginx
            image: nginx:latest
            ports:
            - containerPort: 80
[/code]

**ReplicaSet 동작 원리** :
[code] 
    # 현재 3개의 Pod가 실행 중
    kubectl get pods --show-labels
    
    # Pod 하나를 수동 삭제하면?
    kubectl delete pod replicaset-nginx-xxxxx
    
    # 즉시 새 Pod가 생성됨!
    kubectl get pods   # 여전히 3개
[/code]

**ReplicaSet이 Pod를 인식하는 방법** : `selector.matchLabels`에 정의된 레이블을 가진 Pod가 관리 대상.

  * 레이블이 맞는 Pod가 N개보다 적으면 → 새 Pod 생성
  * 레이블이 맞는 Pod가 N개보다 많으면 → 초과 Pod 삭제
  * Pod의 레이블을 수동으로 제거하면 → ReplicaSet 관리에서 벗어남 (고아 Pod)



### 15.5 Deployment — 버전 관리까지 되는 업그레이드

실제 서비스에서는 ReplicaSet을 직접 다루지 않는다. **Deployment** 를 사용한다.

Deployment = ReplicaSet 관리 + **롤링 업데이트 + 롤백**
[code] 
    # deploy/deploy-nginx.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: test-nginx-deploy
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: test-nginx
      template:
        metadata:
          labels:
            app: test-nginx
        spec:
          containers:
          - name: nginx
            image: nginx:1.10     # 현재 버전
            ports:
            - containerPort: 80
[/code]
[code] 
    # Deployment 생성
    kubectl apply -f deploy/deploy-nginx.yaml
    
    # 생성된 Deployment, ReplicaSet, Pod 확인
    kubectl get deployment
    kubectl get replicasets,pods
    
    # 이미지 버전 업데이트 → 롤링 업데이트 자동 실행
    kubectl set image deploy test-nginx-deploy nginx=nginx:1.19
    
    # 롤링 업데이트 진행 상황 실시간 확인
    kubectl rollout status deployment test-nginx-deploy
    
    # ReplicaSet 2개가 존재 (이전 버전 + 새 버전)
    kubectl get replicasets
    
    # 롤아웃 히스토리 확인
    kubectl rollout history deployment test-nginx-deploy
    
    # 이전 버전으로 롤백 (1번 revision으로)
    kubectl rollout undo deploy test-nginx-deploy --to-revision=1
[/code]

**롤링 업데이트 동작 방식** :  
1\. 새 버전의 ReplicaSet 생성  
2\. 새 ReplicaSet의 Pod를 1개씩 증가  
3\. 이전 ReplicaSet의 Pod를 1개씩 감소  
4\. 완전히 전환될 때까지 반복  
5\. 이전 ReplicaSet은 Pod 0개로 유지 (롤백 대비)

**Deployment를 삭제하면 → 하위 ReplicaSet과 Pod도 모두 삭제됨.**

### 15.6 Service — 고정된 네트워크 진입점

Pod는 동적으로 생성/삭제되어 IP가 매번 변한다. Service는 Pod들에 대한 **고정된 DNS 이름과 IP를 제공** 한다.
[code] 
    Service (고정 IP/DNS)
        ↓ 트래픽 분산
    Pod-1 (172.17.0.4)
    Pod-2 (172.17.0.5)
    Pod-3 (172.17.0.6)
[/code]

Pod가 재생성되어 IP가 바뀌어도 Service를 통해 접근하면 문제없다.

**Service 타입 3가지** :

**① ClusterIP (기본값) — 클러스터 내부 전용**
[code] 
    # svc/svc-clusterip.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: svc-clusterip
    spec:
      ports:
      - name: web-port
        port: 8080        # Service가 노출하는 포트
        targetPort: 80    # Pod의 실제 포트
      selector:
        app: webserver    # 이 레이블의 Pod에 트래픽 전달
      type: ClusterIP
[/code]

클러스터 내부에서만 접근 가능. 서비스 이름으로 DNS 조회 가능:
[code] 
    curl svc-clusterip:8080
[/code]

**② NodePort — 노드 IP로 외부 접근**
[code] 
    # svc/svc-nodeport.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: svc-nodeport
    spec:
      ports:
      - name: web-port
        port: 8080
        targetPort: 80
        # nodePort: 30080   # 생략 시 30000-32767 범위에서 자동 할당
      selector:
        app: webserver
      type: NodePort
[/code]
[code] 
    # 노드의 IP로 외부에서 접근
    curl <노드 Internal IP>:<NodePort>
[/code]

모든 노드에서 같은 NodePort로 접근 가능.

**③ LoadBalancer — 퍼블릭 IP 자동 할당 (클라우드용)**
[code] 
    # svc/svc-lb.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: svc-lb
    spec:
      ports:
      - name: web-port
        port: 80
        targetPort: 80
      selector:
        app: webserver
      type: LoadBalancer
[/code]

AWS EKS, GKE, AKS 등 클라우드 환경에서 사용 시 클라우드 로드밸런서를 자동으로 프로비저닝한다.

**서비스 타입 비교** :

타입| 접근 범위| 사용 케이스  
---|---|---  
ClusterIP| 클러스터 내부만| 서비스 간 내부 통신 (DB, 백엔드)  
NodePort| 클러스터 외부 (노드 IP:포트)| 개발·테스트 환경 임시 노출  
LoadBalancer| 인터넷 (퍼블릭 IP)| 프로덕션 서비스 외부 노출  
  
### 15.7 Ingress — HTTP/HTTPS 경로 기반 라우팅

Service의 LoadBalancer 타입은 서비스마다 별도 로드밸런서를 생성해 비용이 많이 든다. **Ingress** 는 하나의 진입점에서 URL 경로나 호스트 이름을 기준으로 여러 서비스에 라우팅한다.
[code] 
    클라이언트
        ↓
    Ingress (하나의 외부 IP / 로드밸런서)
        ├── /api/users   → users-service:80
        ├── /api/orders  → orders-service:80
        └── /            → frontend-service:80
[/code]
[code] 
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: app-ingress
      annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /
    spec:
      ingressClassName: nginx
      rules:
      - host: app.example.com
        http:
          paths:
          - path: /api/users
            pathType: Prefix
            backend:
              service:
                name: users-service
                port:
                  number: 80
          - path: /api/orders
            pathType: Prefix
            backend:
              service:
                name: orders-service
                port:
                  number: 80
[/code]

Ingress가 동작하려면 **Ingress Controller** 가 클러스터에 설치되어야 한다.

환경| Ingress Controller  
---|---  
온프레미스 / 범용| Nginx Ingress Controller  
AWS EKS| AWS Load Balancer Controller (ALB 자동 생성)  
GKE| GCE Ingress Controller  
Azure AKS| Azure Application Gateway Ingress
[code] 
    kubectl get ingress
    kubectl describe ingress app-ingress
[/code]  
  
### 15.8 HPA — Horizontal Pod Autoscaler

HPA는 CPU 사용률 또는 커스텀 지표를 기준으로 **Pod 수를 자동으로 조절** 한다. Kubernetes 워크로드에 대한 수평 자동 확장이다.
[code] 
    부하 증가 → Pod CPU 80% 초과
        ↓
    HPA 감지 (15초 간격 평가)
        ↓
    Deployment replicas 3 → 6 자동 조정
        ↓
    부하 분산, CPU 하락
        ↓
    CPU 50% 안정 → 일정 시간 후 replicas 다시 축소
[/code]
[code] 
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: nginx-hpa
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: test-nginx-deploy
      minReplicas: 2
      maxReplicas: 10
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 50   # CPU 50% 목표
[/code]

HPA가 동작하려면 Pod에 `resources.requests` 설정이 **필수** 다:
[code] 
    resources:
      requests:
        cpu: "100m"      # 0.1 vCPU
        memory: "128Mi"
      limits:
        cpu: "500m"
        memory: "256Mi"
[/code]
[code] 
    # HPA 생성 (명령어 방식)
    kubectl autoscale deployment test-nginx-deploy --cpu-percent=50 --min=2 --max=10
    
    # HPA 상태 확인
    kubectl get hpa
    
    # 상세 정보 (스케일 이벤트 확인)
    kubectl describe hpa nginx-hpa
[/code]

**HPA vs EC2 Auto Scaling 비교** :

항목| EC2 Auto Scaling| Kubernetes HPA  
---|---|---  
스케일 대상| EC2 인스턴스| Pod  
소요 시간| 수 분 (인스턴스 부팅 포함)| 수 초~수십 초  
비용 단위| 인스턴스 시간| Pod 리소스 사용량  
  
### 15.9 Namespace — 클러스터 내 논리적 격리

Namespace는 하나의 클러스터를 여러 가상 클러스터로 분리하는 방법이다.
[code] 
    # ns/prod-ns.yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: production
[/code]
[code] 
    # 기본 namespace의 Pod
    kubectl get pods                           # default namespace
    kubectl get pods --namespace kube-system   # 시스템 컴포넌트
    
    # namespace 생성 후 리소스 배포
    kubectl apply -f prod-ns.yaml
    kubectl apply -f deploy-svc-ns.yaml
    kubectl get po,svc -n production
    
    # 같은 namespace 서비스 접근
    curl svc-clusterip-ns:8080
    
    # 다른 namespace 서비스 접근 (FQDN: 서비스명.네임스페이스.svc)
    curl svc-clusterip-ns.production.svc:8080
    
    # namespace 삭제 → 안의 모든 리소스 삭제됨
    kubectl delete namespace production
[/code]

활용 예시:

  * `development`, `staging`, `production` 환경 분리
  * 팀별 격리 (`team-a`, `team-b`)
  * 시스템 컴포넌트 분리 (`kube-system`)



### 15.10 ConfigMap과 Secret — 설정 분리

컨테이너 이미지에 설정값을 하드코딩하면 환경마다 이미지를 새로 빌드해야 한다. **ConfigMap** 으로 설정을 분리하면 이미지 변경 없이 설정만 바꿀 수 있다.

**ConfigMap 생성** :
[code] 
    # 명령어로 생성
    kubectl create configmap log-level-configmap --from-literal LOG_LEVEL=DEBUG
    kubectl create configmap start-k8s --from-literal k8s=kubernetes --from-literal container=docker
    
    # 파일로 생성 (설정 파일 전체를 ConfigMap으로)
    echo "Hello, Kubernetes" | sudo tee index.html
    kubectl create configmap index-file --from-file index.html
    
    # ConfigMap 조회
    kubectl get configmap
    kubectl describe configmap log-level-configmap
    kubectl get configmap log-level-configmap -o yaml
[/code]

**ConfigMap을 Pod에 주입하는 방법** :

방법 1 — 환경 변수로 전달:
[code] 
    # 전체 ConfigMap을 환경 변수로
    spec:
      containers:
      - name: my-container
        image: busybox
        args: ['tail', '-f', '/dev/null']
        envFrom:
        - configMapRef:
            name: log-level-configmap  # ConfigMap 전체를 env로
        - configMapRef:
            name: start-k8s
[/code]
[code] 
    # 특정 키만 골라서 환경 변수로
    spec:
      containers:
      - name: my-container
        env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: log-level-configmap
              key: LOG_LEVEL
[/code]

방법 2 — 볼륨으로 파일 마운트:
[code] 
    spec:
      containers:
      - name: nginx
        volumeMounts:
        - name: config-vol
          mountPath: /etc/config
      volumes:
      - name: config-vol
        configMap:
          name: start-k8s
[/code]

ConfigMap의 각 key-value가 파일 이름과 내용으로 마운트된다.

**Secret** — 민감 정보 보관:
[code] 
    # 비밀번호 저장
    kubectl create secret generic my-password --from-literal password=dkagh123.
    
    # 파일로 생성
    echo mypassword | sudo tee pw1 > /dev/null
    kubectl create secret generic our-password --from-file pw1
    
    # Secret 확인 (값은 Base64 인코딩)
    kubectl get secrets my-password -o yaml
    
    # Base64 디코딩으로 실제 값 확인
    echo <base64값> | base64 -d
[/code]

Secret은 ConfigMap과 동일하게 환경 변수 또는 볼륨으로 Pod에 주입한다.

Docker private registry 인증 정보도 Secret으로 관리:
[code] 
    kubectl create secret docker-registry registry-auth \
      --docker-username=myuser \
      --docker-password=mypassword \
      --docker-server=registry.example.com
[/code]

### 15.11 Volume — 데이터 영속성

컨테이너가 죽으면 컨테이너 내부 데이터는 사라진다. Volume을 사용하면 데이터를 영속적으로 저장할 수 있다.

**emptyDir — 임시 공유 볼륨**

Pod가 실행되는 동안만 존재하는 임시 디렉터리. 같은 Pod의 여러 컨테이너가 데이터를 공유할 때 사용.
[code] 
    # content-creator 컨테이너에서 파일 생성
    kubectl exec -it emptydir-pod -c content-creator -- sh
    echo "hello, k8s" > /data/test.html
    exit
    
    # apache-webserver 컨테이너에서 같은 파일 확인
    kubectl exec -it emptydir-pod --container apache-webserver -- cat htdocs/test.html
    # 출력: hello, k8s
[/code]

**hostPath — 노드 파일시스템 마운트**

호스트 노드의 특정 디렉터리를 Pod에 마운트. 로그 수집, 노드 파일 접근 등에 사용.

주의: Pod가 다른 노드에 스케줄되면 데이터가 보이지 않을 수 있음.

**PV/PVC — 클러스터 수준 영구 스토리지**
[code] 
    관리자(Admin)                사용자(Developer)
         │                              │
         ▼                              ▼
    PV 생성 (실제 스토리지 선언)   PVC 생성 (스토리지 요청)
                                         │
                                   PV와 자동 바인딩
                                         │
                                      Pod에서 사용
[/code]
[code] 
    # PV 정의 (관리자가 스토리지 선언)
    apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: pv
    spec:
      capacity:
        storage: 1G
      accessModes:
      - ReadWriteOnce      # 단일 노드 읽기/쓰기
      hostPath:
        path: /pv          # 실제 저장 경로
[/code]
[code] 
    # PVC 정의 (사용자가 스토리지 요청)
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: pvc
    spec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 1G      # 조건에 맞는 PV가 자동 바인딩
[/code]
[code] 
    # PV, PVC, Pod 생성 후 상태 확인
    kubectl get pv,pvc,po
    
    # Pod 내부에서 파일 생성
    kubectl exec -it persistentvolume --container container -- /bin/bash
    cd /mount1
    echo "hello pv" >> test.txt
    exit
    
    # Pod를 삭제해도 PV의 데이터는 유지됨
    kubectl delete pod persistentvolume
[/code]

**accessModes 종류** :

모드| 설명  
---|---  
`ReadWriteOnce` (RWO)| 단일 노드에서 읽기/쓰기  
`ReadOnlyMany` (ROX)| 여러 노드에서 읽기만  
`ReadWriteMany` (RWX)| 여러 노드에서 읽기/쓰기 (NFS 등 필요)  
  
* * *

## 16\. AWS CI/CD — 코드 커밋부터 자동 배포까지

![AWS CodePipeline — Source, Build, Deploy 단계 자동화 흐름](https://media.geeksforgeeks.org/wp-content/uploads/20240219101620/aws-Pipeline.webp)

### 16.1 AWS CI/CD 서비스 구성

서비스| 역할| 비고  
---|---|---  
**AWS CodeCommit**|  관리형 Git 저장소| GitHub로 대체 가능  
**AWS CodeBuild**|  코드 빌드·테스트 자동화| buildspec.yml로 정의  
**AWS CodeDeploy**|  EC2, Lambda, ECS에 자동 배포| appspec.yml로 정의  
**AWS CodePipeline**|  위 서비스들을 연결하는 파이프라인 오케스트레이터| 소스 변경 감지 → 트리거
[code] 
    [소스 (S3 / GitHub)]
        ↓ 변경 감지 (CodePipeline이 트리거)
    [CodeBuild] ← buildspec.yml
        ↓ 빌드 아티팩트 (dist/, .jar 등)
    [CodeDeploy] ← appspec.yml
        ↓
    [EC2 / S3 / ECS / Lambda]
[/code]  
  
### 16.2 Lab 10 — AWS CodePipeline 기본 (S3 → S3 배포)

가장 단순한 파이프라인: Source S3 버킷에 파일을 올리면 → Prod S3 버킷(정적 웹사이트)에 자동 배포.

**구성 요소** :

  * **Source 버킷** : `user-source-website` — 버전 관리 활성화 (트리거에 필요)
  * **Prod 버킷** : `user-prod-website` — 정적 웹사이트 호스팅 활성화, 퍼블릭 액세스 허용



**파이프라인 설정 핵심** :

  * 소스 공급자: Amazon S3
  * 배포 공급자: Amazon S3
  * "배포하기 전에 파일 압축 풀기" 체크
  * 표준 ACL: `public-read` (정적 웹사이트 공개 접근용)



**파이프라인 동작 흐름** :
[code] 
    Source 버킷에 test-website.zip 업로드
        → CodePipeline 자동 감지 (S3 버전 변경 이벤트)
            → Deploy: Prod 버킷에 압축 풀어 배포
                → 웹사이트 자동 업데이트
[/code]

파일 압축 시 주의사항:
[code] 
    ✗ 잘못된 방법: test-website 폴더를 통째로 압축
      → 압축 해제 시 또 폴더가 생겨 경로 오류
    
    ✓ 올바른 방법: 폴더 안으로 들어가 index.html, error.html 파일 선택 후 압축
      → 압축 파일 최상위에 바로 index.html이 있어야 함
[/code]

### 16.3 Lab 11 — GitHub 저장소를 소스로 활용

소스를 S3 대신 GitHub으로 변경하면 `git push`만으로 파이프라인이 자동 실행된다.

**GitHub 설정** :  
1\. Repository 생성 (Private)  
2\. Personal Access Token 생성 (scopes: `repo`)  
3\. AWS CodePipeline에서 GitHub App 연결

**로컬 → GitHub → CodePipeline 흐름** :
[code] 
    # 처음 연결
    git init
    git add .
    git commit -m "first commit"
    git remote add origin https://github.com/<계정>/test-website-repo.git
    git branch -M main
    git push -u origin main
    
    # 이후 변경사항 → 파이프라인 자동 트리거
    git commit -a -m "v2.0 update"
    git push origin main
[/code]

GitHub 웹 UI에서 파일을 직접 편집하고 커밋해도 파이프라인이 트리거된다.

**GitHub App 연결 vs Personal Access Token** :

  * GitHub App: 더 안전하고 세밀한 권한 관리 가능 (권장)
  * Personal Access Token: 간편하지만 관리 주의 필요



### 16.4 Lab 12 — AWS CodeBuild로 빌드 자동화

Angular 같은 프레임워크는 소스 코드를 바로 배포할 수 없다. 빌드 과정이 필요하다. `buildspec.yml` 파일로 빌드 방법을 정의한다.

**buildspec.yml 구조** :
[code] 
    version: 0.2
    
    phases:
      install:                      # 빌드 환경 설정
        runtime-versions:
          nodejs: 20                # Node.js 20 사용
        commands:
          - npm install -g @angular/cli@17  # Angular CLI 전역 설치
    
      pre_build:                    # 빌드 전 준비
        commands:
          - npm install             # 프로젝트 의존성 설치
    
      build:                        # 실제 빌드
        commands:
          - ng build -c production  # 프로덕션 빌드
          - echo "Build completed."
        finally:                    # 성공/실패 무관 항상 실행
          - echo This is the finally block execution!
    
    artifacts:                      # 배포할 결과물
      base-directory: dist/my-angular-project
      files:
        - '**/*'                    # 빌드 결과물 전체
[/code]

**buildspec.yml 위치** : 프로젝트 루트에 있어야 CodeBuild가 자동으로 찾음

**phases 종류** :

Phase| 설명  
---|---  
`install`| 런타임 환경, 도구 설치  
`pre_build`| 빌드 전 작업 (의존성 설치, 인증 등)  
`build`| 실제 빌드, 테스트  
`post_build`| 빌드 후 작업 (알림, 정리 등)  
  
파이프라인 구성:
[code] 
    [GitHub]
        ↓ push 이벤트
    [Source 단계: GitHub 소스 체크아웃]
        ↓
    [Build 단계: CodeBuild]
        buildspec.yml 실행:
        1. Node.js 20 설치
        2. npm install
        3. ng build -c production
        ↓ dist/ 아티팩트
    [Deploy 단계: S3]
        ↓
    [정적 웹사이트 배포]
[/code]

첫 빌드 시 buildspec.yml이 없으면 Build 단계에서 실패한다. 로그를 확인해 실패 원인을 파악하고, 파일을 추가해 다시 push하면 된다.

### 16.5 Lab 13 — AWS CodeDeploy로 EC2 인스턴스에 배포

S3가 아닌 EC2 인스턴스에 빌드 결과물을 배포할 때는 **CodeDeploy** 를 사용한다.

**appspec.yml** — 배포 명세서:
[code] 
    version: 0.0
    os: linux
    
    files:
      - source: dist/my-angular-project    # 빌드 아티팩트의 경로
        destination: /var/www/my-angular-project  # EC2에 복사할 경로
    
    permissions:
      - object: /var/www/my-angular-project
        pattern: '**'
        mode: '0755'       # 실행 권한
        owner: root
        group: root
        type:
          - file
          - directory
    
    hooks:
      ApplicationStart:
        - location: deploy-scripts/application-start-hook.sh
          timeout: 300     # 300초 제한
[/code]

**배포 훅(Hooks)** — 배포 생명주기:
[code] 
    ApplicationStop          ← 현재 실행 중인 앱 종료
    BeforeInstall            ← 파일 복사 전 준비 (의존성 설치 등)
    AfterInstall             ← 파일 복사 후 설정 (설정 파일 적용 등)
    ApplicationStart   ←────  현재 실습에서 사용
    ValidateService          ← 배포 성공 검증 (헬스 체크 등)
[/code]

각 훅에 셸 스크립트를 연결해 세밀한 배포 제어가 가능하다.

**CodeDeploy 작동 요건** :

  * EC2 인스턴스에 **CodeDeploy Agent** 설치
  * EC2 인스턴스에 **IAM 역할** 부여 (S3 아티팩트 접근 권한)
  * CodeDeploy 서비스에도 **IAM 서비스 역할** 필요



**전체 Lab 12+13 파이프라인 흐름** :
[code] 
    GitHub push
        ↓
    CodePipeline 트리거
        ↓
    [Source] GitHub에서 소스 체크아웃
        ↓
    [Build] CodeBuild + buildspec.yml
        → npm install → ng build → S3에 빌드 아티팩트 저장
        ↓
    [Deploy] CodeDeploy + appspec.yml
        → S3에서 아티팩트 다운로드
        → 배포 훅 실행 (ApplicationStop → BeforeInstall → AfterInstall → ApplicationStart)
        → EC2 /var/www/my-angular-project/ 에 파일 배포
        ↓
    [서비스 정상 확인]
[/code]

* * *

## 17\. 소프트웨어 배포 전략

새 버전을 어떻게 기존 운영 환경에 반영할지 결정하는 방법론이다. **다운타임** , **롤백 속도** , **비용** , **위험도** 측면에서 각각 다른 트레이드오프를 가진다.

### 17.1 In-Place 배포 (Rolling 배포)

기존 인스턴스를 교체 없이 순차적으로 새 버전을 덮어쓴다.
[code] 
    배포 전:   [v1][v1][v1][v1]
    배포 중:   [v2][v1][v1][v1]  ← v1, v2 혼재
               [v2][v2][v1][v1]
    배포 완료: [v2][v2][v2][v2]
[/code]

동시 배포 비율 제어(`MinimumHealthyHosts` 설정):

  * `AllAtOnce`: 전체 동시 배포 (가장 빠름, 다운타임 위험)
  * `HalfAtATime`: 절반씩 배포
  * `OneAtATime`: 1개씩 배포 (가장 안전, 가장 느림)

다운타임| 롤백| 비용| 버전 혼재  
---|---|---|---  
없음| 느림 (전체 재배포)| 없음| 있음  
  
### 17.2 Blue/Green 배포

현재 운영 환경(Blue)과 동일한 새 환경(Green)을 별도로 구성한 뒤 트래픽을 한 번에 전환한다.
[code] 
    Blue (현재):  [v1][v1][v1][v1]  ← 전환 전 100% 트래픽
    Green (신버전): [v2][v2][v2][v2]  ← 검증 완료 대기
    
    ALB 전환:  Blue 100% → Green 100%  (순간 전환, 다운타임 없음)
    롤백:      Green → Blue 즉시 재전환
[/code]

CodeDeploy Blue/Green 설정 포인트:

  * Green 환경 구성: ASG에서 자동 프로비저닝 또는 수동 지정
  * 트래픽 재라우팅: 즉시 또는 N분 대기 후 자동 전환
  * Blue 환경 처리: 전환 성공 후 N분 뒤 자동 종료

다운타임| 롤백| 비용| 버전 혼재  
---|---|---|---  
없음| 즉시| 높음 (인스턴스 2배)| 없음  
  
### 17.3 Canary 배포

신버전을 전체 트래픽의 일부(소수)에만 먼저 노출해 이상 여부를 확인하고 점진적으로 확대한다.
[code] 
    1단계 (Canary):   [v2][v1][v1][v1][v1][v1][v1][v1][v1][v1]
                      ↑ 10% 트래픽 → v2 (모니터링)
    2단계 (확대):     v2 비율 50%
    3단계 (완료):     v2 100%
[/code]

AWS CodeDeploy 사전 정의 Canary 설정:

설정 이름| 내용  
---|---  
`Canary10Percent5Minutes`| 10% 먼저, 5분 뒤 나머지 90%  
`Canary10Percent10Minutes`| 10% 먼저, 10분 뒤 나머지 90%  
`Canary10Percent15Minutes`| 10% 먼저, 15분 뒤 나머지 90%  
`Canary10Percent30Minutes`| 10% 먼저, 30분 뒤 나머지 90%  
  
Lambda, ECS에서 주로 활용됨.

다운타임| 롤백| 비용| 버전 혼재  
---|---|---|---  
없음| 빠름| 낮음| 있음  
  
### 17.4 Linear 배포 (점진적 배포)

일정 시간 간격으로 동일한 비율씩 신버전 트래픽을 단계적으로 증가시킨다.
[code] 
    0분:  v2 → 10%
    10분: v2 → 20%
    20분: v2 → 30%
    ...
    90분: v2 → 100%
[/code]

Canary와 차이: Canary는 "소량 먼저 → 한 번에 나머지", Linear는 "균등하게 점진 증가".

AWS CodeDeploy 사전 정의 Linear 설정:

설정 이름| 내용  
---|---  
`Linear10PercentEvery1Minute`| 1분마다 10%씩 증가  
`Linear10PercentEvery2Minutes`| 2분마다 10%씩 증가  
`Linear10PercentEvery3Minutes`| 3분마다 10%씩 증가  
`Linear10PercentEvery10Minutes`| 10분마다 10%씩 증가  
다운타임| 롤백| 비용| 버전 혼재  
---|---|---|---  
없음| 빠름| 낮음| 있음  
  
### 17.5 A/B Testing 배포

동일 기능의 두 버전을 서로 다른 사용자 그룹에 동시에 노출해 **비즈니스 지표(전환율, 클릭률 등)를 비교** 한다.
[code] 
    사용자 그룹 A (50%) → 버전 A (기존 UI)  전환율: 3.2%
    사용자 그룹 B (50%) → 버전 B (새 UI)   전환율: 4.7% ← 더 높음
    → 버전 B를 전체 배포 결정
[/code]

Canary와 차이: Canary는 기술적 안정성 검증, A/B Testing은 사용자 행동 기반 **비즈니스 최적화**.

AWS 구현 방법:

  * ALB 가중치 라우팅 + 헤더/쿠키 기반 Target Group 분리
  * CloudFront + Lambda@Edge: 요청 헤더 기반 오리진 분기
  * **AWS AppConfig** : 기능 플래그(Feature Flag)로 특정 사용자에게만 기능 활성화



### 17.6 Recreate 배포 (All-at-Once)

기존 버전을 모두 종료한 뒤 새 버전을 전체 배포. **다운타임 발생**.
[code] 
    [v1][v1][v1] → 전체 종료 → (다운타임) → [v2][v2][v2]
[/code]

적합한 경우: 개발/스테이징 환경, DB 스키마 변경으로 v1/v2 혼재가 불가능한 상황.

다운타임| 롤백| 비용| 버전 혼재  
---|---|---|---  
**있음**|  중간| 없음| 없음  
  
### 17.7 Shadow 배포 (트래픽 미러링)

실제 프로덕션 트래픽을 신버전에 **복사(미러링)** 해서 응답은 사용자에게 보내지 않고 신버전의 동작만 검증한다.
[code] 
    사용자 요청
        ├── v1 (운영) → 실제 응답 사용자에게 반환
        └── v2 (Shadow) → 요청만 전달, 응답은 버림 (사용자 영향 없음)
    
    v2 모니터링:
    - 응답 시간 비교
    - 에러 발생 여부
    - 데이터 처리 정확성
[/code]

AWS 구현: ALB 미러링 규칙, Istio/AWS App Mesh 트래픽 미러링 기능 활용.

다운타임| 롤백| 비용| 사용자 영향  
---|---|---|---  
없음| 해당 없음| 높음 (v2 인프라)| **없음**  
  
### 17.8 배포 전략 종합 비교

전략| 다운타임| 롤백 속도| 추가 비용| 버전 혼재| 주요 사용 환경  
---|---|---|---|---|---  
In-Place (Rolling)| 없음| 느림| 없음| 있음| 일반 EC2, 비용 절감  
Blue/Green| 없음| **즉시**|  높음| 없음| 프로덕션, 즉시 롤백 필요  
Canary| 없음| 빠름| 낮음| 있음| Lambda, ECS, 리스크 최소화  
Linear| 없음| 빠름| 낮음| 있음| Lambda, ECS 점진 배포  
A/B Testing| 없음| 빠름| 중간| 있음| 기능 비교, UX 최적화  
Recreate| **있음**|  중간| 없음| 없음| 개발/스테이징  
Shadow| 없음| —| 높음| 없음| 신버전 사전 성능 검증  
  
**AWS CodeDeploy 대상별 지원 배포 방식** :

배포 대상| 지원 배포 유형  
---|---  
EC2 / On-Premises| In-Place, Blue/Green  
AWS Lambda| Canary, Linear, AllAtOnce  
Amazon ECS| Canary, Linear, AllAtOnce (Blue/Green 기반)  
  
* * *

## 18\. 서비스 안정성 — 고가용성과 무중단 배포

### 18.1 고가용성 3-Tier 아키텍처

실제 프로덕션 환경의 기본 아키텍처:
[code] 
    인터넷
        ↓
    Route53 (DNS, 장애 조치 라우팅)
        ↓
    CloudFront (CDN, 정적 콘텐츠 캐싱)
        ↓
    Elastic Load Balancer (ELB)
        ↓ ↓
    ┌────────────────────────────────────────┐
    │         퍼블릭 서브넷                  │
    │  [웹/앱 서버 Auto Scaling Group]       │
    │  AZ-1: EC2 × 2                        │
    │  AZ-2: EC2 × 2                        │
    └────────────────────────────────────────┘
        ↓ ↓
    ┌────────────────────────────────────────┐
    │         프라이빗 서브넷                │
    │  [RDS Multi-AZ]                        │
    │  AZ-1: Primary DB + Read Replica      │
    │  AZ-2: Standby DB + Read Replica      │
    └────────────────────────────────────────┘
[/code]

각 컴포넌트 역할:

  * **Route53** : DNS 기반 장애 조치. 헬스 체크 실패 시 다른 리전으로 트래픽 전환
  * **CloudFront** : 정적 콘텐츠(이미지, JS, CSS)를 엣지 로케이션에서 서빙
  * **ELB** : 여러 EC2 인스턴스로 트래픽 분산, 헬스 체크로 비정상 인스턴스 제외
  * **Auto Scaling** : CPU/메모리 지표에 따라 EC2 인스턴스 수 자동 조절
  * **RDS Multi-AZ** : 프라이머리 장애 시 스탠바이로 자동 전환



### 18.2 DR(재해 복구) 전략 — RPO와 RTO

**RPO (Recovery Point Objective)** : 장애 발생 시 얼마나 최근 데이터까지 복구할 수 있는가  
→ 데이터 백업 주기를 결정

**RTO (Recovery Time Objective)** : 장애 발생 시 얼마나 빨리 서비스를 복구해야 하는가  
→ 복구 전략의 비용을 결정
[code] 
    재해 발생 시각
        │
        │←─── RPO ───→│
        │              │
        │    마지막     │
        │    백업 시점  │
                       │
                       │←──── RTO ─────→│
                                         │
                                   서비스 복구
[/code]

**4가지 DR 전략 비교** :

전략| RPO| RTO| 비용| 설명  
---|---|---|---|---  
**백업 및 복원**|  시간 단위| 시간 단위| 매우 낮음| 스냅샷 백업, 장애 시 수동 재구축  
**파일럿 라이트**|  10분 단위| 10분 단위| 낮음| 핵심 서비스(DB)만 상시 운영  
**웜 스탠바이**|  분 단위| 분 단위| 중간| 모든 계층 축소 운영, 장애 시 확장  
**멀티 사이트 Active/Active**|  실시간| 실시간| 매우 높음| 두 리전 동시 운영, 즉각 전환  
  
**전략 상세 설명** :

**① 백업 및 복원**
[code] 
    프로덕션 환경
        → 주기적 스냅샷 (S3, EBS, RDS Snapshot)
            → 장애 발생
                → CloudFormation으로 인프라 재구축
                    → 백업에서 데이터 복원
[/code]

적합한 경우: 비용 최우선, 중요도 낮은 시스템

**② 파일럿 라이트**
[code] 
    평상시:
        DR 리전: DB만 소규모 운영 (프라이머리와 복제)
        
    장애 시:
        DR 리전: 앱 서버, 로드밸런서 신속 가동
        Route53으로 트래픽 전환
[/code]

적합한 경우: 데이터는 중요하지만 앱 서버는 빠르게 재구축 가능한 경우

**③ 웜 스탠바이**
[code] 
    평상시:
        DR 리전: 모든 계층이 축소 규모로 상시 운영
        (웹 × 1, 앱 × 1, DB Standby)
    
    장애 시:
        Auto Scaling으로 전체 용량으로 확장
        Route53으로 트래픽 전환
[/code]

적합한 경우: 빠른 복구가 필요하지만 완전 Active/Active 비용을 감당하기 어려운 경우

**④ 멀티 사이트 Active/Active**
[code] 
    평상시:
        리전 A: 전체 용량으로 서비스 중
        리전 B: 전체 용량으로 서비스 중 (트래픽 분산)
        두 리전 간 Aurora Global Database로 실시간 복제
    
    장애 시:
        Global Accelerator가 자동으로 정상 리전으로 100% 전환
        RTO: 거의 0 (실시간)
[/code]

적합한 경우: 금융, 의료, 글로벌 서비스 — 다운타임이 허용되지 않는 경우

* * *

## 전체 아키텍처 흐름 요약

코드 커밋부터 사용자 요청 처리까지의 전체 흐름:
[code] 
    개발자 git push
        ↓
    CodePipeline 트리거 (GitHub 웹훅 / S3 버전 변경)
        ↓
    [Source] 소스 체크아웃
        ↓
    [Build] CodeBuild + buildspec.yml
        → 의존성 설치 → 빌드 → 단위 테스트 → 빌드 아티팩트 S3 저장
        ↓
    [Deploy] CodeDeploy + appspec.yml
        → 배포 전략 선택 (Blue/Green / Canary / Rolling 등)
        → 헬스 체크 통과 후 트래픽 전환
        ↓
    Route53 (DNS, 장애 조치 라우팅)
        ↓
    CloudFront (CDN — 정적 콘텐츠 엣지 캐싱, HTTPS)
        ↓
    ALB (L7 로드 밸런싱, Target Group 헬스 체크)
        ├── /api/* → EC2 Auto Scaling Group 또는 EKS/ECS
        └── /      → S3 정적 웹사이트
        ↓
    애플리케이션 레이어 (EC2 / Kubernetes Pod / ECS Task)
        ↓
    데이터 레이어
        ├── Aurora / RDS (관계형 DB, Multi-AZ 고가용성)
        ├── ElastiCache Redis (캐싱 — Lazy Loading / Write-Through)
        └── DynamoDB (NoSQL — 세션, 실시간 이벤트)
[/code]

**서비스 계층별 AWS 서비스 매핑** :

계층| 서비스| 역할  
---|---|---  
DNS| Route53| 도메인 → IP 변환, 장애 조치  
CDN| CloudFront| 정적 콘텐츠 엣지 캐싱  
스토리지| S3| 정적 파일, 빌드 아티팩트, 백업  
컴퓨팅| EC2 + Auto Scaling| 가변 트래픽 자동 대응  
로드 밸런싱| ALB / NLB| 트래픽 분산, 헬스 체크  
컨테이너| ECS / EKS| 컨테이너 오케스트레이션  
관계형 DB| RDS / Aurora| ACID 트랜잭션, Multi-AZ  
NoSQL| DynamoDB| 무제한 확장, 밀리초 응답  
캐싱| ElastiCache| DB 부하 감소, 응답 속도 향상  
보안| IAM + SCP| 최소 권한 원칙 적용  
CI/CD| CodePipeline + CodeBuild + CodeDeploy| 배포 자동화  
하이브리드| Direct Connect / VPN| 온프레미스 연결  
  
* * *

## 생각 정리

인프라 관점에서 보면 VPC가 네트워크 경계를 정의하고, ELB와 Auto Scaling이 트래픽 변화에 대응하며, RDS Multi-AZ와 DR 전략이 데이터 가용성을 보장한다. 그 위에 컨테이너와 Kubernetes를 올리면 배포 단위가 인스턴스에서 Pod로 내려오고, CI/CD 파이프라인이 이 전체 흐름을 자동화한다.  
배포 전략을 깊게 들여다보면서 특히 인상적이었던 부분은, "새 버전을 올린다"는 행위 하나에도 다운타임 허용 여부, 롤백 속도, 비용, 버전 혼재 가능성을 모두 고려해 전략을 선택한다는 점이다. Blue/Green은 즉각적인 롤백이 가능한 대신 인프라 비용이 두 배가 되고, Canary는 리스크를 최소화하는 대신 운영 복잡도가 올라간다. 어떤 전략이 무조건 옳은 게 아니라, 서비스의 특성과 팀의 상황에 맞게 선택하는 것이 핵심이다.  
클라우드는 가용성·확장성·보안·비용 최적화를 동시에 설계한다는 것을 실습을 진행하며 그리고 다음 프로젝트를 진행하며 많이 배운거같다.

* * *

## 참고 자료

### AWS 공식 문서

  * [EC2](https://docs.aws.amazon.com/ec2/latest/userguide/concepts.html) / [EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
  * [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) / [Amazon EBS](https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html)
  * [VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
  * [ALB](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) / [NLB](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)
  * [Route53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html) / [CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
  * [IAM](https://docs.aws.amazon.com/iam/latest/userguide/introduction.html) / [AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html)
  * [RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html) / [Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html) / [DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) / [ElastiCache](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html)
  * [Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html) / [Site-to-Site VPN](https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html)
  * [ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
  * [CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html) / [CodeBuild buildspec](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html) / [CodeDeploy appspec](https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file.html)
  * [CodeDeploy 배포 구성](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html)
  * [AWS CLI 레퍼런스](https://awscli.amazonaws.com/v2/documentation/api/latest/index.html)



### Kubernetes 공식 문서

  * [Pod](https://kubernetes.io/ko/docs/concepts/workloads/pods/) / [ReplicaSet](https://kubernetes.io/ko/docs/concepts/workloads/controllers/replicaset/) / [Deployment](https://kubernetes.io/ko/docs/concepts/workloads/controllers/deployment/)
  * [Service](https://kubernetes.io/ko/docs/concepts/services-networking/service/) / [Ingress](https://kubernetes.io/ko/docs/concepts/services-networking/ingress/)
  * [HorizontalPodAutoscaler](https://kubernetes.io/ko/docs/tasks/run-application/horizontal-pod-autoscale/)
  * [ConfigMap](https://kubernetes.io/ko/docs/concepts/configuration/configmap/) / [Secret](https://kubernetes.io/ko/docs/concepts/configuration/secret/)
  * [PersistentVolume](https://kubernetes.io/ko/docs/concepts/storage/persistent-volumes/)
  * [kubeadm](https://kubernetes.io/docs/reference/setup-tools/kubeadm/) / [Calico CNI](https://docs.tigera.io/calico/latest/about/)
  * [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/)



### 참고 아티클

  * [GeeksforGeeks — Kubernetes Architecture](https://www.geeksforgeeks.org/devops/kubernetes-architecture/)
  * [GeeksforGeeks — AWS IAM](https://www.geeksforgeeks.org/identity-and-access-management-iam-in-amazon-web-services-aws/)
  * [GeeksforGeeks — RDS Read Replicas vs Multi-AZ](https://www.geeksforgeeks.org/cloud-computing/rds-read-replicas-how-it-is-different-from-rds-multi-az-deployment/)
  * [GeeksforGeeks — Container vs VM](https://www.geeksforgeeks.org/operating-systems/difference-between-virtual-machines-and-containers/)
  * [GeeksforGeeks — AWS EC2 Instance Types](https://www.geeksforgeeks.org/devops/amazon-ec2-instance-types/)
  * [GeeksforGeeks — AWS CI/CD Pipeline](https://www.geeksforgeeks.org/devops/how-to-build-a-ci-cd-pipeline-with-aws/)
