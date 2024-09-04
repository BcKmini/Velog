<h1 id="📌-14-find">📌 14. find</h1>
<p>With all these files we have on the system it can get a little hectic trying to find a specific one. Well there’s a command we can use for that, find!</p>
<blockquote>
<p>$ find /home -name puppies.jpg</p>
</blockquote>
<p>With find you’ll have to specify the directory you’ll be searching it, what you’re searching for, in this case we are trying to find a file by the name of puppies.jpg.</p>
<p>You can specify what type of file you are trying to find.</p>
<blockquote>
<p>$ find /home -type d -name MyFolder</p>
</blockquote>
<p>You can see that I set the type of file I’m trying to find as (d) for directory and I’m still searching by the name of MyFolder.</p>
<p>One cool thing to note is that find doesn’t stop at the directory you are searching, it will look inside any subdirectories that directory may have as well.</p>
<hr />
<h1 id="📝exercises">📝Exercises</h1>
<p>Find a file from the root directory that has the word net in it.</p>
<hr />
<h1 id="💻quiz">💻Quiz</h1>
<p>What option should I specify for find if I want to search by name?</p>
<hr />
<h1 id="📌-14-찾다">📌 14. 찾다</h1>
<p>시스템에 있는 이 모든 파일을 사용하면 특정 파일을 찾으려고 하면 약간 혼란스러울 수 있습니다. 글쎄요, 그걸 위해 사용할 수 있는 명령어가 있는데, 바로 find!입니다.</p>
<blockquote>
<p>$ find /home -name 강아지.jpg</p>
</blockquote>
<p>find를 사용할 때는 검색할 디렉토리와 검색 내용을 지정해야 합니다. 이 경우 puppies.jpg라는 이름의 파일을 찾으려고 합니다.</p>
<p>찾으려는 파일의 유형을 지정할 수 있습니다.</p>
<blockquote>
<p>$ find /home -type d -name MyFolder</p>
</blockquote>
<p>찾으려는 파일 형식을 (d)로 설정하여 디렉토리로 지정했고, 여전히 MyFolder라는 이름으로 검색하고 있는 것을 볼 수 있습니다.</p>
<p>알아두면 좋은 점은 find가 검색하는 디렉토리에서 멈추지 않고 해당 디렉토리에 있는 모든 하위 디렉토리도 검색한다는 것입니다.</p>
<hr />
<h1 id="📝수업-과정">📝수업 과정</h1>
<p>루트 디렉토리에서 net이라는 단어가 포함된 파일을 찾으세요.
<img alt="" src="https://velog.velcdn.com/images/mi_nini/post/4a832019-efe3-4d6c-a66b-37a9f0514bd7/image.png" /></p>
<hr />
<h1 id="💻퀴즈">💻퀴즈</h1>
<p>이름으로 검색하고 싶은 경우, 어떤 옵션을 지정해야 합니까?
정답 : -name</p>