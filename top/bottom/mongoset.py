import pymongo

class mongoDB(object):
	def __init__(self,host,port,database,collection,username=None,password=None):
		self.connection=pymongo.MongoClient(host, port)
		self.db=self.connection[database]
		self.collection=self.db[collection]
	def setDataBase(self,database,collection):
		self.db=self.connection[database]
		self.collection=self.db[collection]
	def setCollection(self,collection):
		self.collection=self.db[collection]
	def find(self,param=None):
		returnDatas=[]
		for item in self.collection.find(param):
			returnDatas.append(item)
		return returnDatas
	def findOne(self,param=None):
		return self.collection.find_one(param)
	def remove(self,param=None):
		self.collection.remove(param)
	def insert(self,param):
		for item in param:
			self.collection.insert(item)

