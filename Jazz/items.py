from scrapy.item import Item, Field

class Album(Item):
	recSeries = Field()
	title = Field()
	songList = Field()
	personnelList = Field()
	dateList = Field()
	locList = Field()


