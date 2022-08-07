CREATE TABLE public.staging_restaurants (
	resturant_id int4,
	name varchar(256),
	city varchar(256),
	state varchar(256),
	postal_code varchar(256),
	address varchar(512),
	cuisines varchar(256),
	seating bool,
	delivery bool,
    takeout bool,
    private_dining bool,
	reservations bool,
	review_score float4,
	number_of_reviews int4,
	url varchar(2048)
);

CREATE TABLE public.restaurants (
	resturant_id int4,
	name varchar(256),
	city varchar(256),
	state varchar(256),
	postal_code varchar(256),
	address varchar(512),
	url varchar(2048),
    CONSTRAINT restaurant_pkey PRIMARY KEY (resturant_id)
);


CREATE TABLE public.reviews (
	id INT IDENTITY(1,1) PRIMARY KEY,
	review_score float4,
    number_of_reviews int4,
    resturant_id int4,
);

CREATE TABLE public.features (
	id INT IDENTITY(1,1) PRIMARY KEY,
	resturant_id int4,
	cuisines varchar(256),
	seating bool,
	delivery bool,
    takeout bool,
    private_dining bool,
	reservations bool,
);





