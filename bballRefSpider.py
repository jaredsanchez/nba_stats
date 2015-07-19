import scrapy
from scrapy.selector import HtmlXPathSelector


class BballRefSpider(scrapy.Spider):
	name = 'bballRef'
	start_urls = ['http://www.basketball-reference.com/leagues/NBA_2015_games.html?lid=header_seasons']

	def parse(self, response):
		xps = HtmlXPathSelector(response)
		#can try to select each table in line below, and then use class names in for loops
		rows = xps.select('//tr/td/a') #select all rows in tables with links
		rows = rows[1::4] #select only the box score elements (eliminate team/date links)
		# regSeasonRows = rows[0:1230] #reg season rows
		regSeasonRows = rows[0:2]
		playoffRows = rows[1230:] #playoff rows
		
		#extract reg seasons urls
		for row in regSeasonRows:
			boxScoreURL = row.xpath('@href').extract()
			fullURL = 'http://www.basketball-reference.com/' + boxScoreURL[0]
			req1 = scrapy.Request(fullURL, callback=self.parseBoxScoreResponse)
			self.makeRequest(boxScore)
			yield req1

		#extract playoff urls
		# for row in playoffRows:
		# 	boxScoreURL = row.xpath('@href').extract()
		# 	fullURL = 'http://www.basketball-reference.com/' + boxScoreURL[0]
		# 	req2 = scrapy.Request(fullURL, callback=self.parseBoxScoreResponse)
			# self.makeRequest(boxScore)
			# yield req2


	# def makeRequest(self, url):
	# 	fullURL = 'http://www.basketball-reference.com/' + url[0]
	# 	return scrapy.Request(fullURL, callback=self.parseBoxScoreResponse)


	def parseBoxScoreResponse(self, response):
		print 'PRINTING SUCCESSFUL REQUEST/RESPONSE'