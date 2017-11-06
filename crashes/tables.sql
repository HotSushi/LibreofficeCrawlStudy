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

alter table signature add crawled_crash_list BOOLEAN default false;