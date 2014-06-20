02/??/2014 Project Initially Created
06/03/2014 1st Successful Scrape Performed 
06/04/2014 Scripts for using data in .JSON file created
	   First Visualization Made - Records Per Year
06/06/2014 Descision made to pipe all data to MySQL server
	   Day spent setting up test server and starting
	   to write pipeline
06/07/2014 Debugging regular expressions.
06/12/2014 MySQL pipeline and regular expressions almost fully functional.
	   Lazy fix for date catching method, decided to stop tracking location.
06/16/2014 Entire site successfully scraped to MySQL database
06/17/2014 Cleaning Data

Issues/Bugs/Observations:

Python Crawler:
-Issue with date/location re's, not catching years in strings like 'Dec 12, 13, 1957'
-Above issue not caused by the p5 RE, we've checked every entry with an unextracted date does not have a date to extract.
-There appears to is a lack of consistency in the way recording session locations and dates are reported. In the following 
examples there is optional location with or without title, optional month, and always a year. For now, we fix this issue by 
only extracting year and not worrying about location.
	
ex:Rudy Van Gelder Studio, Englewood Cliffs, NJ, October 10, 1961
ex:The Bottom Line, NYC, February 20-23, 1975
ex:NYC, December 12, 1956
ex:1975
ex:Los Angeles, CA, circa 1975
ex:NYC, 1976

-Issue with bandleader name extraction for albums with titles such as "Dave Brubeck Quartet"
-Multi-bandleader names currently are cunjuncted, for example "Ella Fitzgerald/Joe Pass"
-For MySQL pipeline, we can avoid duplicating things such as LabelName and SeriesName. Assuming all (AlbumName,BandLeader) tuples are unique to each record series we can also avoid duplicating albums. Unfortunately, there is no reason for the session dates to be unique on an album, so to avoid duplicating sessions on an album we currently just break our pipeline at the point that we know an album already appears in the database. The consequence of this is that if we re-run our crawler to update new information, it will miss any updates to already existing albums. Since we do not track unfinished albums in the database this should not be a huge issue, however we should try to observe whether the website retroactively adds information to existing 'finished' albums. If this is the case then we will need to implement a different approach to updating the remaining fields.
-Record Note Detector Not reading in last note in list

SQL Tables:
-In the personnel table, we can get a basic sense of which artists were the most prolific in terms of recording sessions.