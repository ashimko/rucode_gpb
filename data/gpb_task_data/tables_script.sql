-- client.address definition

-- Drop table

-- DROP TABLE client.address;

CREATE TABLE client.address (
	app_id numeric(15) NOT NULL,
	run_id numeric(15) NOT NULL,
	regionname varchar(1000) NULL,
	regioncode varchar(100) NULL,
	countrycode varchar(100) NULL,
	street varchar(150) NULL,
	house varchar(100) NULL
);


-- client.application definition

-- Drop table

-- DROP TABLE client.application;

CREATE TABLE client.application (
	app_id numeric(15) NOT NULL,
	run_id numeric(15) NOT NULL,
	opendate date NULL,
	inittermnumber numeric(20,10) NULL,
	initpayment numeric(20,10) NULL,
	asktotalcreditqty numeric(20,10) NULL,
	inputusername varchar(1000) NULL,
	appdatetime date NULL,
	signdate date NULL,
	totalmaxpayment numeric(20,5) NULL,
	card_number numeric(20) NULL,
	client_snils numeric(20) NULL,
	client_inn numeric(20) NULL
);


-- client.client definition

-- Drop table

-- DROP TABLE client.client;

CREATE TABLE client.client (
	app_id numeric(15) NOT NULL,
	run_id numeric(15) NOT NULL,
	client_id numeric(15) NOT NULL,
	lastname varchar(1000) NULL,
	firstname varchar(1000) NULL,
	middlename varchar(1000) NULL,
	sex numeric(10) NULL,
	birthplacetown varchar(1000) NULL,
	birthdate date NULL,
	familymembersnumber numeric(10) NULL,
	maxpayment numeric(18) NULL,
	avg_pure_income numeric(15,5) NULL
);


-- client."document" definition

-- Drop table

-- DROP TABLE client."document";

CREATE TABLE client."document" (
	app_id numeric(15) NOT NULL,
	run_id numeric(15) NOT NULL,
	client_id numeric(15) NOT NULL,
	document_id numeric(15) NOT NULL,
	documenttype varchar(4) NULL,
	series varchar(1000) NULL,
	"number" varchar(1000) NULL,
	issuedate date NULL,
	issuercode varchar(1000) NULL,
	issuer varchar(1000) NULL
);


-- client.phone definition

-- Drop table

-- DROP TABLE client.phone;

CREATE TABLE client.phone (
	app_id numeric(15) NOT NULL,
	run_id numeric(15) NOT NULL,
	client_id numeric(15) NOT NULL,
	work_id numeric(15) NULL,
	phone_id numeric(15) NOT NULL,
	phone_type varchar(100) NULL,
	phone_number varchar(1000) NULL
);


-- client."work" definition

-- Drop table

-- DROP TABLE client."work";

CREATE TABLE client."work" (
	app_id numeric(15) NOT NULL,
	run_id numeric(15) NOT NULL,
	client_id numeric(15) NOT NULL,
	work_id numeric(15) NOT NULL,
	title varchar(1000) NULL,
	inn varchar(1000) NULL,
	positiontitle varchar(1000) NULL,
	standing numeric(15,2) NULL,
	standingfrom date NULL,
	fullstanding numeric(15,2) NULL
);