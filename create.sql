CREATE TABLE Users(
    user_id int NOT NULL PRIMARY KEY ,
    Login varchar(30)  NOT NULL,
    Password varchar(50) NOT NULL,
    Email varchar(50)  NOT NULL,
    Lastname varchar(30),
    Firstname varchar(30)NOT NULL,
    Age int NOT NULL,
    Eyes varchar(50) NOT NULL,
    Hair varchar(100) NOT NULL,
    Height int NOT NULL,
    Created timestamp
                  );

CREATE TABLE Events(
    event_id int NOT NULL PRIMARY KEY,
    Event_name varchar(50) NOT NULL ,
    Created timestamp,
	user_id int,
	FOREIGN KEY (user_id) REFERENCES Users(user_id)
	);

CREATE TABLE Clothes(
    clothe_id int NOT NULL PRIMARY KEY,
    style_name varchar(100) NOT NULL ,
    outwear varchar(50) NOT NULL,
	lowerwear varchar(50) NOT NULL,
	shoes varchar(50) NOT NULL,
	Created timestamp,
	option_idIDFK int,
	FOREIGN KEY (option_idIDFK) REFERENCES options(option_id)
);
