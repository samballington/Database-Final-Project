import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create and return a database connection."""
    try:
        connection = mysql.connector.connect(
            host="database-2.c94soiwsy7xp.us-east-1.rds.amazonaws.com",
            user="admin",
            passwd="samballington",
            database="RestaurantDB",
            auth_plugin='mysql_native_password'
        )
        print("Connection to MySQL database was successful")
        return connection
    except Error as e:
        print(f"Connection Error: {e}")
        return None

def get_all_cuisines():
    """Fetches all distinct cuisines from the database."""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT Cuisine FROM restaurant_cuisines;")
            cuisines = cursor.fetchall()
            return [cuisine[0] for cuisine in cuisines]  # Unpack tuple
        finally:
            cursor.close()
            connection.close()
    else:
        return []

def get_restaurants_by_cuisine(cuisines, sort_by):
    """Fetches restaurant data filtered by selected cuisines with sorting based on rating or price."""
    connection = create_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor()
        placeholders = ', '.join(['%s'] * len(cuisines))
        query = f"""
        SELECT r.Name, r.City, r.Price, rc.Cuisine, AVG(rt.Overall_Rating) AS AvgRating
        FROM restaurants r
        JOIN restaurant_cuisines rc ON r.Restaurant_ID = rc.Restaurant_ID
        JOIN ratings rt ON r.Restaurant_ID = rt.Restaurant_ID
        WHERE rc.Cuisine IN ({placeholders})
        GROUP BY r.Restaurant_ID
        """
        # Sorting based on the user selection
        if sort_by == 'rating':
            query += " ORDER BY AvgRating DESC"
        elif sort_by == 'price':
            query += " ORDER BY r.Price ASC"

        cursor.execute(query, tuple(cuisines))
        results = cursor.fetchall()
        return results
    finally:
        cursor.close()
        connection.close()
   

def get_consumer_preferences(summary=False):
    """Fetches the number of consumers preferring each type of cuisine, with an option for a summary."""
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            query = """
            SELECT Preferred_Cuisine, COUNT(Consumer_ID) AS Consumer_Count
            FROM consumer_preferences
            GROUP BY Preferred_Cuisine
            ORDER BY Consumer_Count DESC
            """
            if summary:
                query += " LIMIT 5"  # Fetch only the top 5

            cursor.execute(query)
            results = cursor.fetchall()
            return results
        finally:
            cursor.close()
            connection.close()
    else:
        return []

if __name__ == "__main__":
    # Quick test prints for debug purposes
    print("Cuisines:", get_all_cuisines())
    print("Restaurants:", get_restaurants_by_cuisine(['Italian', 'Mexican'], 'price'))
    print("Consumer Preferences:", get_consumer_preferences(True))
