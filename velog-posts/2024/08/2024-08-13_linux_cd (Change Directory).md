---
title: "linux_cd (Change Directory)"
date: 2024-08-13 05:54:37
source: "https://velog.io/@mi_nini/8.12-cd-Change-Directory"
---

## 📌3. cd (Change Directory)

Now that you know where you are, let’s see if we can move around the filesystem a bit. Remember we’ll need to navigate our way using paths. There are two different ways to specify a path, with absolute and relative paths.

  * Absolute path: This is the path from the root directory. The root is the head honcho. The root directory is commonly shown as a slash. Every time your path starts with / it means you are starting from the root directory. For example, /home/pete/Desktop.
  * Relative path: This is the path from where you are currently in filesystem. If I was in location /home/pete/Documents and wanted to get to a directory inside Documents called taxes, I don’t have to specify the whole path from root like /home/pete/Documents/taxes, I can just go to taxes/ instead.



Now that you know how paths work, we just need something to help us change to the directory we want to. Luckily, we have cd or “change directory” to do that.

> $ cd /home/pete/Pictures  
>  So now I've changed my directory location to /home/pete/Pictures.

Now from this directory I have a folder inside called Hawaii, I can navigate to that folder with:

> $ cd Hawaii  
>  Notice how I just used the name of the folder? It’s because I was already in /home/pete/Pictures.

It can get pretty tiring navigating with absolute and relative paths all the time, luckily there are some shortcuts to help you out.

  * . (current directory). This is the directory you are currently in.
  * .. (parent directory). Takes you to the directory above your current.
  * ~ (home directory). This directory defaults to your “home directory”. Such as /home/pete.
  * \-- (previous directory). This will take you to the previous directory you were just at.

> $ cd .  
>  $ cd ..  
>  $ cd ~  
>  $ cd -




Give them a try!

* * *

Exercises  
Run the cd command without any flags, where does it take you?

* * *

Quiz  
If you are in /home/pete/Pictures and wanted to go to /home/pete, what’s a good shortcut to use?

* * *

## 📌3. cd (디렉토리 변경)

이제 어디에 있는지 알았으니 파일 시스템을 조금 돌아다닐 수 있는지 봅시다. 경로를 사용하여 길을 찾아야 한다는 것을 기억하세요. 경로를 지정하는 방법에는 절대 경로와 상대 경로의 두 가지가 있습니다.

  * 절대 경로: 루트 디렉토리에서 시작하는 경로입니다. 루트는 헤드 혼초입니다. 루트 디렉토리는 일반적으로 슬래시로 표시됩니다. 경로가 /로 시작할 때마다 루트 디렉토리에서 시작한다는 의미입니다. 예를 들어, /home/pete/Desktop.
  * 상대 경로: 현재 파일 시스템에서 있는 위치부터의 경로입니다. 내가 /home/pete/Documents 위치에 있고 Documents 내부의 taxes라는 디렉토리로 이동하고 싶다면 /home/pete/Documents/taxes처럼 루트에서 전체 경로를 지정할 필요가 없고 대신 taxes/로 이동하면 됩니다.  
이제 경로가 어떻게 작동하는지 알았으니, 원하는 디렉토리로 변경하는 데 도움이 되는 것이 필요합니다. 다행히도 cd 또는 "디렉토리 변경"이 있습니다.



> $ cd /홈/피트/사진  
>  이제 디렉토리 위치를 /home/pete/Pictures로 변경했습니다.

이제 이 디렉토리에서 Hawaii라는 폴더가 생성되었고, 다음을 사용하여 해당 폴더로 이동할 수 있습니다.

> $ cd 하와이  
>  내가 방금 폴더 이름을 사용한 것을 알아차렸나요? 내가 이미 /home/pete/Pictures에 있었기 때문입니다.

절대 경로와 상대 경로를 항상 사용해 탐색하는 건 꽤나 지루할 수 있지만, 다행히도 여러분을 도와주는 단축키가 몇 가지 있습니다.

> . (현재 디렉토리). 현재 있는 디렉토리입니다.  
>  .. (상위 디렉토리). 현재 디렉토리보다 상위 디렉토리로 이동합니다.  
>  ~ (홈 디렉토리). 이 디렉토리는 기본적으로 "홈 디렉토리"로 설정됩니다. 예를 들어 /home/pete.
> 
>   * (이전 디렉토리). 방금 있었던 이전 디렉토리로 이동합니다.
> 


> $ cd .  
>  $ cd ..  
>  $ cd ~  
>  $ cd -

한 번 시도해 보세요!

* * *

수업 과정  
플래그 없이 cd 명령을 실행하면 어디로 가나요?  
-> 홈 디렉토리

* * *

퀴즈  
/home/pete/Pictures에 있고 /home/pete로 이동하고 싶은 경우, 어떤 단축키를 사용하면 좋을까요?  
정답 : cd ..
