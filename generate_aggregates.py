import json,sys

with open("jazz_db.json") as jazz_db:
    db_length=-1
    for line in jazz_db:
        db_length+=1

def recordsPerYear():
    output = {}
    with open("jazz_db.json") as jazz_db:
        index=0
        for album in jazz_db:
            if index==0:
                album = album[1:]
            if index==db_length:
                album = album[:-1]
            else:
                album = album[:-2]
            try:
                album_dict = json.loads(album)
                album_dates = album_dict["DateList"]
                try:
                    if (album_dates[0]!="NA"):
                        year_sum=0
                        try:
                            for date in album_dates:
                                year=int(date[-4:])
                                year_sum+=year
                            mean_year=year_sum/len(album_dates)
                            mean_year=int(round(mean_year))
                            if mean_year in output:
                                output[mean_year]+=1
                            else:
                                output[mean_year]=1
                        except ValueError:
                            pass
                except IndexError:
                    pass
            except:
                print index
                print album
                print sys.exc_info()[0]
                break
            index+=1
    return output

def songCount():
    songs = {}
    with open("jazz_db.json") as jazz_db:
        index=0
        for album in jazz_db:
            if index==0:
                album = album[1:]
            if index==db_length:
                album = album[:-1]
            else:
                album = album[:-2]
            try:
                album_dict = json.loads(album)
                songList=album_dict["SongList"]

                for subList in songList:
                    for song in subList:
                         song = song.lower()
                         if song in songs:
                             songs[song]+=1
                         else:
                             songs[song]=1
                            
            except:
                print index
                print album
                print sys.exc_info()[0]
                break
            index+=1
    return songs
 
            
recordsPerYear = recordsPerYear()
songCount = songCount()
