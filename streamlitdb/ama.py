 

import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from mysql.connector import Error
import plotly.graph_objs as go



# Add custom CSS to create a navigation bar
st.markdown("""
<style>
.navbar {
  overflow: hidden;
  background-color: #333;
            width: 100%; /* Set width to 100% */
}

.navbar a {
  float: left;
  display: block;
  color: #f2f2f2;
  text-align: center;
  padding: 20px 50px;
  text-decoration: none;
}
            .navbar img {
  height: 60px; /* Adjust height of the logo */
  width: auto; /* Ensure aspect ratio is maintained */
  padding: 4px; /* Add padding around the logo */
            }

.navbar a:hover {
  background-color: #ddd;
  color: black;
}

.navbar a.active {
  background-color: #4CAF50;
  color: white;
}
</style>
""", unsafe_allow_html=True)

# Initialize session_state variables
if 'nav_selection' not in st.session_state:
    st.session_state.nav_selection = 'Home'

# Navigation bar HTML
nav_html = """
<div class="navbar">
<img src="data:image/png;base64,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" alt="Logo">
  <a class="{home_class}" href="#home">Home</a>
  <a class="{about_class}" href="#about">About</a>
  <a class="{contact_class}" href="#contact">Contact</a>
</div>
""".format(
    home_class="active" if st.session_state.nav_selection == 'Home' else "",
    about_class="active" if st.session_state.nav_selection == 'About' else "",
    contact_class="active" if st.session_state.nav_selection == 'Contact' else ""
)

# Display the navigation bar
st.markdown(nav_html, unsafe_allow_html=True)

# Main content based on selection
if st.session_state.nav_selection == 'Home':
    st.title('')
    # Add content for the home page here
elif st.session_state.nav_selection == 'About':
    st.title('About Page')
    # Add content for the about page here
elif st.session_state.nav_selection == 'Contact':
    st.title('Contact Page')






# Add custom CSS to create a background color
st.markdown("""
<style>
body {
    background-color: #e0f7fa;
}
.sidebar .sidebar-content {
    background-color: #004d40;
}
.sidebar .sidebar-content button {
    background-color: #e0f7fa;
    color: black;
}
.sidebar .sidebar-content button:hover {
    background-color: #b2ebf2;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# Initialize session_state variables
if 'page' not in st.session_state:
    st.session_state.page = 'Show 1'
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

# Function to establish a connection to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='qwert',
            database='college'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return None

# Function to fetch data from a given table
def fetch_data(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=cursor.column_names)
        cursor.close()
        return df
    except Error as e:
        st.error(f"Error fetching data from MySQL: {e}")
        return pd.DataFrame()

# Function to display data and plots
def display_data(df):
    st.subheader('Channel Data')
    st.write(df)

    st.title('Bar Graph')
    fig = px.bar(df, x='Timeslots', y='Shows', labels={'Timeslots': 'Timeslots', 'Shows': 'Shows'})
    st.plotly_chart(fig)

    st.subheader('Pie Chart')
    pie_fig = px.pie(df, values='Shows', names='Timeslots', title='Pie Chart')
    st.plotly_chart(pie_fig)

    time_slots = {
        1: '00:00:00-03:00:00',
        2: '03:00:00-06:00:00',
        3: '06:00:00-09:00:00',
        4: '09:00:00-12:00:00',
        5: '12:00:00-15:00:00',
        6: '15:00:00-18:00:00',
        7: '18:00:00-21:00:00',
        8: '21:00:00-24:00:00'
    }

    selected_timeslot = st.slider('Select a timeslot', min_value=1, max_value=8, value=1, key='timeslot_slider')
    st.subheader(f'Selected Timeslot: {time_slots[selected_timeslot]}')

    if f'TD{selected_timeslot}' in df.columns:
        selected_pie_fig = px.pie(df, values=f'TD{selected_timeslot}', names='T1',  width=500, height=500)
        selected_pie_fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
        st.plotly_chart(selected_pie_fig)
    else:
        st.warning(f"Timeslot TD{selected_timeslot} not found in the data.")

    line_data = [go.Scatter(x=df['Timeslots'], y=df['Shows'], mode='lines', name='Shows')]
    line_layout = go.Layout(title='Line Chart', xaxis=dict(title='Timeslots'), yaxis=dict(title='Shows'))
    line_fig = go.Figure(data=line_data, layout=line_layout)
    st.plotly_chart(line_fig)

# Function to navigate to a different page and fetch data
def navigate_to(page, table_name=None):
    st.session_state.page = page
    if table_name:
        connection = create_connection()
        if connection:
            df = fetch_data(connection, table_name)
            connection.close()
            if not df.empty:
                st.session_state.df = df
            else:
                st.session_state.df = pd.DataFrame()
                st.error("No data found or failed to fetch data.")

# Create a side navigation bar
with st.sidebar:
    st.title("Navigation")
    if st.button(' Week 1 Data'):
        navigate_to('Show 1', 'tenmay10')
    if st.button(' Week 2 Data'):
        navigate_to('Show 2', 'rock1')
    if st.button(' Week 3 Data'):
        navigate_to('Show 3','timedb3')
    if st.button(' Week 4 Data'):
        navigate_to('Show 4','timedb0')
    if st.button(' Week 5 Data'):
        navigate_to('Show 5','timedb7')
    if st.button(' Week 6 Data'):
        navigate_to('Show 6','timedb8')
# Main content based on selection
if st.session_state.page == 'Show1 ':
    st.title(' Week 1 Data ')
    if not st.session_state.df.empty:
        display_data(st.session_state.df)
elif st.session_state.page == 'Show 2':
    st.title('  Week 2 Data ')
    if not st.session_state.df.empty:
        display_data(st.session_state.df)
elif st.session_state.page == 'Show 3':
    st.title('  Week 3 Data ')
    if not st.session_state.df.empty:
        display_data(st.session_state.df)
elif st.session_state.page == 'Show 4':
    st.title('  Week 4 Data')
    if not st.session_state.df.empty:
        display_data(st.session_state.df)        
elif st.session_state.page == 'Show 5':
    st.title('  Week 5 Data ')
    if not st.session_state.df.empty:
        display_data(st.session_state.df)  
elif st.session_state.page == 'Show 6':
    st.title('  Week 6 Data ')
    if not st.session_state.df.empty:
        display_data(st.session_state.df)                    
# elif st.session_state.page == 'Show 3':
    else:
     st.write("This is Show 3 page content.")


# Initialize session_state variables for each show
if 'show1_df' not in st.session_state:
    connection = create_connection()
    if connection:
        st.session_state.show1_df = fetch_data(connection, 'tenmay10')
        connection.close()
        
        if st.session_state.show1_df.empty:
            st.session_state.show1_df = pd.DataFrame()
            st.error("No data found or failed to fetch data.")

if 'show2_df' not in st.session_state:
    st.session_state.show2_df = pd.DataFrame()
if 'show3_df' not in st.session_state:
    st.session_state.show3_df = pd.DataFrame()

# Function to navigate to a different page for Show 1
def navigate_to_show1():
    st.session_state.page = 'Show 1'

    

# Function to navigate to a different page and fetch data for Show 2
def navigate_to_show2():
    st.session_state.page = 'Show '
    connection = create_connection()
    if connection:
        st.session_state.show2_df = fetch_data(connection, 'rock1')
        connection.close()
        if st.session_state.show2_df.empty:
            st.session_state.show2_df = pd.DataFrame()
            st.error("No data found or failed to fetch data.")

# Function to navigate to a different page for Show 3
def navigate_to_show3():
    st.session_state.page = 'Show '


# Main content based on selection
if st.session_state.page == 'Show 1':
    st.title('')
    if not st.session_state.show1_df.empty:
        display_data(st.session_state.show1_df)
elif st.session_state.page == 'Show 2':
    st.title('')
    if not st.session_state.show2_df.empty:
        display_data(st.session_state.show2_df)
elif st.session_state.page == 'Show 3':
    st.title('')
    if not st.session_state.show3_df.empty:
        display_data(st.session_state.show3_df)    
elif st.session_state.page == 'Show 3':
    st.title('')
    if not st.session_state.show4_df.empty:
        display_data(st.session_state.show4_df)   
elif st.session_state.page == 'Show 4':
    st.title('')
    if not st.session_state.show5_df.empty:
        display_data(st.session_state.show5_df)

elif st.session_state.page == 'Show 3':
    st.title('')
    st.write("")



























