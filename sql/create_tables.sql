CREATE TABLE products (
	product_pk			serial primary key,
	vendor				text,
	description			text,
	alt_description		text
);

CREATE TABLE assets (
	asset_pk			serial primary key,
	product_fk			integer REFERENCES products (product_pk),
	asset_tag			text,
	description			text,
	alt_description		text
);

CREATE TABLE vehicles (
	vehicle_pk			serial primary key,
	asset_fk			integer REFERENCES assets (asset_pk) not null
);


CREATE TABLE facilities (
	facility_pk			serial primary key,
	fcode				text,
	common_name			text,
	location			text
);

CREATE TABLE asset_at (
	asset_fk			integer REFERENCES assets (asset_pk) not null,
	facility_fk			integer REFERENCES facilities (facility_pk),
	arrive_dt			timestamp,
	depart_dt			timestamp
);

CREATE TABLE convoys (
	convoy_pk			serial primary key,
	request				text,
	source_fk			integer REFERENCES facilities (facility_pk),
	dest_fk				integer REFERENCES facilities (facility_pk),
	arrive_dt			timestamp,
	depart_dt			timestamp
);

CREATE TABLE used_by (
	vehicle_fk			integer REFERENCES vehicles (vehicle_pk),
	convoy_fk			integer REFERENCES convoys (convoy_pk)
);

CREATE TABLE asset_on (
	asset_fk			integer REFERENCES assets (asset_pk) not null,
	convoy_fk			integer REFERENCES convoys (convoy_pk),
	load_dt				timestamp,
	unload_dt			timestamp
);

CREATE TABLE users (
	user_pk				serial primary key,
	username			text,
	active				boolean
);

CREATE TABLE roles (
	role_pk				serial primary key,
	title				text
);

CREATE TABLE user_is (
	user_fk				integer REFERENCES users (user_pk) not null,
	role_fk				integer REFERENCES roles (role_pk) not null DEFAULT 1
);

CREATE TABLE user_supports (
	user_fk				integer REFERENCES users (user_pk) not null,
	facility_fk			integer REFERENCES facilities (facility_pk) not null
);

CREATE TABLE levels (
	level_pk			serial primary key,
	abbrv				text,
	comment				text
);

CREATE TABLE compartments (
	compartment_pk		serial primary key,
	abbrv				text,
	comment				text
);

CREATE TABLE security_tags (
	tag_pk				serial primary key,
	level_fk			integer REFERENCES levels (level_pk) not null,
	compartment_fk		integer REFERENCES compartments (compartment_pk) not null,
	user_fk				integer REFERENCES users (user_pk),
	product_fk			integer REFERENCES products (product_pk),
	asset_fk			integer REFERENCES assets (asset_pk)
);