###############################################################################
#Title:Jazz Database Initialization Script
#
#Purpose: Defines all of the tables in the jazzDBDevelopment database
#
###############################################################################

CREATE DATABASE jazzDBDevelopment;
USE jazzDBDevelopment;

CREATE TABLE RecordLabels (
	LabelName VARCHAR(40) NOT NULL,
	LabelID INT PRIMARY KEY NOT NULL auto_increment
);

CREATE TABLE RecordSeries (
	LabelID INT NOT NULL,
	SeriesName VARCHAR(120) NOT NULL,
	SeriesID INT PRIMARY KEY NOT NULL auto_increment
);

CREATE TABLE Albums (
	SeriesID INT NOT NULL,
	AlbumName VARCHAR(255) NOT NULL,
	BandLeader VARCHAR(255), 
	AlbumID INT PRIMARY KEY NOT NULL auto_increment
);

CREATE TABLE Sessions (
	AlbumID INT NOT NULL,
	SessionDate VARCHAR(4),
	SessionID INT PRIMARY KEY NOT NULL auto_increment
);

CREATE TABLE Personnel (
	SessionID INT NOT NULL,
	Musician  VARCHAR(70), 
	Instrument  VARCHAR(70)
);

CREATE TABLE Songs (
	SessionID INT NOT NULL,
	SongName VARCHAR(255) NOT NULL
);