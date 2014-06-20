USE jazzDBDevelopment;

SELECT Instrument, COUNT(*) FROM Personnel GROUP BY Instrument HAVING COUNT(*)>2;
SELECT Musician, COUNT(*) FROM Personnel GROUP BY Musician;

SET SQL_SAFE_UPDATES = 0;

#Insert Primary Keys into Personnel and Song tables for easy editing###########
ALTER TABLE Personnel ADD COLUMN PersonnelID int PRIMARY KEY AUTO_INCREMENT;
ALTER TABLE Songs ADD COLUMN SongID int PRIMARY KEY AUTO_INCREMENT;


SELECT * FROM Personnel WHERE LOCATE('including ', Musician) != 0;
SELECT * FROM Personnel WHERE Musician = 'Annie Ross';
SELECT * FROM Personnel WHERE Instrument = '4';
SELECT * FROM Personnel WHERE SessionID = 26464;
SELECT AlbumName FROM Albums WHERE 
	AlbumID = (SELECT AlbumID FROM Sessions WHERE SessionID=7890);

SELECT SongName,count(*) FROM Songs GROUP BY SongName HAVING COUNT(*)>70;

#General Fixes to Whole Personnel Table########################################

#Eliminate unknown and unidentified musicians
DELETE FROM Personnel WHERE LOCATE('unknown', Musician)!=0;
DELETE FROM Personnel WHERE LOCATE('unidentified', Musician)!=0;

#Remove adverb prefixes
UPDATE Personnel SET Musician=REPLACE(Musician,'with ','') WHERE 
	LOCATE('with ', Musician)=1;
UPDATE Personnel SET Musician=REPLACE(Musician,'including ','') WHERE 
	LOCATE('including ', Musician)=1;





#Fixing session 901
UPDATE Personnel SET Instrument='drums' WHERE SessionID=901 AND Instrument='Paulinho';
UPDATE Personnel SET Instrument='cavaco' WHERE SessionID=901 AND Instrument='Neco';
DELETE FROM Personnel WHERE SessionID=901 AND Musician='';

