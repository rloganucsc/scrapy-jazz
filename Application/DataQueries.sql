#Visualization Queries
SELECT * FROM 
(
	Personnel LEFT JOIN 
		(Sessions LEFT JOIN Albums ON Sessions.AlbumID = Albums.AlbumID) 
	ON Personnel.SessionID = Sessions.SessionID
)
LEFT JOIN
(
	SELECT SessionID, COUNT(*) AS SongCount FROM Songs GROUP BY SessionID
) AS Temp
ON Temp.SessionID = Personnel.SessionID
INTO OUTFILE '/tmp/orders.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
