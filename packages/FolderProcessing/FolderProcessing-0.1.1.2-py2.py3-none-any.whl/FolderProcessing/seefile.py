#coding:gbk

import os

def seefile(path, file, cmd=''):
    for root,dirs,files in os.walk(path+':/',topdown=True):
        if cmd == 'Y' or cmd == 'y':
            print(root)
        else:
            pass
        if file in files:
            print(root+f"\{file}")
            break
        else:
            pass

def seeSuffix(path, suffix):
    for i,j,k in os.walk(path+"://"):
        for file in k:
            if file.endswith(suffix):
                print(os.path.join(i,file))
