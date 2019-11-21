INSERT INTO users  ( user_id, login, password, email, lastname, firstname, created, age, eyes, hair ,height )
VALUES (1, 'Kat13','1234qwerty','Kat13@gmail.com', 'Katia', 'Kolobaieva', NOW(), 20,'blue','brown',161);

INSERT INTO users  ( user_id, login, password, email, lastname, firstname, created, age, eyes, hair ,height )
VALUES (2, 'Dashaaa','qwerty','Dash@gmail.com', 'Dasha', 'Zagrebelna', NOW(), 15,'green','brown',155);

INSERT INTO users  ( user_id, login, password, email, lastname, firstname, created, age, eyes, hair ,height )
VALUES (3, 'Mila111','qwerty111','Mila@gmail.com', 'Mila', 'Nilson', NOW(), 24,'grey','red',174);

-- 
INSERT INTO events  (event_id, event_name ,Created, user_idIDFK)
VALUES (1,'birthday', NOW(),1);

INSERT INTO events  (event_id, event_name ,Created,user_idIDFK)
VALUES ( 2,'concert',NOW(),2);

INSERT INTO events  (event_id, event_name ,Created, user_idIDFK )
VALUES (3, 'party',NOW(),3);


-- 
INSERT INTO options (option_id,place ,season, Created,temperature, event_idIDFK )
VALUES (1,'cafe', 'summer',NOW(),19,1);

INSERT INTO options  (option_id,place ,season,Created,temperature,event_idIDFK)
VALUES ( 2,'hall','summer',NOW(),27,3);

INSERT INTO options (option_id,place ,season,Created,temperature,event_idIDFK)
VALUES ( 3,'club', 'autumn',NOW(),15,3);

-- 
INSERT INTO clothes (clothe_id, style_name ,outwear, lowerwear ,shoes, Created, option_idIDFK )
VALUES (1,'romantic', 't-shirt', 'jeans','high heel shoels', NOW(),1);

INSERT INTO clothes(clothe_id,style_name ,outwear, lowerwear ,shoes, Created, option_idIDFK )
VALUES (2, 'gala', 't-shirt','jeans','sneakers', NOW(),2);

INSERT INTO clothes(clothe_id,style_name ,outwear, lowerwear ,shoes, Created, option_idIDFK  )
VALUES ( 3,'disco', 'bluse','jeans','sneakers', NOW(),3);




select * from Users;
select * from Events;
select * from Options;
select * from Clothes;
