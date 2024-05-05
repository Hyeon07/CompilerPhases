import sys
import os
import shlex
import csv
import tkinter as tk
import keyword
from infix import PostfixResult
from tkinter import *
from tkinter import filedialog as fd
def GetFiles(file_type):
    global InputFile,GrammarFile,TableFile
    if file_type == 1:
        InputFile = fd.askopenfilename(filetypes=[("Text files", "*.txt")])
        print("Selected input file:", InputFile)
    elif file_type == 2:
        GrammarFile = fd.askopenfilename(filetypes=[("Text files", "*.txt")])
        print("Selected grammar file:", GrammarFile)
    elif file_type == 3:
        TableFile = fd.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if TableFile:
            print("Selected table file:", TableFile)
        else:
            print("No file selected.")
#GUI Implementation
def GUI():
    global op,win
    win=tk.Tk()
    win.configure(background="#219ebc")
    win.title("Phases of compiler")
    win.geometry("1300x900")
    lb=tk.Label(win,text="Phases of compiler")
    lb.config(font=("Arial",20),background="#219ebc")
    lb.pack()
    IpBtn=tk.Button(win,width="20",text="Open Input File",command=lambda:GetFiles(1)).place(x=50,y=100)
    GrBtn=tk.Button(win,width="20",text="Open Grammar File",command=lambda:GetFiles(2)).place(x=50,y=150)
    TbBtn=tk.Button(win,width="20",text="Open Table File",command=lambda:GetFiles(3)).place(x=50,y=200)
    StBtn=tk.Button(win,width="20",text="Submit",command=showOutput).place(x=50,y=250)
    win.mainloop()
#Show Output and it's results in ListBox
def showOutput():
    fr=tk.Frame(win,bd=3,background="#219ebc")
    tk.Label(win,text="Parsed",font=("Arial",15),background="#219ebc").place(x=250,y=70)
    scrollx=tk.Scrollbar(fr,orient=HORIZONTAL)
    scrolly=tk.Scrollbar(fr)
    LB=tk.Listbox(fr,font=(40),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,width=30)
    scrollx.config(command=LB.xview)
    scrollx.pack(side=BOTTOM,fill=X)
    scrolly.pack(side=RIGHT,fill=Y)
    fr.place(x=250,y=100)
    LB.pack()
    rows=open(InputFile,'r')
    for j,i in enumerate(rows):
        try:
            LB.insert(j,"{0:40}{1}".format(i,main(i)))
        except:
            LB.insert(j,"{0:38}Rejected".format(i))
    Tokenization()
    OperatorCodeGeneration()
    CodeGeneration()
    Semantic()
#Lexical Analysis Symbol Table
def Tokenization():
    frame=tk.Frame(win,bd=3,background="#219ebc")
    LB=Listbox(frame,font=("Arial",40),background="#219ebc")
    tk.Label(win,text="Tokens",font=("Arial",15),background="#219ebc").place(x=950,y=70)
    scrollx=tk.scrollbar(frame,orient=HORIZONTAL)
    scrolly=tk.Scrollbar(frame)
    LB=tk.Listbox(frame,font=(40),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,width=30)
    scrollx.config(command=LB.xview)
    scrolly.pack(side=BOTTOM,fill=Y)
    frame.place(x=950,y=100)
    LB.pack()
    Reserved=keyword.kwlist
    Operators=["*","%","/","+","-","<",">","==","<=",">=","="]
    Identifiers=[]
    Tokens=open(InputFile,"r")
    Inserted=[]
    LB.insert(END,"{0:30}{1}".format("Lexeme","Token"))
    for j in Tokens:
        for i in j:
            i=i.strip()
            if i.isnumeric() and i not in Inserted:
                LB.insert(END,"{0:40}{1}".format(i,"number"))
                Inserted.append(i)
            if i in Reserved and i not in Inserted:
                LB.insert(END,"{0:40}{1}".format(i,i))
            elif i in Operators and i not in Inserted:
                LB.insert(END,"{0:40}{1}".format(i,"relation"))
            elif i not in Inserted and len(i)>0:
                LB.insert(END,"{0:40}{1}".format(i,"id"))
                Identifiers.append(i)
                Inserted.append(i)
    SymbolTable(Identifiers)
#SymbolTable
def SymbolTable(identifiers):
    frame=tk.Frame(win,bd=3,background="#219ebc")
    LB=Listbox(frame,font=("Arial",40),background="#219ebc")
    tk.Label(win,text="Tokens",font=("Arial",15),background="#219ebc").place(x=600,y=70)
    scrollx=tk.scrollbar(frame,orient=HORIZONTAL)
    scrolly=tk.Scrollbar(frame)
    LB=tk.Listbox(frame,font=(40),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,width=30)
    scrollx.config(command=LB.xview)
    scrolly.pack(side=BOTTOM,fill=Y)
    frame.place(x=600,y=100)
    LB.pack()
    LB.insert(END,'{0:<10}{1:>8}{2:>8}'.format("Symbol","Type","Scope"))
    for i in identifiers:
        typeval=""
        if i.isnumeric(): typeval="int"
        else: typeval="string"
        LB.insert(END,'{0:<10}{1:>15}{2:>11}'.format(i,typeval,"gloabal"))
#Machine Code Generation
def CodeGeneration():
    frame=tk.Frame(win,bd=3,background="#219ebc")
    tk.Label(win,text="Machine Code Generation",font=("Arial",15),backgroung="gray").place(x=250,y=320)
    scrollx=tk.scrollbar(frame,orient=HORIZONTAL)
    scrolly=tk.Scrollbar(frame)
    LB=tk.Listbox(frame,font=(40),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,width=30)
    scrollx.config(command=LB.xview)
    scrolly.pack(side=BOTTOM,fill=Y)
    frame.place(x=250,y=360)
    LB.pack()
    rows=open(InputFile,'r')
    for i in rows:
        LB.insert(END,''.join(format(ord(x),'b')for x in i))
#convert * in X and / into mathematical divide operator
def OperatorCodeGeneration():
    frame=tk.Frame(win,bd=3,background="#219ebc")
    tk.Label(win,text="Mathematical Expression Generation",font=("Arial",15),backgroung="gray").place(x=950,y=320)
    scrollx=tk.scrollbar(frame,orient=HORIZONTAL)
    scrolly=tk.Scrollbar(frame)
    LB=tk.Listbox(frame,font=(40),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,width=30)
    scrollx.config(command=LB.xview)
    scrolly.pack(side=RIGHT,fill=Y)
    frame.place(x=950,y=360)
    LB.pack()
    rows=open(InputFile,"r")
    for i in rows:
        i=i.replace("*","x")
        i=i.replace("/","\u00f7")
        LB.insert(END,i)
#Semantic Analysis
def Semantic():
    frame=tk.Frame(win,bd=3,background="#219ebc")
    tk.Label(win,text="Semantic Analyis",font=("Arial",15),background="#219ebc").place(x=600,y=320)
    scrollx=tk.scrollbar(frame,orient=HORIZONTAL)
    scrolly=tk.Scrollbar(frame)
    LB=tk.Listbox(frame,font=(40),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,width=30)
    scrollx.config(command=LB.xview)
    scrolly.pack(side=BOTTOM,fill=Y)
    frame.place(x=600,y=360)
    LB.pack()
    rows=open(InputFile,'r')
    try:
        for i in rows:
            for j in i:
                if j.isnumeric()==False:
                    continue 
            result=PostfixResult(i)
            if len(result)==1:
                LB.insert(END,result)
    except:
        if LB.size()==0:
            LB.insert(END,"Semantically incorrect input")

#Syntax Analyzer Parser
def main(input_string):
    input_ind=list(shlex.shlex(input_string))
    input_ind.append('$')
    master={}
    master_list=[]
    new_list=[]
    non_terminals=[]
    grammar=open(GrammarFile,'r')
    for row2 in grammar:
        if "->" in row2:
            #new production
            if len(new_list)==0:
                start_state=row2[0]
                non_terminals.append(row2[0])
                new_list=[]
                new_list.append(row2.rstrip("\n"))
            else:
                master_list.append(new_list)
                del new_list
                new_list=[]
                new_list.append(row2.rstrip('\n'))
                non_terminals.append(row2[0])
        elif '|' in row2:
            new_list.append(row2.rstrip('\n'))
    master_list.append(new_list)
    for x in range(len(master_list)):
        for y in range(len(master_list[x])):
            master_list[x][y]=[s.replace('|','') for s in master_list[x][y]]
            master_list[x][y]=''.join(master_list[x][y])
            master[master_list[x][y]]=non_terminals[x]
    for key,value in master.items():
        if '->' in key:
            length=len(key)
            for i in range(length):
                if key[i]=='-' and key[i+1]=='>':
                    index=i+2
                    break
            var_key=key
            new_key=key[index:]
    var=master[var_key]
    del master[var_key]
    master[new_key]=var
    order_table=[]
    with open(TableFile,'r') as file2:
        order=csv.reader(file2)
        for row in order:
            order_table.append(row)
    operators=order_table[0]
    stack=[]
    stack.append('$')
    vlaag=1
    while vlaag:
        if input_ind[0] =='$' and len(stack)==2:
            vlaag=0
        length=len(input_ind)
        buffer_inp=input_ind[0]
        temp1=operators.index(str(buffer_inp))
        if stack[-1] in non_terminals:
            buffer_stack=stack[-2]
        else:
            buffer_stack=stack[-1]
        temp2=operators.index(str(buffer_stack))
        precedence=order_table[temp2][temp1]
        if precedence=='<':
            action="shift"
        elif precedence==">":
            action="reduce"
        if action=="shift":
            stack.append(buffer_inp)
            input_ind.remove(buffer_inp)
        elif action=="reduce":
            for key,value in master.items():
                var1="".join(stack[-1:])
                var2="".join(stack[-3:])
                if str(key)==str(buffer_stack):
                    stack[-1]=value
                    break
                elif key==var1 or stack[-3:]==list(var1):
                    stack[-3:]=value
                    break
                elif key==var2:
                    stack[-3:]=value
        del buffer_inp,temp1,buffer_stack,temp2,precedence
        if vlaag==0:
            return "Accepted"
    #if __name__=="__main__":
GUI()