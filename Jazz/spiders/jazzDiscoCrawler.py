from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from Jazz.items import Album
import Jazz.htmlCleanup
import re

##################################
# Define and Compile Expressions #
##################################

'''
Expression Name:	Purpose:
p1			Grabs record series blocks
q1			Grabs record series block names
p2			Takes record type block, splits into album blocks
p3			Takes album block, extracts AlbumName

note: For the following RE's we assume that existence of one instance of a feature implies existence of the other features, so they all share
common indices when extracted. That is if these expressions return lists of length greaterthan 1 item, then we safely assume all the n-th
items the different lists are assosciated to the same block of information.

p4			Takes album block, extracts personnel lists
p5			Takes album block, extracts location date strings
p6			Takes album block, extracts song lists

note: The following RE's are for the cleanup functions

s1			Cleans the SongList
s2			Detects the date in dateLoc
s3			Detects the loc  "	"
s4			Detects player, instrument tuples in personnel
s5			Used for removing those pesky \n signs
'''

p1 = re.compile(r'<h2>.*?(?=<h2>|$)', re.DOTALL) 
q1 = re.compile(r"(?<=<h2>).*?(?=</h2>)") 
p2 = re.compile(r'<h3>.*?(?=<h3>|$)', re.DOTALL) 
p3 = re.compile(r'(?<=\xa0 ).*?(?=</a>)', re.DOTALL) 
p4 = re.compile(r'(?<=</h3>).*?(?=<div class="date">)|(?<=</table>).*?(?=<div class="date">)', re.DOTALL)
p5 = re.compile(r'(?<=<div class="date">).*?(?=</div>)', re.DOTALL) 
p6 = re.compile(r'(?<=<table width="100%">).*?(?=</table>)', re.DOTALL) 
s1 = re.compile(r"(?<=</td><td>).+?(?=\n</td>)",re.DOTALL)
s2 = re.compile(r"[0-9]{4}")
#s3 = re.compile(r".+?(?=, \w+? [0-9]{2}.*?[0-9]{4})")
s4 = re.compile(r"(.*?)[(](.*?)[)]")
s5 = re.compile(r"\n")

############################
# Define Cleanup Functions #
############################

def songClean(SongList):
    cleanList=[]
    for song in SongList:
        entry=s1.findall(song)		
        cleanList.append(entry)
    return cleanList

def dateClean(dateLocList):
    DateList=[]
    for dateLoc in dateLocList:
        try:
            date = s2.findall(dateLoc)[0]
        except IndexError:
            date = ""
        DateList.append(date)
    for i in xrange(len(DateList)):
        if DateList[i]=="":
            if i==0:
                DateList[i]="NA"
            else:
                DateList[i]=DateList[i-1]
    return DateList
    
'''
def locClean(dateLocList):
    LocList=[]
    for dateLoc in dateLocList:
        try:
            loc = s3.findall(dateLoc)[0]
        except IndexError:
            loc = ""
            LocList.append(loc)
    for i in xrange(len(LocList)):
        if LocList[i]=="":
            if i==0:
                LocList[i]="NA"
            else:
                LocList[i]=LocList[i-1]
    return LocList
'''

def personnelClean(PersonnelList):
    out=[]
    for subList in PersonnelList:
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
            request = Request( 'http://www.jazzdisco.org' + link,
                              callback = self.parse2 )
            request.meta['albumList'] = albumList
            request.meta['labelName'] = link.replace("-"," ").replace("/","").title()
            yield request

	# Parse 2: This function operates similarly to the Parse 1 fct.

    def parse2(self, response):
        albumList = response.meta['albumList']
        labelName = response.meta['labelName']
        
        sel = Selector(response)
        sel = sel.xpath('/html/body/div/div[2]/div/div/div/ul[1]')		
        links = sel.xpath('li/a[1]/@href').extract()
        
        for link in links:
            request = Request( 'http://www.jazzdisco.org' + link,
                              callback = self.parse3 )
            request.meta['albumList'] = albumList
            request.meta['labelName'] = labelName
            yield request
	
	#Parse 3: Due to the flat nature of the source HTML, this parsing function uses a considerably more complicated approach of
	#	breaking apart the text using regular expressions
    def parse3(self, response):
        albumList = response.meta['albumList']
        labelName = response.meta['labelName']
        
        sel = Selector(response)
        doc = sel.xpath('//div[@id="catalog-data"]').extract()
        recList = p1.findall(doc[0])
        for rec in recList:
            
            seriesName = q1.search(rec).group()
            recList = p2.findall(rec)
            
            for album in recList:
    
                out = Album()
                
                out['LabelName'] = labelName
                out['SeriesName'] = seriesName
    
                title=p3.findall(album)[0]
                title=title.split(" - ")
                if len(title)==2:
                    bandLeader = title[0]
                    albumName=title[1]
                else:
                    bandLeader = "NA"
                    albumName = title[0]
                out['BandLeader'] = bandLeader
                out['AlbumName'] = albumName
    
                personnel = p4.findall(album)
                personnel = personnelClean(personnel)
    
                dateLoc = p5.findall(album)
                dateList = dateClean(dateLoc)
                #LocList = locClean(dateLoc)
                #out['DateList'] = dateList
                #out['LocList'] = locList
    
                songs = p6.findall(album)
                songs = songClean(songs)
                
                personnel,songs,dateList=Jazz.htmlCleanup.main(
                    personnel,songs,dateList)
                
                out['PersonnelList'] = personnel    
                out['DateList'] = dateList
                out['SongList'] = songs
                                
                albumList.append(out)
		
            return albumList
		

	



