from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request, Response
from Jazz.items import Album
import re

##################################
# Define and Compile Expressions #
##################################

'''
Expression Name:	Purpose:
p1			Grabs record series blocks
q1			Grabs record series block names
p2			Takes record type block, splits into album blocks
p3			Takes album block, extracts title

note: For the following RE's we assume that existence of one instance of a feature implies existence of the other features, so they all share 		common indices when extracted. That is if these expressions return lists of length greaterthan 1 item, then we safely assume all the 
	n-th items the different lists are assosciated to the same block of information.

p4			Takes album block, extracts personnel lists
p5			Takes album block, extracts location date strings
p6			Takes album block, extracts song lists

note: The following RE's are for the cleanup functions

s1			Cleans the songlist
s2			Detects the date in dateLoc
s3			Detects the loc  "	"
s4			Detects player, instrument tuples in personnel
s5			Used for removing those pesky \n signs
'''

p1 = re.compile(r'<h2>.*?(?=<h2>|$)', re.DOTALL) 
q1 = re.compile(r"(?<=<h2>).*?(?=</h2>)") 
p2 = re.compile(r'<h3>.*?(?=<h3>|$)', re.DOTALL) 
p3 = re.compile(r'(?<=nbsp; ).*(?=</a>)', re.DOTALL) 
p4 = re.compile(r'(?<=</h3>).*?(?=<div class="date">)|(?<=</table>).*?(?=<div class="date">)', re.DOTALL)
p5 = re.compile(r'(?<=<div class="date">).*?(?=</div>)', re.DOTALL) 
p6 = re.compile(r'(?<=<table width="100%">).*?(?=</table>)', re.DOTALL) 
s1 = re.compile(r"(?<=</td><td>).+?(?=\n</td>)",re.DOTALL)
s2 = re.compile(r"(?<=, )\w+? [0-9]+, [0-9]+")
s3 = re.compile(r".+?(?=, \w+? [0-9]+, [0-9]+)")
s4 = re.compile(r"(.+?)[(](.+?)[)]")
s5 = re.compile(r"\n")

############################
# Define Cleanup Functions #
############################

def songClean(songList):
	cleanList=[]
	for song in songList:
		entry=s1.findall(song)		
		cleanList.append(entry)
	return cleanList

def dateClean(dateLocList):
	dateList=[]
	for dateLoc in dateLocList:
		try:
			date = s2.findall(dateLoc)[0]
		except IndexError:		
			date = ""			
		dateList.append(date)
	for i in xrange(len(dateList)):
		if dateList[i]=="":
			if i==0:
				dateList[i]="NA"
			else:
				dateList[i]=dateList[i-1]
	return dateList

def locClean(dateLocList):
	locList=[]
	for dateLoc in dateLocList:
		try:
			loc = s3.findall(dateLoc)[0]
		except IndexError:
			loc = ""
		locList.append(loc)
	for i in xrange(len(locList)):
		if locList[i]=="":
			if i==0:
				locList[i]="NA"
			else:
				locList[i]=locList[i-1]
	return locList

def personnelClean(personnelList):
	out=[]
	for subList in personnelList:
		subList = s5.sub("",subList)
		subOut = s4.findall(subList)
		corrected = []
		for i in xrange(len(subOut)):
			try:
				if "," in subOut[i][0]:
					offender=subOut.pop(i)
					for name in offender[0].split(", "):
						corrected.append((name,offender[1]))
			except IndexError:
				pass
		subOut = subOut + corrected
		out.append(subOut)
	return out

#######################
# Main crawler script #
#######################

class JazzSpider(Spider):
	'''
		The idea here is to scrape all of the URLs for different studio's discographies, then scrape album info from each subsequent
	webpage. Note: Since each studio has multiple pages we're gonna need an intermediary function to get us to the final songlists. The 
	first parse function creates an AlbumList item and then generates the list of URLs to check next. The for loop then calls the parse2
	function on each of these URLs passing along the AlbumList so that it can be populated and returned. The parse2 function operates as
	a typical parse function in that it just scrapes data to fill the required song and album fields for each album.

	Required Fields:

	AlbumList - albums (STR),
	Album - title (STR), songlist (LIST)
	Song - songTitle(STR), personnel (LIST of STR), recordingDate (), recordingLoc ()
	
	'''

	#Spider Info:
	
	name = 'Jazz'
	allowed_domains = ['jazzdisco.org']
	start_urls = ['http://www.jazzdisco.org']
	
	# Parse 1: This function takes in the homepage of the database
	#	Then calls parse2 on each link to a record company's
	#	discography page.
	
	def parse(self, response):

		albumList = []
		
		sel = Selector(response)
		sel = sel.xpath('/html/body/div/div[2]/div/div/div/table/tr/td[3]/ul')
		links = sel[1].xpath('li/a/@href').extract()
		
		for link in links:
			request = Request( 'http://www.jazzdisco.org' + link , callback = self.parse2 )
			request.meta[ 'albumList' ] = albumList 
			yield request

	# Parse 2: This function operates similarly to the Parse 1 fct.
	
	def parse2(self, response):

		albumList = response.meta['albumList']
		
		sel = Selector(response)
		sel = sel.xpath('/html/body/div/div[2]/div/div/div/ul[1]')		
		links = sel.xpath('li/a[1]/@href').extract()

		for link in links:
			request = Request( 'http://www.jazzdisco.org' + link , callback = self.parse3 )
			request.meta[ 'albumList' ] = albumList 
			yield request
	
	#Parse 3: Due to the flat nature of the source HTML, this parsing function uses a considerably more complicated approach of
	#	breaking apart the text using regular expressions.
	
	def parse3(self, response):

		albumList = response.meta['albumList']
		recList = p1.findall(doc)
			for rec in recList:
	
				recSeries = q1.search(rec).group()
				recList = p2.findall(rec)

				for album in recList:

					out = Album()
		
					out['recSeries'] = recSeries

					title=p3.findall(album)[0]
					out['title'] = title
		
					personnel = p4.findall(album)
					personnel = personnelClean(personnel)
					out['personnelList'] = personnel

					dateLoc = p5.findall(album)
					dateList = dateClean(dateLoc)
					locList = locClean(dateLoc)
					out['dateList'] = dateList
					out['locList'] = locList

					songs = p6.findall(album)
					songs = songClean(songs)
					out['songList'] = songs

					albumList.append(out)
		return albumList
		

	



"""	
	def dateLocSplit(self, strIn):
		out = []
		strIn = strIn.lower()
		monthlist = ['(january)', '(february)', '(march)', '(april)', '(may)', '(june)', '(july)', '(august)', 				'(september)','(october)','(november)','(december)']
		splitStr = re.split(monthlist,strIn)
		loc = ''.join(splitStr[:-2])
		date = ''.join(splitStr[-2:])
		out.append(loc)
		out.append(date)
		return out

class JazzTestSpider(Spider):
	
	name = 'JazzTest'
	allowed_domains=['jazzdisco.org']
	start_urls=['http://www.jazzdisco.org/atlantic-records/catalog-1200-series/']
	pattern=re.compile(r'.xa0')

	def parse(self, response):
		albumList = AlbumList()
		albumList['albums']=[]
		
		sel = Selector(response)
		sel = sel.xpath('//*[@id="catalog-data"]').extract()[0]

		blocks = sel.split("<h3>")
		print blocks[1:10]
		for block in blocks:
			title = JazzTestSpider.pattern.search(block)
				

"""
