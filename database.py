import sqlite3
import requests


# Function to fetch data from the API
def fetch_data():
    api_url = "https://restcountries.com/v3.1/all"
    response = requests.get(api_url)
    # If the response is successful
    if response.status_code == 200:
        data = response.json()
        countries = []
        # Loop through the first 10 countries in the response
        for i in range(10):
            country = {
                "id": i + 1,
                "common_name": data[i]["name"]["common"],
                "official_name": data[i]["name"]["official"],
                "continent": data[i]["continents"][0],
                "flag": data[i]["flags"]["png"],
            }
            # Add the country information to the list
            countries.append(country)

        return countries  # Return the list of country information
    else:
        return None


# Function to create a database table if it doesn't exist
def create_table():
    # Connect to the SQLite database
    conn = sqlite3.connect("restcountries.db")
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS countryinfo (
            id INTEGER PRIMARY KEY,
            common_name TEXT NOT NULL,
            official_name TEXT NOT NULL,
            continent TEXT NOT NULL,
            flag TEXT NOT NULL
        )
    """
    )

    conn.commit()
    conn.close()


# Function to insert data into the database
def insert_data(countries):
    conn = sqlite3.connect("restcountries.db")
    cursor = conn.cursor()

    for countryinfo in countries:
        cursor.execute(
            """
            INSERT INTO countryinfo ( common_name, official_name, continent, flag)
            VALUES ( ?, ?, ?, ?)
        """,
            (
                countryinfo["common_name"],
                countryinfo["official_name"],
                countryinfo["continent"],
                countryinfo["flag"],
            ),
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Fetch data from the API
    countries = fetch_data()
    if countries:
        create_table()  # Create the database table
        insert_data(countries)  # Insert data into the database
        print("Data inserted.")
    else:
        print("Failed to fetch data.")
