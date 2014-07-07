USE jazzDBDevelopment;

SELECT Instrument, SessionDate, count(*) 
FROM Personnel JOIN Sessions ON Personnel.SessionID=Sessions.SessionID
GROUP BY SessionDate, Instrument;