# -*- coding: utf-8 -*-
"""
Created in Feb 2014

@title: Items
@author: Robert
"""

from scrapy.item import Item, Field

class Album(Item):
    LabelName = Field()
    SeriesName = Field()
    AlbumName = Field()
    BandLeader = Field()
    SongList = Field()
    PersonnelList = Field()
    DateList = Field()
    #LocList = Field()


