#-*-coding:utf-8-*-
import urllib.request
import http.cookiejar
import re
import threading,time


class MyPrecious:

	def __init__(self):
		#重要物品列表
		self.vidList = ("127037","124116","124106")
		#header
		self.Cookie = r'wow.auction.lastBrowse=?reverse=false&sort=unitBid&itemId=124106; slideViewed=17411771%2C17429138%2C17411770%2C17430757%2C17433353%2C17433438%2C17433354%2C17434211%2C17434831; JSESSIONID=09DAEC7685FFCADD639230323E0D7851.blade13_04_bnet_wow; xstoken=e9d84df8-697e-4315-bf2b-69229ab292b3; eu-cookie-compliance-agreed=1; _ga=GA1.3.1696783307.1468576771; __utma=124133273.1696783307.1468576771.1473003233.1473041215.91; __utmz=124133273.1472917001.85.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; web.id=CN-0795b522-b684-4d55-ad70-e1e413aafd66; 70584433-VID=1124501665965071; discussion.sort=best; BA-tassadar-login.key=ace7b8373b7336a79b6cf6eac0b3a2e1; login.key=ace7b8373b7336a79b6cf6eac0b3a2e1; xstoken=46518e8a-ba5b-4e73-a072-11b162b2da80; loginChecked=1; __utmb=124133273.69.9.1473042523449; __utmc=124133273; JSESSIONID=F3873866B6F1AB669BC8F214429B951F.blade09_03_bnet; opt=1'
		self.user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0' 
		self.host = r"www.battlenet.com.cn"
		self.accept = r"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
		self.lang = r"en-US,en;q=0.5"
		self.enc = r"gzip, deflate, br"
		self.ref = r"https://www.battlenet.com.cn/wow/zh/vault/character/auction/auctions"
		self.conn = r"keep-alive"

		#拍卖物品页面价格关键字
		self.copperPat = re.compile('icon-copper">(.*?)<')
		self.silverPat = re.compile('icon-silver">(.*?)<')
		self.goldPat = re.compile('icon-gold">(.*?)<')
		#拍卖物品url前缀
		self.baseURL = r"https://www.battlenet.com.cn/wow/zh/vault/character/auction/browse?reverse=false&sort=unitBuyout&itemId="

		#其他
		self.opener = 0
		#初始化
		self.initOpener()


	def initOpener(self):
		cj = http.cookiejar.CookieJar()
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
		urllib.request.install_opener(self.opener)

	def getHtml(self,url):
		req = urllib.request.Request(url)
		req.add_header('User-Agent',self.user_agent)
		req.add_header('Cookie',self.Cookie)
		res = urllib.request.urlopen(req)
		html = res.read()
		res.close()
		return html.decode('utf-8')

	#获取物品最低一口价
	def getItemBuyout(self,itemId):
		itemHtml = self.getHtml(self.baseURL + itemId)
		goldList = self.goldPat.findall(itemHtml)
		count = len(goldList)
		#未查找到物品
		if count == 3:
			return "0"
		silverList = self.silverPat.findall(itemHtml)
		copperList = self.copperPat.findall(itemHtml)
		lowGold = goldList[1]
		lowSilver = silverList[1]
		lowCopper = copperList[1]
		return "%sg%ss%sc"%(lowGold,lowSilver,lowCopper)

	def getInterestPrice(self):
		for itemId in self.vidList:
			print(itemId)
			print(self.getItemBuyout(itemId))


if __name__=="__main__":
	mp = MyPrecious()
	itemUrl = mp.baseURL + "127037"
	itemHtml = mp.getHtml(itemUrl)
	print(itemUrl)
	file = open("aaa.txt",'w',encoding ='utf-8')
	file.write(itemHtml)
	file.close
	while 1:
		mp.getInterestPrice()
		time.sleep(50)