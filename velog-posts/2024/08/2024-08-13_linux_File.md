---
title: "linux_File"
date: 2024-08-13 14:06:08
source: "https://velog.io/@mi_nini/File"
---

📌6. file


In the previous lesson we learned about touch, let’s go back to that for a bit. Did you notice that the filename didn’t conform to standard naming like you’ve probably seen with other operating systems like Windows? Normally you would expect a file called banana.jpeg and expect a JPEG picture file.


In Linux, filenames aren’t required to represent the contents of the file. You can create a file called funny.gif that isn’t actually a GIF.


To find out what kind of file a file is, you can use the file command. It will show you a description of the file’s contents.




$ file banana.jpg






📝Exercises


Run the file command on a few different directories and files and note the output.




💻Quiz


What command can you use to find the file type of a file?




📌6. 파일


이전 수업에서 터치에 대해 배웠는데, 잠깐 그 내용으로 돌아가 봅시다. 파일 이름이 Windows와 같은 다른 운영 체제에서 본 것과 같은 표준 명명법에 맞지 않는다는 것을 알아차렸나요? 일반적으로 banana.jpeg라는 파일을 기대하고 JPEG 사진 파일을 기대합니다.


리눅스에서 파일 이름은 파일의 내용을 나타내는 데 필요하지 않습니다. 실제로 GIF가 아닌 funny.gif라는 파일을 만들 수 있습니다.


파일이 어떤 종류의 파일인지 알아내려면 file 명령을 사용하면 됩니다. 파일의 내용에 대한 설명이 표시됩니다.




$ 파일 banana.jpg

$ file banana.jpg






📝수업 과정


몇 개의 다른 디렉토리와 파일에 file 명령을 실행하고 출력을 살펴보세요.






💻퀴즈


파일의 유형을 찾으려면 어떤 명령을 사용할 수 있나요?

정답 : file
