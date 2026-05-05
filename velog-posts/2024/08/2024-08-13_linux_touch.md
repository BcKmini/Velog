---
title: "linux_touch"
date: 2024-08-13 14:00:33
source: "https://velog.io/@mi_nini/8.13-5.-touch"
---

📌 5. touch


Let’s learn how to make some files. A very simple way is to use the touch command. Touch allows you to the create new empty files.




$ touch mysuperduperfile




And boom, new file!


Touch is also used to change timestamps on existing files and directories. Give it a try, do an ls -l on a file and note the timestamp, then touch that file and it will update the timestamp.


There are many other ways to create files that involve other things like redirection and text editors, but we’ll get to that in the Text Manipulation course.




📝Exercises


Create a new file

Note the timestamp

Touch the file and check the timestamp once again




💻Quiz


How do you create a file called myfile?




📌 5. touch


파일을 만드는 방법을 알아보겠습니다. 아주 간단한 방법은 touch 명령을 사용하는 것입니다. touch를 사용하면 새 빈 파일을 만들 수 있습니다.




$ 내 슈퍼듀퍼파일을 터치하세요

$ touch mysuperduperfile




붐, 새로운 파일이 생겼어요!


Touch는 기존 파일과 디렉토리의 타임스탬프를 변경하는 데에도 사용됩니다. 시도해 보세요. 파일에서 ls -l을 실행하고 타임스탬프를 기록한 다음 해당 파일을 touch하면 타임스탬프가 업데이트됩니다.


리디렉션이나 텍스트 편집기 등 다른 것들을 포함하는 파일을 만드는 방법은 많이 있지만, 여기서는 텍스트 조작 과정에서 다루겠습니다.




📝수업 과정


새 파일을 만듭니다

타임스탬프를 확인하세요

파일을 터치하여 타임스탬프를 다시 한번 확인하세요






💻퀴즈


myfile이라는 파일은 어떻게 만듭니까?

정답 : touch myfile
