
-----------------------------------------------------
-- CLEAR TABLES
DROP TABLE business;
DROP TABLE review;
DROP TABLE tip;
DROP TABLE checkin;
DROP TABLE user;
DROP TABLE photo;

------------------------------
---
--------------------------------
CREATE TABLE  business (
	 name  text,
	 city  text,
	 review_count  int,
	 hours  text,
	 categories  text,
	 latitude  REAL,
	 stars  REAL,
	 attributes  text,
	 longitude  REAL,
	 address  text,
	 postal_code  text,
	 state  text,
	 is_open  int,
	 business_id  VARCHAR,
     PRIMARY KEY(business_id),
     UNIQUE(business_id) 
);
--------------------------------
---
--------------------------------
CREATE TABLE  user (
	 user_id  varchar,
	 name  text,
	 review_count  int,
	 yelping_since  DATE,
	 friends  text,
	 useful  text,
	 funny  text,
	 cool  text,
	 fans  text,
	 elite  text,
	 average_stars  REAL,
	 compliment_hot  text,
	 compliment_more  text,
	 compliment_profile  text,
	 compliment_cute  text,
	 compliment_list  text,
	 compliment_note  text,
	 compliment_plain  text,
	 compliment_cool  text,
	 compliment_funny  text,
	 compliment_writer  text,
	 compliment_photos  text,
     UNIQUE(user_id)
);

--------------------------------
---
--------------------------------
CREATE TABLE  review (
	 review_id  varchar,
	 user_id  varchar,
	 date  DATE,
	 useful  text,
	 text  text,
	 cool  text,
	 stars  REAL,
	 business_id  varchar,
	 funny  text,
     PRIMARY KEY(review_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id), 
    FOREIGN KEY (business_id) REFERENCES business(buisness_id)
);
--------------------------------
---
--------------------------------
CREATE TABLE  tip (
	 business_id  varchar,
	 user_id  varchar,
	 date  DATE,
	 text  text,
	 compliment_count  int,
    FOREIGN KEY (user_id) REFERENCES users(user_id), 
    FOREIGN KEY (business_id) REFERENCES business(buisness_id)
);
--------------------------------
---
--------------------------------
CREATE TABLE  checkin (
	 business_id  varchar,
	 date  DATE,
     FOREIGN KEY (business_id) REFERENCES business(buisness_id)
);


--------------------------------
---
--------------------------------
CREATE TABLE  photo (
	 caption  text,
	 photo_id  varchar,
	 business_id  varchar,
	 label  text,
);
               


-- change mode to csv to import
.mode csv
.import ./yelp_data/business.csv business
.import ./yelp_data/review.csv review
.import ./yelp_data/tip.csv tip
.import ./yelp_data/checkin.csv checkin
.import ./yelp_data/user.csv user
.import ./yelp_data/photo.csv photo
