import streamlit as st
import mysql.connector
from datetime import datetime

# Function to connect to MySQL database
def connect_to_db():
    return mysql.connector.connect(
        user='root',
        password='ahmed_2021',
        host='localhost',
        database='carrental'
    )

# Function to sign up a new user
def sign_up(username, email, password):
    try:
        cnx = connect_to_db()
        cursor = cnx.cursor()
        query = "INSERT INTO users (name, email, password, create_at) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, email, password, datetime.now()))
        cnx.commit()
        st.success("Signed up successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err.msg}")
    finally:
        cursor.close()
        cnx.close()

# Function to check user credentials
def check_credentials(email, password):
    try:
        cnx = connect_to_db()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        st.error(f"Error: {err.msg}")
    finally:
        cursor.close()
        cnx.close()

# Function to fetch and display available cars
def display_available_cars():
    try:
        cnx = connect_to_db()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM vehicles WHERE stock > 0"
        cursor.execute(query)
        cars = cursor.fetchall()
        st.write("## Available Cars:")
        for car in cars:
            st.write(f"**Name:** {car['name']}, **Description:** {car['description']}, **Price:** {car['price']}")
    except mysql.connector.Error as err:
        st.error(f"Error: {err.msg}")
    finally:
        cursor.close()
        cnx.close()

# Function to upload a new car
def upload_car(name, description, location_id, type_id, stock, price):
    try:
        cnx = connect_to_db()
        cursor = cnx.cursor()
        query = "INSERT INTO vehicles (name, description, locations_id, types_id, stock, price, create_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, description, location_id, type_id, stock, price, datetime.now()))
        cnx.commit()
        st.success("Car uploaded successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err.msg}")
    finally:
        cursor.close()
        cnx.close()

# Main Streamlit app
def main():
    st.title("Car Rental Management System")

    # Sign Up
    st.write("### Sign Up")
    new_username = st.text_input("Enter Username:")
    new_email = st.text_input("Enter Email:")
    new_password = st.text_input("Enter Password:", type="password")
    if st.button("Sign Up"):
        sign_up(new_username, new_email, new_password)

    # Sign In
    st.write("### Sign In")
    login_email = st.text_input("Enter Email:")
    login_password = st.text_input("Enter Password:", type="password")
    if st.button("Sign In"):
        user = check_credentials(login_email, login_password)
        if user:
            st.success("Logged in successfully!")
            st.write(f"Welcome back, {user['name']}!")
            display_available_cars()
        else:
            st.error("Invalid email or password.")

    # Upload Car
    st.write("### Upload Car")
    car_name = st.text_input("Enter Car Name:")
    car_description = st.text_area("Enter Car Description:")
    car_location_id = st.number_input("Enter Location ID:")
    car_type_id = st.number_input("Enter Type ID:")
    car_stock = st.number_input("Enter Stock:")
    car_price = st.number_input("Enter Price:")
    if st.button("Upload Car"):
        upload_car(car_name, car_description, car_location_id, car_type_id, car_stock, car_price)

if __name__ == "__main__":
    main()
