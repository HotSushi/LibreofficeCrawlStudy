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