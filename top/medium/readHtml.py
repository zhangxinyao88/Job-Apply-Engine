from bottom.http import *
from bottom.setfile import *
from bottom.mongoset import *
from medium.formatResult import *
from urllib.request import Request
import asyncio
import configparser
class httpCatch(object):
	def __init__(self,configPath):
		config=configparser.ConfigParser()
		config.read(configPath)
		self.position=0
		self.isMax=config.getint('GlobalConfig','isMax')
		self.readMax=config.getint('GlobalConfig','readMax')
		self.saveMax=config.getint('GlobalConfig','saveMax')
		self.readaheadMax=config.getint('GlobalConfig','readaheadMax')
		self.root=readConfig(config.get('GlobalConfig','rulePath'))
		self.resultPath=config.get('GlobalConfig','resultPath')
		self.untreatedPath=config.get('GlobalConfig','untreatedPath')
		self.readPath=config.get('GlobalConfig','readPath')
		dataBase=config.get('GlobalConfig','dataBase')
		postCollection=config.get('GlobalConfig','postCollection')
		untreatedCollection=config.get('GlobalConfig','untreatedCollection')
		saveCollection=config.get('GlobalConfig','saveCollection')

		self.readaheadList=[]
		self.copyreadList=[]
		self.rules=[]
		self.readPathNum=0
		self.writePathNum=0
		self.untreatedPathNum=0
		self.readPath=self.readPath.replace('.txt','0.txt')
		self.writePath=self.readPath
		self.untreatedPath=self.untreatedPath.replace('.txt','0.txt')
		self.resultPath=self.resultPath.replace('.txt','0.txt')

		self.mongoPost=mongoDB('localhost',27017,dataBase,postCollection)
		self.untreatData=mongoDB('localhost',27017,dataBase,untreatedCollection)
		self.resultData=mongoDB('localhost',27017,dataBase,saveCollection)
		self.descriptions=[]
		writeFile(self.readPath,'','w')
		writeFile(self.untreatedPath,'','w')
		writeFile(self.resultPath,'','w')
		for urlRoot in self.root:
			if urlRoot.nodeName=='url':
				readahead={}
				if urlRoot.getAttribute('method')!='post':
					readahead['url']=urlRoot.getAttribute('url')
					readahead['deep']=1
					readahead['maxDeep']=int(urlRoot.getAttribute('maxDeep'))
					readahead['ruleNum']=urlRoot.getAttribute('ruleNum')
					readahead['Host']=urlRoot.getAttribute('Host')
					readahead['code']=urlRoot.getAttribute('code')
					readahead['method']='get'
					self.readaheadList.append(readahead)
				else:
					self.mongoPost.setCollection(urlRoot.getAttribute('dataform'))
					param=urlRoot.getAttribute('postparam')
					for postdata in self.mongoPost.find():
						readahead['url']=urlRoot.getAttribute('url')
						readahead['ruleNum']=urlRoot.getAttribute('ruleNum')
						readahead['Host']=urlRoot.getAttribute('Host')
						readahead['deep']=1
						readahead['maxDeep']=int(urlRoot.getAttribute('maxDeep'))
						readahead['code']=urlRoot.getAttribute('code')
						readahead['method']='post'
						readahead['postdata']=postdata[param]
						self.readaheadList.append(readahead)
						readahead={}
			elif urlRoot.nodeName=='rule':
				self.rules.append(urlRoot)
	def aioBegin(self):
		loop = asyncio.get_event_loop()
		f = asyncio.wait([self.catchList(res) for res in self.readaheadList])
		loop.run_until_complete(f)
		count=0
		while 1:
			count+=1
			print(str(count*self.isMax)+"urls have done---deep:"+str(self.readaheadList[0]['deep']))
			if self.readTolist()==0:
				break
			loop = asyncio.get_event_loop()
			f = asyncio.wait([self.catchList(res) for res in self.readaheadList])
			loop.run_until_complete(f)
		print("Format untreated data begin")
		'''
		formatTxt(self.resultPath,self.untreatedPath,self.untreatedPathNum)
		'''
		formatMongo(self.untreatData,self.resultData)
	@asyncio.coroutine
	def domatch(self,request):
		page=''
		code=request['code']
		url=request['url']
		postdata=None if request['method']!='post' else request['postdata']
		if not 'http' in url:
			url=request['Host']+url
		sem = asyncio.Semaphore(self.readMax)
		with (yield from sem):
			try:
				page = yield from get_page(url,postdata)
			except:
				return []
		try:
			page=page.decode(code,'ignore').encode('utf-8').decode('utf-8')
		except:
			return []
		for rule in self.rules:
			if rule.getAttribute('ruleNum')==request['ruleNum']:
				return htmlToDict(page,rule)
	@asyncio.coroutine
	def catchList(self,request):
		if request['deep']<=request['maxDeep']:
			resultList=yield from self.domatch(request)
			if len(resultList)>0:
				writeLines=[]
				writeResultList=[]
				for result in resultList:
					if request['deep']<request['maxDeep'] and result['ruleNum']!='':
						try:
							writeContent={}
							writeContent['url']=result['content']
							writeContent['deep']=request['deep']+1
							writeContent['code']=request['code']
							writeContent['maxDeep']=request['maxDeep']
							writeContent['ruleNum']=result['ruleNum']
							writeContent['Host']=request['Host']
							writeContent['method']='get'						
							writeLines.append(writeContent)
						except:
							continue
					if result['save']=='':
						writeResultList.append(result)
				self.writeTolist(writeLines)
				'''
				self.writeResult(writeResultList,request['code'])
				self.untreatData.insert(writeResultList)
				'''
				self.untreatData.insert(resultList)
	def writeResult(self,resultList,code):
		if len(resultList)!=0:
			if getSize(self.untreatedPath)>self.saveMax*1048576:
				self.untreatedPath=self.untreatedPath.replace(str(self.untreatedPathNum)+'.txt','')
				self.untreatedPathNum+=1
				self.untreatedPath+=str(self.untreatedPathNum)+'.txt'
				writeFile(self.untreatedPath,'','w')
				print(str(self.untreatedPathNum)+"M untreated datas have Saved")
			writeFile(self.untreatedPath,dictToJson(resultList),code=code)
	def writeTolist(self,writeLines):
		outLines=[]
		if getSize(self.writePath)>self.readaheadMax*1024:
			self.writePath=self.writePath.replace(str(self.writePathNum)+'.txt','')
			self.writePathNum+=1
			self.writePath+=str(self.writePathNum)+'.txt'
			writeFile(self.writePath,'','w')
		for singleContent in writeLines:
			if len(self.copyreadList)<self.isMax:
				self.copyreadList.append(singleContent)
			else:
				outLines.append(singleContent)
		if len(outLines)!=0:
			writeFile(self.writePath,dictToJson(outLines))
	def readTolist(self):
		self.readaheadList=self.copyreadList
		if len(self.copyreadList)==0:
			return 0
		elif len(self.copyreadList) < self.isMax:
			self.copyreadList=[]
			return 1
		else:
			readStr=readFile(self.readPath)
			if readStr=='':
				self.copyreadList=[]
				return 1
			else:
				readaheadList=jsonToDict(readStr)
				self.copyreadList=[]
				count=0
				isMax=0
				Ifbreak=0
				for readahead in readaheadList:
					if count==self.position:
						self.copyreadList.append(readahead)
						isMax+=1
						self.position+=1
					count+=1
					if isMax>self.isMax:
						Ifbreak=1
						break
				if Ifbreak == 0:
					self.readPath=self.readPath.replace(str(self.readPathNum)+'.txt','')
					self.readPathNum+=1
					self.readPath+=str(self.readPathNum)+'.txt'
					writeFile(self.readPath,'','a')
					self.position=0
				return 1