from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)


# Define a route for the home page
@app.route("/")
def main():
    conn = sqlite3.connect("restcountries.db")
    cursor = conn.cursor()

    # Execute SQL query to fetch country information
    cursor.execute("SELECT id, common_name FROM countryinfo")
    # Fetch all rows from the result set
    con_info = cursor.fetchall()

    conn.close()
    # Render the main.html template with country information
    return render_template("main.html", con_info=con_info)


# Define a route for displaying country details
@app.route("/user/<int:user_id>")
def country_details(user_id):
    conn = sqlite3.connect("restcountries.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM countryinfo WHERE id=?", (user_id,))
    details = cursor.fetchone()

    conn.close()
    # Render the country_details.html template with country details
    return render_template("country_details.html", details=details)


# Define a route for creating a country
@app.route("/create", methods=["GET", "POST"])
def create_country():
    if request.method == "POST":
        common_name = request.form["common_name"]
        official_name = request.form["official_name"]
        continent = request.form["continent"]
        flag = request.form["flag"]

        conn = sqlite3.connect("restcountries.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO countryinfo (common_name, official_name, continent, flag)
            VALUES (?, ?, ?, ?)
        """,
            (common_name, official_name, continent, flag),
        )

        conn.commit()
        conn.close()

        # Redirect to the main page after successful insertion
        return redirect(url_for("main"))

    # Render the create_country.html template
    return render_template("create_country.html")


# Define a route for updating country details
@app.route("/update/<int:user_id>", methods=["GET", "POST"])
def update_country(user_id):
    if request.method == "POST":
        common_name = request.form["common_name"]
        official_name = request.form["official_name"]
        continent = request.form["continent"]
        flag = request.form["flag"]

        conn = sqlite3.connect("restcountries.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE countryinfo 
            SET common_name=?, official_name=?, continent=?, flag=?
            WHERE id=?
        """,
            (common_name, official_name, continent, flag, user_id),
        )

        conn.commit()
        conn.close()

        # Redirect to the country details page after successful update
        return redirect(url_for("country_details", user_id=user_id))

    conn = sqlite3.connect("restcountries.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM countryinfo WHERE id=?", (user_id,))
    update_details = cursor.fetchone()

    conn.close()
    # Render the update_country.html template
    return render_template("update_country.html", update_details=update_details)


# Define a route for deleting a country
@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_country(user_id):
    conn = sqlite3.connect("restcountries.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM countryinfo WHERE id=?
    """,
        (user_id,),
    )

    conn.commit()
    conn.close()

    # Redirect to the main page after successful deletion
    return redirect(url_for("main"))


if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
