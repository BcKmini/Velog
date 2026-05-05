---
title: "linux_mv(Move)"
date: 2024-08-14 08:11:00
source: "https://velog.io/@mi_nini/linuxmvMove"
---

## 📌11. mv (Move)

Used for moving files and also renaming them. Quite similar to the cp command in terms of flags and functionality.

You can rename files like this:

> $ mv oldfile newfile

Or you can actually move a file to a different directory:

> $ mv file2 /home/pete/Documents

And move more than one file:

> $ mv file_1 file_2 /somedirectory

You can rename directories as well:

> $ mv directory1 directory2

Like cp, if you mv a file or directory it will overwrite anything in the same directory. So you can use the -i flag to prompt you before overwriting anything.

> mv -i directory1 directory2

Let’s say you did want to mv a file to overwrite the previous one. You can also make a backup of that file and it will just rename the old version with a ~.

> $ mv -b directory1 directory2

* * *

## 📝Exercises

Rename a file, then move that file to a different directory.

* * *

## 💻Quiz

How do you rename a file called cat to dog?

* * *

## 📌11. mv(이동)

파일을 이동하고 이름을 바꾸는 데 사용됩니다. 플래그와 기능 면에서 cp 명령과 매우 유사합니다.

다음과 같이 파일 이름을 바꿀 수 있습니다.

> $ mv oldfile newfile

또는 실제로 파일을 다른 디렉토리로 이동할 수 있습니다.

> $ mv file2 /home/pete/문서

그리고 두 개 이상의 파일을 이동합니다.

> $ mv 파일_1 파일_2 /일부 디렉토리

디렉토리의 이름도 바꿀 수 있습니다.

> $ mv 디렉토리1 디렉토리2

cp처럼, 파일이나 디렉토리를 mv하면 같은 디렉토리에 있는 모든 것을 덮어씁니다. 따라서 -i 플래그를 사용하여 덮어쓰기 전에 묻습니다.

> mv -i 디렉토리1 디렉토리2

이전 파일을 덮어쓰기 위해 mv를 실행하고 싶다고 가정해 보겠습니다. 해당 파일의 백업을 만들 수도 있으며, 그러면 이전 버전의 이름을 ~로 바꿀 뿐입니다.

> $ mv -b 디렉토리1 디렉토리2

* * *

## 📝수업 과정

파일 이름을 바꾼 다음, 해당 파일을 다른 디렉토리로 옮깁니다.  
![](https://velog.velcdn.com/images/mi_nini/post/9bf56b09-540d-4c52-b79d-4326ccda6240/image.png)

![](https://velog.velcdn.com/images/mi_nini/post/e89909fd-83dc-4835-b26c-ebcfb6d70b7c/image.png)

* * *

## 💻퀴즈

cat이라는 파일의 이름을 dog로 바꾸려면 어떻게 해야 하나요?  
정답 : mv cat dog
