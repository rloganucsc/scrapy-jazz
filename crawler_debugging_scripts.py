"""
Created on Sat Jun 07 10:34:48 2014

@title: Bug Catcher
@author: Robert
@description: This code searches through the .json file to find duplicates of
    albums, albums with incorrectly formatted date and location fields, and
    albums with no songs.
"""
import json

class Debugger():
    def __init__(self):
        self.db_length = self.getLength()
    
    def lineClean(self,line,index):
        if index==0:
            out = line[1:-2]
        elif index==self.db_length:
            out = line[:-1]
        else:
            out = line[:-2]
        return out
    
    def line2Dict(self,line):
        try:
            out=json.loads(line)
            return out
        except:
            print "Error Converting Following Line:"
            print line
        
        
    def getLength(self):
        with open("jazz_db.json") as jazz_db:
            db_length=-1
            for line in jazz_db:
                db_length+=1
        return db_length
    
    def getDateErrors(self):
        with open("jazz_db.json") as jazz_db:
            errors = 0
            index = 0
            for line in jazz_db:
                if errors <= 100:
                    line = self.lineClean(line,index)
                    album_dict = self.line2Dict(line)
                    try:
                        date_fields = album_dict["DateList"]
                        if date_fields == []:
                            print "Index: "+str(index)
                            print "No Date Info Extracted"
                            print line
                            errors +=1
                        for date in date_fields:
                            if date=="NA":
                                print "Index: "+str(index)
                                print "Unknown Date"
                                print album_dict
                                errors+=1
                                break
                            try:
                                int(date[-4:])
                            except:
                                print date[-4:]
                                print "Index: "+str(index)
                                print "Transcription Error"
                                print album_dict
                                errors+=1
                    except TypeError,KeyError:
                        pass

                else:
                    break
                index += 1
                
                
        