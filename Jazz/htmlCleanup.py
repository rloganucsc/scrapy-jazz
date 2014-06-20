# -*- coding: utf-8 -*-
"""
Created on Mon Jun 09 12:45:16 2014

@title: HTML Cleanup Functions
@author: Robert
"""

import re

"""
Function:       rm_wspc_trail

Input:          string
Output:         string
Used By:        fix_multipersonnel

Description:    Iteratively removes any whitespace at the beggining or end of 
                the input_string then returns the trimmed string.
"""

def rm_wspc_trail(input_string):
    try_again = False
    try:
        if (input_string != "")&(input_string != " ")&(input_string != None):
            if input_string[0] == " ":
                input_string = input_string[1:]
                try_again = True
            if input_string[-1] == " ":
                input_string = input_string[:-1]
                try_again = True
        else:
            input_string = ""
        if try_again:
            input_string = rm_wspc_trail(input_string)
        return(input_string)
    except:
        print("ERROR: rm_wspc_trail used incorrectly")
        print(input_string)

"""
Function:       rm_html_tags

Input:          string
Output:         string
Used By:        fix_multipersonnel

Description:    Removes any html tags at the beggining of the input_string then 
                returns the trimmed string.
"""

html_tag=re.compile(r"<.*?>") 

def rm_html_tags(input_string):
    try:
        input_string = html_tag.sub("",input_string)
        return(input_string)
    except:
        print("ERROR: rm_html_tags used incorrectly")
        print(input_string)

"""
Function:       fix_multipersonnel

Input:          list
Output:         list
Used By:        fix_listings

Description:    Takes in an entry in a personnel list, and creates individual 
                entries when multiple personnel are credited to a single 
                instrument or vice versa.
                I.E. ("Bob,Sue","Bass,Horn")-->("Bob","Bass"),("Bob","Horn")...
                                            ...("Sue","Bass"),("Sue","Horn")
"""

def fix_multipersonnel(input_list):
    output_list = []
    try:
        if input_list != []:
            for personnel_tuple in input_list:
                name_list = personnel_tuple[0].split(",")
                inst_list = personnel_tuple[1].split(",")
                for name in name_list:
                    for inst in inst_list:
                        name = rm_html_tags(name)
                        name = rm_wspc_trail(name)
                        inst = rm_wspc_trail(inst)
                        output_list.append((name,inst))
        return output_list
    except:
        print("ERROR: fix_multipersonnel used incorrectly")

"""
Function:       gen_playlists

Input:          list, list
Output:         list, list
Used By:        fix_listings

Description:    Function parses notes in inst text to determine which songs
                each personnel member played on. Takes in a personnel_list
                as well as a song_list and spits out a playlist (i.e. a vector
                each of whose entries represents a player, and contains a list
                of all of the indexes of the songs they played on) as well as
                a personnel_list which has been cleaned of all performance
                notes.
"""

note_detector=re.compile(" -[^,-]*")

def gen_playlists(personnel_list,song_list):
    playlists = []
    cleaned_personnel_list = []
    for personnel_tuple in personnel_list:
        inst = personnel_tuple[1]
        
        #Find any notes for personnel & clean inst string        
        try:        
            notes = note_detector.findall(inst)[0][2:]
            notes = notes.split(",")
        except IndexError:
            notes = []
        inst = note_detector.sub("",inst)
        
        #Construct list of songs artist performed on
        appears_on = []
        if notes == []:
            appears_on = range(0,len(song_list))
        for note in notes:
            note = note.split("/")
            if len(note) == 1:
                appears_on.append(int(note[0]))
            if len(note) == 2:
                a = int(note[0])
                b = int(note[1])
                appears_on = appears_on+range(a-1,b)
        playlists.append(appears_on)
        cleaned_personnel_list.append((personnel_tuple[0],inst))
    return playlists, cleaned_personnel_list

"""
Function:       update_group

Input:          list, list
Output:         list
Used By:        fix_listings

Description:    A grouping is a list of indices which has been broken into
                sublists. I.E. [[1,4,5],[2,3]] is a grouping of the numbers
                [1,2,3,4,5]. Given that performance notes imply that certain
                players will not have played on certain songs, we want to
                create a grouping of song indexes such that all of the songs
                whose index are in the same subgroup/sublist have the same
                personnel. We also want as few subgroups as possible. This
                function achieves this goal when iterated over the list of all
                personnel, by splitting up subgroups of the input 'group' to
                account for the 'update' of another player's playlist.
"""

def update_group(group,update):
    out = []
    for subgroup in group:
        intersection = list(set(subgroup) & set(update))
        compliment = list(set(subgroup) - set(update))
        if intersection != []:
            out.append(intersection)
        if compliment != []:
            out.append(compliment)
    return out
    
"""
Function:       fix_listings

Input:          list, list, list
Output:         list, list, list
Used By:        

Description:    Uses all of the above functions to fix any known errors with 
                the way the Jazz crawler populates the personnelList, songList,
                and dateList fields in an album item.
"""

def fix_listings(personnel_list,song_list,date):
    
    #Initialize outputs
    output_personnel_list = []
    output_song_list = []
    output_date_list = []
    
    #Generate playlists for each player in personnel
    playlists, personnel_list = gen_playlists(personnel_list,song_list)
    
    #Generate grouping of song indices so that all indices in same subgroup
    #represent songs which share the same personnel
    group = [range(len(song_list))]
    for playlist in playlists:
        group = update_group(group,playlist)
    
    #Use grouping information to split up personnel, song, and date lists so
    #they can be properly inserted into MySQL tables and interpreted accurately
    for subgroup in group:
        output_date_list.append(date)
        song_sublist=[]
        personnel_sublist=[]
        for i in subgroup:
            song_sublist.append(song_list[i])
            for j in xrange(len(personnel_list)):
                if i in playlists[j]:
                    if personnel_list[j] not in personnel_sublist:
                        personnel_sublist.append(personnel_list[j])
        output_song_list.append(song_sublist)
        personnel_sublist = fix_multipersonnel(personnel_sublist)
        output_personnel_list.append(personnel_sublist) 
    
    #Return properly formatted output    
    return output_personnel_list,output_song_list,output_date_list

"""
Function:       main

Input:          list, list, list
Output:         list, list, list
Used By:        JazzCrawler

Description:    Applies the 'fix_listings' function over lists composed of 
                lists.
"""

                    
def main(personnel_list,song_list,date_list):
    num_entries = len(personnel_list)
    corrected_personnel = []
    corrected_song = []
    corrected_date = []
    for index in xrange(num_entries):
        personnel = personnel_list[index]
        songs = song_list[index]
        date = date_list[index]
        personnel,songs,date = fix_listings(personnel,songs,date)
        corrected_personnel += personnel
        corrected_song += songs
        corrected_date += date
    return corrected_personnel,corrected_song,corrected_date
                
            

        
        
        
        
    
        
    
