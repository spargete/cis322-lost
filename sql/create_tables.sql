CREATE TABLE users (
	user_pk				serial primary key,
	username			varchar(16),
	password			varchar(16)
); /* Chose to also have a numeric primary key because serial makes it really easy to do that
and chose the password length as 16 because longer is generally better with passwords -- sure, they're stored in plaintext,
but at least they can be longer and therefore harder to guess */