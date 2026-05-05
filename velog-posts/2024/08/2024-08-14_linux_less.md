---
title: "linux_less"
date: 2024-08-14 07:41:28
source: "https://velog.io/@mi_nini/linux8.-less"
---

📌8. less


If you are viewing text files larger than a simple output, less is more. (There is actually a command called more that does something similar, so this is ironic.) The text is displayed in a paged manner, so you can navigate through a text file page by page.


Go ahead and look at the contents of a file with less. Once you’re in the less command, you can actually use other keyboard commands to navigate in the file.




$ less /home/pete/Documents/text1




Use the following command to navigate through less:


q - Used to quit out of less and go back to your shell.

Page up, Page down, Up and Down - Navigate using the arrow keys and page keys.

g - Moves to beginning of the text file.

G - Moves to the end of the text file.

/search - You can search for specific text inside the text document. Prefacing the words you want to search with /

h - If you need a little help about how to use less while you’re in less, use help.




📝Exercises


Run less on a file, then page up and around the file. Try searching for a specific word. Quickly navigate to the beginning or the end of the file.




💻Quiz


How do you quit out of a less command?




📌8. less


간단한 출력보다 큰 텍스트 파일을 보고 있다면 less is more입니다. (실제로 more라는 명령이 비슷한 것을 하는데, 아이러니합니다.) 텍스트는 페이지 방식으로 표시되므로 텍스트 파일을 페이지별로 탐색할 수 있습니다.


less로 파일의 내용을 살펴보세요. less 명령에 들어가면 실제로 다른 키보드 명령을 사용하여 파일을 탐색할 수 있습니다.




$ less /home/pete/문서/text1

$ less /home/pete/Documents/text1




다음 명령을 사용하여 less를 탐색하세요.




q - less를 종료하고 쉘로 돌아가는 데 사용됩니다.

페이지 위로, 페이지 아래로, 위아래 - 화살표 키와 페이지 키를 사용하여 탐색합니다.


g - 텍스트 파일의 시작 부분으로 이동합니다.


G - 텍스트 파일의 끝으로 이동합니다.


/search - 텍스트 문서 내에서 특정 텍스트를 검색할 수 있습니다. 검색하려는 단어 앞에 /를 붙입니다.


h - less를 사용하는 동안 less를 사용하는 방법에 대한 약간의 도움이 필요하면 help를 사용하세요.






📝수업 과정


파일에서 less를 실행한 다음, 파일을 위로 페이지 이동하고 돌아다닙니다. 특정 단어를 검색해 보세요. 파일의 시작 또는 끝으로 빠르게 이동합니다.








💻퀴즈


less 명령을 어떻게 종료하나요?

정답 : q
