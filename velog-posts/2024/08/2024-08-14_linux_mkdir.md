---
title: "linux_mkdir"
date: 2024-08-14 08:21:24
source: "https://velog.io/@mi_nini/linuxmkdir"
---

## 📌12. mkdir (Make Directory)

We’re gonna need some directories to store all these files we’ve been working on. The mkdir command (Make Directory) is useful for that, it will create a directory if it doesn’t already exist. You can even make multiple directories at the same time.

> $ mkdir books paintings

You can also create subdirectories at the same time with the -p (parent flag).

> $ mkdir -p books/hemmingway/favorites

* * *

## 📝Exercises

Make a couple of directories and move some files into that directory.

* * *

## 💻Quiz

What command is use to make a directory?

* * *

## 📌12. mkdir (디렉토리 만들기)

우리가 작업한 모든 파일을 저장할 디렉토리가 필요합니다. mkdir 명령(디렉토리 만들기)이 유용합니다. 디렉토리가 없으면 디렉토리를 만듭니다. 여러 디렉토리를 동시에 만들 수도 있습니다.

> $ mkdir 책 그림  
>  $ mkdir books paintings

-p (부모 플래그)를 사용하면 동시에 하위 디렉토리를 만들 수도 있습니다.

> $ mkdir -p books/hemmingway/favorites

* * *

## 📝수업 과정

몇 개의 디렉토리를 만들고 일부 파일을 해당 디렉토리로 옮깁니다.  
![](https://velog.velcdn.com/images/mi_nini/post/04084427-54ca-4a4e-9da6-603884726924/image.png)

![](https://velog.velcdn.com/images/mi_nini/post/0770e897-6254-47ba-84c2-bb4cdfa6d119/image.png)

* * *

## 💻퀴즈

디렉토리를 만드는 데 어떤 명령어를 사용하나요?  
정답 : mkdir

* * *

> ## mkdir의 뜻 make directorymkdir [옵션][생성 할 디렉토리]
> 
>   * new_folder 디렉토리 생성  
>  ex) mkdir new_folder
>   * /home/user/위치에 new_folder 디렉토리 생성  
>  ex) mkdir /home/user/new_folder
>   * new_folder, new_folder2, new_folder3 디렉토리 생성  
>  ex) mkdir new_folder new_folder2 new_folder3
> 


> -m : 디렉토리를 생성할 때 권한을 설정합니다. (defualt : 755)  
>  -p : 상위 경로도 함께 생성합니다.  
>  -v : 디렉토리를 생성하고 생성된 디렉토리에 대한 메시지를 출력합니다.
