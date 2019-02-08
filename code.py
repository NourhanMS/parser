from anytree import Node, RenderTree
#from anytree.exporter import DotExporter
import numpy as np
def isNumber(c):
  return (c=='0' or c=='1'or c=='2'or c=='3' or c=='4'or c=='5'or c=='6' or c=='7'or c=='8'or c=='9')

def isSymbol(c):
  return (c=='+' or c=='-'or c=='*'or c=='/' or c=='=' or c=='<' or c=='(' or c==')'or c==';'or c==':' );

def isLetter(c):
  return (c>=97 and  c<=122)or(c=='_');

def isIdentifier(s):
   return dic[s]=="identifier"

dic={"if":"reserved word","then":"reserved word","end":"reserved word","else":"reserved word",
       "repeat":"reserved word","until":"reserved word","read":"reserved word","write":"reserved word" }
    
def scanner():
  result=[] 
  characters=[]
  with open("simpleTest") as fileObj:
    for line in fileObj:  
        for ch in line:
               characters.append(ch)
  i=0
  while(i<len(characters)): #scan the characters
        ch=characters[i]
    
        if(ch==' '): 
            i+=1
            continue
        if(ch=='{'): #handling comment
            while(characters[i+1]!='}'):
                i+=1
            i+=3
            continue;
        if(isLetter(ord(ch))):
            s =ch
            while(isLetter(ord(characters[i+1]))):
                s2=characters[i+1]
                s+=s2
                i+=1
            result.append(s)
            i+=1
            if(s not in dic):
                dic[s]="identifier"
        if(isSymbol(ch)):  #handle symbols
            if(ch==':'and characters[i+1]=='='):
               result.append(":=");
               i+=2
               continue
            elif(ch==':'): 
                i+=1
                continue
            s=ch
            i+=1
            result.append(s)
        if(isNumber(ch)):
            s=ch
            while(isNumber(characters[i+1])):
                s2=characters[i+1]
                s+=s2
                i+=1
            result.append(s)
            i+=1

        else:
            i+=1

  return result
              
def match(expectedToken):
  global token,index
  if(token==expectedToken):
      index+=1
      if(index<len(result)):
          token=result[index]
  else:
     return "error"
    

def printTree(nodeName):
    for pre, fill, node in RenderTree(nodeName):
        print("%s%s" % (pre, node.name))
              
def stmt_sequence():
    temp=statement()
    while(token==";"):
        newTemp=Node(token)
        match(token)
        newTemp.children=[temp,statement()]
        temp=newTemp
    return temp

def factor():
    if(isNumber(token[0]) or token[0]=='-'):
       temp=Node(token)
       match(token)
       return temp

    elif(token=="("):
        match("(")
        temp=exp()
        match(")")
        return temp
    
    elif(isIdentifier(token)):
        temp=Node("id( "+token+")")
        match(token)
        return temp
    else:
        return print


def term():
    temp=factor()
    while(token=="*"):
        newTemp=Node(token)
        match(token)
        newTemp.children=[temp,factor()]
        temp=newTemp
    return temp

def exp():
    temp=simple_exp()
    if(token=="<" or token=="="):
        newTemp=Node(token)
        match(token)
        newTemp.children=[temp,simple_exp()]
        temp=newTemp
    return temp

def if_stmt():
    match("if")
    temp=Node("if")
    temp1=exp()
    match("then");
    temp2=stmt_sequence()
    temp.children=[temp1,temp2]
    if(token=="else"):
        match("else")
        temp3=stmt_sequence()
        temp3.parent=temp
    match("end")
    return temp

def read_stmt():
    match("read")
    temp=Node("read("+token+")")
    match(token)
    return temp

def write_stmt():
    temp=Node("Write")
    match("write")
    temp.children=[exp()]
    return temp

def repeat_stmt():
    temp=Node("repeat")
    match("repeat")
    temp1=stmt_sequence()
    match("until")
    temp2=exp()
    temp.children=[temp1,temp2]
    return temp

def assign_stmt():
    temp=Node("assign("+ token+")")
    match(token);
    match(":=");
    temp.children=[exp()]
    return temp

def statement():
    if(token=="if"):
        return if_stmt()
    elif (token=="read"):
        return read_stmt()
    elif (token=="write"):
        return write_stmt()
    elif(token=="repeat"):
        return repeat_stmt()
    elif(isIdentifier(token)):
        return assign_stmt()
    
def simple_exp():
    temp=term()
    while(token=="+" or token=="-"):
        newTemp=Node(token)
        match(token)
        newTemp.children=[temp,term()]
        temp=newTemp
    return temp
def exportTree(rootName):
    DotExporter(rootName).to_picture("result.png")
              
def parser():
    resulted=stmt_sequence()
    printTree(resulted)
   # exportTree(resulted)
    
result=scanner()
index=0
token=result[index]
parser()

