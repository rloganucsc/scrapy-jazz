# -*- coding: utf-8 -*-
"""
Created on Mon Jun 09 12:21:31 2014

@title: SQL Test Scripts
@author: Robert
@description: This script is for testing out the behaviour of functions in the
    MySQL pipeline
"""
import MySQLdb

"""
Goal is to commit the following item to the development database:
RecordLabel: testLabel
RecordSeries: testSeries
"""
'''
LabelName = "Robby Records"
SeriesName = "Vinyl 800 Series"
AlbumName = "Songs of Derpface - Remastered"
BandLeader = "Rugsberto Malone"
DateList=['1942','1943','1943']
SongList=[["ABD124","I'll Tell"],["Ballsweat Symphony"],["Mal Tortuga","Gigante Gazungas"]]
PersonnelList=[[["Timmdo","Piano"],["Vinhdo","Sax"]],[["Rugsby","Dudemanchego"]],["Rugsby","Dudemanchego"]]
'''

class MySQLPipeline():
    
    def __init__(self):    
        #Define connection
        self.conn = MySQLdb.connect("192.168.0.10","jazzAdmin","Banana123","jazzDBDevelopment")
        
    def process_item(self,item,spider):
        
        LabelName = item['LabelName']
        SeriesName = item['SeriesName']
        AlbumName = item['AlbumName']
        BandLeader = item['BandLeader']
        SongList = item['SongList']
        PersonnelList = item['PersonnelList']
        DateList = item['DateList']
        
        with self.conn:
            #Create a cursor object to execute queries
        
            cursor = self.conn.cursor()
            
            #Lookup or insert LabelName in RecordLabels table, extract LabelID
            
            cursor.execute("SELECT (LabelID) FROM RecordLabels WHERE LabelName = %s",(LabelName))
            LabelID=cursor.fetchone()
            if LabelID==None:
                cursor.execute("INSERT INTO RecordLabels (LabelName) VALUES (%s)",(LabelName))
                cursor.execute("SELECT LAST_INSERT_ID()")
                LabelID=cursor.fetchone()[0]
                
            else:
                LabelID=LabelID[0]
            
            print "Label_ID = "+str(LabelID)
            
            #Lookup or insert SeriesName in RecordSeries table, extract SeriesID
            
            cursor.execute("SELECT (SeriesID) FROM RecordSeries WHERE SeriesName = %s",(SeriesName))
            SeriesID=cursor.fetchone()
            if SeriesID==None:
                cursor.execute("INSERT INTO RecordSeries (LabelID,SeriesName) VALUES (%s,%s)",(LabelID,SeriesName))
                cursor.execute("SELECT LAST_INSERT_ID()")
                SeriesID=cursor.fetchone()[0]   
            else:
                SeriesID=SeriesID[0]
                
            print "Series_ID = "+str(SeriesID)
                
            #Lookup or insert AlbumName and BandLeader in Albums table, extract AlbumID
                
            cursor.execute("""  SELECT (AlbumID) FROM Albums 
                                WHERE AlbumName = %s AND BandLeader = %s AND SeriesID = %s""",
                                (AlbumName,BandLeader,SeriesID))
            AlbumID=cursor.fetchone()
            if AlbumID==None:
                cursor.execute("""  INSERT INTO Albums (SeriesID,AlbumName,BandLeader)
                                    VALUES (%s,%s,%s)""",
                                    (SeriesID,AlbumName,BandLeader))
                cursor.execute("SELECT LAST_INSERT_ID()")
                AlbumID=cursor.fetchone()[0]
            else:
                AlbumID=AlbumID[0]
                
                # Lazy fix to avoid session duplication
                
                return item
                print "You should never see this statement if everything works correctly"
                
            print "Album_ID = "+str(AlbumID)
            
            #Insert Dates from DateList into the Sessions table
            for i in xrange(len(DateList)):
                cursor.execute("""  INSERT INTO Sessions (AlbumID,SessionDate)
                                    VALUES (%s, %s))""",
                                    (AlbumID,DateList[i]))
                cursor.execute("SELECT LAST_INSERT_ID()")
                SessionID=cursor.fetchone()
                try:
                    for Song in SongList[i]:
                        cursor.execute("""  INSERT INTO Songs (SessionID,SongName)
                                            VALUES (%s, %s)""",
                                            (SessionID,Song))
                except:
                    print "Song Insertion Error, Session: "+str(SessionID)
                try:
                    for j in xrange(len(PersonnelList[i])):
                        cursor.execute("""  INSERT INTO Personnel (SessionID,Musician,Instrument)
                                            VALUES (%s, %s, %s)""",
                                            (SessionID,PersonnelList[i][j][0],PersonnelList[i][j][1]))
                except:
                    print "Personnel Insertion Error, Session: "+str(SessionID)
            
            return item
    