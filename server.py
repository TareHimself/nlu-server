import asyncio
from os import path, getcwd,listdir
from typing import Callable



# Built-in library
import json
from uuid import uuid4
# Third-party library
from aiohttp import web
from regex import F

class WebServer:
	def __init__(self):
		self.app = web.Application()
		
	
	def Get(self,path:str):
		def inner(func):
			self.app.router.add_get(path,func)
			return func
		return inner

	def Post(self,path:str):
		def inner(func):
			self.app.router.add_post(path,func)
			return func
		return inner

	def Put(self,path:str):
		def inner(func):
			self.app.router.add_put(path,func)
			return func
		return inner

	def Delete(self,path:str):
		def inner(func):
			self.app.router.add_delete(path,func)
			return func
		return inner

	def Delete(self,path:str):
		def inner(func):
			self.app.router.add_delete(path,func)
			return func
		return inner

	def listen(self,host:str,port:int):
		web.run_app(self.app, host=host, port=port)



#import yaml

#with open(path.join(getcwd(),'rasa','nlu.yml')) as ym:
#	print(yaml.load(ym, Loader=yaml.FullLoader))

#