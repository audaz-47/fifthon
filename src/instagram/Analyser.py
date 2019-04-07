import pymongo
from src.instagram.ApiCrawler import ApiCrawler
from src.common.utils import *
import time

class database:
	def db_connect(self):
		self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		self.mydb = self.myclient["instagram"]
		self.mycol = self.mydb["users"]

	def crawl_and_find(self,credentials):
		self.crawler = ApiCrawler(credentials['instagram'], credentials['instagram']['user'])
		self.crawler.getFollowingsByApi()
		self.followings=self.crawler.followings

		self.handle=credentials['instagram']['user']
		self.followings_list=[]
		for i in range(0,len(self.followings)):
			self.followings_list.append(self.followings[i]['node'])
			#print(followings[i]['node']['username'])
		self.ts = time.time()
		self.crawler.getFollowersByApi()
		self.followers=self.crawler.followers
		self.followers_list=[]
		for i in range(0,len(self.followers)):
			self.followers_list.append(self.followers[i]['node'])

	def database_query(self):
		self.myquery = { "handle": self.handle }
		self.mydoc = self.mycol.find(self.myquery)

		self.followers_who_have_unfollowed_you=[]
		self.prefollowers=[]
		if self.mydoc.count()>0:
			for doc in self.mydoc:
				for rec in doc['followers']:
					self.prefollowers.append(rec['username'])
			for followers in self.prefollowers:
				flag=0
				for i in range(0,len(self.followers_list)):
					if(followers==self.followers_list[i]['username']):
						flag=1
						break
					else:
						continue
				if(flag==0):
					self.followers_who_have_unfollowed_you.append(followers)

			print(self.followers_who_have_unfollowed_you)
			self.newvalues = { "$set": { "followers": self.followers_list,"followings": self.followings_list, "time":self.ts } }
			self.mycol.update_one(self.myquery, self.newvalues)

		else:
			self.mydict = { "handle": self.handle, "followers": self.followers_list, "followings": self.followings_list, "time":self.ts }
			self.mycol.insert_one(self.mydict)


