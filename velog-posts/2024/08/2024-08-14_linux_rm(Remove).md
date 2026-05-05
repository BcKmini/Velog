---
title: "linux_rm(Remove)"
date: 2024-08-14 08:29:47
source: "https://velog.io/@mi_nini/linuxrmRemove"
---

## 📌 13. rm (Remove)

Now I think we have too many files, let’s remove some files. To remove files you can use the rm command. The rm (remove) command is used to delete files and directories.

> $ rm file1

Take caution when using rm, there is no magical trash can that you can fish out removed files. Once they are gone, they are gone for good, so be careful.

Fortunately there are some safety measures put into place, so the average joe can’t just remove a bunch of important files. Write-protected files will prompt you for confirmation before deleting them. If a directory is write-protected it will also not be easily removed.

Now if you don’t care about any of that, you can absolutely remove a bunch of files.

> $ rm -f file1

-f or force option tells rm to remove all files, whether they are write protected or not, without prompting the user (as long as you have the appropriate permissions).

> $ rm -i file

Adding the -i flag like many of the other commands, will give you a prompt on whether you want to actually remove the files or directories.

> $ rm -r directory

You can’t just rm a directory by default, you’ll need to add the -r flag (recursive) to remove all the files and any subdirectories it may have.

You can remove a directory with the rmdir command.

> $ rmdir directory

* * *

## 📝Exercises

Create a file called -file (don't forget the dash!).  
Remove that file.

* * *

## 💻Quiz

How do you remove a file called myfile?

* * *

## 📌13. rm (제거)

이제 파일이 너무 많은 것 같습니다. 파일을 제거해 보겠습니다. 파일을 제거하려면 rm 명령을 사용할 수 있습니다. rm(제거) 명령은 파일과 디렉토리를 삭제하는 데 사용됩니다.

> $ rm 파일1  
>  rm을 사용할 때는 조심하세요. 제거된 파일을 꺼낼 수 있는 마법의 휴지통은 없습니다. 파일이 사라지면 영원히 사라지므로 조심하세요.

다행히도 몇 가지 안전 조치가 마련되어 있어서 일반 사용자가 중요한 파일을 그냥 제거할 수는 없습니다. 쓰기 보호된 파일은 삭제하기 전에 확인을 요청합니다. 디렉토리가 쓰기 보호되어 있으면 쉽게 제거할 수 없습니다.

이제 여러분이 이런 것에 관심이 없다면, 여러분은 분명히 많은 파일을 제거할 수 있습니다.

> $ rm -f 파일1

-f 또는 force 옵션은 사용자에게 묻지 않고(적절한 권한이 있는 경우) 쓰기 보호되어 있든 없든 모든 파일을 제거하도록 rm에 지시합니다.

> $ rm -i 파일

다른 많은 명령과 마찬가지로 -i 플래그를 추가하면 실제로 파일이나 디렉토리를 제거할지 여부에 대한 메시지가 표시됩니다.

> $ rm -r 디렉토리

기본적으로 디렉토리에 대해 rm 명령을 실행할 수 없으며, -r 플래그(재귀적)를 추가하여 모든 파일과 디렉토리의 하위 디렉토리를 모두 제거해야 합니다.

rmdir 명령을 사용하여 디렉토리를 제거할 수 있습니다.

> $ rmdir 디렉토리

* * *

## 📝수업 과정

-file이라는 이름의 파일을 만드세요(대시(D)를 잊지 마세요!).  
해당 파일을 제거하세요.  
![](https://velog.velcdn.com/images/mi_nini/post/03931cf6-b82d-44ee-8a96-05951cf2268b/image.png)

* * *

## 💻퀴즈

myfile이라는 파일을 어떻게 제거하나요?  
정답 : rm myfile
