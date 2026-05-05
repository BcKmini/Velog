---
title: "linux_history"
date: 2024-08-14 07:51:32
source: "https://velog.io/@mi_nini/linuxhistory"
---

📌9. history


In your shell, there is a history of the commands that you previously entered, you can actually look through these commands. This is quite useful when you want to find and run a command you used previously without actually typing it again.




$ history




Want to run the same command you did before, just hit the up arrow.


Want to run the previous command without typing it again? Use !!. If you typed cat file1 and want to run it again, you can actually just go !! and it will run the last command you ran.


Another history shortcut is ctrl-R, this is the reverse search command, if you hit ctrl-R and you start typing parts of the command you want it will show you matches and you can just navigate through them by hitting the ctrl-R key again. Once you found the command you want to use again, just hit the Enter key.


Our terminal is getting a little cluttered no? Let’s do a little cleanup, use the clear command to clear up your display.




$ clear




There that looks better doesn’t it?


While we are talking about useful things, one of the most useful features in any command-line environment is tab completion. If you start typing the beginning of a command, file, directory, etc and hit the Tab key, it will autocomplete based on what it finds in the directory you are searching as long as you don’t have any other files that start with those letters. For example if you were trying to run the command chrome, you can type chr and press Tab and it will autocomplete chrome.




📝Exercises


Navigate through your previous command history with the Up and Down keys. Play around with ctrl-R reverse search.




💻Quiz


What is the command to clear the terminal?




📌9. 역사


쉘에는 이전에 입력한 명령의 기록이 있으며, 실제로 이러한 명령을 살펴볼 수 있습니다. 이는 실제로 다시 입력하지 않고 이전에 사용한 명령을 찾아 실행하려는 경우 매우 유용합니다.




$ 역사

$ history




이전에 했던 것과 동일한 명령을 실행하려면 위쪽 화살표를 누르세요.


다시 입력하지 않고 이전 명령을 실행하고 싶으신가요? !!를 사용하세요. cat file1을 입력하고 다시 실행하고 싶다면, 실제로 !!를 입력하면 마지막으로 실행한 명령이 실행됩니다.


또 다른 히스토리 단축키는 ctrl-R입니다. 이것은 역방향 검색 명령입니다. ctrl-R을 누르고 원하는 명령의 일부를 입력하기 시작하면 일치 항목이 표시되고 ctrl-R 키를 다시 눌러서 탐색할 수 있습니다. 다시 사용하고 싶은 명령을 찾으면 Enter 키를 누르기만 하면 됩니다.


터미널이 좀 지저분해지지 않나요? 조금 정리를 해보고, clear 명령어를 사용해서 화면을 비우세요.




$ 지우기

$ clear




그게 더 나아 보이지 않나요?


유용한 것에 대해 이야기하는 동안, 모든 명령줄 환경에서 가장 유용한 기능 중 하나는 탭 완성입니다. 명령, 파일, 디렉토리 등의 시작 부분을 입력하기 시작하고 탭 키를 누르면 해당 문자로 시작하는 다른 파일이 없는 한 검색하는 디렉토리에서 찾은 내용을 기반으로 자동 완성합니다. 예를 들어 chrome 명령을 실행하려고 하는 경우 chr을 입력하고 Tab 키를 누르면 chrome이 자동 완성됩니다.




📝수업 과정


위, 아래 키를 사용하여 이전 명령 기록을 탐색합니다. ctrl-R 역방향 검색을 사용해 보세요.






💻퀴즈


터미널을 지우는 명령어는 무엇인가요?

정답 : clear






Clear:


기존에 실행한 명령어 이력을 보여 주거나 실행할때 사용한다. 


📌기존 히스토리 리스트 지우기


-c

기존 히스토리 리스트 지우기

-d offset

offset 해당하는 히스토리 제거

-a

히스토리 라인을 히스토리 파일에 추가

-n

히스토리파일에서 읽지않은 라인 읽기

-r

히스토리 파일을 읽어서 히스토리 리스트에 추가

-w

현재 히스토리를 히스토리 파일에 저장

-p

히스토리 확장수행하나 히스토리 리스트 미저장

-s

히스토리 리스트로 ARGs 추가하나 실행안함.
