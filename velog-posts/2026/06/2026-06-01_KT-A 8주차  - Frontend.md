---
title: "KT-A 8주차  / Frontend"
date: 2026-06-01 15:13:03
source: "https://velog.io/@mi_nini/KT-A-8주차-Frontend"
---

## 들어가며

### 목차

  * 들어가며
  * 1\. VS Code 세팅부터 HTML/CSS 뼈대 잡기
    * Semantic Tag를 활용한 문서 구조화
    * CSS Flexbox로 유연하고 깔끔한 레이아웃 구성
  * 2\. JavaScript / React 컴포넌트 설계
    * JavaScript 심화: 배열 내장 함수
  * 3\. React 입문 및 컴포넌트(Component) 분리
    * Vite React 프로젝트 생성
    * Props를 통한 단방향 데이터 흐름 제어
  * 4\. React State 관리와 CRUD 구현
    * useState와 이벤트 핸들링
    * 폼(Form) 제어와 조건부 렌더링
    * 불변성을 유지하는 Create / Delete 로직 구현
  * 5\. 비동기 처리와 API 연동
    * useEffect와 컴포넌트 생명주기 제어
    * Axios를 활용한 REST API 연동 (비동기 처리)
  * 6\. 생각정리



> [Raact 학습_ko](https://ko.react.dev/learn)

* * *

# VS Code 세팅부터 HTML/CSS 뼈대 잡기

4일간의 프론트엔드 강의를 진행했다. 1일차에 목표는 React를 활용한 동적인 SPA(Single Page Application)를 구축하는것이다.

## Semantic Tag를 활용한 문서 구조화

본격적으로 게시판을 제작하며 가장 강조된 부분은 어떻게 하면 문서의 구조를 의미론적으로 명확하게 짤 수 있을까? 였다.  
단순히 화면의 구역을 나누기 위해 무의미한 `<div>` 태그만을 남발하지 않고, 철저하게 Semantic Tag를 활용에 대해 학습했다. 시맨틱 태그를 사용하면 검색 엔진 최적화에 유리하다.
[code] 
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <title>미니 게시판 프로젝트</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <header class="board-header">
        <h1>미니 게시판</h1>
        <nav>
          <button class="btn-create">새 글 작성</button>
        </nav>
      </header>
    
      <main class="board-container">
        <section class="post-list-section">
          
          <article class="post-item">
            <h2 class="post-title">프론트엔드 회고입니다.</h2>
            <div class="post-meta">
              <span class="author">작성자: 김경민</span>
              <span class="date">2026-05-15</span>
            </div>
          </article>
    
          <article class="post-item">
            <h2 class="post-title">시맨틱 태그와 VS Code 세팅</h2>
            <div class="post-meta">
              <span class="author">작성자: 이순신</span>
              <span class="date">2026-05-15</span>
            </div>
          </article>
    
        </section>
      </main>
    </body>
    </html> 
[/code]

이렇게 명확하게 나누어진 구조는 당장 코드를 읽기 편하게 해줄 뿐만 아니라, React를 학습할 때 `header` 영역은 Header 컴포넌트로, `article`영역은 PostItem 컴포넌트로 분리하는데 도움이 된다.

### CSS Flexbox로 유연하고 깔끔한 레이아웃 구성

간단하게 CSS를 통해 시각적인 레이아웃을 잡았다. 게시판 UI를 화면에 보기 좋게 배치하기 익힌 기술은 CSS Flexbox였다. 요소들을 가로로 배치하기 위해 복잡하게 위치를 계산하거나 화면이 깨지는 현상을 걱정할 필요 없이, Flexbox를 사용하면 1차원(가로 또는 세로) 레이아웃을 매우 직관적으로 제어할 수 있다. VS Code의 화면을 반으로 분할하여 왼쪽에는 HTML을, 오른쪽에는 CSS를 띄워두고 게시판의 디자인을 입혀나갔다. 부모 컨테이너에 display: flex를 선언하고, 주축(Main Axis)과 교차축(Cross Axis)을 정렬하는 코드를 작성했다.
[code] 
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    .board-header {
      display: flex;
      justify-content: space-between; 
      align-items: center; 
      padding: 20px 40px;
      background-color: #2c3e50;
      color: white;
    }
    
    .board-container {
      display: flex;
      flex-direction: column; /* 세로 방향으로 자식 요소 배치 */
      gap: 20px; /* 요소들 사이의 일정한 간격 유지 */
      padding: 40px;
      max-width: 800px;
      margin: 0 auto; /* 화면 중앙 정렬 */
    }
    
    .post-item {
      display: flex;
      flex-direction: column;
      gap: 10px;
      padding: 20px;
      background-color: #f8f9fa;
      border: 1px solid #dee2e6;
      border-radius: 8px;
    }
    
    .post-meta {
      display: flex;
      justify-content: flex-start;
      gap: 15px;
      font-size: 0.9rem;
      color: #6c757d;
    }
[/code]

특히 justify-content: space-between을 통해 헤더의 제목과 버튼을 손쉽게 양 끝으로 밀어내고, gap 속성을 사용해 margin 겹침 현상에 대한 고민 없이 요소 간의 여백을 일정하게 주입하는 과정이 편리했다. 브라우저 창 크기를 이리저리 줄였다 늘여도 레이아웃이 유연하게 변경되는 Flexbox를 잘 이용하자

* * *

# JavaScript / React 컴포넌트 설계

![](https://velog.velcdn.com/images/mi_nini/post/91bbee2d-3121-4aa7-bb71-75700ac8e5a9/image.png)

만들어놓은 HTML/CSS에 웹 페이지에 데이터를 다루고 사용자와 상호작용하는 Modern JavaScript의 핵심 문법을 배우고 React를 학습했다.

## JavaScript - 배열 내장 함수 (map, filter, reduce)

게시판 프로젝트를 진행하면서 가장 많이 다루게 될 데이터 형태는 결국 '게시글 객체들이 담긴 배열(Array)'이다. 서버로부터 여러 개의 게시글 데이터를 받아와 화면에 뿌려주고, 특정 글을 삭제하거나 검색해야 하기 때문이다. 이를 위해 기존의 지루한 `for` 루프를 벗어나, ES6+의 강력한 배열 내장 함수들을 학습했다.

> 불변성을 지키면서 원본 배열을 훼손하지 않고 새로운 배열을 반환하는 이 함수들은 추후 React의 상태 관리 로직에서 핵심적인 역할을 한다.

  * map(): 배열의 모든 요소를 순회하며 내가 원하는 형태(주로 HTML/JSX UI 요소)로 가공하여 새로운 배열을 만들어낸다. 게시글 목록을 렌더링할 때 필수적이다.


  * filter(): 조건에 맞는 요소들만 걸러내어 새로운 배열을 만든다. 게시글 삭제 기능이나 검색 기능을 구현할 때 주로 사용된다.
  * reduce(): 배열의 모든 값을 하나로 누적하여 병합한다. 총 게시글 수 계산이나 복잡한 데이터 포맷팅에 유용하다.


[code] 
    const posts = [
      { id: 1, title: '프론트엔드 1일차 회고', author: '김경민' },
      { id: 2, title: 'React 너무 재밌네요', author: '김민' },
      { id: 3, title: 'JavaScript 배열 함수 정리', author: '경민' }
    ];
    
    const postTitles = posts.map(post => `제목: ${post.title}`);
    console.log(postTitles); 
    // ["제목: 프론트엔드 1일차 회고", "제목: React 너무 재밌네요", "제목: JavaScript 배열 함수 정리"]
    
    const filteredPosts = posts.filter(post => post.id !== 2);
    console.log(filteredPosts); // id가 1, 3인 객체만 남은 새 배열 반환
[/code]

> 출처/참고  
>  <https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array>  
>  <https://adjh54.tistory.com/66>

* * *

## React 입문 및 컴포넌트(Component) 분리

> 들어가기전 VS Code 터미널에서 create-react-app 또는 Vite를 통해 기본 React 환경을 세팅하고 갑시다.

### Vite React 프로젝트 생성

단계| 명령어| 설명  
---|---|---  
1| `npm create vite@latest`| 프로젝트 생성 및 템플릿 선택  
2| `cd my-app`| 생성한 프로젝트 폴더로 이동  
3| `npm install`| 필요한 라이브러리 설치  
4| `npm run dev`| 개발 서버 실행  
  
### 전체 명령어
[code] 
    npm create vite@latest
    cd my-app
    npm install
    npm run dev
[/code]

### 실행 결과

주소| 설명  
---|---  
`http://localhost:5173`| 개발 서버 기본 실행 주소  
  
React의 가장 큰 장점 중 하나는 위에서 만들었던 '통짜 HTML' 문서를 레고 블록과 같은 Component 단위로 잘게 쪼개어 재사용할 수 있다는 것이다. 유지보수의 효율성을 극대화하기 위해, 나는 게시판 UI를 크게 Header, PostList(게시글 목록), PostItem(개별 게시글)이라는 독립적인 함수형 컴포넌트로 분리했다.  
이렇게 컴포넌트를 분리하면 각 파일이 맡은 역할이 명확해져 코드를 읽고 수정하기가 훨씬 수월해진다.

![](https://velog.velcdn.com/images/mi_nini/post/90033b78-1ace-4178-9c7d-7fa99936d3fc/image.png)

## Props를 통한 단방향 데이터 흐름 제어

컴포넌트를 여러 개로 분리하고 나면 필연적으로 "데이터를 어떻게 주고받을 것인가?"라는 문제에 부딪힌다. React는 부모 컴포넌트에서 자식 컴포넌트로만 데이터가 흐르는 단방향 데이터 바인딩 원칙을 가진다. 이때 전달되는 데이터의 매개체가 바로 Props다.  
앞서 배운 map() 함수와 React의 Props 개념을 결합하여, 최상위 컴포넌트(App.js)가 가진 배열 데이터를 하위 컴포넌트(PostItem)까지 안전하게 전달하여 화면에 그리는 로직을 구현했다.
[code] 
    // 1. 개별 게시글을 담당하는 자식 컴포넌트 (PostItem.jsx)
    // 부모로부터 post 객체를 Props로 전달받아 화면에 렌더링한다.
    const PostItem = ({ post }) => {
      return (
        <article className="post-item">
          <h2 className="post-title">{post.title}</h2>
          <div className="post-meta">
            <span className="author">작성자: {post.author}</span>
          </div>
        </article>
      );
    };
    
    export default PostItem;
    
    
    // 2. 게시글 목록을 렌더링하는 부모 컴포넌트 (PostList.jsx)
    // 서버에서 받아왔다고 가정한 데이터 배열을 map으로 순회하며 자식에게 Props로 넘겨준다.
    import PostItem from './PostItem';
    
    const PostList = () => {
      const dummyData = [
        { id: 1, title: '프론트엔드 1일차 회고', author: '김경민' },
        { id: 2, title: 'React 입문기', author: '김민' }
      ];
    
      return (
        <section className="post-list-section">
          {/* 배열의 map 함수를 이용해 컴포넌트를 반복 생성 */}
          {dummyData.map((post) => (
            // 컴포넌트 반복 시 고유한 key 값을 반드시 부여해야 함
            <PostItem key={post.id} post={post} /> 
          ))}
        </section>
      );
    };
    
    export default PostList;
[/code]

> 출처/참고  
>  <https://yhuj79.github.io/Vue/241230/>  
>  <https://dkkim2318.tistory.com/161>

* * *

# React State 관리와 CRUD 구현

![](https://velog.velcdn.com/images/mi_nini/post/84df7c7f-5dc3-4c75-87c0-15dd68ca387b/image.png)

단순히 정해진 데이터를 보여주는 것이 아닌, 사용자가 직접 글을 작성하고 삭제할 수 있는 동적인 CRUD(Create, Read, Update, Delete) 게시판을 프론트엔드 단에서 완벽하게 제어하는 실습을 가졌다.

## useState와 이벤트 핸들링

React에서 가장 중요하고 혁신적인 개념을 꼽으라면 State 관리일 것이다. 일반적인 JavaScript 변수는 값이 바뀌어도 화면이 스스로 업데이트되지 않지만, React의 `useState` Hook을 통해 생성된 상태는 값이 변경될 때마다 컴포넌트를 자동으로 다시 렌더링하게 만든다.  
사용자가 입력창에 글씨를 타이핑하거나 버튼을 클릭하는 등의 행동을 Event라고 한다. 나는 `onChange`와 `onClick` 같은 이벤트 핸들러를 통해 사용자의 동작을 감지하고, 그 결과를 `useState`의 상태 변경 함수(setState)에 전달하여 화면이 즉각적으로 갱신되도록 로직을 짰다. 

## 폼(Form) 제어와 조건부 렌더링

게시판의 핵심인 '글 작성' 기능을 만들기 위해 입력 폼을 제어하는 방법을 익혔다. React에서는 사용자의 입력값을 DOM 자체에 맡겨두는 것이 아니라, React의 State를 '신뢰 가능한 단일 출처'로 삼는 제어 컴포넌 패턴을 권장한다.

입력 필드의 `value` 속성을 State와 연결하여 폼을 완벽하게 제어했고, 사용자가 빈 값을 제출하려 할 때 제출을 막고 경고창을 띄우는 간단한 유효성 검사도 추가했다.  
또한, 상태 값에 따라 화면의 UI가 다르게 보이도록 하는 조건부 렌더링 개념도 도입했다. 예를 들어, 게시글 배열의 길이가 0일 때는 "작성된 게시글이 없습니다"라는 안내 문구를 보여주고, 게시글이 존재할 때만 목록 컴포넌트를 렌더링하도록 삼항 연산자를 적극 활용했다.

## 불변성을 유지하는 Create / Delete 로직 구현

가장 많은 고민을 했던 부분은 상태로 관리되는 배열에 새로운 데이터를 추가하고 삭제하는 로직이었다.  
React에서는 상태를 변경할 때 반드시 불변성을 지켜야 한다. 기존 배열을 직접 수정해버리는 `push()`나 `splice()` 같은 메서드는 사용할 수 없었다.

  * **Create (추가):** 전개 연산자(`...`)를 사용하여 기존 배열의 요소들을 새로운 배열에 흩뿌리듯 복사한 뒤, 그 뒤에 새로운 게시글 객체를 덧붙여 새로운 배열을 반환하도록 했다.
  * **Delete (삭제):** 특정 게시글의 삭제 버튼을 누르면, 해당 게시글의 고유 `id`를 인자로 전달받아 `filter()` 함수를 돌렸다. 즉, 삭제하려는 `id`와 일치하지 않는 게시글들만 남긴 '새로운 배열'로 상태를 통째로 교체하는 방식이다.



이러한 불변성 유지 로직을 실제 코드로 구현한 모습은 다음과 같다.
[code] 
    import React, { useState } from 'react';
    import PostList from './PostList'; // 2일차에 만든 목록 컴포넌트 불러오기
    
    const BoardApp = () => {
      // 게시글 목록 상태 관리
      const [posts, setPosts] = useState([
        { id: 1, title: '리액트 상태 관리 학습', author: '김경민' }
      ]);
      
      // 폼 입력창 상태 관리
      const [inputValue, setInputValue] = useState('');
    
      // Create: 폼 제출 시 새로운 게시글 추가
      const handleSubmit = (e) => {
        e.preventDefault(); // 브라우저의 기본 새로고침 동작 방지
        
        // 유효성 검사: 빈 문자열 제출 방지
        if (inputValue.trim() === '') {
          alert('내용을 입력해주세요.');
          return;
        }
    
        const newPost = {
          id: Date.now(), // 고유한 식별자를 위해 현재 시간의 타임스탬프 활용
          title: inputValue,
          author: '익명'
        };
    
        // 기존 배열을 건드리지 않고(불변성 유지) 새 데이터가 추가된 새 배열로 상태 변경
        setPosts([...posts, newPost]);
        
        // 글 작성이 완료되면 입력창 초기화
        setInputValue(''); 
      };
    
      // Delete: 특정 게시글 삭제
      const handleDelete = (idToRemove) => {
        // filter를 이용해 삭제 대상 id와 일치하지 않는 요소만 걸러내어 새 배열 생성
        const filteredPosts = posts.filter(post => post.id !== idToRemove);
        setPosts(filteredPosts);
      };
    
      return (
        <div className="board-container">
          <h2>새 글 작성</h2>
          {/* 폼 제출 이벤트 핸들링 */}
          <form onSubmit={handleSubmit}>
            <input 
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="게시글 제목을 입력하세요"
            />
            <button type="submit">등록</button>
          </form>
    
          <hr />
          
          {/* 조건부 렌더링: 게시글 유무에 따라 다른 UI 노출 */}
          {posts.length === 0 ? (
            <p className="empty-message">아직 작성된 게시글이 없습니다.</p>
          ) : (
            <PostList posts={posts} onDelete={handleDelete} />
          )}
        </div>
      );
    };
    
    export default BoardApp;
[/code]

> 출처/참고  
>  <https://ko.react.dev/reference/react/useState>  
>  <https://ko.react.dev/learn/conditional-rendering>

* * *

# 비동기 처리와 API 연동

지금까지 완성한 게시판은 화면 단에서 CRUD가 완벽하게 작동했지만, 브라우저를 새로고침하는 순간 모든 데이터가 날아가는 치명적인 한계가 있었다. 데이터가 메모리(State)에만 존재하기 때문이다.  
실제 백엔드 서버(REST API)와 연결하여 영구적으로 데이터를 읽고 쓰는 웹 애플리케이션을 만든다.

## useEffect와 컴포넌트 생명주기 제어

![](https://velog.velcdn.com/images/mi_nini/post/7def7a4d-cc4d-4b63-902d-1a3ce4651579/image.png)  
서버에서 데이터를 가져오려면 언제 요청을 보내야 할까? 단순히 컴포넌트 함수 내부에 요청 코드를 작성하면, 상태가 변경되어 렌더링이 일어날 때마다 무한히 서버에 요청을 보내는 대참사가 발생한다.  
이러한 부수 효과(Side Effect)를 통제하기 위해 React의 useEffect 훅을 학습했다. `useEffect`는 컴포넌트가 화면에 처음 나타날 때(Mount), 사라질 때(Unmount), 특정 상태가 변경될 때(Update) 등 컴포넌트의 생명주기에 맞춰 특정 코드를 실행할 수 있게 해준다. 두 번째 인자인 의존성 배열을 비워두면 `[]`, 오직 처음 화면이 렌더링될 때 딱 한 번만 서버에 데이터를 요청하도록 안전하게 제어할 수 있다.

## Axios를 활용한 REST API 연동 (비동기 처리)

서버와 통신하기 위해 자바스크립트 내장 `fetch` 대신, 실무에서 표준처럼 쓰이는 Axios 라이브러리를 도입했다. 데이터를 가져오는 데는 필연적으로 네트워크 지연(시간)이 발생하므로, 코드의 흐름이 멈추지 않도록 비동기 처리(async/await) 개념을 확인하자.

서버의 API 명세에 맞추어 HTTP 메서드를 매핑

  * **GET:** 서버에서 전체 게시글 목록 받아오기
  * **POST:** 내가 작성한 새 글을 서버에 저장하기
  * **DELETE:** 특정 `id`의 게시글을 서버에서 삭제하기



이러한 비동기 통신 로직을 기존 코드에 붙여보자
[code] 
    import React, { useState, useEffect } from 'react';
    import axios from 'axios';
    import PostList from './PostList';
    
    const ApiBoardApp = () => {
      const [posts, setPosts] = useState([]);
      const [inputValue, setInputValue] = useState('');
    
      // 1. Read (GET): 컴포넌트가 마운트될 때 딱 한 번 서버에서 데이터 로드
      useEffect(() => {
        const fetchPosts = async () => {
          try {
            const response = await axios.get('[https://api.example.com/posts](https://api.example.com/posts)');
            setPosts(response.data); // 서버에서 받은 데이터로 상태 초기화
          } catch (error) {
            console.error('데이터를 불러오는데 실패했습니다.', error);
          }
        };
        fetchPosts();
      }, []);
    
      // 2. Create (POST): 서버에 새 게시글 데이터 전송
      const handleAddPost = async (e) => {
        e.preventDefault();
        if (!inputValue.trim()) return;
    
        try {
          // 서버에 데이터 저장 요청
          const response = await axios.post('[https://api.example.com/posts](https://api.example.com/posts)', { 
            title: inputValue 
          });
          // 서버에서 응답받은 새 객체(DB에서 생성된 id 포함)를 상태에 추가
          setPosts([...posts, response.data]);
          setInputValue('');
        } catch (error) {
          console.error('게시글 작성에 실패했습니다.', error);
        }
      };
    
      // 3. Delete (DELETE): 서버에 특정 게시글 삭제 요청
      const handleDeletePost = async (id) => {
        try {
          await axios.delete(`https://api.example.com/posts/${id}`);
          // 서버 삭제 성공 시, 프론트엔드 상태에서도 제거
          setPosts(posts.filter(post => post.id !== id));
        } catch (error) {
          console.error('게시글 삭제에 실패했습니다.', error);
        }
      };
    
      return (
        <div className="board-container">
          <h2>API 연동 미니 게시판</h2>
          <form onSubmit={handleAddPost}>
            <input 
              value={inputValue} 
              onChange={(e) => setInputValue(e.target.value)} 
              placeholder="새 글을 입력하세요" 
            />
            <button type="submit">작성</button>
          </form>
          <hr />
          <PostList posts={posts} onDelete={handleDeletePost} />
        </div>
      );
    };
    
    export default ApiBoardApp;
[/code]

> 출처/참고  
>  <https://ko.react.dev/learn/lifecycle-of-reactive-effects>  
>  <https://velog.io/@sukong/REACT-%EB%A6%AC%EC%95%A1%ED%8A%B8%EC%9D%98-%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0%EC%99%80-useEffect-Hook>

* * *

## 생각정리

React를 배우며 가장 뼈저리게 느낀 핵심은 단연 '상태기반의 UI 제어'와 '불변성 유지'의 중요성이다.  
과거 바닐라 자바스크립트로 개발할 때는 이벤트가 발생할 때마다 일일이 DOM 요소를 찾아내서 직접 멱살을 잡고 수정해야 했다. 하지만 React는 이 귀찮은 과정을 거치지 않는다. 우리는 데이터만 신경 쓰면 된다 -> (상태를 변경하면 React가 알아서 변경점을 감지하고 화면을 업데이트) 여기에 더해 화면을 독립적인 Component 단위로 잘게 쪼개는 설계 방식은 코드의 재사용성을 엄청나게 끌어올려 주었다. 컴포넌트 분리를 통해 각 UI가 맡은 역할이 명확해지니, 코드가 아무리 길어져도 어디를 고쳐야 할지 한눈에 파악된다. 유지보수하기 좋은 코드란 무엇인지 제대로 배운 기분이다. (에러나는 부분에 터미널로 자세하게 나오니 이렇게 친절할수가..)  
하나에 불편한점이라고 생각한다면 React는 상태가 곧 화면이 되기 때문에, 결국 '이 상태를 어디서 어떻게 관리할 것인가'가 애플리케이션의 성능과 구조를 좌우하는 핵심이 된다고 생각한다. 무분별하게 상태를 변경했다가는 불필요한 Re-rendering이 폭발적으로 발생하기 때문이다. 편리해진 만큼, 상태 설계를 더 꼼꼼하게 작성하는 습관을 가지자.  
8주차를 마무리한다.

### [Gitprivate](https://github.com/KT-E/08-Week)
