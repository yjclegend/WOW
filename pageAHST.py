#-*-coding:utf-8-*-
#collect merchant price of all Items
import urllib.request
import re,threading

class PageItemDb(object):
	"""docstring for PageItemDb"""
	def __init__(self):
		super(PageItemDb, self).__init__()
		self.url_base = r"http://www.battlenet.com.cn/wow/zh/item/"
		self.nonExistKeyword = r"<title>魔兽世界</title>"
		self.priceKeyword = "出售价格"
		self.pickBindKeyword = "拾取后绑定"
		self.accountBindKeyword = "战网账号绑定"
		self.titlePat = re.compile('<title>(.*?)\s-')
		self.copperPat = re.compile('icon-copper">(.*?)<')
		self.silverPat = re.compile('icon-silver">(.*?)<')
		self.goldPat = re.compile('icon-gold">(.*?)<')
		self.itemDb = dict()

	def parseItem(self,itemId):
		itemUrl = '%s%s'%(self.url_base,itemId)
		itemLink = urllib.request.urlopen(itemUrl)
		itemPage = itemLink.read().decode('utf-8')
		if self.isItemExist(itemPage):
			if not self.isItemBind(itemPage):
				print(itemId)
				name = self.getItemName(itemPage)
				price = self.getItemPrice(itemPage)
				self.itemDb[itemId] = (name,price)

	def isItemExist(self,pageContent):
		if pageContent.find("self.nonExistKeyword") > 0:
			return False
		return True

	def isItemBind(self,pageContent):
		if (pageContent.find(self.pickBindKeyword) > 0) or \
		   (pageContent.find(self.accountBindKeyword) > 0):
			return True
		return False

	def getItemName(self,pageContent):
		itemName=''
		hResult = self.titlePat.search(pageContent)
		if hResult:
 			itemName = hResult.group(1)
		return itemName

	def getItemPrice(self,pageContent):
		price = 0
		keyIndex = pageContent.find(self.priceKeyword)
		pageContent = pageContent[keyIndex:]
		hResult = self.goldPat.search(pageContent)
		if hResult:
			itemGold = hResult.group(1)
			price += int(itemGold.replace(',','')) * 10000
		hResult = self.silverPat.search(pageContent)
		if hResult:
			itemSilver = hResult.group(1)
			price += int(itemSilver)*100
		hResult = self.copperPat.search(pageContent)
		if hResult:
			itemCopper = hResult.group(1)
			price += int(itemCopper)
		return price

	def watchItem(self,itemId):
		name = self.itemDb[itemId][0]
		price = self.itemDb[itemId][1]
		print(name,price)

if __name__ == '__main__':
	pageItemDb = PageItemDb()
	pageItemDb.parseItem(237)
	pageItemDb.watchItem(237)


# url_base = r"http://www.battlenet.com.cn/wow/zh/item/"

# itemID = 0
# count = 3
# keyword = "出售价格"
# titlePat = re.compile('<title>(.*?)\s-')
# copperPat = re.compile('icon-copper">(.*?)<')
# silverPat = re.compile('icon-silver">(.*?)<')
# goldPat = re.compile('icon-gold">(.*?)<')

# flag = 0

# itemName = ''
# itemGold = ''
# itemSilver = ''
# itemCopper = ''
# itemPrice = ''
# #HTMLFILE = open('result.html','w')
# DBFILE = open('pageDB.txt','w')

# for itemID in range(1,130000):
# 	print itemID
# 	itemUrl = '%s%d'%(url_base,itemID)
# 	itemLink = urllib.urlopen(itemUrl)
# 	for line in itemLink:
# 		if count:
# 			count = count - 1
# 			if count == 0 and line.find('http') >= 0:
# 				break;
# 			continue;
# 		if line.find('<title>') >= 0:
# 			hResult = titlePat.search(line)
# 			itemName = hResult.group(1)
# 		if line.find(keyword) >=0:
# 			flag = 1
# 		if flag:
# 			hResult = goldPat.search(line)
# 			if hResult:
# 				itemGold = hResult.group(1)
# 				continue
# 			hResult = silverPat.search(line)
# 			if hResult:
# 				itemSilver = hResult.group(1)
# 				continue
# 			hResult = copperPat.search(line)
# 			if hResult:
# 				itemCopper = hResult.group(1)
# 				break;
# 	itemPrice = 0
# 	if itemGold:
# 		itemPrice = itemPrice + int(itemGold.replace(',','')) * 10000
# 	if itemSilver:
# 		itemPrice = itemPrice + int(itemSilver)*100
# 	if itemCopper:
# 		itemPrice = itemPrice + int(itemCopper)
# 	if itemPrice:
# 		fileLine = '%d,%s,%s,0,\n'%(itemID,itemName,itemPrice)
# 		DBFILE.writelines(fileLine)

# 	count = 3
# 	flag = 0
# 	itemGold = ''
# 	itemSilver = ''
# 	itemCopper = ''
# 	itemPrice = ''
# 	#file_object.writelines(ah_base)

# 	itemLink.close()

# DBFILE.close()