# -*- coding: utf-8 -*-
"""
Created on Tues Jun 10 15:40:31 2014

@title: Items
@author: Robert
"""

import MySQLdb
from scrapy.exceptions import DropItem

'''
class MySQLPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            user="jazzAdmin",
            passwd="Banana123",
            db="JazzDBDevelopment",
            host="192.168.0.10:3306",
            charset="utf8",
            use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        try:
            self.cursor.execute("""INSERT INTO RecordLabels (LabelName)
                        VALUES (%s)""",(item['']))
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
'''

class EmptyItemPipeline(object):
    
    def process_item(self,item,spider):
        if (item["SongList"]==[]) & (item["PersonnelList"]==[]):
            raise DropItem()
        else:
            return item
            
class DuplicatesPipeline(object):

    def __init__(self):
        self.items_seen = set()

    def process_item(self, item, spider):
        clause = item in self.items_seen
        if clause:
            raise DropItem()
        else:
            self.items_seen.add(item)
            return item
            
class MySQLPipeline():
    
    def __init__(self):    
        #Define connection
        self.conn = MySQLdb.connect("192.168.0.10","jazzAdmin","Banana123","jazzDBDevelopment",charset='utf8')
        
        #Create a cursor object to perform queries
        self.cursor = self.conn.cursor()
        
    def process_item(self,item,spider):
        
        LabelName = item['LabelName']
        SeriesName = item['SeriesName']
        AlbumName = item['AlbumName']
        BandLeader = item['BandLeader']
        SongList = item['SongList']
        PersonnelList = item['PersonnelList']
        DateList = item['DateList']
        
        #Lookup or insert LabelName in RecordLabels table, extract LabelID
        
        self.cursor.execute("SELECT (LabelID) FROM RecordLabels WHERE LabelName = %s",(LabelName))
        LabelID=self.cursor.fetchone()
        if LabelID==None:
            self.cursor.execute("INSERT INTO RecordLabels (LabelName) VALUES (%s)",(LabelName))
            self.conn.commit()
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            LabelID=self.cursor.fetchone()[0]
            
        else:
            LabelID=LabelID[0]
        
        #Lookup or insert SeriesName in RecordSeries table, extract SeriesID
        
        self.cursor.execute("SELECT (SeriesID) FROM RecordSeries WHERE SeriesName = %s",(SeriesName))
        SeriesID=self.cursor.fetchone()
        if SeriesID==None:
            self.cursor.execute("INSERT INTO RecordSeries (LabelID,SeriesName) VALUES (%s,%s)",(LabelID,SeriesName))
            self.conn.commit()
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            SeriesID=self.cursor.fetchone()[0]   
        else:
            SeriesID=SeriesID[0]
        #Lookup or insert AlbumName and BandLeader in Albums table, extract AlbumID
            
        self.cursor.execute("""  SELECT (AlbumID) FROM Albums 
                            WHERE AlbumName = %s AND BandLeader = %s AND SeriesID = %s""",
                            (AlbumName,BandLeader,SeriesID))
        AlbumID=self.cursor.fetchone()
        if AlbumID==None:
            self.cursor.execute("""  INSERT INTO Albums (SeriesID,AlbumName,BandLeader)
                                VALUES (%s,%s,%s)""",
                                (SeriesID,AlbumName,BandLeader))
            self.conn.commit()
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            AlbumID=self.cursor.fetchone()[0]  
            Duplicate=False
        else:
            AlbumID=AlbumID[0]
            Duplicate=True
        
        #Insert Dates from DateList into the Sessions table, then accordingly
        #insert corresponding Song Titles with SessionID into the Songs table
        #and insert corresponding Musician,Instrument tuples with SessionID
        #into the Personnel table.
        if not Duplicate:
            for i in xrange(len(DateList)):
                try:
                    self.cursor.execute(""" INSERT INTO Sessions (AlbumID,SessionDate)
                                            VALUES (%s,%s)""",
                                            (AlbumID,str(DateList[i])))
                    self.conn.commit()
                    self.cursor.execute("SELECT LAST_INSERT_ID()")
                    SessionID=self.cursor.fetchone()[0]
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    
                try:
                    for Song in SongList[i]:
                        self.cursor.execute("""  INSERT INTO Songs (SessionID,SongName)
                                            VALUES (%s, %s)""",
                                            (SessionID,Song))
                        self.conn.commit()
                except:
                    print "Song Insertion Error, Session: "+str(SessionID)
                try:
                    for j in xrange(len(PersonnelList[i])):
                        self.cursor.execute("""  INSERT INTO Personnel (SessionID,Musician,Instrument)
                                            VALUES (%s, %s, %s)""",
                                            (SessionID,PersonnelList[i][j][0],PersonnelList[i][j][1]))
                        self.conn.commit()
                except:
                    print "Personnel Insertion Error, Session: "+str(SessionID)
        
        
        return item
