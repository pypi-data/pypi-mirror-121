#coding:utf-8
import os
import shutil
def new(command, path, name, number, Suffix=''):
    Creation_time="2021/8/30"
    """NEW Folder"""
    if command == 'n':
        path_new = path
        name_new = name
        number_new = number
        try:
            po = 0
            if int(number) > int(1):
                print("When the file is repeated, a number is added after it")
                for i in range(int(number_new)):
                    if int(i) == int(0):
                        os.makedirs(path_new+name_new)
                    if int(i) >= int(1):
                        os.makedirs(path_new+name_new+str(i))
                    po += 1
                    print(f"The first{po} Name is {name_new}")
                print("success!")
            if int(number_new) <= 1:
                os.makedirs(path_new+name_new)
                print(f"The first{number_new} Name is {name_new}")
            print("success!")
        except:
            print("FileExistsError: The folder already exists and cannot be created. Please change the file name")
            print("FileExistsError: 文件夹已存在无法创建请更换文件名")
    """NEW File"""
    if command == 'n_file':
        path_file = path
        name_file = name
        number_file = number
        Suffix_file = Suffix
        if int(number_file) > int(1):
            print("When the file is repeated, a number is added after it")
            for r in range(int(number_file)):
                if int(r) == int(0):
                    new_files = open(f'{path_file}' f"{name_file}" + str(Suffix_file),"a")
                    new_files.write("")
                    new_files.close()
                if int(r) > int(1):
                    new_files = open(f'{path_file}' f"{name_file}{r}" + str(Suffix_file),"a")
                    new_files.write("")
                    new_files.close()
                print(f"The first{r} Name is {name_file}")
            print("success!")
        if int(number_file) == int(1):
            new_files = open(f'{path_file}' f"{name_file}" + str(Suffix_file),"a")
            new_files.write("")
            new_files.close()
            print(f"The first{number_file} Name is {name_file}{Suffix_file}")
            print("success!")

def new_del(command, path):
    import shutil
    Creation_time="2021/8/30"
    """del File"""
    if command == 'del':
        path_del = path
        #name_del = name
        try:
            os.remove(f'{path_del}')
            print(f"{name_del} File deleted !")
        except:
            print(f"file {path_del} does not exist !")
    if command == 'del_folder': 
        path_folder = path
        #name_folder = name
        try:
            shutil.rmtree(f'{path_folder}')
            print(f"Deleted folder{path_folder} ！")
        except:
            print(f"NO {path_folder} folders !")
def new_input(file, message=''):
    Creation_time="2021/8/30"
    input_message = message
    input_file = file
    try:
        input_file = open(f"{input_file}","w")
        input_file.write(input_message)
        input_file.flush()
        print("Entered successfully !")
    except:
        print(f"file {input_file} does not exist!")

def new_print(path):
    Creation_time="2021/8/30"
    try:
        print_wj = open(path, 'r', encoding='utf-8')
        print_sc = print_wj.read()
        print(print_sc)
        print_wj.close()
    except:
        print(f"Not{path} file !")

def new_add(path, message=''):
    try:
        add = open(path, 'a')
        add.write(f'\n{message}')
        add.close()
    except:
        print("Not {path} file !")

def filename(file, name):
    Creation_time="2021/8/30"
    try:
        file_new = file
        file_name = name
        os.rename(file_new,file_name)
        print("重命名成功！")
        print(f"文件{file_new} 重命名为 {name} ！")
        print("Rename succeeded!")
        print(f"Rename succeeded! File {file_new} renamed {name} !")
    except:
        print(f"错误！你可能输入了无效路径，或者路径为空！你的路径为：{file_new}")
        print(f"Wrong! You may have entered an invalid path, or the path is empty! Your path is: {file_new}")

def move(path, file):
    Creation_time="2021/8/30"
    try:
        shutil.move(path,file)
        print(f"成功 将 {path} 移动至 {file}")
        print(f"Successfully moved {path} to {file}")
    except PermissionError:
        print("拒绝访问")
        print("access denied")
    except:
        print(f"没有 {file} 这个路径！")
        print(f"There is no {file} this path!")
    else:
        if not os.path.isfile(path):
            print(f"没有 {path} 路径！")
            print(f"No {path} path!")
            #shutil.move(path,file)

def copyfor(path):
    Creation_time="2021/9/1"
    for l,k,j in os.walk(path):
        print(l,k,j)

def copy(cmd, paths, file, number):
    Creation_time="2021/9/1"
    if cmd == 'file':
        shutil.copyfile(paths,file)
        print(f"成功 将{paths} 复制到 {file}")
        print(f"Successfully copied {paths} to {file}")
    if cmd == 'copy':
        shutil.copy(paths,file)
        print(f"成功将 {paths} 复制到 {file}")
        print(f"Successfully copied {paths} to {file}")
    if cmd == 'tree':
        if int(number) > 1:
            for i in range(int(number)):
                if int(i) == 0:
                    shutil.copytree(paths,file)
                    print(f"创建文件夹{file} 将{paths}复制进去")
                    print(f"Create a folder {file} and copy {paths} into it")
                else:
                    shutil.copytree(paths,file+f"{i}")
                    print(f"创建文件夹{file} 将{paths}{i}复制进去")
                    print(f"Create a folder {file} and copy {paths}{i} into it")
        if int(number) <= 1:
            shutil.copytree(paths,file)
            print(f"创建文件夹{file} 将{paths}复制进去")
            print(f"Create a folder {file} and copy {paths} into it")
#try
