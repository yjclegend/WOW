#-*-coding:utf-8-*-
import urllib,urllib2,cookielib
import re


class AucFun:
	"""docstring for AucFun
		Auctioning is so funny
	"""
	def __init__(self):
		self.Cookie = r"wow.auction.priceType=perItem; wow.auction.lastBrowse=?itemId=21877&sort=unitBid&reverse=false; slideViewed=13118918; slideViewed=13118918%2C13133948%2C13118917; JSESSIONID=5BFFE53337EAB8EAB85BBDD35C153827.blade18_04_bnet-wow; xtoken=e2dfef37-0e97-4423-858d-1347fa5a01fd; serviceBar.html5Warning=1; serviceBar.browserWarning=0; web.id=CN-377ae279-7760-4982-a83e-acd65d87a5ad; _ga=GA1.3.1924452016.1406540014; loc=zh; __utma=124133273.1924452016.1406540014.1406808272.1406824571.26; __utmz=124133273.1406684125.9.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E9%AD%94%E5%85%BD%20%E5%AE%A0%E7%89%A9%E7%AC%BC; xstoken=8d6d406a-56e0-4935-b9b2-8716f14c58e8; BA-tassadar-login.key=5f3842e68af7f1969aa06574fee34c7e; login.key=5f3842e68af7f1969aa06574fee34c7e; opt=1"
		self.user_agent = r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 SE 2.X MetaSr 1.0' 
		self.baseURL = r"https://www.battlenet.com.cn/wow/zh/vault/character/auction/horde/browse?itemId="
		self.copperPat = re.compile('icon-copper">(.*?)<')
		self.silverPat = re.compile('icon-silver">(.*?)<')
		self.goldPat = re.compile('icon-gold">(.*?)<')
		self.opener = 0
		self.itemTable = []
		self.initializeOpener()
		self.initializeDB()

	def initializeOpener(self):
		cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(self.opener)


	def initializeDB(self):
		ITEMS = open('pageDB.txt','r')
		for item in ITEMS:
			colList = item.split(',')
			if colList[3] == '':
				colList[3] = '0'
			#itemInfo = [colList[0],colList[1],colList[2]
			self.itemTable.append(colList)
		ITEMS.close()

	def verifyCookie(self):
		FILE = open('result.html','w')
		testItem = '2447'
		testURL = '%s%s'%(self.baseURL,testItem)
		html = self.getHtml(testURL)
		FILE.writelines(html)
		if html.find("<title>战网通行证") >= 0:
			print "invalid cookie"
			exit()
		else:
			print "valid cookie"

	def parseItem(self,item):

		itemURL = '%s%s'%(self.baseURL,item[0])
		itemHtml = self.getHtml(itemURL)
		goldList = self.goldPat.findall(itemHtml)
		count = len(goldList)
		#print count
		if count == 3:
			return
		silverList = self.silverPat.findall(itemHtml)
		copperList = self.copperPat.findall(itemHtml)
		#print goldList
		#print silverList
		#print copperList
		index = 1
		lastPrice = int(item[3])
		marketMinA = 0
		marketMinB = 0
		while 1:
			index = index + 2
			itemPriceA = int(goldList[index].replace(',','')) * 10000 + int(silverList[index]) * 100 + int(copperList[index])
			if goldList[index - 1] == "--":
				index = index + 1
				itemPriceB = itemPriceA	
			else:
				index = index + 1
				itemPriceB = int(goldList[index].replace(',','')) * 10000 + int(silverList[index]) * 100 + int(copperList[index])
				index = index + 1
			#print itemPriceA,itemPriceB,item[2]
			if itemPriceA <= int(item[2]) or itemPriceB <= int(item[2]):
				print "vendor ",item[0],itemPriceA,itemPriceB,item[2]
			#print itemPriceA,itemPriceB
			if marketMinA == 0 or itemPriceA < marketMinA:
				marketMinA = itemPriceA
			if itemPriceB and marketMinB == 0 or itemPriceB < marketMinB:
				marketMinB = itemPriceB

			if lastPrice:
				if itemPriceA < lastPrice * 0.8:
					print "low price A ",item[0],itemPriceA
				if itemPriceB < lastPrice * 0.8:
					print "low price B ",item[0],itemPriceB
			if index + 3 > count:
				break
		if lastPrice:
			highThreshold = lastPrice * 1.2
			if marketMinA >highThreshold or marketMinB > highThreshold:
				print "check ",item[0],marketMinA,marketMinB,lastPrice
		item[3] = marketMinB
				
	def getHtml(self,url):
		req = urllib2.Request(url)
		req.add_header('User-Agent',self.user_agent)
		req.add_header('Cookie',self.Cookie)
		res = urllib2.urlopen(req)
		html = res.read()
		res.close()
		return html

	def updateDB(self):
		ITEMS = open('pageDB.csv','w')
		for item in self.itemTable:
			itemInfo = '%s,%s,%s,%s,\n'%(item[0],item[1],item[2],item[3])
			ITEMS.writelines(itemInfo)
		ITEMS.close()



if __name__=="__main__":
	myAuc = AucFun()
	myAuc.verifyCookie()
	myAuc.initializeDB()
	i=0
	for item in myAuc.itemTable:
		i=i+1
		if i%1000 == 0:
			print item[0]
		#if item[0] == '10603':
		myAuc.parseItem(item)
		#	break
	myAuc.updateDB()
