CREATE Table Signature (
	sign varchar(200) NOT NULL,
	url varchar(500) NOT NULL,
	PRIMARY KEY(sign)
);

CREATE Table Bugs (
	id varchar(200) NOT NULL,
	sign varchar(200),
	url varchar(500) NOT NULL,
	PRIMARY KEY(id)
);

CREATE Table Crash (
	id varchar(200) NOT NULL,
	sign varchar(200),
	url varchar(500) NOT NULL,
	PRIMARY KEY(id)
);

ALTER TABLE Crash
ADD COLUMN crash_date DATETIME,
ADD COLUMN os_name VARCHAR(200),
ADD COLUMN os_version VARCHAR(200),
ADD COLUMN cpu_info VARCHAR(200),
ADD COLUMN build VARCHAR(200),
ADD COLUMN version VARCHAR(200),
ADD COLUMN reason VARCHAR(200),
ADD COLUMN opengldriver VARCHAR(200),
ADD COLUMN opengldevice VARCHAR(200)
;

ALTER TABLE Signature
ADD COLUMN last_crawled_crash_url VARCHAR(400);

ALTER TABLE Bugs
ADD COLUMN create_time DATETIME,
ADD COLUMN last_modified DATETIME,
ADD COLUMN priority VARCHAR(300),
ADD COLUMN severity VARCHAR(300),
ADD COLUMN cc_count VARCHAR(30),
ADD COLUMN comment_count VARCHAR(30),
ADD COLUMN status VARCHAR(300),
ADD COLUMN resolution VARCHAR(300),
ADD COLUMN attachment_count VARCHAR(30),
ADD COLUMN duplicate_of VARCHAR(300)
;