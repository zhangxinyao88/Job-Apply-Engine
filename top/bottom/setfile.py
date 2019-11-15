import os
import xml.dom.minidom
import linecache
def readLinesFile(path,lines=None):
	f=open(path,'r')
	re_Lines=f.readlines(lines)
	f.close()
	return re_Lines
def readLine(path,line=0):
	re_Line=linecache.getline(path,line)
	linecache.clearcache()
	return re_Line
def readFile(path,code=None):
	if code==None:
		f=open(path,'r')
	else:
		f=open(path,'r',encoding=code)
	re=f.read()
	f.close()
	return re	
def wirteLinesFile(path,lines,wirtetype='a'):
	f=open(path,wirtetype)
	f.writelines(lines)
	f.close()
def writeLine(path,line):
	print(line)
	f=open(path,'a')
	f.writeline(line)
	f.close()
def writeFile(path,content,wirtetype='a',code=None):
	if code==None:
		f=open(path,wirtetype)
	else:
		f=open(path,wirtetype,encoding=code)
	f.write(content)
	f.close()

def creatFolder(path):
	if not os.path.exists(path):
		os.mkdir(path)	
def creatFile(path):
	if not os.path.exists(path):
		f=open(path,'w')
		f.close()	
def readConfig(path):
	dom = xml.dom.minidom.parse(path)
	root = dom.documentElement
	return root.childNodes
def readIni(cf,host,port,returnType):
	if returnType==0:
		return cf.get(host,port)
	elif returnType == 1:
		return cf.getint(host,port)
def getSize(path):
	return os.path.getsize(path)

