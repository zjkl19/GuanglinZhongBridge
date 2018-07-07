
set fileName=GuanglinZhongBridge.py
set fromPath=E:\vsProjects\GuanglinZhongBridge\GuanglinZhongBridge
set toPath=D:\simulia\temp\

xcopy %fromPath% %toPath%  /e /h /y
abaqus cae noGUI=%toPath%%fileName%

