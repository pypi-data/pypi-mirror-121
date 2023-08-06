#-*- coding:utf-8 -*-
def OsList(file):
    import os
    import re
    import glob
    filePath = (file)
    if file == '':
        print("file路径不能为空！ file The path cannot be empty!")
        return
    os.listdir(filePath)
    number = 0
    for i,j,k in os.walk(filePath):
        number += 1
        print(f"\n\t第{number}个文件夹",i,j,k)
    print(f"\n\n所有文件如上,共{number}个文件夹")
    print(f"\nAll files as above, a {number} total folder")
