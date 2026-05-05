---
title: "linux_ls (List Directories)"
date: 2024-08-13 06:11:43
source: "https://velog.io/@mi_nini/8.12"
---

## 📌4. ls (List Directories)

Now that we know how to move around the system, how do we figure out what is available to us? Right now it’s like we are moving around in the dark. Well, we can use the wonderful ls command to list directory contents. The ls command will list directories and files in the current directory by default, however you can specify which path you want to list the directories of.

> $ ls  
>  $ ls /home/pete

ls is a quite useful tool, it also shows you detailed information about the files and directories you are looking at.

Also note that not all files in a directory will be visible. Filenames that start with . are hidden, you can view them however with the ls command and pass the -a flag to it (a for all).

> $ ls -a

There is also one more useful ls flag, -l for long, this shows a detailed list of files in a long format. This will show you detailed information, starting from the left: file permissions, number of links, owner name, owner group, file size, timestamp of last modification, and file/directory name.

> $ ls -l

> pete@icebox:~$ ls -l  
>  total 80  
>  drwxr-x--- 7 pete penguingroup 4096 Nov 20 16:37 Desktop  
>  drwxr-x--- 2 pete penguingroup 4096 Oct 19 10:46 Documents  
>  drwxr-x--- 4 pete penguingroup 4096 Nov 20 09:30 Downloads  
>  drwxr-x--- 2 pete penguingroup 4096 Oct 7 13:13 Music  
>  drwxr-x--- 2 pete penguingroup 4096 Sep 21 14:02 Pictures  
>  drwxr-x--- 2 pete penguingroup 4096 Jul 27 12:41 Public  
>  drwxr-x--- 2 pete penguingroup 4096 Jul 27 12:41 Templates  
>  drwxr-x--- 2 pete penguingroup 4096 Jul 27 12:41 Videos

Commands have things called flags (or arguments or options, whatever you want to call it) to add more functionality. See how we added -a and -l, well you can add them both together with -la. The order of the flags determines which order it goes in, most of the time this doesn’t really matter so you can also do ls -al and it would still work.

> $ ls -la

* * *

## 📝 Exercises

Run ls with different flags and see the output you receive.

  * ls -R: recursively list directory contents
  * ls -r: reverse order while sorting
  * ls -t: sort by modification time, newest first



* * *

## ⛳ Quiz

What command would you use to see hidden files?

* * *

## 📌4. ls (디렉토리 목록)

이제 시스템을 어떻게 돌아다닐지 알았으니, 우리가 사용할 수 있는 것이 무엇인지 어떻게 알아낼까요? 지금은 마치 어둠 속을 돌아다니는 것과 같습니다. 글쎄요, 우리는 훌륭한 ls 명령을 사용하여 디렉토리 내용을 나열할 수 있습니다. ls 명령은 기본적으로 현재 디렉토리의 디렉토리와 파일을 나열하지만, ​​디렉토리를 나열할 경로를 지정할 수 있습니다.

> $ ls  
>  $ ls / 홈 / 피트

ls는 꽤 유용한 도구이며, 사용자가 보고 있는 파일과 디렉토리에 대한 자세한 정보도 보여줍니다.

또한 디렉토리의 모든 파일이 표시되는 것은 아니라는 점에 유의하세요. .으로 시작하는 파일 이름은 숨겨져 있지만 ls 명령으로 볼 수 있으며 -a 플래그를 전달하면 됩니다(a는 모든 것을 의미).

> $ ls -a

유용한 ls 플래그가 하나 더 있는데, -l은 long을 의미하는데, 이는 긴 형식으로 파일의 자세한 목록을 보여줍니다. 왼쪽부터 시작하여 자세한 정보를 보여줍니다: 파일 권한, 링크 수, 소유자 이름, 소유자 그룹, 파일 크기, 마지막 수정 타임스탬프, 파일/디렉토리 이름.

> $ ls -l  
>  pete@icebox:~$ ls -l  
>  총 80  
>  drwxr-x--- 7 pete penguingroup 4096 11월 20일 16:37 데스크톱  
>  drwxr-x--- 2 pete penguingroup 4096 10월 19일 10:46 문서  
>  drwxr-x--- 4 pete penguingroup 4096 11월 20일 09:30 다운로드  
>  drwxr-x--- 2 pete penguingroup 4096 10월 7일 13:13 음악  
>  drwxr-x--- 2 pete penguingroup 4096 9월 21일 14:02 사진  
>  drwxr-x--- 2 pete penguingroup 4096 7월 27일 12:41 공개  
>  drwxr-x--- 2 pete penguingroup 4096 7월 27일 12:41 템플릿  
>  drwxr-x--- 2 pete penguingroup 4096 7월 27일 12:41 비디오

명령어에는 플래그(또는 인수 또는 옵션, 원하는 대로 부르세요)라고 하는 것이 있어 더 많은 기능을 추가합니다. -a와 -l을 추가한 방법을 보세요. -la로 둘 다 추가할 수 있습니다. 플래그의 순서에 따라 플래그가 어떤 순서로 들어가는지 결정하는데, 대부분의 경우 이는 중요하지 않으므로 ls -al을 실행해도 여전히 작동합니다.

> $ ls -라

* * *

## 📝수업 과정

다른 플래그를 사용하여 ls를 실행하고 출력되는 내용을 확인하세요.

  * ls -R: 디렉토리 내용을 재귀적으로 나열합니다
  * ls -r: 정렬 시 역순으로 정렬
  * ls -t: 수정 시간순으로 정렬, 최신순으로 정렬  
![](https://velog.velcdn.com/images/mi_nini/post/8996cbe4-897a-446e-86ea-08aa301f3642/image.png)



* * *

## ⛳퀴즈

숨겨진 파일을 보려면 어떤 명령을 사용해야 하나요?  
정답 : ls -a
