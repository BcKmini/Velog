---
title: "linux_pwd(Print Working Directory)"
date: 2024-08-10 19:29:30
source: "https://velog.io/@mi_nini/8.11-pwdPrint-Working-Directory"
---

2. pwd (Print Working Directory)


Everything in Linux is a file, as you journey deeper into Linux you’ll understand this, but for now just keep that in mind. Every file is organized in a hierarchical directory tree. The first directory in the filesystem is aptly named the root directory. The root directory has many folders and files which you can store more folders and files, etc. Here is an example of what the directory tree looks like:




/

|-- bin

|     |-- file1

|     |-- file2

|-- etc

|    |-- file3

|        directory1

|                 |-- file4

|                 `-- file5

|-- home

|-- var




The location of these files and directories are referred to as paths. If you had a folder named home with a folder inside of it named pete and another folder in that folder called Movies, that path would look like this: /home/pete/Movies, pretty simple huh?


Navigation of the filesystem, much like real life is helpful if you know where you are and where you are going. To see where you are, you can use the pwd command, this command means “print working directory” and it just shows you which directory you are in, note the path stems from the root directory.




$ pwd




Where are you? Where am I? Give it a try.




2. 📌pwd (작업 디렉토리 인쇄)


Linux의 모든 것은 파일입니다. Linux에 대해 더 깊이 여행하면 이를 이해하게 될 것이지만 지금은 이 점만 명심하세요. 모든 파일은 계층적 디렉토리 트리로 구성됩니다. 파일 시스템의 첫 번째 디렉토리는 적절하게 루트 디렉토리라고 명명되었습니다. 루트 디렉토리에는 더 많은 폴더와 파일 등을 저장할 수 있는 많은 폴더와 파일이 있습니다. 디렉토리 트리가 어떤 모습인지 보여주는 예는 다음과 같습니다.


/


|-- bin


| |-- file1


| |-- file2


|-- etc


| |-- file3


| `-- directory1


| |-- file4


| `-- file5


|-- home


|-- var


이러한 파일과 디렉토리의 위치를 ​​경로라고 합니다. home이라는 폴더가 있고 그 안에 pete라는 폴더가 있고 그 폴더 안에 Movies라는 폴더가 있다면, 그 경로는 다음과 같습니다. /home/pete/Movies, 꽤 간단하죠?


파일 시스템 탐색은 실제 생활과 매우 유사하며, 어디에 있는지, 어디로 가는지 알고 있다면 유용합니다. 어디에 있는지 확인하려면 pwd 명령을 사용할 수 있습니다. 이 명령은 "작업 디렉토리 인쇄"를 의미하며, 현재 어떤 디렉토리에 있는지 보여줍니다. 경로는 루트 디렉토리에서 유래합니다.




$ 비밀번호




당신은 어디에 있습니까? 나는 어디에 있습니까? 시도해 보세요.


#Exercises

No exercises for this lesson.


💻Quiz


How do I find what directory you are currently in?




Answer


pwd










📌로지컬 위치와 피지컬 위치의 차이


$ pwd --help
pwd: pwd [-LP]
    Print the name of the current working directory.

    Options:
      -L    print the value of $PWD if it names the current working
            directory
      -P    print the physical directory, without any symbolic links

    By default, `pwd' behaves as if `-L' were specified.

    Exit Status:
    Returns 0 unless an invalid option is given or the current directory
    cannot be read.


: PWD는 사용자가 현재 작업하는 디렉토리 또는 현재 위치하는 디레토리의 경로를 호출할 때 사용하는 환경변수이다. OLDPWD와는 다르게 항상 어떠한 리눅스 사용자라도 현재 디렉토리가 존재하기 때문에 PWD환경변수는 현재 디렉토리를 저장하고 있다.
