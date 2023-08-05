#coding:gbk
import os

class openfile:
    def __init__(self,name, file, cmd, coding, message=''):
        self.name = name
        self.file = file
        self.cmd = cmd
        self.message = message
        self.coding = coding

    def fileopen(self):
        if self.cmd == 'help':
            helps = ("访问模式	说明\n"\
            "\tr	以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。\n"\
            "\tw	打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。\n"\
            "\ta	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。\n"\
            "\trb	以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。\n"\
            "\twb	以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。\n"\
            "\tab	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。\n"\
            "\tr+	打开一个文件用于读写。文件指针将会放在文件的开头。\n"\
            "\tw+	打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。\n"\
            "\ta+	打开一个文件用于读写，如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果改文件不存在，创建新文件用于读写。\n"\
            "\trb+	以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头\n"\
            "\twb+	以二进制格式打开一个文件用于读写。如果改文件已存在则会覆盖。如果改文件不存在，创建新文件。\n"\
            "\tab+	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果改文件不存在，创建新文件用于读写。\n"\
                 )
            print(helps)
            return
        self.name = open(self.file,f'{self.cmd}',encoding=f'{self.coding}')
        if self.message == '':
            return
        else:
            self.name.write(f"{self.message}")
            print(f'write {self.message}')
            self.name.close()

    def read(self):
        #openfile(f'{self.name}', f'{self.file}', 'r', f'{self.coding}')
        andre = self.name.read()
        print(andre)
    
    def readlines(self):
        andli = self.name.readlines()
        print(andli)
    def readiine(self):
        andi = self.name.readline()
        print(andi)
