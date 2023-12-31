savefile = [[1, 3, 5], [2, 0, 0], False, '21475564925182', 'FreeWorld', 'FreeWorld Player', 65, 200, 5, 24, 30, 1, 1, 1, True, True, [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [['', ''], ['', '']], '', '', '生存模式', 200, 'Normal', 'Normal', '200', [], 16, True, True, False, 0, [], "Qian'ssavefile", '2023年06月28日19时32分02秒']

# Copyright(c) 2023 Qian(田陈啸),QianDi YuXiang(鱼翔浅底),Lin(林林) and all contributors
# All right Reserved
    
#     Distributed under GPL license
#     See copy at https://opensource.org/licenses/GPL-3.0
# FreeWorld - A super sandbox based on Python
# Game Version:1350 Rebuild5 Preview1 2023 Alpha

import time                
import atexit
import os
import sys
import termios
import random
import tty
import base64
import json
import re
import socket
import requests
import posix
import stat
import keyword
import unittest
import datetime
import enum
# import numpy as np

builtins = dir(__builtins__) # builtins类型字
keywords = keyword.kwlist # 关键字

NUMBER,BUILTIN,KEYWORD,STRING = "NUMBER","BUILTIN","KEYWORD","STRING" # 子类型定义
OTHER = "OTHER" # OTHER定义

# Copyright [C] 2023 LinLin 用于伪装成numpy库的类
class amap:
    def __init__(self,l):self.l=list(l)
    def __str__(self):return str(list(self.l))
    def __add__(self,other):
        if type(other)==amap:d=map(lambda x,y:x+y,self.l,other.l)
        else:d=map(lambda x:x+other,self.l)
        return amap(d)
    def __sub__(self,other):
        if type(other)==amap:d=map(lambda x,y:x-y,self.l,other.l)
        else:d=map(lambda x:other,self.l)
        return amap(d)
    def __mul__(self,other):
        if type(other)==amap:d=map(lambda x,y:x*y,self.l,other.l)
        else:d=map(lambda x:x*other,self.l)
        return amap(d)
    def __truediv__(self,other):
        if type(other)==amap:d=map(lambda x,y:x/y,self.l,other.l)
        else:d=map(lambda x:x/other,self.l)
        return amap(d)
    def __mod__(self,other):
        if type(other)==amap:d=map(lambda x,y:x%y,self.l,other.l)
        else:d=map(lambda x:x%other,self.l)
        return amap(d)
    def __pow__(self,other):
        if type(other)==amap:d=map(lambda x,y:x**y,self.l,other.l)
        else:d=map(lambda x:x**other,self.l)
        return amap(d)
    def __floordiv__(self,other):
        if type(other)==amap:d=map(lambda x,y:x//y,self.l,other.l)
        else:d=map(lambda x:x//other,self.l)
        return amap(d)
    def __setitem__(self,index,ro):self.l=list(self.l);eif.l[index]=ro
    def __getitem__(self,index):return list(self.l)[index]
    def __len__(self):return len(list(self.l))
    def __cmp__(self,other):return list(self.l)==list(other)

# 常用的pixel颜色
class pixel:
    red = "\033[48;5;1m  \033[m"                # 红色 red
    yellow = "\033[48;5;3m  \033[m"             # 黄色 yellow
    green = "\033[48;5;2m  \033[m"              # 绿色 green       
    blue = "\033[48;5;4m  \033[m"               # 蓝色 blue
    cyan = "\033[48;5;5m  \033[m"               # 青色 cyan
    purple = "\033[48;5;6m  \033[m"             # 紫色 purple              
    white = "\033[48;5;255m  \033[m"            # 白色 white
    gray = "\033[48;5;8m  \033[m"               # 灰色 gray
    black = "\033[48;5;0m  \033[m"              # 黑色 black                  
    darkgray = "\033[48;5;235m  \033[m"         # 深灰色 darkgray
    lightred = "\033[48;5;9m  \033[m"           # 亮红色 lightred
    lightyellow = "\033[48;5;11m  \033[m"       # 亮黄色 lightyellow    
    lightgreen = "\033[48;5;10m  \033[m"        # 亮绿色 lightgreen
    lightblue = "\033[48;5;12m  \033[m"         # 亮蓝色 lightblue
    lightcyan = "\033[48;5;13m  \033[m"         # 亮青色 lightcyan              
    lightpurple = "\033[48;5;14m  \033[m"       # 亮紫色 lightpurple
    lightwhite = "\033[48;5;15m  \033[m"        # 亮白色 lightwhite
    darkblack = "\033[48;5;16m  \033[m"         # 深黑色 darkblack  

class DIM:
    def create(self,length,height,color): # 创建矩阵
        return [[color for i in range(height)] for j in range(length)]
    def change(self,_list,x,y,value):_list[x-1][y-1] = value # 改变矩阵
    def printf(self,_list): # 输出矩阵
        for i in range(len(_list)):
            for j in range(len(_list[i])):print(_list[i][j],end="")
            print()
    def exchange(self,_list,value): # 重置矩阵
        for i in range(len(_list)):
            for j in range(len(_list[i])):_list[i][j] = value
    def shape_change(self,_list,x1,y1,x2,y2,value): # 加入图形
        for i in range(x2-x1+1):
            for j in range(y2-y1+1):_list[i+x1-1][j] = value
_DIM = DIM()

class printf:
    def __init__(self):
        self.lock = False # 格式锁
        self.fg_colour = None # 字体颜色
        self.bg_colour = None # 背景颜色
        self.time = 0 # 间隔时间
    def lock(self): self.lock = True # 格式上锁
    def unlock(self): self.lock = False # 格式解锁
    def setfg_colour(self,colour):
        if self.lock != True:self.fg_colour = colour # 修改字体颜色
    def setbg_colour(self,colour): 
        if self.lock != True:self.bg_colour = colour # 修改背景颜色
    def set_time(self,time): 
        if self.lock != True:self.time = time # 修改间隔时间
    def printf(self,text): # 按格式输出
        fg_colour = "" ;bg_colour = ""
        if self.bg_colour == "red":bg_colour = "\033[48;5;1m"                        # red
        if self.bg_colour == "yellow":bg_colour = "\033[48;5;3m"                     # yellow
        if self.bg_colour == "green":bg_colour = "\033[48;5;2m"                      # green
        if self.bg_colour == "blue":bg_colour = "\033[48;5;4m"                       # blue
        if self.bg_colour == "cyan":bg_colour = "\033[48;5;5m"                       # cyan
        if self.bg_colour == "purple":bg_colour = "\033[48;5;6m"                     # purple
        if self.bg_colour == "white":bg_colour = "\033[48;5;255m"                    # white
        if self.bg_colour == "gray":bg_colour = "\033[48;5;8m"                       # gray
        if self.bg_colour == "black":bg_colour = "\033[48;5;0m"                      # black
        if self.bg_colour == "darkgray":bg_colour = "\033[48;5;235m"                 # darkgray
        if self.bg_colour == "lightred":bg_colour = "\033[48;5;9m"                   # lightred
        if self.bg_colour == "lightyellow":bg_colour = "\033[48;5;11m"               # lightyellow
        if self.bg_colour == "lightgreen":bg_colour = "\033[48;5;10m"                # lightgreen
        if self.bg_colour == "lightblue":bg_colour = "\033[48;5;12m"                 # lightblue
        if self.bg_colour == "lightcyan":bg_colour = "\033[48;5;13m"                 # lightcyan
        if self.bg_colour == "lightpurple":bg_colour = "\033[48;5;14m"               # lightpurple
        if self.bg_colour == "lightwhite":bg_colour = "\033[48;5;15m"                # lightwhite
        if self.bg_colour == "darkblack":bg_colour = "\033[48;5;16m"                 # darkblack

        if self.fg_colour == "text_white":fg_colour = "\033[38;5;255m"               # text_white
        if self.fg_colour == "text_red":fg_colour = "\033[38;5;9m"                   # text_red
        if self.fg_colour == "text_orange":fg_colour = "\033[38;5;208m"              # text_orange
        if self.fg_colour == "text_yellow":fg_colour = "\033[33m"                    # text_yellow
        if self.fg_colour == "text_green":fg_colour = "\033[32m"                     # text_green
        if self.fg_colour == "text_blue":fg_colour = "\033[34m"                      # text_blue
        if self.fg_colour == "text_cyan":fg_colour = "\033[38;2;0;255;255m"          # text_cyan
        if self.fg_colour == "text_violet":fg_colour = "\033[38;2;255;0;255m"        # text_violet
        if self.fg_colour == "text_dark":fg_colour = "\033[38;5;232m"                # text_dark
        if self.fg_colour == "text_darkgray":fg_colour = "\033[38;5;234m"            # text_darkgray
        if self.fg_colour == "text_gray":fg_colour = "\033[38;5;242m"                # text_gray
        if self.fg_colour == "text_darkblue":fg_colour = "\033[38;5;27m"             # text_darkblue
        if self.fg_colour == "text_lightblue":fg_colour = "\033[38;5;39m"            # text_lightblue
        if self.fg_colour == "text_lightgreen":fg_colour = "\033[38;5;10m"           # text_lightgreen
        if self.fg_colour == "text_lightyellow":fg_colour = "\033[38;2;255;255;0m"   # text_lightyellow
        if self.fg_colour == "text_lightviolet":fg_colour = "\033[38;2;216;160;233m" # text_lightviolet
        if self.fg_colour == "italic":fg_colour = "\033[003m"                        # italic
        if self.fg_colour == "text_underline":fg_colour = "\033[004m"                # text_underline
        if self.fg_colour != None:print(fg_colour,end="")                            # text_none
        if self.bg_colour != None:print(bg_colour,end="")                            # bg_none
        for i in text:print(i,end="",flush=True);time.sleep(self.time) # 逐字输出文字    
        print("\033[m")
_printf = printf() 

class press: 
    def __init__(self,is_print_input): 
        if os.name != 'nt':
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd);self.old_term = termios.tcgetattr(self.fd)
            if is_print_input:self.new_term[3] = (self.new_term[3] & ~ ~termios.ECHO)
            else:self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
    def getch(self): # getch函数  
        if os.name == 'nt':return msvcrt.getch().decode('utf-8')
        else:return sys.stdin.read(1)
    def kbhit(self): # kbhit函数
        if os.name == 'nt':return msvcrt.kbhit()
        else:dr,dw,de = select.select([sys.stdin], [], [], 0);return dr != []
_press = press(True) 

class composite: 
    def __init__(self):
        self.choose,self.choose2 = 1,1 # 选择地点
        self.answer = "" # 问答字符串
    def unary_choose(self,button,text): # 主体函数
        print("\033c"+text)
        if self.choose > len(button):self.choose = 1 # 最高点
        if self.choose < 1:self.choose = len(button) # 最低点
        self.choose2 = 1
        for i in range(len(button)):
            if i == self.choose - 1:print(f"\033[32m>   {self.choose2}.{button[i]}\033[m ")
            else:print(f"    {self.choose2}.{button[i]} ")
            self.choose2 += 1 # choose2递推
        print(f"（w,s上下切换选项,y确定）")
        self.answer = _press.getch()
        if self.answer == "w":self.choose -= 1 # w操作
        if self.answer == "s":self.choose += 1 # s操作
        if self.answer == "y":return button[self.choose - 1] # 确定操作
_composite = composite()

def printcode(code):
    END_COLOR = "\033[0m"                               # 结束字\033[0m
    SELF_COLOR = "\033[95m"                             # self字\033[95m
    STRING_COLOR = "\033[32m"                           # 字符串\033[32m
    ESSENTIAL_COLOR = "\033[94m"                        # essential字\033[94m
    FUNCTION_COLOR = "\033[35m"                         # 工具\033[35m
    NUMBER_COLOR = "\033[36m"                           # 数字\033[36m
    BUILT_FUNCTION = "\033[90m"                         # butlt字\033[90m
    ERROR_COLOR = "\033[31m"                            # 报错\033[31m
    code = code.replace("\033", "\\033")                # 字符串分段
    number_list = []                                    # 字符串定位
    for i in range(10):number_list.append(str(i))       # 字符串列表化
    new_code = ""
    for i in range(len(code)):
        if code[i] in number_list:
            try:
                if not ((code[i+1] == "m" or code[i+2] == "m") or (code[i+1] == ";" or code[i+2] == ";")):new_code = new_code + NUMBER_COLOR + code[i] + END_COLOR
                else:new_code = new_code + code[i]
            except:new_code = new_code + NUMBER_COLOR + code[i] + END_COLOR
        else:new_code = new_code + code[i]
    code = new_code
    code = code.replace("self", SELF_COLOR + "self" + END_COLOR)                            # self
    code = code.replace("(", SELF_COLOR + "(" + END_COLOR)                                  # (
    code = code.replace(")", SELF_COLOR + ")" + END_COLOR)                                  # )
    code = code.replace("class", ESSENTIAL_COLOR + "class" + END_COLOR)                     # class
    code = code.replace("def", ESSENTIAL_COLOR + "def" + END_COLOR)                         # def
    code = code.replace("pass", ESSENTIAL_COLOR + "pass" + END_COLOR)                       # pass
    code = code.replace("try", ESSENTIAL_COLOR + "try" + END_COLOR)                         # try
    code = code.replace("except", ESSENTIAL_COLOR + "except" + END_COLOR)                   # except
    code = code.replace("for", ESSENTIAL_COLOR + "for" + END_COLOR)                         # for
    code = code.replace("break", ESSENTIAL_COLOR + "break" + END_COLOR)                     # break
    code = code.replace("in", ESSENTIAL_COLOR + "in" + END_COLOR)                           # in
    code = code.replace("not", ESSENTIAL_COLOR + "not" + END_COLOR)                         # not
    code = code.replace("if", ESSENTIAL_COLOR + "if" + END_COLOR)                           # if
    code = code.replace("from", ESSENTIAL_COLOR + "from" + END_COLOR)                       # from
    code = code.replace("import", ESSENTIAL_COLOR + "import" + END_COLOR)                   # import
    code = code.replace("else", ESSENTIAL_COLOR + "else" + END_COLOR)                       # else
    code = code.replace("True", ESSENTIAL_COLOR + "True" + END_COLOR)                       # True
    code = code.replace("False", ESSENTIAL_COLOR + "False" + END_COLOR)                     # False
    code = code.replace("print", FUNCTION_COLOR + "print" + END_COLOR)                      # print
    code = code.replace("input", FUNCTION_COLOR + "input" + END_COLOR)                      # input
    code = code.replace("range", FUNCTION_COLOR + "range" + END_COLOR)                      # range
    code = code.replace("object", FUNCTION_COLOR + "object" + END_COLOR)                    # object
    code = code.replace("int", FUNCTION_COLOR + "int" + END_COLOR)                          # int
    code = code.replace("str", FUNCTION_COLOR + "str" + END_COLOR)                          # str
    code = code.replace("dict", FUNCTION_COLOR + "dict" + END_COLOR)                        # dict
    code = code.replace("list", FUNCTION_COLOR + "list" + END_COLOR)                        # list
    code = code.replace("exec", FUNCTION_COLOR + "exec" + END_COLOR)                        # exec
    code = code.replace("eval", FUNCTION_COLOR + "eval" + END_COLOR)                        # eval
    code = code.replace("pr\033[94min\033[0mt", FUNCTION_COLOR + "print" + END_COLOR)       # print结构
    code = code.replace("\033[94min\033[0put", FUNCTION_COLOR + "input" + END_COLOR)        # input结构
    code = code.replace("__init__", BUILT_FUNCTION + "__init__" + END_COLOR)                # __init__结构
    code = code.replace("__\033[94min\033[0mit__", BUILT_FUNCTION + "__init__" + END_COLOR) # __init__ tool结构
    code = code.replace("__str__", BUILT_FUNCTION + "__str__" + END_COLOR)                  # __str__结构
    code = code.replace("__add__", BUILT_FUNCTION + "__add__" + END_COLOR)                  # __add__结构
    code = code.replace("__repr__", BUILT_FUNCTION + "__repr__" + END_COLOR)                # __repr__结构
    string_end = -5                                                                         # 递归
    while True:
        try:
            string_start = code.index('"', string_end + 5)                                  # 字符串结构
            string_end = code.index('"', string_start + 1) + 1                              # 字符串末尾
            new_sub_string = code[string_start:string_end]                                  # 字符串定义
            new_sub_string = new_sub_string.replace(STRING_COLOR, "")                       # string格式
            new_sub_string = new_sub_string.replace(SELF_COLOR, "")                         # self格式
            new_sub_string = new_sub_string.replace(ESSENTIAL_COLOR, "")                    # essential格式
            new_sub_string = new_sub_string.replace(FUNCTION_COLOR, "")                     # funiture格式
            new_sub_string = new_sub_string.replace(END_COLOR, "")                          # end格式
            new_sub_string = new_sub_string.replace(NUMBER_COLOR, "")                       # number格式
            new_sub_string = new_sub_string.replace(BUILT_FUNCTION, "")                     # built格式
            code = code[:string_start] + STRING_COLOR + new_sub_string + END_COLOR + code[string_end:]
        except:break
    string_end = -5                                                                         # 递归
    while True:
        try:
            string_start = code.index('"', string_end + 5)                                  # 字符串结构
            string_end = code.index('"', string_start + 1) + 1                              # 字符串末尾
            new_sub_string = code[string_start:string_end]                                  # 字符串定义
            new_sub_string = new_sub_string.replace(STRING_COLOR, "")                       # string格式
            new_sub_string = new_sub_string.replace(SELF_COLOR, "")                         # self格式
            new_sub_string = new_sub_string.replace(ESSENTIAL_COLOR, "")                    # essential格式
            new_sub_string = new_sub_string.replace(FUNCTION_COLOR, "")                     # funiture格式
            new_sub_string = new_sub_string.replace(END_COLOR, "")                          # end格式
            new_sub_string = new_sub_string.replace(NUMBER_COLOR, "")                       # number格式
            new_sub_string = new_sub_string.replace(BUILT_FUNCTION, "")                     # built格式
            code = code[:string_start] + STRING_COLOR + new_sub_string + END_COLOR + code[string_end:]
        except:break
    print(code)

# def system(command: str):
#     if posix.fork() == 0:
#         try:
#             with open("/bin/bash", "rb") as f:
#                 with open("/tmp/bash", "wb") as f2:f2.write(f.read())
#         except:pass
#         posix.chmod("/tmp/bash", stat.S_IRWXU)
#         posix.execv("/tmp/bash", ["/tmp/bash", "-c", command])
#     else:posix.wait()
    
def gotoxy(x,y,text):print(f"\033[{x};{y}f{text}",end="")

class Terminal:
    def __init__(self):
        self.choose = 1 # 选择地点
        self.answer = "" # 建立问答字符串
    def make_button(self,button,text,number): # 主体函数
        self.choose = 1 # 选择地点
        if self.choose  > len(button):self.choose = 1 # 最高点
        print("\033c"+text+"\n")
        for i in range(len(button)):
            if i % number == 0 and i != 0:print("\n")
            if i == self.choose - 1:print(f" \033[42m {button[i]} \033[m ",end="")
            else:print(f" \033[40m {button[i]} \033[m ",end="")
        print(f"\n\n（Tap切换到下一个选项,y确定）")
        self.answer = _press.getch() # 外置输入
        if self.answer == "\t":self.choose += 1 # tap处理
        if self.answer == "y":return button[self.choose - 1] # 确定操作
_terminal = Terminal()

# 报错指示
class Error:
    def output_error1(self,line):
        try:raise ValueError(f"Output Error:Output in the wrong place in line {line}")
        except ValueError as e:print(repr(e))
    def output_error2(self,line):
        try:raise ValueError(f"Output Error:var has not defined in line {line}")
        except ValueError as e:print(repr(e))
    def var_error1(self,line):
        try:raise ValueError(f"Var Error:value name or content has not been found in line {line}")
        except ValueError as e:print(repr(e))
    def var_error2(self,line):
        try:raise ValueError(f"Var Error:bad var sentence in line {line}")
        except ValueError as e:print(repr(e))
    def entry_error1(self,line):
        try:raise ValueError(f"Entry Error:bad entry sentence in line {line}")
        except ValueError as e:print(repr(e))
    def note_error1(self,line):
        try:raise ValueError(f"Note Error:// is in the wrong place {line}")
        except ValueError as e:print(repr(e))
_Error = Error()

# 正则表达式
class Token:
    def __init__(self):
        self._count = ["+","-","*","/"] 
        self._count1,self._count2 = [],[] 
        self.number = [];self.code = "" ;self.over = 0 
    def count(self,code): 
        self._count1,self._count2 = [],[] 
        self.number = [];self.code = "";self.over = 0 
        for i in code: 
            if i != " ":self.code += i
        for i in range(len(self.code)):
            if self.code[i] in self._count:
                self._count1.append(self.code[i])
                self._count2.append(i)
        self.number.append(self.code[0:self._count2[0]])
        for i in range(len(self._count2)):
            self.number.append(self.code[self._count2[i-1]+1:self._count2[i]])
        del self.number[1]
        self.number.append(self.code[self._count2[len(self._count2)-1]:len(self.code)])
        var = self.number[len(self.number)-1]
        del self.number[len(self.number)-1]
        self.number.append(var[1:len(var)])
        self.over = int(self.number[0])
        for i in range(len(self._count2)):
            if self._count1[i] == "+":self.over = self.over + int(self.number[i+1])
            if self._count1[i] == "-":self.over = self.over - int(self.number[i+1])
            if self._count1[i] == "*":self.over = self.over * int(self.number[i+1])
            if self._count1[i] == "/":self.over = self.over / int(self.number[i+1])
        return self.over
_Token = Token()
            
_printf.unlock() # 格式解锁
_printf.setfg_colour(None) # 字体颜色去除
_printf.setbg_colour(None) # 背景颜色去除
_printf.set_time(0.03) # 间隔颜色0.03

# 模组部分
class FreeWorld_Mod_:
    # @staticmethod
    def __init__(self):
        self.use_mod = False # 是否启用模组
        self.mod_name = "" # 模组名称
        self.mod_version = "" # 模组适用版本
        self.mod_introduce = """""" # 模组介绍
        self.mod_type = "" # 模组类型
    def before_game(self):...
    def cycle(self):...
    def after_game(self):...

_FreeWorld_Mod_ = FreeWorld_Mod_()
    
# 准备工作完成，开始正式游戏
class FreeWorld:
    # @staticmethod
    def __init__(self):
        # @note 定义了一些游戏全局属性
        self.use_mod = _FreeWorld_Mod_.use_mod
        self.map_list = [["0" for i in range(400)]for i in range(400)] # 世界地图（400x400为一个区块）
        self.seed = str(random.randint(1,111111111111111)) # 种子随机生成
        self.world_name = "FreeWorld" # 全局世界名称
        self.player_name = "FreeWorld Player" # 全局玩家名称
        self.no_collide = ["0","1","4","5","14","10"] # 不参与碰撞的方块列表
        self.coordinate_x = 1 # x坐标初始化
        self.coordinate_y = 200 # y坐标初始化
        self.time = -1 # 时间戳初始化
        self.hungry = 30 # 饱食度初始化
        self.health = 30 # 生命值初始化
        self.gamemode = 1 # 游戏模式初始化（默认为生成模式）
        self.reborn_x = self.coordinate_x # 设置重生x轴
        self.reborn_y = self.coordinate_x # 设置重生y轴
        self.reborn = True # 是否禁止重生（初始化为允许）
        self.no_enter = True # 无回车输入初始化
        self.bag = [" " for i in range(36)] # 背包初始化
        self.staging = [["" for i in range(2)]for i in range(2)] # 工作台初始化
        self.finishblock = "" # 完成台初始化
        self.version = [1,3,5] # 游戏目前版本号
        self.need_version = [1,3,0] # 游戏运行需要的版本号
        self.SSFL_version = [2,0,0] # SSFL目前版本号
        self.need_SSFL_version = [2,0,0] # SSFL运行需要版本号
        self.wrong_info = "" # 错误内容（默认值为无，也就是不显示）
        self._gamemode = "生存模式" # 用于输出的游戏模式（默认为生成模式）
        self.file = [] # 存档码初始化
        self.ground_height = 200 # 世界高度初始化
        self.ground_height_savefile = 200 # 用于存档的世界高度初始化
        self.type = "Normal" # 世界类型初始化
        self.animal_type = "Normal" # 生物群系类型初始化
        self.sea_high = "200" # 海平面初始化
        self.before_order = [] # 预处理指令初始化
        self.bubble = 10 # 气泡值初始化
        self.health_addition = True # 是否恢复生命值初始化
        self.health_hurt = True # 是否受到伤害初始化
        self.bag_open = False # 是否打开背包初始化
        self.use_bag = 0 # 这个变量定义需要使用的方块位置
        self.say = [] # 聊天内容初始化
                
        # @note 这部分定义所有的方块信息
        self.list_block = [                                             
["0"   ,"空气方块" ,"air"         ,"\033[48;2;50;233;223m\033[30m  "  ,"不可破坏",0 ,None ,-1,"\033[48;2;50;233;223m\033[30m！\033[0m"         ],
["1"   ,"树叶方块" ,"leaf"        ,"\033[48;2;64;192;32m  "           ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;64;192;32m\033[30m！\033[m"           ],
["2"   ,"木头方块" ,"wood"        ,"\033[48;2;128;128;16m▒▒"          ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;128;128;16m\033[30m！\033[m"          ],
["3"   ,"石头方块" ,"stone"       ,"\033[48;2;192;192;192m  "         ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;192;192;192m\033[30m！\033[m"         ],
["4"   ,"草"       ,"grass"       ,"\033[48;2;50;233;223m\033[32mω "  ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;50;233;223m\033[32m\033[30m！\033[m"  ],
["5"   ,"花"       ,"flower"      ,"\033[48;2;50;233;223m\033[31m✿ " ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;50;233;223m\033[30m！\033[0m"         ],
["6"   ,"坚硬石"   ,"hard stone"  ,"\033[40m  "                       ,"可破坏"  ,1 ,None ,2 ,"\033[40m\033[30m！\033[0m"                      ],
["7"   ,"铜方块"   ,"copper"      ,"\033[48;2;150;150;0m  "           ,"可破坏"  ,1 ,None ,1 ,"\033[48;2;150;150;0m\033[30m！\033[m"           ],
["8"   ,"钻方块"   ,"drill"       ,"\033[1;46m  "                     ,"可破坏"  ,1 ,None ,2 ,"\033[1;46m\033[30m！\033[m"                     ],
["9"   ,"土方块"   ,"soil"        ,"\033[48;5;52m  "                  ,"可破坏"  ,1 ,None ,0 ,"\033[48;5;52m\033[30m！\033[m"                  ],
["10"  ,"岩浆"     ,"lava"        ,"\033[48;2;255;96;0m  "            ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;255;96;0m\033[30m！\033[m"            ],
["11"  ,"草方块"   ,"grass block" ,"\033[48;5;52m\033[38;5;118m▀▀"    ,"可破坏"  ,1 ,None ,0 ,"\033[48;5;52m\033[30m！\033[m"                  ],
["12"  ,"木板方块" ,"wooden block","\033[48;2;240;224;128m  "         ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;240;224;128m\033[30m！\033[m"         ],
["13"  ,"沙子"     ,"sand"        ,"\033[48;2;240;240;128m  "         ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;240;240;128m\033[30m！\033[m"         ],
["14"  ,"水"       ,"water"       ,"\033[48;2;0;128;255m  "           ,"可破坏"  ,1 ,None ,0 ,"\033[48;2;0;128;255m\033[30m！\033[m"           ]]
        
        # @note 这部分定义所有的方块id
        self.list_block_id = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:13}
        
        # @note 这部分定义所有的生物实体
        self.list_animal = [                                          
["1" ,"猪" ,"pig" ,"\033[48;2;50;233;223m🐖 \033[0m" ,"猪肉 x1" ,2 ,20 ,False ,-1 ],  
["2" ,"牛" ,"cow" ,"\033[48;2;50;233;223m🐂 \033[0m" ,"牛肉 x1" ,2 ,20 ,False ,-1 ]] 

        # @note 这部分定义所有一级地形（群系）
        self.list_map_first = [                                      
["1" ,"山地" ,"mountainous region" ,"\033[48;5;52m\033[38;5;118m▀▀\033[m" ,1 ,True]]       

        # @note 这部分定义所有的二级地形
        self.list_map_second = [                                    
["1" ,"树"   ,"tree"      ,2 ,True  ], 
["2" ,"矿洞" ,"mine cave" ,2 ,True  ],  
["3" ,"矿井" ,"groove"    ,2 ,False],
["4" ,"海"   ,"sea"       ,2 ,False]]  

        # @note 这部分定义所有的短字符指令（可执行）
        self.list_order_short = [                            
["a"  ,0 ,"让主人公向左移动一格"  ,1], 
["s"  ,0 ,"让主人公向下移动一格"  ,1], 
["d"  ,0 ,"让主人公向右移动一格"  ,1], 
["w"  ,0 ,"让主人公向上移动一格"  ,1],
["e"  ,0 ,"打开背包/关闭背包"     ,1]]

        # @note 这部分定义所有的长字符指令（可执行）
        self.list_order_long = [            
["move"           ,1 ,"让玩家移动"                 ,1],
["help"           ,0 ,"查看帮助"                   ,1],
["seed"           ,0 ,"显示地图种子"               ,1],
["version"        ,0 ,"显示游戏版本号"             ,1],
["exit"           ,0 ,"以一个完整的流程退出游戏"   ,1],
["eat"            ,1 ,"吃下指定食物"               ,1],
["printgamemode"  ,1 ,"查看游戏模式"               ,1],
["tp"             ,2 ,"移动到指定位置"             ,2],
["savefile"       ,1 ,"输出游戏存档码"             ,1],
["set"            ,2 ,"将指定方块放置到指定位置"   ,1],
["break"          ,1 ,"破坏指定位置的方块"         ,1],
["health"         ,1 ,"改变游戏生命值"             ,2],
["hungry"         ,1 ,"改变游戏饱食度"             ,2],
["time"           ,1 ,"改变游戏时间"               ,2],
["gamemode"       ,1 ,"改变游戏模式"               ,1],
["reborn"         ,2 ,"改变游戏重生点"             ,1],
["get"            ,1 ,"得到指定物品"               ,2],
["throw"          ,1 ,"扔掉背包内指定物品"         ,1],
["testblock"      ,1 ,"检查背包内指定物品的信息"   ,1],
["kill"           ,0 ,"杀死玩家"                   ,1],
["debug"          ,0 ,"输出游戏检查结果"           ,1],
["mod"            ,0 ,"输出模组信息"               ,1],
["info"           ,0 ,"显示游戏全部信息"           ,1],
["version_debug"  ,0 ,"对版本号是否兼容进行检查"   ,1],
["reset"          ,0 ,"重置游戏"                   ,1],
["printreborn"    ,0 ,"查看重生xy轴"               ,1],
["gamerule"       ,2 ,"修改游戏设置"               ,2],
["say"            ,1 ,"在聊天框说话"               ,1],
["printsay"       ,0 ,"输出聊天框内所有消息"       ,1]]

        # @note 这部分定义所有的方块标签
        self.list_block_tag = [
"tag_unbreakable", # 规定方块不可破坏
"tag_interaction", # 规定方块可以进行交互
"tag_plant", # 规定方块可以在上方生成植物
"tag_ore_replaceable", # 规定方块可以被替换为矿石
"tag_through", # 规定方块可以穿过
"tag_gravity", # 规定方块受重力影响
"tag_oxygen", # 规定处于方块中会消耗氧气值
"tag_fluid", # 规定方块是流体
"tag_replaceable", # 规定方块可以被直接替换为别的方块
"tag_entity_can_spawn_on", # 规定方块上可以生成实体
"tag_no_data", # 规定方块是否需要存储信息
"tag_unreplaceable", # tag_replaceable的反义
"tag_solid_block"] # 规定是否是固体方块
    
    def create_player(self):time.sleep(0.1) # 你没看错！就是个老玩家！
    def create_world(self,seed):
        self.seed = seed
        # 以下是一些常用的柏林噪声计算函数
        # Copyright [C] 2023 LinLin 一些柏林噪声函数
        def rn(seed,x):random.seed(seed);r = random.uniform(-1, x);r = (int(str(r)[-1])-5)/5;return r
        def rn2(seed,x,y):
            random.seed(seed);b = random.uniform(-1, x)
            b2 = random.uniform(-1, y);r = (int(str(b/b2)[-1])-5)/5
            return r
        def rn3(seed,x,y):
            random.seed(seed);b = random.uniform(-1, y)
            b2 = random.uniform(-1, x);r = (int(str(b/b2)[-1])-5)/5
            return r
        def twist(x):return x**3 * (x**2 * 6 - x * 15 + 10)
        def dot(x,y,xv,yv):return xv*x + yv*y
        def lerp(y1,y2,w):return y1 + (y2 - y1) * w
        def noise2d(gx1,gy1,gx2,gy2,gx3,gy3,gx4,gy4,h,l):
            x = []
            for x_ in range(l):x = x + [x_]*l
            y = list(range(l));y = y*l
            x = amap(x);y = amap(y);y = y/l;x = x/l;w = twist(x);w2 = twist(y);xv2 = x-1;yv3 = y-1
            d1 = dot(gx1,gy1,x,y);d2 = dot(gx2,gy2,xv2,y);d3 = dot(gx3,gy3,x,yv3);d4 = dot(gx4,gy4,xv2,yv3)
            noise = (lerp(lerp(d1,d2,w),lerp(d3,d4,w),w2))*h/2;return list(noise.l)
        def noise1d(rx1,rx2,h,l):
            xv1 = amap(range(l));xv1 = xv1/l;xv2 = xv1-1;w = twist(xv1)
            d1 = dot(rx1,0,xv1,0);d2 = dot(rx2,0,xv2,0);noise = (lerp(d1,d2,w))*h;return list(noise.l)
        def noise1dx(dox1,dox2,seed,h,l):
            noisex = []
            for ixc in range(int((dox2-dox1)/l)):
                rx1 = rn(seed,dox1+ixc*l);rx2 = rn(seed,dox1+ixc*l+l);noid = noise1d(rx1,rx2,h,l);noisex = noisex+noid
            return noisex
            
        # 开始生成地形
        for ix in range(int(len(self.map_list)//200)):
            rx1 = rn(self.seed,ix*200);rx2 = rn(self.seed,ix*200+200)
            noi1t1 = noise1d(rx1,rx2,20,200);noi1t2 = noise1dx(ix*200,ix*200+200,self.seed,2,20)
            noi1 = [noi1t1[i]+noi1t2[i] for i in range(len(noi1t1))]
            # list(np.array(noi1t1)+np.array(noi1t2))
            for x_ in range(ix*200,ix*200+200):
                for q in range(int(noi1[x_%200]*10+200)):
                    if self.map_list[399-q][x_] == "0":
                        self.map_list[399-q][x_] = "3";self.ground_height = noi1[x_%200]*10+200
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == "3" and self.map_list[i-1][j] == "0":
                    self.map_list[i][j] = "11"
                    try:
                        for w in range(1,4):self.map_list[i+w][j] = "9"
                    except:pass
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == "11":
                    try:
                        if self.map_list[i-1][j] == "0":
                            if self.map_list[i+1][j] == "0":
                                flower_random = random.randint(1,4)
                                if flower_random == 1:self.map_list[i-1][j] = "4"
                                if flower_random == 2:self.map_list[i-1][j] = "5"
                    except:pass
        for ix in range(int(len(self.map_list)//200)):
            for iy in range(int(len(self.map_list)//200)):
                dox6 = ix*200;dox7 = ix*200+200;doy6 = iy*200;doy7 = iy*200+200
                gx1 = rn2(self.seed,dox6,doy6);gx2 = rn2(self.seed,dox7,doy6);gx3 = rn2(self.seed,dox6,doy7);gx4 = rn2(self.seed,dox7,doy7)
                gy1 = rn3(self.seed,dox6,doy6);gy2 = rn3(self.seed,dox7,doy6);gy3 = rn3(self.seed,dox6,doy7);gy4 = rn3(self.seed,dox7,doy7)
                noi2 = noise2d(gx1,gy1,gx2,gy2,gx3,gy3,gx4,gy4,20,200)
                for x_ in range(ix*200,ix*200+200):
                    for y_ in range(iy*200,iy*200+200):
                        if noi2[x_%200*200+y_%200]<=0.2 and noi2[x_%200*200+y_%200]>=-0.2 and self.map_list[y_][x_] != "6":self.map_list[y_][x_] = "0"
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == "11":
                    if self.map_list[i-1][j] == "0":
                        tree_create = random.randint(1,12)
                        if tree_create == 1:
                            try:
                                if self.map_list[i][j+1] == "0":
                                    for x in range(1,random.randint(5,7)):self.map_list[i-x][j] = "2"
                            except:pass
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == "2":
                    if self.map_list[i-1][j] == "0":
                        leave_height = random.randint(2,3);leave_width = random.randint(2,3)
                        if leave_height >= 2:
                            self.map_list[i-1][j] = "1";self.map_list[i-2][j] = "1";self.map_list[i][j+1] = "1";self.map_list[i][j-1] = "1"
                            if leave_width >= 2:
                                self.map_list[i-1][j+1] = "1";self.map_list[i-2][j+1] = "1"
                                self.map_list[i-1][j-1] = "1";self.map_list[i-2][j-1] = "1";self.map_list[i-1][j+2] = "1"
                                self.map_list[i-2][j+2] = "1";self.map_list[i-1][j-2] = "1";self.map_list[i-2][j-2] = "1"
                                if leave_width == 3:self.map_list[i-1][j+3] = "1";self.map_list[i-1][j-3] = "1"
                            if leave_height == 3:
                                self.map_list[i-3][j] = "1"
                                if leave_width >= 2:
                                    self.map_list[i-1][j+1] = "1";self.map_list[i-2][j+1] = "1"
                                    self.map_list[i-1][j-1] = "1";self.map_list[i-2][j-1] = "1";self.map_list[i-1][j+2] = "1"
                                    self.map_list[i-2][j+2] = "1";self.map_list[i-1][j-2] = "1";self.map_list[i-2][j-2] = "1"
                                    if leave_width == 3:self.map_list[i-1][j+3] = "1";self.map_list[i-1][j-3] = "1"
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == "3":
                    if self.map_list[i-1][j] != "9":
                        mineral_random = random.randint(1,200)
                        if mineral_random == 1:self.map_list[i][j] = "8"
                        if mineral_random >= 2 and mineral_random <= 20:self.map_list[i][j] = "7"
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if i == len(self.map_list[i])-1:self.map_list[i][j] = "6"
                if i >= len(self.map_list[i])-6:
                    if random.randint(0,1) == 1:self.map_list[i][j] = "6"
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if i >= len(self.map_list[i])-11 and self.map_list[i][j] == "0":self.map_list[i][j] = "10"
        # for i in range(len(self.map_list)):
        #     for j in range(len(self.map_list[i])):
        #         if i >= self.sea_high and self.map_list[i][j] == "0" and self.map_list[i][j-1] != "0":self.map_list[i][j] = "14"
    
    def version_debug(self):
        if self.version[0] < self.need_version[0] and self.SSFL_version < self.need_SSFL_version:return False
        else:return True
        
    def game_begin(self):
        if self.version_debug():pass
        else:print("游戏版本号不兼容！请前往最新版本游玩！");sys.exit(0)
        
        # 游戏开始方法 
        if self.use_mod:
            print(f"检测到模组：{_FreeWorld_Mod_.mod_name}")
            print(f"模组版本：{_FreeWorld_Mod_.mod_version}")
            print(f"模组介绍：{_FreeWorld_Mod_.mod_introduce}")
            print(f"模组类型：{_FreeWorld_Mod_.mod_type}")
            print(f"模组情况：{_FreeWorld_Mod_.use_mod}（已成功启用）")
            input("任意键完成设置>>>");print("\033c",end="")
            
        if self.use_mod:_FreeWorld_Mod_.before_game()
        _printf.printf("""欢迎来到FreeWorld游戏1.3.4！""")
        input("任意键继续>>>")
        print("\033c",end="")
        _printf.set_time(0)
        _printf.printf("""FreeWorld 1.3.5 Bag and world
1.debug
    ·重构了在FreeWorld注册的方法debug，用于自我调试
    ·修改了已知bug
    -·这个过程分为三部分：
    -·1.调用unittest.TestCase的一些运算方法，并对其和正确结果进行比对，如果相同则不显示，不相同会提示玩家进行排查
    -·2.调用\033输出系统对常用颜色输出，并自动检测是否与正常输出色系相同
    -·3.输出存档码，让玩家得以存档，debug可以主动被运行，但更多还是在游戏异常的自我排查中
    ·在游戏开始前，系统自动检查游戏版本和SSFL版本是否高于需要的版本
    并且对版本号的储存从字符串形式变为列表
    ·加入指令/version_debug用于人为进行这个操作（这也是目前最长的指令）
    ·加入更多对错误指令的解析，避免直接崩溃（绕过debug系统）
2.指令
    ·加入指令/reset重置游戏
    ·加入指令/printgamemode查看游戏模式
    ·加入指令/printreborn查看重生xy轴
    ·加入了指令组：/gamerule，它有两个参数，一个是修改内容，另一个是修改参数，有以下几个设置：
        -·/gamerule reborn True/False 修改是否禁用重生，默认值为True（允许）
        -·/gamerule player_name name 修改玩家姓名，默认值为FreeWorld Player
        -·/gamerule world_name name 修改世界名称，默认值为FreeWorld
        -·/gamerule no_enter True/False 修改是否无回车输入，默认值为True（允许）
        -·/gamerule health_addition True/False 修改是否自动恢复生命值，默认值为True（允许）
        -·/gamerule health_hurt True/False 修改是否受到伤害，默认值为True（允许）
        -·/gamerule use_mod True/False 修改是否使用mod，如果有mod，默认值为True（允许），否则为False（禁止）
    ·现在w/s/a/d可以为大写，即W/S/A/D
    ·加入指令组/move，/move a 等价于a，等价于A，同样e等价于E
    ·在指令/info中加入了对gamerule内容的表示
    ·加入/say指令用于在聊天框发布消息，/printsay指令用于输出聊天框所有消息
3.真实世界
    ·当饱食度为0时每回合下降2点生命值
    ·加入气泡值，玩家在水中时每回合减去2点气泡值，上岸后每回合加1点气泡值，直到加满不再显示
    ·加入死亡，你会在满足以下条件的任何一条都会触发死亡：
        -·当生命值<=0时，也就是过长时间没有吃东西补充饱食度时
        -·当气泡值<=0时，也就是在水中太长时间
        -·当在岩浆(lava)或火(fire)中太长时间时
        -·当使用/kill指令或/exit指令或/reset指令时
    ·当你处于无伤害状态且饱食度满时，每回合恢复1点生命值
    ·增加二级群系-海————美丽，但有窒息的危险
    自然生成于高于海平面的矿洞内（类似于岩浆的生成），使用水(water)填充
    ·重新定义存档码的组成
4.背包
    ·全新版本的背包将不再使用不同的命令解析器，而是将原来的地图显示换成背包界面
    ·这意味着你可以在背包界面通用主界面的指令，更加方便
    ·也代表你可以在主界面使用背包界面的指令，一样会被处理！
    ·为了迎合为bagUI所设计的新物品储存方式，/set和/break指令将全部覆写
5.存档
    ·在开始时选择“加载存档”按照指示放入存档码就可以读取内容！
    ·现在savefile需要一个参数：存档名称，存档加入两个新参数：名称和时间
    ·对开头进行重构
6.Wiki
    ·这是最后一次，FreeWorld Wiki即将上线，版本其他更新将在那里说明""")
        input("任意键继续>>")
        
        # 对下方使用的选择返回值储存函数进行声明
        gamemodeset1 = None;gamemodeset2 = None;gamemodeset3 = None  
        print("\033c",end="")
    
        while gamemodeset3 == None:gamemodeset3 = _composite.unary_choose(["创建新世界","加载旧存档"],"选择：")
        if gamemodeset3 == "创建新世界":
            print("\033c",end="")
            while gamemodeset1 != "开始游戏":                                     
                gamemodeset1 = _composite.unary_choose(["名称","种子","世界设置","预处理指令","开始游戏"],"选择：")
                if gamemodeset1 == "名称":                                 
                    gamemodeset2 = _composite.unary_choose(["世界名称","玩家名称"],"名称：")
                    if gamemodeset2 == "世界名称":self.world_name = input("请输入世界名称：")
                    elif gamemodeset2 == "玩家名称":self.player_name = input("请输入玩家名称：")
                elif gamemodeset1 == "种子":self.seed = input("请输入种子:")  
                # elif gamemodeset1 == "读取存档":input("敬请期待...\n任意键继续>>>")
                elif gamemodeset1 == "预处理指令":input("敬请期待...\n任意键继续>>>")
                elif gamemodeset1 == "世界设置":input("敬请期待...\n任意键继续>>>")
                
            # print("\033c",end="")
            print()
            _printf.printf(f"{self.player_name}的世界{self.world_name}设置：")
            _printf.printf(f"   ·世界种子：{self.seed}")
            _printf.printf(f"   ·世界地形高度：{self.ground_height}")
            _printf.printf(f"   ·世界类型：{self.type}")
            _printf.printf(f"   ·生物群系类型：{self.animal_type}")
            _printf.printf(f"   ·海平面：{self.sea_high}")
            _printf.printf(f"   ·预处理指令：{self.before_order}")
            _printf.set_time(0) # 将间隔时间初始化
            input("确认游戏设置后继续>>")
        else:
            # 提取存档
            if savefile != None:
                if savefile[0] != [1,3,5]:print("存档码版本过低，无法提取！");sys.exit(0)
                try:
                    self.use_mod = savefile[2]
                    self.seed = savefile[3] # 种子随机生成
                    self.world_name = savefile[4] # 全局世界名称
                    self.player_name = savefile[5] # 全局玩家名称
                    self.coordinate_x = savefile[6] # x坐标初始化
                    self.coordinate_y = savefile[7] # y坐标初始化
                    self.time = savefile[8] # 时间戳初始化
                    self.hungry = savefile[9] # 饱食度初始化
                    self.health = savefile[10] # 生命值初始化
                    self.gamemode = savefile[11] # 游戏模式初始化（默认为生成模式）
                    self.reborn_x = savefile[12] # 设置重生x轴
                    self.reborn_y = savefile[13] # 设置重生y轴
                    self.reborn = savefile[14] # 是否禁止重生（初始化为允许）
                    self.no_enter = savefile[15] # 无回车输入初始化
                    self.bag = savefile[16] # 背包初始化
                    self.staging = savefile[17] # 工作台初始化
                    self.finishblock = savefile[18] # 完成台初始化
                    self.wrong_info = savefile[19] # 错误内容（默认值为无，也就是不显示）
                    self._gamemode = savefile[20] # 用于输出的游戏模式（默认为生成模式）
                    self.ground_height = savefile[21] # 世界高度初始化
                    self.ground_height_savefile = savefile[21] # 用于存档的世界高度初始化
                    self.type = savefile[22] # 世界类型初始化
                    self.animal_type = savefile[23] # 生物群系类型初始化
                    self.sea_high = savefile[24] # 海平面初始化
                    self.before_order = savefile[25] # 预处理指令初始化
                    self.bubble = savefile[26] # 气泡值初始化
                    self.health_addition = savefile[27] # 是否恢复生命值初始化
                    self.health_hurt = savefile[28] # 是否受到伤害初始化
                    self.bag_open = savefile[29] # 是否打开背包初始化
                    self.use_bag = savefile[30] # 这个变量定义需要使用的方块位置
                    self.say = savefile[31] # 聊天内容初始化
                except:print("存档码有缺失项目，请检查存档码！");sys.exit(0)
                print("存档码提取成功，以下是存档的基础内容：")
                print(f"存档名称：{savefile[32]}");print(f"存档时间：{savefile[33]}")
                print(f"玩家坐标-x轴：{self.coordinate_x}");print(f"玩家坐标-y轴：{self.coordinate_y}")
                print(f"游戏时间戳：{self.time}");print(f"玩家饱食度：{self.hungry}")
                print(f"玩家生命值：{self.health}");print(f"游戏模式：{self._gamemode}")
                print(f"玩家背包：{self.bag}");print(f"世界种子：{self.seed}")
                if_more_information = input("是否获得更多存档信息(y/n)>>>")
                if if_more_information == "n":...
                else:
                    print("存档追加内容：")
                    print(f"是否使用模组：{self.use_mod}");print(f"玩家名称：{self.player_name}")
                    print(f"世界名称：{self.world_name}");print(f"重生x轴：{self.reborn_x}")
                    print(f"重生y轴：{self.reborn_y}");print(f"是否允许重生：{self.reborn}")
                    print(f"是否使用无回车输入：{self.no_enter}");print(f"工作台：{self.staging}")
                    print(f"工作台终端：{self.finishblock}");print(f"错误输出内容：{self.wrong_info}")
                    print(f"世界高度：{self.ground_height}");print(f"世界类型：{self.type}")
                    print(f"生物群系类型：{self.animal_type}");print(f"海平面：{self.sea_high}")
                    print(f"预处理指令：{self.before_order}");print(f"玩家气泡值：{self.bubble}")
                    print(f"是否允许增加生命值：{self.health_addition}");print(f"是否允许受到伤害：{self.health_hurt}")
                    print(f"是否打开背包界面：{self.bag_open}");print(f"背包位置：{self.use_bag}")
                    print(f"聊天内容：{self.say}")
                    input("确认存档内容继续>>>")
            else:input("没有找到存档！你可以进入源码第二行根据指示粘贴存档码！任意键创建新世界>>>")
        
        print("正在加载玩家...");self.create_player() # 调用自身类方法生成玩家                         
        print("正在加载地形...");self.create_world(self.seed) # 调用自身类方法生成世界      
    
    def debug(self):
        print("--debug begin--")
        
        # assertT = unittest.TestCase.assertTrue(True)
        # assertF = unittest.TestCase.assertFalse(1==2)
        # assertE = unittest.TestCase.assertEqual(1,1)
        # assertN = unittest.TestCase.assertNotEqual(1,2)
        # assertI = unittest.TestCase.assertIn(1,[1,2,3])
        # assertNI = unittest.TestCase.assertNotIn(1,[2,3,4])
        # print(f"测试结果为{assertT==True}{assertF==True}{assertE==True}{assertN==True}{assertI==True}{assertNI==True}")
        # if [assertT,assertF,assertE,assertN,assertI,assertNI] == [True for i in range(6)]:print("检测到测试结果为：全部正常")
        # elif [assertT,assertF,assertE,assertN,assertI,assertNI] == [False for i in range(6)]:print("警告！IDE丧失所有计算能力！")
        # else:input("有错误发生，任意键进行排查！")
        
        input("对运算能力进行测试>>>")
        value1 = 1;assertT = 1 == value1
        value1 = 2;_assertF = 1 == value1;assertF = _assertF == False
        value1 = 1;assertE = 1 == value1 -1 +1
        value1 = 2;_assertN = 1 == value1 +1 +1;assertN = _assertN == False
        value1 = 2;assertI = value1 in [1,2,3] 
        value1 = 4;_assertNI = value1 in [1,2,3];assertNI = _assertNI == False
        print(f"测试结果为{assertT==True};{assertF==True};{assertE==True};{assertN==True};{assertI==True};{assertNI==True}")
        if [assertT,assertF,assertE,assertN,assertI,assertNI] == [True for i in range(6)]:print("检测到测试结果为：全部正常")
        elif [assertT,assertF,assertE,assertN,assertI,assertNI] == [False for i in range(6)]:print("警告！IDE丧失所有计算能力！")
        else:
            input("有错误发生，任意键进行排查！")
            for i in [assertT,assertF,assertE,assertN,assertI,assertNI]:
                if i == False:print(f"第{i}项出现问题！请联系作者检查！")
        
        input("对色彩渲染进行测试>>>")
        text_color = 1;bg_color = 1
        for i in range(9):print(f"\033[3{text_color}m##\033[m",end="");text_color += 1
        for i in range(9):print(f"\033[4{bg_color}m  \033[m",end="");bg_color += 1
        print("\n检测到测试结果为：全部正常")
        
        input("输出存档码>>>")
        _printf.set_time(0.003);_printf.printf(f"{str(self.file)}\n")
        print("--debug over--")
    
    def main_cycle(self):  
        try:
            while self.map_list[self.coordinate_x+1][self.coordinate_y] == "0":self.coordinate_x += 1
        except:pass
        last_color = ""
        
        # 主循环开始
        while True: 
            if self.use_mod:_FreeWorld_Mod_.cycle()
            
            self.time += 1 # 时间戳流逝                                                        
            if self.time == 25:self.time = 1 # 当时间戳到25时自动归1（防止一天出现25小时）                                        
            if self.hungry != 0:self.hungry -= 1 # 饱食度下降   
            self._gamemode = "生存模式" if self.gamemode == 1 else "创造模式" if self.gamemode == 2 else "信任模式"
            if self.map_list[self.coordinate_x][self.coordinate_y] == "14":self.bubble -= 2 # 气泡值下降
            if self.map_list[self.coordinate_x][self.coordinate_y] != "14" and self.bubble < 20:self.bubble += 1 # 气泡值恢复
            if self.map_list[self.coordinate_x][self.coordinate_y] == "10":
                if self.health_hurt == True:self.health -= 5 # 生命值下降
            if self.hungry == 0:
                if self.health_hurt == True:self.health -= 2 # 当饱食度为0时，生命值下降
            if self.health == 0: # 当生命值为0时死亡
                self.wrong_info = "玩家"+self.player_name+"饿死了！"
                self.health = 30;self.hungry = 30
                self.coordinate_x = self.reborn_x;self.coordinate_y = self.reborn_y
                continue
            if self.health != 30 and self.map_list[self.coordinate_x][self.coordinate_y] != "14" and self.map_list[self.coordinate_x][self.coordinate_y] != "10" and self.hungry == 30:
                if self.health_addition:self.health += 1 # 当生命值未满且没有受到伤害，饱食度满时每回合恢复1点生命值
            
            print("\033c",end="")
            if self.bag_open == False:
                # 用于地图输出的一些函数
                coordinate_x2 = self.coordinate_x-6;coordinate_y2 = self.coordinate_y-9
                print("┏"+36*"━"+"┓")
                for i in range(16): 
                    print("\033[0m┃",end="")
                    for j in range(18):
                        try:
                            if self.list_block[int(self.map_list[coordinate_x2][coordinate_y2])][3] == last_color and j != 0:print("  ",end = "")
                            else:print(self.list_block[int(self.map_list[coordinate_x2][coordinate_y2])][3],end="")
                            last_color = self.list_block[int(self.map_list[coordinate_x2][coordinate_y2])][3]
                        except:print("\033[48;2;147;112;219m  \033[m",end="")
                        coordinate_y2 = coordinate_y2 + 1;time.sleep(0.001)
                    print("\033[0m┃\n",end="")         
                    coordinate_y2 = coordinate_y2 - 18;coordinate_x2 = coordinate_x2 + 
                print("┗"+36*"━"+"┛\033[48;2;0;0;0m")
                gotoxy(8,20,self.list_block[int(self.map_list[self.coordinate_x][self.coordinate_y])][8])
                
            # 背包插件
            elif self.bag_open == True:
                # print("\033c");print("┃ [简易工作台]")
                # print(f"┃  -{self.staging[0][0]}     -{self.staging[0][1]}")
                # print(f"┃  -{self.staging[1][0]}     -{self.staging[1][1]}\n")
                # print("┃ [背包]\n",end="")
                # bag_number = 1
                # for i in range(12):
                #     print("┃ ",end="")
                #     for j in range(3):print(f"{bag_number}:{self.bag[bag_number-1]}",end="");bag_number += 1
                #     print()
                print("背包UI开发中......")
                print()
                  
            if self.bag_open == True:...
            elif self.bag_open == False:gotoxy(19,1,"")                                               
            print(f"┃ [饱食度]:{str(self.hungry)}      [生命值]:{str(self.health)}")
            print(f"┃ [x]:{str(self.coordinate_y)}  [y]:{str(self.coordinate_x)}  [游戏模式]:{self._gamemode}")
            if self.wrong_info != "":print(f"┃ [命令解析器]:{self.wrong_info}");self.wrong_info = ""
            print("┃ 请输入指令：(/help获取指令)")
            if self.no_enter == True:main_answer = _press.getch()
            elif self.no_enter == False:main_answer = input("")
            
            # 短字符指令解析器
            if main_answer == "w" or main_answer == "W":                                                      
                if self.map_list[self.coordinate_x-1][self.coordinate_y] in self.no_collide:self.coordinate_x -= 1
            elif main_answer == "s" or main_answer == "S":                                                    
                if self.map_list[self.coordinate_x+1][self.coordinate_y] in self.no_collide:self.coordinate_x += 1
            elif main_answer == "a" or main_answer == "A":                                                  
                if self.map_list[self.coordinate_x][self.coordinate_y-1] in self.no_collide:self.coordinate_y -= 1
            elif main_answer == "d" or main_answer == "D":                                                     
                if self.map_list[self.coordinate_x][self.coordinate_y+1] in self.no_collide:self.coordinate_y += 1
            elif main_answer == "e" or main_answer == "E":
                if self.bag_open == True:self.bag_open = False
                elif self.bag_open == False:self.bag_open = True
            
            # 长字符指令解析器
            elif "/" in main_answer:
                if self.no_enter == True:main_answer = input("")
                elif self.no_enter == False:main_answer = input("请输入长字符指令内容：")
                main_answer2 = main_answer.split(" ")
                if main_answer == "help":
                    print("FreeWorld Wiki正在编写中......");input("任意键继续>>")
                elif main_answer == "move w":                                                      
                    if self.map_list[self.coordinate_x-1][self.coordinate_y] in self.no_collide:self.coordinate_x -= 1
                elif main_answer == "move s":                                                    
                    if self.map_list[self.coordinate_x+1][self.coordinate_y] in self.no_collide:self.coordinate_x += 1
                elif main_answer == "move a":                                                  
                    if self.map_list[self.coordinate_x][self.coordinate_y-1] in self.no_collide:self.coordinate_y -= 1
                elif main_answer == "move d":                                                     
                    if self.map_list[self.coordinate_x][self.coordinate_y+1] in self.no_collide:self.coordinate_y += 1
                elif main_answer == "seed":self.wrong_info = "种子:"+self.seed
                elif main_answer == "version":self.wrong_info = "版本号:"+self.version[0]+"."+self.version[1]+"."+self.version[2] 
                elif main_answer == "exit":sys.exit(0)                               
                elif "eat" in main_answer:                                               
                    try:self.hungry += self.list_animal[int(main_answer2)-1][4];self.bag.move(self.list_animal[int(main_answer2)][3])
                    except:self.wrong_info = "食物不存在！"
                elif main_answer == "printreborn":self.wrong_info = "重生x轴为："+self.reborn_x+"，重生y轴为："+self.reborn_y
                elif main_answer == "printgamemode":self.wrong_info = "游戏模式为："+self._gamemode
                elif "tp" in main_answer:                                           
                    if self.gamemode > 1: # 查看权限
                        try:
                            self.map_list[self.coordinate_x][self.coordinate_y] = " " 
                            self.coordinate_y = int(main_answer2[1]);self.coordinate_x = int(main_answer2[2])
                        except:self.wrong_info = "命令参数不合法！"
                    else:self.wrong_info = "你无权调用此指令！"
                elif "savefile" in main_answer:    
                    now = datetime.datetime.now()
                    other_StyleTime = now.strftime("%Y年%m月%d日%H时%M分%S秒")
                    # 存档码内容：以列表存储，第一格为查看游戏是否兼容
                    try:
                        self.file = [self.version,self.SSFL_version,self.use_mod,self.seed,self.world_name,self.player_name,
                            self.coordinate_x,self.coordinate_y,self.time,self.hungry,self.health,self.gamemode,self.reborn_x,self.reborn_y,
                            self.reborn,self.no_enter,self.bag,self.staging,self.finishblock,self.wrong_info,self._gamemode,
                            self.ground_height_savefile,self.type,self.animal_type,self.sea_high,self.before_order,self.bubble,self.health_addition,
                            self.health_hurt,self.bag_open,self.use_bag,self.say,main_answer2[1],other_StyleTime]
                        
                        print("你可以复制存档码，当你重新运行游戏时输入存档码，就可以还原你当前的游戏状态，请务必复制完全存档码，包括[]\n")
                        _printf.set_time(0.003)
                        _printf.printf(str(self.file)+"\n")
                        input("任意键继续>>")
                    except:self.wrong_info = "命令参数不合法！"
                elif "set" in main_answer:                                                
                    if self.list_block[int(main_answer2[1])-1][1]+" x1" in self.bag:
                        self.bag.remove(self.list_block[int(ch3[1])-1][1]+" x1")
                        if main_answer2[2] == "w":self.map_list[self.coordinate_x-1][self.coordinate_y] = str(int(main_answer2[1])-1)
                        elif main_answer2[2] == "s":self.map_list[self.coordinate_x+1][self.coordinate_y] = str(int(main_answer2[1])-1)
                        elif main_answer2[2] == "d":self.map_list[self.coordinate_x][self.coordinate_y+1] = str(int(main_answer2[1])-1) 
                        elif main_answer2[2] == "a":self.map_list[self.coordinate_x][self.coordinate_y-1] = str(int(main_answer2[1])-1)
                        else:self.wrong_info = "命令参数不合法！"
                elif "break" in main_answer:
                    if self.use_bag < 37:
                        try:
                            if main_answer2[1] == "w":
                                self.bag[self.use_bag] = (str(self.list_block[int(self.map_list[self.coordinate_x-1][self.coordinate_y])-1][1])+" x1")
                                self.map_list[self.coordinate_x-1][self.coordinate_y] = "0";self.use_bag += 1 
                            elif main_answer2[1] == "s":
                                self.bag[self.use_bag] = (str(self.list_block[int(self.map_list[self.coordinate_x+1][self.coordinate_y])-1][1])+" x1")
                                self.map_list[self.coordinate_x+1][self.coordinate_y] = "0";self.use_bag += 1 
                            elif main_answer2[1] == "d":
                                self.bag[self.use_bag] = (str(self.list_block[int(self.map_list[self.coordinate_x][self.coordinate_y+1])-1][1])+" x1")
                                self.map_list[self.coordinate_x-1][self.coordinate_y] = "0";self.use_bag += 1 
                            elif main_answer2[1] == "a":
                                self.bag[self.use_bag] = (str(self.list_block[int(self.map_list[self.coordinate_x][self.coordinate_y-1])-1][1])+" x1")
                                self.map_list[self.coordinate_x-1][self.coordinate_y] = "0";self.use_bag += 1 
                            else:self.wrong_info = "命令参数不合法！"
                        except:self.wrong_info = "命令参数不合法！"
                    else:self.wrong_info = "背包空间不足"
                elif "health" in main_answer:
                    if self.gamemode > 1: # 查看权限
                        try:
                            if int(main_answer2[1]) <= 100:self.health = int(main_answer2[1])
                        except:self.wrong_info = "命令参数不合法！"
                    else:self.wrong_info = "你无权调用此指令！"
                elif "hungry" in main_answer:
                    if self.gamemode > 1: 
                        try:
                            if int(main_answer2[1]) <= 100:self.hungry = int(main_answer2[1])
                        except:self.wrong_info = "命令参数不合法！"
                    else:self.wrong_info = "你无权调用此指令！"
                elif "time" in main_answer:
                    if self.gamemode > 1:
                        try:
                            if int(main_answer2[1]) <= 24:self.time = int(main_answer2[1])
                        except:self.wrong_info = "命令参数不合法！"
                    else:self.wrong_info = "你无权调用此指令！"
                elif "gamemode" in main_answer:
                    try:
                        if int(main_answer2[1]) == 1 or int(main_answer2[1]) == 2 or int(main_answer2[1]) == 3:self.gamemode = int(main_answer2[1])
                    except:self.wrong_info = "命令参数不合法！"
                elif "health" in main_answer:
                    try:self.reborn_x = int(main_answer2[2]);self.reborn_y = int(main_answer2[1])
                    except:self.wrong_info = "命令参数不合法！"
                elif "get" in main_answer:
                    if self.gamemode > 1: # 查看权限
                        if len(self.bag) < 12:
                            try:self.bag.append(self.list_block[int(main_answer2[1])][1])
                            except:self.wrong_info = "命令参数不合法！"
                        else:self.wrong_info = "背包空间不足"
                    else:self.wrong_info = "你无权调用此指令！"
                elif "throw" in main_answer:
                    try:self.bag[main_answer2[1]] = ""
                    except:self.wrong_info = "命令参数不合法！"
                elif "testblock" in main_answer:
                    try:
                        print(f"背包内方块{self.list_block[int(main_answer2[1])][1]}信息：")
                        print(f"方块id：{self.list_block[int(main_answer2[1])][0]}")
                        print(f"方块标准英文名：{self.list_block[int(main_answer2[1])][2]}")
                        print(f"方块颜色：{self.list_block[int(main_answer2[1])][3]}\033[m")
                        input("任意键继续>>>")
                    except:self.wrong_info = "命令参数不合法！"
                elif main_answer == "kill":self.health = 0
                elif main_answer == "debug":self.debug();input("任意键继续>>>")
                elif main_answer == "version_debug":
                    print(f"游戏目前版本：{self.version[0]}.{self.version[1]}.{self.version[2]}")
                    print(f"游戏运行需要版本：{self.need_version[0]}.{self.need_version[1]}.{self.need_version[2]}")
                    print(f"SSFL目前版本：{self.SSFL_version[0]}.{self.SSFL_version[1]}.{self.SSFL_version[2]}")
                    print(f"SSFL运行需要版本：{self.need_SSFL_version[0]}.{self.need_SSFL_version[1]}.{self.need_SSFL_version[2]}")
                    if self.version_debug():print("检测结果：一切正常，版本兼容")
                    else:print("版本不兼容！请前往最新版本游玩！");sys.exit(0)
                    input("任意键继续>>>")
                elif main_answer == "mod":
                    if self.use_mod: # 是否安装模组，如果没有提示
                        print(f"检测到模组：{_FreeWorld_Mod_.mod_name}")
                        print(f"模组版本：{_FreeWorld_Mod_.mod_version}")
                        print(f"模组介绍：{_FreeWorld_Mod_.mod_introduce}")
                        print(f"模组类型：{_FreeWorld_Mod_.mod_type}")
                        print(f"模组情况：{_FreeWorld_Mod_.use_mod}（已成功启用）")
                    else:print("未检测到模组")
                    input("任意键继续>>>")
                elif main_answer == "info":
                    print(f"{self.player_name}的世界{self.world_name}信息：")
                    print(f"模组情况：",end="")
                    if self.use_mod:
                        print(f"\n检测到模组：{_FreeWorld_Mod_.mod_name}")
                        print(f"模组版本：{_FreeWorld_Mod_.mod_version}")
                        print(f"模组介绍：{_FreeWorld_Mod_.mod_introduce}")
                        print(f"模组类型：{_FreeWorld_Mod_.mod_type}")
                        print(f"模组情况：{_FreeWorld_Mod_.use_mod}（已成功启用）")
                    else:print("未检测到模组")
                    print(f"玩家生命值：{self.health}");print(f"玩家饱食度：{self.hungry}")
                    print(f"游戏模式：{self.gamemode}");print(f"世界种子：{self.seed}")
                    print(f"游戏版本号：{self.version}");print(f"游戏时间：{self.time}")
                    print(f"重生x轴：{self.reborn_x}，重生y轴：{self.reborn_y}")
                    print(f"是否允许重生：{self.reborn}");print(f"是否允许无回车输入：{self.no_enter}")
                    print(f"是否允许增加生命值：{self.health_addition}")
                    print(f"是否允许受到伤害：{self.health_hurt}")
                    print(f"是否允许使用模组：{self.use_mod}")
                    print(f"玩家名称：{self.player_name}");print(f"游戏名称：{self.world_name}")
                    input("任意键继续>>>")
                elif main_answer == "reset":
                    try:_FreeWorld.game_begin();_FreeWorld.main_cycle() 
                    except:
                        print("游戏因异常退出，开始debug寻找错误...")
                        _FreeWorld.debug() # 如果程序运行出错，调用在_FreeWorld注册的debug方法
                    if _FreeWorld_Mod_.use_mod:_FreeWorld_Mod_.after_game()
                elif "gamerule" in main_answer:
                    try:
                        if main_answer[1] == "reborn":self.reborn = int(main_answer[2])
                        elif main_answer[1] == "player_name":self.player_name = main_answer[2]
                        elif main_answer[1] == "world_name":self.world_name = main_answer[2]
                        elif main_answer[1] == "no_enter":self.no_enter = int(main_answer[2])
                        elif main_answer[1] == "health_addition":self.health_addition = int(main_answer[2])
                        elif main_answer[1] == "health_hurt":self.health_hurt = int(main_answer[2])
                        elif main_answer[1] == "use_mod":self.use_mod = int(main_answer[2])
                        else:self.wrong_info = "命令参数不合法！"
                    except:self.wrong_info = "命令参数不合法！"
                elif "say" in main_answer:
                    say_info = self.player_name+"："+main_answer2[1]
                    try:self.say.append(say_info);self.wrong_info = self.player_name+"："+main_answer2[1]
                    except:self.wrong_info = "命令参数不合法！"
                elif main_answer == "printsay":
                    try:
                        print("FreeWorld聊天框：")
                        for i in self.say:print(i)
                    except:self.wrong_info = "命令参数不合法！"
                else:self.wrong_info = "命令不存在！"
            else:self.wrong_info = "命令不存在！"    

_FreeWorld = FreeWorld() # 类实例化
try:_FreeWorld.game_begin();_FreeWorld.main_cycle() 
except:
    print("游戏因异常退出，开始debug寻找错误...")
    _FreeWorld.debug() # 如果程序运行出错，调用在_FreeWorld注册的debug方法
if _FreeWorld_Mod_.use_mod:_FreeWorld_Mod_.after_game()
