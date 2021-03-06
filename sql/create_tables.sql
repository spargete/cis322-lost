CREATE TABLE users (
	user_pk					serial primary key,
	username				varchar(16),
	password				varchar(64),
	active					boolean DEFAULT TRUE
); /* Chose to also have a numeric primary key because serial makes it really easy to do that
and chose the password length as 64 because longer is generally better with passwords -- sure, they're stored in plaintext,
but at least they can be longer and therefore harder to guess */

CREATE TABLE roles (
	role_pk					serial primary key,
	role_name				varchar(32)
);

INSERT INTO roles (role_name) VALUES ('Logistics Officer');

INSERT INTO roles (role_name) VALUES ('Facilities Officer');

CREATE TABLE user_is (
	role_fk					integer REFERENCES roles (role_pk),
	user_fk					integer REFERENCES users (user_pk)
); /* I am using a user_is table -- a many-to-many relation -- to represent my roles. I am doing this because it is the best
future-proofing option in my opinion. */

CREATE TABLE assets (
	asset_pk				serial primary key,
	asset_tag				varchar(16),
	description				text,
	intake_dt				timestamp,
	disposed_dt				timestamp DEFAULT NULL
); /* The assets table now stores intake date as well as disposed date -- this makes for easier exporting of data */

CREATE TABLE facilities (
	facility_pk				serial primary key,
	facility_common_name	varchar(32),
	facility_fcode			varchar(6)
);

CREATE TABLE asset_at (
	asset_fk				integer REFERENCES assets (asset_pk),
	facility_fk				integer REFERENCES facilities (facility_pk),
	arrive_dt				timestamp,
	depart_dt				timestamp
); /* I am using an asset_at table for history purposes. This could get very large if there is a lot of movement of assets going on,
but I think that is an acceptable issue for this point in the project. */

CREATE TABLE transfer_requests (
	request_pk				serial primary key,
	requester_fk			integer REFERENCES users (user_pk),
	request_dt				timestamp,
	source_fk				integer REFERENCES facilities (facility_pk),
	dest_fk					integer REFERENCES facilities (facility_pk),
	asset_fk				integer REFERENCES assets (asset_pk),
	approver_fk				integer REFERENCES users (user_pk),
	approval_dt				timestamp
);  /* Minimal implementation here, apart from the request_pk unique identifier. */

CREATE TABLE transfers (
	asset_fk				integer REFERENCES assets (asset_pk),
	request_fk				integer REFERENCES transfer_requests (request_pk),
	load_dt					timestamp,
	unload_dt				timestamp
); /* Here I decided to relate the transfers table to the requests table so the source_fk and dest_fk are there instead of here. */