CREATE TABLE products (
	product_pk			serial primary key,
	vendor				varchar(128),
	description			varchar(256),
	alt_description		varchar(256)
);

CREATE TABLE assets (
	asset_pk			serial primary key,
	product_fk			integer REFERENCES products (product_pk) not null,
	asset_tag			varchar(128),
	description			varchar(256),
	alt_description		varchar(256)
);

CREATE TABLE vehicles (
	vehicle_pk			serial primary key,
	asset_fk			integer REFERENCES assets (asset_pk) not null
);


CREATE TABLE facilities (
	facility_pk			serial primary key,
	fcode				varchar(128),
	common_name			varchar(128),
	location			varchar(256)
);

CREATE TABLE asset_at (
	asset_fk			integer REFERENCES assets (asset_pk) not null,
	facility_fk			integer REFERENCES facilities (facility_pk) not null,
	arrive_dt			timestamp,
	depart_dt			timestamp
);

CREATE TABLE convoys (
	convoy_pk			serial primary key,
	request				varchar(128),
	source_fk			integer REFERENCES facilities (facility_pk) not null,
	dest_fk				integer REFERENCES facilities (facility_pk) not null,
	arrive_dt			timestamp,
	depart_dt			timestamp
);

CREATE TABLE used_by (
	vehicle_fk			integer REFERENCES vehicles (vehicle_pk) not null,
	convoy_fk			integer REFERENCES convoys (convoy_pk) not null
);

CREATE TABLE asset_on (
	asset_fk			integer REFERENCES assets (asset_pk) not null,
	convoy_fk			integer REFERENCES convoys (convoy_pk) not null,
	load_dt				timestamp,
	unload_dt			timestamp
);

