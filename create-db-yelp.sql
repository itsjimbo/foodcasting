
-----------------------------------------------------
-- CLEAR TABLES
-- DROP TABLE summary;
-- DROP TABLE menu;
-- DROP TABLE concat_menu;
-- DROP TABLE flat_menu;
-- DROP TABLE usa_2010_population_by_zip;

CREATE TABLE  category_summary (
			slug varchar,
			categories text,
			categories2 text,
			categories3 text,
			distance REAL,
			name text,
			price_level varchar,
			rating REAL,
			review_count int,
			url text,
			lat REAL,
			lng REAL,
			Sp1 text,
			type text,
			homeurl text,
			resource_id1 text,
			resource_id2 text,
			lat2 REAL,
			lng2 REAL,
     PRIMARY KEY(slug),
     UNIQUE(slug)
);
------------------------------
---
--------------------------------
CREATE TABLE  summary (
			slug varchar,
			categories text,
			distance REAL,
			name text,
			price_level varchar,
			rating REAL,
			review_count int,
			url text,
			lat REAL,
			lng REAL,
			Sp1 text,
			type text,
			homeurl text,
			resource_id1 text,
			resource_id2 text,
			lat2 REAL,
			lng2 REAL,
     PRIMARY KEY(slug),
     UNIQUE(slug)
);
--------------------------------
---
--------------------------------
CREATE TABLE  menu (
	slug  varchar,
	title  text,
	description  text,
	price  REAL,
  FOREIGN KEY (slug) REFERENCES summary(slug)
);
--------------------------------
---
--------------------------------
CREATE TABLE  concat_menu (
	slug  varchar,
	menu_item  text,
  FOREIGN KEY (slug) REFERENCES summary(slug)
);
--------------------------------
---
--------------------------------
CREATE TABLE  flat_menu (
	slug  varchar,
	menu  text,
  FOREIGN KEY (slug) REFERENCES summary(slug)
);

--------------------------------
---
--------------------------------
CREATE TABLE usa_2010_population_by_zip(
	population bigint,
	minimum_age REAL,
	maximum_age REAL,
	gender VARCHAR ,
	zipcode VARCHAR
	geo_id VARCHAR
);

.mode csv
.import ./scrapy_yelp/summary.csv summary
.import ./scrapy_yelp/menu.csv menu
.import ./scrapy_yelp/flat_menu.csv flat_menu
.import ./scrapy_yelp/category_summary.csv category_summary
.import ./data/chicago-concat_menu.csv concat_menu
.import ./data/chicago-flat_menu.csv flat_menu
.import ./data/chicago-flat_menu.csv flat_menu



-- gunzip -c ./data/summary.csv.gz | sqlite3 -csv -separator ',' sql-lite-cache/foodcasting.db '.import /dev/stdin summary'
-- gunzip -c ./data/menu.csv.gz | sqlite3 -csv -separator ',' sql-lite-cache/foodcasting.db '.import /dev/stdin menu'



---what's your longest one-liner?
--- this unzips and creates a table in our db without needing to define table
--- gunzip -c scrapy_yelp/data/population_by_zip_2010.csv.gz | sqlite3 -csv -separator ',' sql-lite-cache/foodcasting.db '.import /dev/stdin usa_2010_population_by_zip'
---
