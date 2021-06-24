CREATE DATABASE BOOKSMANAGER
GO 
USE BOOKSMANAGER
GO

CREATE TABLE BOOKS
(
	ID INT,
	BOOK_NAME VARCHAR(100),
	AUTHOR VARCHAR(50),
	PUBLICING_YEAR INT,
	PRIMARY KEY(ID)
)
GO

CREATE TABLE MEMBERS(
	ID INT,
	USERNAME VARCHAR(150),
	PASS_WORD VARCHAR(255),
	PRIMARY KEY (ID)
)
GO
