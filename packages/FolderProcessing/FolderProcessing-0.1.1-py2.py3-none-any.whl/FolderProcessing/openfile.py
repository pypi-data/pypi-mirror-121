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
            helps = ("����ģʽ	˵��\n"\
            "\tr	��ֻ����ʽ���ļ����ļ���ָ�뽫������ļ��Ŀ�ͷ������Ĭ��ģʽ��\n"\
            "\tw	��һ���ļ�ֻ����д�롣������ļ��Ѵ������串�ǡ�������ļ������ڣ��������ļ���\n"\
            "\ta	��һ���ļ�����׷�ӡ�������ļ��Ѵ��ڣ��ļ�ָ�뽫������ļ��Ľ�β��Ҳ����˵���µ����ݽ��ᱻд�뵽��������֮��������ļ������ڣ��������ļ�����д�롣\n"\
            "\trb	�Զ����Ƹ�ʽ��һ���ļ�����ֻ�����ļ�ָ�뽫������ļ��Ŀ�ͷ������Ĭ��ģʽ��\n"\
            "\twb	�Զ����Ƹ�ʽ��һ���ļ�ֻ����д�롣������ļ��Ѵ������串�ǡ�������ļ������ڣ��������ļ���\n"\
            "\tab	�Զ����Ƹ�ʽ��һ���ļ�����׷�ӡ�������ļ��Ѵ��ڣ��ļ�ָ�뽫������ļ��Ľ�β��Ҳ����˵���µ����ݽ��ᱻд�뵽��������֮��������ļ������ڣ��������ļ�����д�롣\n"\
            "\tr+	��һ���ļ����ڶ�д���ļ�ָ�뽫������ļ��Ŀ�ͷ��\n"\
            "\tw+	��һ���ļ����ڶ�д��������ļ��Ѵ������串�ǡ�������ļ������ڣ��������ļ���\n"\
            "\ta+	��һ���ļ����ڶ�д��������ļ��Ѵ��ڣ��ļ�ָ�뽫������ļ��Ľ�β���ļ���ʱ����׷��ģʽ��������ļ������ڣ��������ļ����ڶ�д��\n"\
            "\trb+	�Զ����Ƹ�ʽ��һ���ļ����ڶ�д���ļ�ָ�뽫������ļ��Ŀ�ͷ\n"\
            "\twb+	�Զ����Ƹ�ʽ��һ���ļ����ڶ�д��������ļ��Ѵ�����Ḳ�ǡ�������ļ������ڣ��������ļ���\n"\
            "\tab+	�Զ����Ƹ�ʽ��һ���ļ�����׷�ӡ�������ļ��Ѵ��ڣ��ļ�ָ�뽫������ļ��Ľ�β��������ļ������ڣ��������ļ����ڶ�д��\n"\
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
