import streamlit as st  
from streamlit_option_menu import option_menu
import base64
import folium
from streamlit_folium import folium_static
import requests
from streamlit_carousel import carousel
from datetime import datetime
import sqlite3
import os

#SQLite database
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (first_name TEXT, last_name TEXT, email TEXT)''')
    conn.commit()
    conn.close()

# add user
def add_user(first_name, last_name, email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (first_name, last_name, email) VALUES (?, ?, ?)",
              (first_name, last_name, email))
    conn.commit()
    conn.close()

# Function to get all users from the SQLite database
def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

# Initialize users table
create_users_table()



today_date = datetime.now().strftime("%B %d, %Y")

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("logo.png")

col1, col2, col3 = st.columns(3)

with col1:
    pass

with col2:
    st.image('logo.png')

with col3:
    pass


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://github.com/ClaudeLVU18/web-streamlit/blob/main/Untitled%20design%20(5).png?raw=true");
background-size: cover; 
background-position: center; 
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

</style>
"""

def get_weather():
    api_key = "687372cc75d14c0f82d183756230701"  # Replace with your WeatherAPI API key
    city = "Abu Dhabi"  # Fetch weather for Abu Dhabi
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx errors
        data = response.json()
        weather = {
            "description": data["current"]["condition"]["text"],
            "temperature": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"],
        }
        return weather
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

# Define a function to display weather information for Abu Dhabi
def display_weather():
    weather = get_weather()
    if weather:
        st.markdown("""
        <style>
        .weather-card {
            border-radius: 10px;
            padding: 20px;
            background-color: #f0f0f0;
            width: 400px;
            margin: auto;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .weather-card-icon {
            width: 100px;
            height: 100px;
            margin: auto;
        }
        .weather-card-description {
            font-size: 18px;
            margin-top: 10px;
        }
        .weather-card-temp {
            font-size: 24px;
            font-weight: bold;
            margin-top: 10px;
        }
        .weather-card-humidity {
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.title("Weather in Abu Dhabi")

        st.markdown("""
        <div class="weather-card">
            <img class="weather-card-icon" src="https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather02-512.png" alt="Weather Icon">
            <div class="weather-card-description">{}</div>
            <div class="weather-card-temp">{} °C</div>
            <div class="weather-card-humidity">Humidity: {} %</div>
        </div>
        """.format(weather['description'].capitalize(), weather['temperature'], weather['humidity']), unsafe_allow_html=True)

    else:
        st.error("Weather information not available.")
        
st.markdown(page_bg_img, unsafe_allow_html=True)


    
def maps():
        

        coords = [24.4539, 54.3773]  # Default coordinates (Abu Dhabi)
        
        if st.session_state.location == "Hudayriyat Cycling Track":
            coords = [24.41747877819097, 54.34773109613836]  
        elif st.session_state.location == "YMC":
            coords = [24.477436972153047, 54.60613205735251]  
        elif st.session_state.location == "Al Wathba":
            coords = [24.155891135881497, 54.782889483232296]  
        elif st.session_state.location == "corniche":
            coords = [24.488199390752868, 54.34998283638465]  
        elif st.session_state.location == "alain":
            coords = [24.222964219967842, 55.72625019906443 ]  
        elif st.session_state.location == "dhafra":
            coords = [24.22424626357369, 55.63696579178918]  

        map = folium.Map(location=coords, zoom_start=13)
        
        folium.Marker(location=coords, popup=st.session_state.location).add_to(map)
        
        folium_static(map)

        google_maps_url = f"https://www.google.com/maps/search/?api=1&query={coords[0]},{coords[1]}"
        
        button_style = """
        <style>
            .button {
                background-color: #FFFFFF;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }
        </style>
        """

        # Display the button-like link
        st.markdown(button_style, unsafe_allow_html=True)
        st.markdown(f'<i class="bi bi-cloud-sun-fill"></i><a href="{google_maps_url}" class="button">Open in Google Maps</a>', unsafe_allow_html=True)

if 'registered' not in st.session_state:
    st.session_state.registered = ''
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if 'location' not in st.session_state:
    st.session_state.location = None
    
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
        
def delete_account(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE email=?", (email,))
    conn.commit()
    conn.close()
        
# Authenticator Page
if not st.session_state.authenticated:
    st.title("Login / Signup")

    auth_choice = st.radio("Choose Authentication Method", ["Login", "Sign Up"])

    if auth_choice == "Login":
        email = st.text_input("Email")
        if st.button("Login"):
            users = get_users()
            if any(user[2] == email for user in users):
                st.session_state.authenticated = True
                st.success("Login Successful! Click again to continue.")
            else:
                st.error("User not found. Please sign up.")
    else:
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        if st.button("Sign Up"):
            add_user(first_name, last_name, email)
            st.session_state.authenticated = True
            st.success("Sign Up Successful! Click again to continue.")

else:

    

    def go_to_maps(location=None):
        return 'Maps', location

    selected = option_menu(
        menu_title=None,
        options=["Home", "Profile", "My Rides", "Maps", "Weather"],
        icons=['house-fill', 'person-circle', 'bi bi-bicycle', 'bi bi-google', 'bi bi-cloud-sun-fill'],
        default_index=0,
        orientation="horizontal"
    )

    if st.session_state.page != selected:
        st.session_state.page = selected

    if st.session_state.page == "Home":
        st.title(f"Upcoming Rides: {today_date}")

        # First Card
        image_path_1 = "https://visitabudhabi.ae/-/media/project/vad/plan-your-trip/article-hub/cycling-in-abu-dhabi/cycling-main-image.jpg"
        card_css = """
        <style>
        .card {
            border-radius: 1px;
            padding: 20px;
            background-color: #ffffff;
            width: 400px;
            margin: auto;
            box-shadow: 5px 5px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .card img {
            width: 100%;
            border-radius: 10px;
        }
        .card h3 {
            margin-top: 10px;
        }
        .card .dropdown {
            margin-top: 20px;
        }
        .card button {
            margin-top: 20px;
        }
        </style>
        """

        st.markdown(card_css, unsafe_allow_html=True)

        card_html_1 = """
        <div class="card">
            <img src="{}" alt="Hudayriyat Cycling Track">
            <h3>Hudayriyat Cycling Track</h3>
            <div class="dropdown"></div>
            <div></div>
        </div>
        """.format(image_path_1)

        st.markdown(card_html_1, unsafe_allow_html=True)
        
        
    
        options_1 = ["06:00", "10:00", "14:00", "17:00", "19:00"]

        selected_option_1 = st.selectbox("Select a cycling track", options_1)

        if st.button("Register for Hudayriyat Ride"):
            st.success("You have succesfully registered for this ride.")
            if selected_option_1 == "06:00":
                ride_1 = "Hudayriyat Cycling Track - 06:00 AM"
            elif selected_option_1 == "10:00":
                ride_1 = "Hudayriyat Cycling Track - 10:00 AM"
            elif selected_option_1 == "14:00":
                ride_1 = "Hudayriyat Cycling Track - 14:00 PM"
            elif selected_option_1 == "17:00":
                ride_1 = "Hudayriyat Cycling Track - 17:00 PM"
            elif selected_option_1 == "19:00":
                ride_1 = "Hudayriyat Cycling Track - 19:00 PM"
            
            if not st.session_state.registered:
                st.session_state.registered = [ride_1]  # Initialize the list if it doesn't exist
            elif ride_1 not in st.session_state.registered:
                st.session_state.registered.append(ride_1)  # Append the new ride if it's not already registered
            else:
                st.warning("You are already registered for this ride.")
        
        if st.button("Hudayriyat Cycling Track on Maps"):
            st.session_state.page, st.session_state.location = go_to_maps(location="Hudayriyat Cycling Track")
            maps()

        # Second Card
        image_path_2 = "https://visitabudhabi.ae/-/media/project/vad/plan-your-trip/article-hub/cycling-in-abu-dhabi/yas-marina-circuit-cycling-03.jpg?cx=0&cy=0&cw=2174&ch=1434&hash=C1CD80E62F86EA4A3669B2BAA02935DA"  # URL for the second image
        card_css = """
        <style>
        .card {
            border-radius: 1px;
            padding: 20px;
            background-color: #ffffff;
            width: 400px;
            margin: auto;
            box-shadow: 5px 5px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .card img {
            width: 100%;
            border-radius: 10px;
        }
        .card h3 {
            margin-top: 10px;
        }
        .card .dropdown {
            margin-top: 20px;
        }
        .card button {
            margin-top: 20px;
        }
        </style>
        """

        st.markdown(card_css, unsafe_allow_html=True)

        card_html_2 = """
        <div class="card">
            <img src="{}" alt="Yas Marina Circuit">
            <h3>Yas Marina Circuit</h3>
            <div class="dropdown"></div>
            <div></div>
        </div>
        """.format(image_path_2)

        st.markdown(card_html_2, unsafe_allow_html=True)
        
        
    
        options_2 = ["18:00", "20:00", "22:00"]  # Options for the second card

        selected_option_2 = st.selectbox("Select a cycling track", options_2)

        if st.button("Register for Yas Marina Circuit TrainYAS"):
            st.success("You have succesfully registered for this ride.")
            if selected_option_2 == "18:00":
                ride_2 = "Yas Marina Circuit - 18:00 PM"
            elif selected_option_2 == "20:00":
                ride_2 = "Yas Marina Circuit - 20:00 PM"
            elif selected_option_2 == "22:00":
                ride_2 = "Yas Marina Circuit - 22:00 PM"
            
            
            if not st.session_state.registered:
                st.session_state.registered = [ride_2]  # Initialize the list if it doesn't exist
            elif ride_2 not in st.session_state.registered:
                st.session_state.registered.append(ride_2)  # Append the new ride if it's not already registered
            else:
                st.warning("You are already registered for this ride.")
        
        if st.button("Yas Marina Circuit on Maps"):
            st.session_state.page, st.session_state.location = go_to_maps(location="YMC")
            maps()
            
        # Third Card
        image_path_3 = "https://visitabudhabi.ae/-/media/project/vad/plan-your-trip/article-hub/cycling-in-abu-dhabi/al-wathba-cycling.jpg?cx=0&cy=0&cw=2174&ch=1434&hash=3FD56CAFE4A8592192FF7DCF3F2F5F53"  # URL for the second image
        card_css = """
        <style>
        .card {
            border-radius: 1px;
            padding: 20px;
            background-color: #ffffff;
            width: 400px;
            margin: auto;
            box-shadow: 5px 5px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .card img {
            width: 100%;
            border-radius: 10px;
        }
        .card h3 {
            margin-top: 10px;
        }
        .card .dropdown {
            margin-top: 20px;
        }
        .card button {
            margin-top: 20px;
        }
        </style>
        """

        st.markdown(card_css, unsafe_allow_html=True)

        card_html_3 = """
        <div class="card">
            <img src="{}" alt="Al Wathba">
            <h3>Al Wathba</h3>
            <div class="dropdown"></div>
            <div></div>
        </div>
        """.format(image_path_3)

        st.markdown(card_html_3, unsafe_allow_html=True)
        
        
    
        options_3 = ["4:30", "6:30", "8:30", "10:30"]  # Options for the second card

        selected_option_3 = st.selectbox("Select a cycling track", options_3)

        if st.button("Register for Al Wathba Ride"):
            st.success("You have succesfully registered for this ride.")
            if selected_option_3 == "4:30":
                ride_3 = "Al Wathba - 4:30 AM"
            elif selected_option_3 == "6:30":
                ride_3 = "Al Wathba - 6:30 AM"
            elif selected_option_3 == "8:30":
                ride_3 = "Al Wathba - 8:30 AM"
            elif selected_option_3 == "10:30":
                ride_3 = "Al Wathba - 10:30 AM"

            
            if not st.session_state.registered:
                st.session_state.registered = [ride_3]  # Initialize the list if it doesn't exist
            elif ride_3 not in st.session_state.registered:
                st.session_state.registered.append(ride_3)  # Append the new ride if it's not already registered
            else:
                st.warning("You are already registered for this ride.")
        
        if st.button("Al Wathba Cycling Track on Maps"):
            st.session_state.page, st.session_state.location = go_to_maps(location="Al Wathba")
            maps()
            
        # Fourth Card
        image_path_4 = "https://visitabudhabi.ae/-/media/project/vad/plan-your-trip/article-hub/cycling-in-abu-dhabi/al-dhafra-cycling.jpg?cx=0&cy=0&cw=334&ch=220&hash=6D494CBA1FCDA39756AE52627877A129"  # URL for the fourth image
        card_css = """
        <style>
        .card {
            border-radius: 1px;
            padding: 20px;
            background-color: #ffffff;
            width: 400px;
            margin: auto;
            box-shadow: 5px 5px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .card img {
            width: 100%;
            border-radius: 10px;
        }
        .card h3 {
            margin-top: 10px;
        }
        .card .dropdown {
            margin-top: 20px;
        }
        .card button {
            margin-top: 20px;
        }
        </style>
        """

        st.markdown(card_css, unsafe_allow_html=True)

        card_html_4 = """
        <div class="card">
            <img src="{}" alt="Your Image 4">
            <h3>Corniche Bike Lane</h3>
            <div class="dropdown"></div>
            <div></div>
        </div>
        """.format(image_path_4)

        st.markdown(card_html_4, unsafe_allow_html=True)
        
        
    
        options_4 = ["4:00 AM", "6:00 AM", "8:00 AM", "10:00 AM"]  # Options for the fourth card

        selected_option_4 = st.selectbox("Select a cycling track", options_4)

        if st.button("Register for Corniche Ride"):
            st.success("You have succesfully registered for this ride.")
            if selected_option_4 == "4:00 AM":
                ride_4 = "Corniche - 4:00 AM"
            elif selected_option_3 == "6:00 AM":
                ride_4 = "Corniche - 6:00 AM"
            elif selected_option_3 == "8:00 AM":
                ride_4 = "Corniche - 8:00 AM"
            elif selected_option_3 == "10:00 AM":
                ride_4 = "Corniche - 10:00 AM"
            
            if not st.session_state.registered:
                st.session_state.registered = [ride_4]  # Initialize the list if it doesn't exist
                
            elif ride_4 not in st.session_state.registered:
                st.session_state.registered.append(ride_4)  # Append the new ride if it's not already registered
            else:
                st.warning("You are already registered for this ride.")
        
        if st.button("Corniche Track on Maps"):
            st.session_state.page, st.session_state.location = go_to_maps(location="Corniche")
            maps()
            
        
        image_path_5 = "https://visitabudhabi.ae/-/media/project/vad/plan-your-trip/article-hub/cycling-in-abu-dhabi/al-dhafra-cycling.jpg?cx=0&cy=0&cw=730&ch=482&hash=F4BCACF477FEE47E8066490A7AB3154E" 

        st.markdown(card_css, unsafe_allow_html=True)

        card_html_5 = """
        <div class="card">
            <img src="{}" alt="Your Image 5">
            <h3>Al Dhafra</h3>
            <div class="dropdown"></div>
            <div></div>
        </div>
        """.format(image_path_5)

        st.markdown(card_html_5, unsafe_allow_html=True)
        
        
    
        options_5 = ["15:00", "16:00", "17:00", "18:00", "19:00"]  

        selected_option_5 = st.selectbox("Select a cycling track", options_5)

        if st.button("Register for Al Dhafra Ride"):
            st.success("You have succesfully registered for this ride.")
            if selected_option_5 == "15:00":
                ride_5 = "Al Dhafra - 15:00 PM"
            elif selected_option_5 == "16:00":
                ride_5 = "Al Dhafra - 16:00 PMI"
            elif selected_option_5 == "17:00":
                ride_5 = "Al Dhafra - 17:00 PM"
            elif selected_option_5 == "18:00":
                ride_5 = "Al Dhafra - 18:00 PM"
            elif selected_option_5 == "19:00":
                ride_5 = "Al Dhafra - 19:00 PM"
            
            if not st.session_state.registered:
                st.session_state.registered = [ride_5]  # Initialize the list if it doesn't exist
            elif ride_5 not in st.session_state.registered:
                st.session_state.registered.append(ride_5)  # Append the new ride if it's not already registered
            else:
                st.warning("You are already registered for this ride.")
        
        if st.button("Al Dhafra on Maps"):
            st.session_state.page, st.session_state.location = go_to_maps(location="dhafra")
            maps()

        # Sixth Card
        image_path_6 = "https://visitabudhabi.ae/-/media/project/vad/plan-your-trip/article-hub/cycling-in-abu-dhabi/al-ain-cycling.jpg?cx=0&cy=0&cw=730&ch=482&hash=195DF388331294DFEB010424379DD1FB"  # URL for the sixth image

        st.markdown(card_css, unsafe_allow_html=True)

        card_html_6 = """
        <div class="card">
            <img src="{}" alt="Your Image 6">
            <h3>Al Ain Cycling Road</h3>
            <div class="dropdown"></div>
            <div></div>
        </div>
        """.format(image_path_6)

        st.markdown(card_html_6, unsafe_allow_html=True)
        
        
    
        options_6 = ["5:00 AM -7:30 AM", "8:00 AM - 10:30 AM", "11:00 AM- 13:30PM", "15:30 PM - 17:00 PM"]  # Options for the sixth card

        selected_option_6 = st.selectbox("Select a cycling track", options_6)

        if st.button("Register for Al Ain Ride"):
            st.success("You have succesfully registered for this ride.")
            if selected_option_6 == "5:00 AM -7:30 AM":
                ride_6 = "Al Ain Cycling Road - 5:00 AM -7:30 AM"
            elif selected_option_6 == "8:00 AM - 10:30 AM":
                ride_6 = "Al Ain Cycling Road - 8:00 AM - 10:30 AM"
            elif selected_option_6 == "11:00 AM- 13:30PM":
                ride_6 = "Al Ain Cycling Road - 11:00 AM- 13:30PM"
            elif selected_option_6 == "15:30 PM - 17:00 PM":
                ride_6 = "Al Ain Cycling Road - 15:30 PM - 17:00 PM"

            if not st.session_state.registered:
                st.session_state.registered = [ride_6]  # Initialize the list if it doesn't exist
            elif ride_6 not in st.session_state.registered:
                st.session_state.registered.append(ride_6)  # Append the new ride if it's not already registered
            else:
                st.warning("You are already registered for this ride.")
        
        if st.button("Al Ain Cycling Road on Maps"):
            st.session_state.page, st.session_state.location = go_to_maps(location="alain")
            maps()

    elif st.session_state.page == "Profile":
        st.title("Profile")
        users = get_users()
        user = users[-1] if users else None  # Fetch the most recently added user
        
        if user:
            full_name = f"{user[0]} {user[1]}"
            email = user[2]
            profile_card = f"""
            <style>
            .profile-card {{
                border-radius: 10px;
                padding: 20px;
                background-color: #f0f0f0;
                width: 400px;
                margin: auto;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            .profile-card h2 {{
                margin-top: 0;
            }}
            </style>
            <div class="profile-card">
                <h2>{full_name}</h2>
                <p>{email}</p>
            </div>
            """
            st.markdown(profile_card, unsafe_allow_html=True)
       
        else:
            st.error("User not found.")
            
        if st.button("Log Out"):
            reset_session()
            st.session_state.page = "Auth"
            st.experimental_rerun()
        if st.button("Delete Account"):
            delete_account(email)
            reset_session()
            st.session_state.page = "Auth"
            st.experimental_rerun()


    elif st.session_state.page == "My Rides":
        st.title(selected)
        
        # Display registered rides
        if st.session_state.registered:
            st.write("Registered Rides:")
            for ride in st.session_state.registered:
                st.write(ride)
                # Add unregister button for each ride
                if st.button(f"Unregister from {ride}"):
                    st.session_state.registered.remove(ride)

        else:
            st.write("No rides registered yet.")
        
        
            
    elif st.session_state.page == "Maps":
        st.title("Maps")
        maps()
        
    elif st.session_state.page == "Weather":
        display_weather()