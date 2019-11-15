import asyncio
import aiohttp
 
'''
request['url']
request['method']
request['data']
'''
@asyncio.coroutine
def get_page(url,postdata=None):
	if postdata == None:
		response = yield from aiohttp.request('GET', url)
	else:
		response = yield from aiohttp.request('POST', url,data=postdata)
	return(yield from response.read_and_close())


def request_list(requestList,maxNum=20):
	loop = asyncio.get_event_loop()
	f = asyncio.wait([get_page(request) for request in requestList])
	loop.run_until_complete(f)
