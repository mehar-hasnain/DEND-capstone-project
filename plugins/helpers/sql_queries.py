class SqlQueries:
    restaurants_table_insert = """
        INSERT INTO public.restaurants (
            resturant_id,
            name,
            city,
            state,
            postal_code,
            address,
            url
        )
        SELECT
            resturant_id,
	        name,
	        city,
	        state,
	        postal_code,
	        address,
	        url
        FROM staging_restaurants;
    """
    
    reviews_table_insert = """
        INSERT INTO public.reviews (
            review_score,
            number_of_reviews,
            resturant_id
        )
        SELECT
            review_score,
            number_of_reviews,
            resturant_id
        FROM staging_restaurants;
    """
    
    features_table_insert = """
        INSERT INTO public.features(
            resturant_id,
	        cuisines,
	        seating,
	        delivery,
            takeout,
            private_dining,
	        reservations
        )
        SELECT
            resturant_id,
	        cuisines,
	        seating,
	        delivery,
            takeout,
            private_dining,
	        reservations
        FROM staging_restaurants;
    """

