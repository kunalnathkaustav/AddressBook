
# --- importing the libraries needed for the project
import streamlit as st
import json
from streamlit_lottie import st_lottie
import sqlite3 as sq
import datetime
from string import *
import re
import random as ra
from streamlit_option_menu import option_menu


# --- dimensions of the page
st.set_page_config(page_title= "Address-Manager",page_icon="🗺",layout= "wide")



mydb = sq.connect('address.db')
cursor = mydb.cursor()


cursor.execute('''
        CREATE TABLE IF NOT EXISTS Address_book (
            Sl_no INTEGER PRIMARY KEY AUTOINCREMENT,
            flat varchar(200),
            area varchar(200),
            landmark varchar(200),
            favourite char(4),
            ph_no int(10),
            date DATE);''')


cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authentication(
            user_id varchar(30) PRIMARY KEY,
            user_name TEXT,
            password varchar(10));''')



# --- functions for inserting data in the table


def add_address(f,a,ph_no,l = "no",d = datetime.date.today(),fv = "no"):
    cursor.execute("INSERT INTO Address_book(flat,area,landmark,favourite,ph_no,date) VALUES(?,?,?,?,?,?)",(f,a,l,fv,ph_no,d))
    mydb.commit()
    return cursor.lastrowid

def add_to_fav(fav_id):
    cursor.execute("UPDATE Address_book set favourite = 'yes' where sl_no = ?",(fav_id,))
    mydb.commit()

def show():
    cursor.execute("SELECT * FROM Address_book")
    data = cursor.fetchall()
    mydb.commit()
    s_data = [tuples for tuples in data ]
    return s_data    

def search_by_date(search_date):
    cursor.execute("SELECT * FROM Address_book WHERE date = ?",(search_date,))
    search_data = cursor.fetchall()
    d_data = [tuples for tuples in search_data]
    return d_data

def show_favourites():
    cursor.execute("SELECT * FROM Address_book WHERE favourite = 'yes'")
    fav_data = cursor.fetchall()
    mydb.commit()
    f_data = [tuples for tuples in fav_data]
    return f_data



# --- country names for country input widget
country_names = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
    "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso",
    "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic",
    "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia",
    "Cuba", "Cyprus", "Czechia", "Denmark", "Djibouti", "Dominica", "Dominican Republic",
    "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea",
    "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia",
    "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India",
    "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica",
    "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South",
    "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia",
    "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia",
    "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico",
    "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
    "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua",
    "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama",
    "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar",
    "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia",
    "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
    "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore",
    "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan",
    "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan",
    "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
    "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]


# --- list for storing the sentences for giggle of the day
funny_quotes = ["Lost your keys? No worries, our address book can find your house faster than you can say 'I left them on the kitchen counter.",
                "Our address manager is so smart, it once gave directions to Narnia - turns out it's just a wardrobe away!",
                "Forget GPS, our address book knows where you are before you even get there!",
                "Our address book is so efficient, it once delivered a letter to Santa before the writer even finished their wishlist!",
                "We're so confident in our address book that we sent it on a vacation to the Bermuda Triangle - it came back with postcards!",
                "Our address manager is like a superhero for lost mail - faster than a speeding envelope!",
                "We don't just store addresses; we whisper sweet directions to lost packages until they find their way home.",
                "Our address book is so well-connected, it knows the guy who knows the guy who knows the guy... you get the idea.",
                "If our address book were a detective, Sherlock Holmes would be asking for its autograph."]



# --- a variable to store the date
min_date = datetime.date(2000,1,1)
max_date = datetime.date.today()







# --- function for loading images in the webpage
def load_lottie(filepath:str):
    with open(filepath, "r") as f:
        return json.load(f)

head_emj = load_lottie("lotties\head_emj.json")
feature_emj = load_lottie("lotties\feature.json")
app_emj = load_lottie("lotties\app_emj.json")
search_emj = load_lottie("lotties\search_emj.json")
fav_emj = load_lottie("lotties\fav_emj.json")
add_emj = load_lottie("lotties\add_emj.json")
modify_emj = load_lottie("lotties\modify_emj.json")
about_emj = load_lottie("lotties\about_emj.json")
view_add_emj = load_lottie("lotties\view_address_emj.json")





opt_selected = option_menu(
    menu_title= None,
    options = ["Home","Your Addresses","About"],
    icons=  ["house-fill", "bookmarks-fill","info-circle-fill"],
    default_index = 0,
    orientation= "horizontal")


# --- containers for storing different parts of the webpage
header = st.container()
feature_body = st.container()
app_body = st.container()
about = st.container()



if opt_selected == 'Home':
    with header:

        st.write("##")
        left,mid,right = st.columns((2,1,5))

        with left:
            st.subheader("Welcome to,")
            st.title("Address Manager")

        with mid:
            st_lottie(head_emj, loop = True, speed = 1, quality = 'high',height = 180,key = "head")

        st.write('---')
        st.write('<span style = "color : white;">Welcome to the Address Manager, your personalized\
                    solution for organizing and managing addresses with ease. This app is designed to\
                    simplify your life by providing a user-friendly interface to store,\
                    retrieve, and manage addresses efficiently.</span>',unsafe_allow_html= True)
        


            
    with feature_body:
        st.write('---')

        left_col,right_col = st.columns((2,1))

        with left_col:
            st.header('Features')
            st.write('##')
            st.write(
                """
                Say goodbye to address amnesia - our solution makes remembering a breeze!
                - Add addresses - Effortlessly expand your address book with a simple tap - adding locations made swift and easy!
                - Modify addresses - Tailor your addresses to perfection with the power to edit and update details on the fly.
                - Search by date - Navigate through time seamlessly - find addresses based on dates for a personalized touch.
                - Favourites - Elevate your go-to spots - mark favorites and access them with a single touch, making every address special.
                """
                )        
        with right_col:
            st_lottie(feature_emj,loop = True, height = 300, key = "feature")
        
        st.write('---')





    with app_body:

        l_app,m_app,m2_app,r_app = st.columns((3,1,0.5,10))
        with l_app:
            st.header('Get Started Here!')
        with m_app:
            st_lottie(app_emj, loop = True,key = "app")
        with r_app:
            st.header('Unleash the Power of Connected Living with our Address Book Wizardry!')
            st.write('''
                        Get ready to revolutionize the way you manage your contacts. 
                        Our Address manager empowers you with a suite of user-friendly functions designed to simplify your 
                        contact management experience. From effortless data input to powerful search capabilities, discover how you
                        can effortlessly organize and access your contacts like never before. Dive into the future of contact 
                        management - get started with Your Address manager today!
                    ''')
            
        st.write("##")
        
        st.subheader("Add address:")

        a_left,a_right = st.columns((2,10))
        inp_left,inp_mid,inp_right = st.columns((2,2,8))

        with a_left:
            st_lottie(add_emj, loop = True, quality = "high", height= 200, key = "add address emoji")

        with inp_left:
            
            input_placeholder = st.empty()
            
            flat = st.text_input('Flat/ House no/ Floor/ Building *',placeholder='Type here...',key = "flat input")
            area = st.text_input('Area/ Sector/ Locality *',placeholder='Type here...',key = "area input")
            landmark = st.text_input('Nearby Landmark (optional) ',placeholder='Type here...',key = "landmark input")
        
        with inp_mid:

            pincode = st.text_input('Pincode *',placeholder='Type here...', key = 'pincode input', help = "areas marked as * can't be empty")
            country = st.selectbox('Country *',country_names,index = country_names.index("India"),key = "country input")
            ph_no = st.text_input('Contact Number *',placeholder='Type here...', key = "phone number input")

        l_add, r_add = st.columns((1,20))
        with l_add:
            save = st.button('save', key = "save button")
        with r_add:
            fav = st.button('Add to favourites',key = "favourite button")
        


        if "button_value" not in st.session_state:
            st.session_state.button_value = None 
        
        if save:
            if flat == '':
                st.error("Flat/ House no/ Floor/ Building * can't be empty!",icon="❌")
            elif area == '':
                st.error("Area/ Sector/ Locality * can't be empty!",icon="❌")
            elif ph_no == '':
                st.error("Contact Number * can't be empty!",icon="❌")
            
            elif ph_no:
                try:
                    pattern = re.compile(r"^\d{10}$|^\d{3}-\d{3}-\d{4}$")
                    result = pattern.match(ph_no)
                    
                    if not result:
                        st.error("Contact number must contain digits (0-9) in the format 555-555-5555 or 5555555555!",icon="❌")
                    
                    else:
                        if landmark == '':
                            fav_val = add_address(flat,area,ph_no)
                            st.session_state.button_value = fav_val
                            st.success('Address saved!',icon="✅")
                        else:
                            fav_val = add_address(flat,area,ph_no,landmark)
                            st.session_state.button_value = fav_val
                            st.success('Address saved!',icon="✅")
                
                except Exception:
                    st.error(f"An error occured while saving contact number ")

        if fav:
            if flat == '':
                st.error("Flat/ House no/ Floor/ Building * can't be empty!",icon="❌")
            elif area == '':
                st.error("Area/ Sector/ Locality * can't be empty!",icon="❌")
            elif ph_no == '':
                st.error("Contact Number * can't be empty!",icon="❌")
            else:
                add_to_fav(st.session_state.button_value)
                st.warning('Added to favourites!',icon = "⭐")
    st.write('---')

#- Your address section of the day
        
elif opt_selected == "Your Addresses":
    st.write("##")
    st.subheader("Your Addresses")
    st.write('''
                Dive into the "Your Addresses" section to view, modify, and search through your personalized collection. Easily navigate through your records, 
                and with the click of a button, toggle between viewing your addresses or modifying them seamlessly. Looking for a specific entry? Our powerful 
                search feature allows you to find addresses by date, ensuring you locate information swiftly. Take it a step further by marking your favorites for quick access in the "View Favourites" option.
                Simplify your address management experience with our user-friendly interface, designed to make your life easier and more organized!
                ''')
    st.write("---")
    y_left,y_mid,y_right = st.columns((5,5,10))
    
    with y_left:   
        options = st.radio('**Select option:**',('View Addresses','Search by date','Favourites'))

    with y_mid:
        st_lottie(view_add_emj, loop = True , height = 240, key = "view addrress emoji")

    with y_right:
        num = ra.randint(0,len(funny_quotes)-1)
        st.header("Giggle of the day!!")
        st.subheader(funny_quotes[num])
    
    if options == 'View Addresses':

        st.write("##")
        st.subheader('Showing Addresses:')
        st.write("Unlock the Magic: Locate Your Addresses on Gmaps! 🗺️✨")
        st.write('##')
        counter = 1
        m_counter = 0
        values = show()
        
        for tuples in values:
            show_d = [i for i in tuples if i not in ("yes","no")]
            st.write(tuple(show_d))
            m_counter += 1
            counter += 1
            if counter > 2:
                break 

        show_m = st.button('Show More',key = "show button")
        if show_m:
            m_counter = 0
            for tuples in values:
                show_d = [i for i in tuples if i not in ("yes","no")]
                if int(show_d[0]) > 2:
                    st.write(tuple(show_d))    
                elif show_d == []:
                    st.info("No More Addresses!!")
                m_counter += 1
            
            st.info("All Addresses shown!!")                    
            
    
    
    elif options == 'Search by date':

        st.write("##")
        st.subheader('Search by date:')

        s_left,s_mid,s_right = st.columns((2,1,10))

        with s_left:
            st_lottie(search_emj, loop = True, quality = "high", height = 200,key = "search emoji")

        date = st.date_input("Select date",help = 'choose a date from the calendar',value = max_date,min_value=min_date,max_value=max_date)
        s_data = search_by_date(date)        
        for tuples in s_data:
            show_d = [i for i in tuples if i not in ("yes","no")]
            st.write(tuple(show_d))

    
    
    elif options == 'Favourites':
        st.write("##")
        st.subheader("Your Favourite List: ")

        f_left,f_mid,f_right = st.columns((2,1,10))

        with f_left:
            st_lottie(fav_emj, loop = True, quality = "high", key = "favourite emoji")

        favourite_data = show_favourites()
        for tuples in favourite_data:
            show_d = [i for i in tuples if i not in ("yes","no")]
            st.write(tuple(show_d))        



# -- about section of the app
elif opt_selected == "About":
    
    with about:

        st.write("---")
        st.write("##")
        st.header("About this app!")
        st.write('''
                    Greetings! I'm the creator of Address Manager, a humble endeavor that emerged from my personal
                  commitment and efforts during my capstone project at VIT-AP. In this journey, I sought to bring you an
                  innovative web app designed to simplify the management of your addresses.

                    Fueled by my passion for technology and a relentless pursuit of learning,
                  I poured my heart and soul into crafting a tool that embodies simplicity and functionality. 
                 I firmly believe in the power of connectivity and the transformative potential of thoughtful design.

                    Join me on this solo venture as I invite you to explore and engage with my web app.
                  Every click, every feature, and every interaction reflects not just my technical skills but also
                  my dedication to creating a tool that makes a positive impact on your daily life.
                    ''')
        st.write("---")
        st.write("##")
        w_left,w_right = st.columns((3,7))
        
        with w_right:
            st_lottie(about_emj, loop= True,height= 270,key= "about emoji")
        with w_left:
            st.header("About the Creator!")
            st.write('''
                  I am a student at VIT-AP, and for my capstone project, I have developed a straightforward yet effective data storage and retr
                 ieval application using Streamlit. The app serves as a basic platform for storing and displaying addresses without the complexity of a login page.
                  Its simplicity is intentional, focusing on providing users with a user-friendly experience for managing and
                  accessing address information effortlessly. As part of my academic journey, this project reflects my 
                 commitment to practical application and problem-solving, showcasing the skills I've acquired during my time at VIT-AP.
                ''')
            st.write('---')
        st.markdown("[LinkedIN](https://www.linkedin.com/in/kunal-nath-882b2326b/)",unsafe_allow_html= True)
        
