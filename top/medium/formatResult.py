import json
import re
from bottom.setfile import *
def formatTxt(resultPath,untreatedPath,maxNum,code='utf-8'):
	try:
		readTxt=readFile(untreatedPath,code)
	except:
		code='gbk'
		readTxt=readFile(untreatedPath,code)
	finally:
		readList=jsonToDict(readTxt)
		writeResult=[]
		writeContent={}
		for readContent in readList:
			if readContent['description'] =='name':
				if not writeContent in writeResult:
					writeResult.append(writeContent)
				writeContent={}
				writeContent['name']=readContent['content']
			else:
				if readContent['description'] in writeContent.keys():
					try:
						writeContent[readContent['description']].append(readContent['content'])
					except:
						oldContent=writeContent[readContent['description']]
						writeContent[readContent['description']]=[]
						writeContent[readContent['description']].append(oldContent)
						writeContent[readContent['description']].append(readContent['content'])
				else:
					writeContent[readContent['description']]=readContent['content']
		try:
			print('write try')
			writeFile(resultPath,str(writeResult),'w',code)
			readTxt=readFile(resultPath,code)
		except:
			print('write wrong')
			formatTxt(resultPath,untreatedPath,maxNum,code)
		finally:
			if resultPath=='[]':
				formatTxt(resultPath,untreatedPath,maxNum,code)
			else:
				print("Result "+str(maxNum)+" untreated datas have Done")
				maxNum-=1
				resultPath=resultPath.replace(str(maxNum+1)+'.txt',str(maxNum)+'.txt')
				untreatedPath=untreatedPath.replace(str(maxNum+1)+'.txt',str(maxNum)+'.txt')
				if maxNum>=0:
					formatTxt(resultPath,untreatedPath,maxNum)

def formatMongo(untreatdb,resultdb):
	writeResult=[]
	writeContent={}
	flagName=untreatdb.findOne()['description']
	print(flagName)
	for readContent in untreatdb.find():
		if readContent['description'] ==flagName:
			if not writeContent in writeResult:
				writeResult.append(writeContent)
			writeContent={}
			writeContent[flagName]=readContent['content']
		else:
			if readContent['description'] in writeContent.keys():
				try:
					writeContent[readContent['description']].append(readContent['content'])
				except:
					oldContent=writeContent[readContent['description']]
					writeContent[readContent['description']]=[]
					writeContent[readContent['description']].append(oldContent)
					writeContent[readContent['description']].append(readContent['content'])
			else:
				writeContent[readContent['description']]=readContent['content']
	resultdb.insert(writeResult)
def dictToJson(stringObj):
	stringObj=str(stringObj).replace('[',',').replace(']','').replace("'",'"')
	return stringObj
def jsonToDict(stringObj):
	readStr=stringObj.replace(',','[',1)+"]"
	try:
		return json.loads(readStr)
	except:
		return []
def htmlToDict(content,rule,tt=0):
	returnList=[]
	matchList=rule.childNodes
	for matchContent in matchList:
		if matchContent.nodeName=='match':
			description=matchContent.getAttribute('description')
			pattern=matchContent.getAttribute('pattern')
			if pattern == '':
				front=matchContent.getAttribute('front')
				behind=matchContent.getAttribute('behind')
				pattern=front+'(.*?)'+behind
			ruleNum=matchContent.getAttribute('ruleNum')
			haveChild=matchContent.getAttribute('haveChild')
			save=matchContent.getAttribute('save')
			patt = re.compile(pattern,re.S)
			resultList = re.findall(patt,content)
			if haveChild=='1':
				for result in resultList:
					nextResult=htmlToDict(str(result),matchContent.childNodes[1],1)
					for ne in nextResult:
						returnList.append(ne)
			else:
				for result in resultList:
					echoSingle={}
					if haveChild!=1:
						echoSingle['content']=str(result)+matchContent.getAttribute('addUrl')
						echoSingle['description']=description
						echoSingle['ruleNum']=ruleNum
						echoSingle['save']=save
						returnList.append(echoSingle)
	return returnList
	
