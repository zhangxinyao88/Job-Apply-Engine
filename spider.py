from bottom.http import *
from bottom.setfile import *
from bottom.wordObject import *
from urllib.request import Request

def getTest(request):
	config=readConfig('config.xml')
	page=''
	sem = asyncio.Semaphore(5)
	with (yield from sem):
		page = yield from get_page(request)
	try:
		page=page.decode('utf-8')
	except:
		page=page.decode('gbk')
	htmlToDict(page,config)
requestList=[]
request={}
request['url']='http://www.taobao.com'
request['method']=0
requestList.append(request)
loop = asyncio.get_event_loop()
f = asyncio.wait([getTest(res) for res in requestList])
loop.run_until_complete(f)