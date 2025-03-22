import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk
import base64

# Set page config first
st.set_page_config(
    page_title="Friendship Tracker",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Simplified styling for better performance and mobile responsiveness
def add_styling():
    st.markdown(
        """
        <style>
        /* Clean solid background instead of gradient for better performance */
        .stApp {
            background-color: #1e3c72;
            color: white !important;
        }
        
        /* Simplified text styling */
        .css-18e3th9, .css-1d391kg, .css-1wrcr25, .stMarkdown {
            color: white !important;
        }
        
        /* Simplified headers */
        h1, h2, h3 {
            color: #f0f2f6 !important;
            font-weight: bold !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Simplified dataframe */
        .dataframe {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: none !important;
        }
        
        /* Remove card styling completely */
        div.element-container {
            background-color: transparent;
            border-radius: 0;
            padding: 2px;
            margin: 2px 0px;
            box-shadow: none;
        }
        
        /* Simpler metric containers */
        div[data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
            font-weight: bold;
            color: #ffffff !important;
        }
        
        /* Map styling - minimal */
        iframe {
            border: none !important;
            width: 100% !important;
        }
        
        /* Mobile responsive adjustments */
        @media (max-width: 768px) {
            .stApp {
                padding: 0 !important;
            }
            div.element-container {
                padding: 0px;
                margin: 0px;
            }
            div[data-testid="stMetricValue"] {
                font-size: 1.1rem !important;
            }
            h1 {
                font-size: 1.4rem !important;
            }
            h2 {
                font-size: 1.1rem !important;
            }
            h3 {
                font-size: 0.9rem !important;
            }
        }
        
        /* Clean profile images - simplified */
        .stImage img {
            border-radius: 50% !important;
            border-width: 2px !important;
            border-style: solid !important;
        }
        
        .best-friend-img img {
            border-color: #00ff00 !important;
        }
        
        .active-friend-img img {
            border-color: #4285f4 !important;
        }
        
        .inactive-friend-img img {
            border-color: #ffa500 !important;
        }
        
        .ex-friend-img img {
            border-color: #db4437 !important;
        }

        /* Clean up tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 5px 10px;
        }

        /* Minimize whitespace */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the styling function
add_styling()

# App title with clean styling
st.markdown('<h1 style="text-align: center;">Friendship Tracker (2022-2025)</h1>', unsafe_allow_html=True)

# Updated Karachi friends data with Ali Raza from Dadu
friends_data = [
    {"name": "Muhammad Uzair", "lat": 24.8760, "lon": 67.1768, "status": "Inactive Friend", "neighborhood": "Shah Faisal", "since": "2023", "image": "https://randomuser.me/api/portraits/men/32.jpg"},
    {"name": "Muhammad Raza Shirazi", "lat": 24.8937, "lon": 67.0466, "status": "Ex-Friend", "neighborhood": "Charminar Bahadurabad", "since": "2022", "image": "https://cdn.pixabay.com/photo/2017/06/20/08/55/small-dog-2422326_960_720.jpg"},
    {"name": "Sohail", "lat": 24.9027, "lon": 67.0877, "status": "Ex-Friend", "neighborhood": "Gulshan Block 6", "since": "2023", "image": "https://randomuser.me/api/portraits/men/33.jpg"},
    {"name": "Ehsan Elahi", "lat": 24.9372, "lon": 67.0626, "status": "Best Friend", "neighborhood": "Metrovile Site Area", "since": "2023", "image": "https://randomuser.me/api/portraits/men/88.jpg", "soulmate": True},
    {"name": "Najeebullah", "lat": 24.9214, "lon": 67.0495, "status": "Best Friend", "neighborhood": "FB Area Dastagir Colony", "since": "2022", "image": "https://randomuser.me/api/portraits/men/11.jpg", "soulmate": True},
    {"name": "Usman", "lat": 24.9143, "lon": 67.0552, "status": "Active Friend", "neighborhood": "FB Area", "since": "2023", "image": "https://randomuser.me/api/portraits/men/22.jpg"},
    {"name": "Waqar", "lat": 24.9256, "lon": 67.0600, "status": "Active Friend", "neighborhood": "Water Pump Sarena Mobile Market", "since": "2023", "image": "https://randomuser.me/api/portraits/men/45.jpg"},
    {"name": "Masharib", "lat": 24.9260, "lon": 67.0605, "status": "Active Friend", "neighborhood": "Water Pump Sarena Mobile Market", "since": "2023", "image": "https://randomuser.me/api/portraits/men/55.jpg"},
    {"name": "Ahmed Hussain", "lat": 24.8732, "lon": 67.1537, "status": "Active Friend", "neighborhood": "Shah Faisal", "since": "2023", "image": "https://randomuser.me/api/portraits/men/65.jpg"},
    {"name": "Ali Raza", "lat": 24.9008, "lon": 67.1146, "status": "Active Friend", "neighborhood": "Malir", "since": "2023", "image": "https://randomuser.me/api/portraits/men/75.jpg"},
    {"name": "Ahmed Ali", "lat": 24.9015, "lon": 67.1150, "status": "Active Friend", "neighborhood": "Malir", "since": "2023", "image": "https://randomuser.me/api/portraits/men/85.jpg"},
    {"name": "Barbar Behn", "lat": 39.2904, "lon": -76.6122, "status": "Best Friend", "neighborhood": "Baltimore, Maryland", "since": "2022", "image": "https://i.pravatar.cc/150?img=32", "soulmate": True},
    {"name": "Sahil", "lat": 24.9783, "lon": 67.0348, "status": "Best Friend", "neighborhood": "Surjani Town", "since": "Birth", "image": "https://randomuser.me/api/portraits/men/16.jpg"},
    {"name": "Ayan", "lat": 24.9783, "lon": 67.0348, "status": "Best Friend", "neighborhood": "Surjani Town", "since": "Birth", "image": "https://randomuser.me/api/portraits/men/23.jpg"},
    {"name": "Aqsa", "lat": 24.9783, "lon": 67.0348, "status": "Best Friend", "neighborhood": "Surjani Town", "since": "Birth", "image": "https://randomuser.me/api/portraits/women/52.jpg"},
    {"name": "Ammara", "lat": 24.9783, "lon": 67.0348, "status": "Best Friend", "neighborhood": "Surjani Town", "since": "Birth", "image": "https://randomuser.me/api/portraits/women/26.jpg"},
    {"name": "Zainab", "lat": 24.9783, "lon": 67.0348, "status": "Best Friend", "neighborhood": "Surjani Town", "since": "Birth", "image": "https://randomuser.me/api/portraits/women/29.jpg"},
    {"name": "Ammar", "lat": 24.9396, "lon": 67.0661, "status": "Best Friend", "neighborhood": "Al Noor Society", "since": "2024", "image": "https://randomuser.me/api/portraits/men/18.jpg"},
    {"name": "Zayan", "lat": 24.9343, "lon": 67.0425, "status": "Best Friend", "neighborhood": "PECHS", "since": "2023", "image": "https://randomuser.me/api/portraits/men/36.jpg"},
    {"name": "Yahyah", "lat": 24.9125, "lon": 67.0825, "status": "Best Friend", "neighborhood": "Gulshan-e-Iqbal", "since": "2024", "image": "https://randomuser.me/api/portraits/men/46.jpg"},
    {"name": "Maaz", "lat": 24.8978, "lon": 67.0775, "status": "Inactive Friend", "neighborhood": "Gulistan-e-Johar", "since": "2023", "image": "https://randomuser.me/api/portraits/men/56.jpg"},
    {"name": "Aridaman", "lat": 28.7041, "lon": 77.1025, "status": "Active Friend", "neighborhood": "Delhi, India", "since": "2025", "image": "https://randomuser.me/api/portraits/men/66.jpg"},
    {"name": "Ali Raza (Dadu)", "lat": 26.7319, "lon": 67.7769, "status": "Best Friend", "neighborhood": "Dadu, Sindh", "since": "2023", "image": "https://randomuser.me/api/portraits/men/77.jpg"},
]

friends_df = pd.DataFrame(friends_data)

# Set up color map
color_map = {
    "Best Friend": [0, 255, 0, 180],      # Green
    "Active Friend": [66, 133, 244, 180],    # Blue
    "Inactive Friend": [255, 165, 0, 180],  # Orange
    "Ex-Friend": [219, 68, 55, 180]         # Red
}

friends_df["color"] = friends_df["status"].map(lambda x: color_map[x])

# Create statistics for sidebar
total_friends = len(friends_df)
best_friends = len(friends_df[friends_df["status"] == "Best Friend"])
active_friends = len(friends_df[friends_df["status"] == "Active Friend"])
inactive_friends = len(friends_df[friends_df["status"] == "Inactive Friend"])
ex_friends = len(friends_df[friends_df["status"] == "Ex-Friend"])

# Show statistics in a neat row
cols = st.columns(5)
with cols[0]:
    st.metric("Total", total_friends)
with cols[1]:
    st.metric("Best", best_friends)
with cols[2]:
    st.metric("Active", active_friends)
with cols[3]:
    st.metric("Inactive", inactive_friends)
with cols[4]:
    st.metric("Ex", ex_friends)

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Map View", "Friend List", "Analytics"])

with tab1:
    # Map Subtabs
    map_tab1, map_tab2 = st.tabs(["Karachi", "Global"])
    
    with map_tab1:
        # Karachi view
        karachi_view_state = pdk.ViewState(
            latitude=24.8607, longitude=67.0011, zoom=10, pitch=0, bearing=0
        )
        
        karachi_friends = friends_df[~friends_df["neighborhood"].str.contains("Baltimore|Delhi|Dadu")]
        
        karachi_layer = pdk.Layer(
            "ScatterplotLayer",
            karachi_friends,
            get_position=["lon", "lat"],
            get_radius=300,
            get_fill_color="color",
            pickable=True,
            opacity=0.8,
            auto_highlight=True,
        )
        
        karachi_deck = pdk.Deck(
            layers=[karachi_layer],
            initial_view_state=karachi_view_state,
            tooltip={"text": "{name}\n{status}\n{neighborhood}\nSince: {since}"}
        )
        
        st.pydeck_chart(karachi_deck)
    
    with map_tab2:
        # Global view
        global_view_state = pdk.ViewState(
            latitude=25, longitude=67, zoom=4, pitch=0
        )
        
        global_friends_df = friends_df.copy()
        
        # Special highlighting for specific points
        global_friends_df["radius"] = global_friends_df.apply(
            lambda row: 100000 if row["name"] == "Barbar Behn" else 
                        50000 if row["name"] == "Aridaman" else
                        25000 if "Dadu" in row["neighborhood"] else
                        10000,
            axis=1
        )
        
        # Add special colors
        global_friends_df["color"] = global_friends_df.apply(
            lambda row: [255, 255, 0, 200] if row["name"] == "Barbar Behn" else 
                        [255, 0, 255, 200] if row["name"] == "Aridaman" else 
                        row["color"],
            axis=1
        )
        
        global_layer = pdk.Layer(
            "ScatterplotLayer",
            global_friends_df,
            get_position=["lon", "lat"],
            get_radius="radius",
            get_fill_color="color",
            pickable=True,
            opacity=0.8,
            auto_highlight=True,
        )
        
        # Text layer for special friends
        text_layer = pdk.Layer(
            "TextLayer",
            data=global_friends_df[(global_friends_df["name"] == "Barbar Behn") | 
                                  (global_friends_df["name"] == "Aridaman") | 
                                  (global_friends_df["name"] == "Ali Raza (Dadu)")],
            get_position=["lon", "lat"],
            get_text="name",
            get_size=16,
            get_color=[255, 255, 255],
            get_angle=0,
            get_text_anchor="middle",
            get_alignment_baseline="bottom",
            get_pixel_offset=[0, -20]
        )
        
        global_deck = pdk.Deck(
            layers=[global_layer, text_layer],
            initial_view_state=global_view_state,
            tooltip={"text": "{name}\n{status}\n{neighborhood}\nSince: {since}"}
        )
        
        # Simple color legend
        st.markdown("**🟢 Best | 🔵 Active | 🟠 Inactive | 🔴 Ex**")
        st.pydeck_chart(global_deck)

with tab2:
    # Friend List with better categorization
    
    # Function to apply CSS class based on friend status
    def get_css_class(status):
        if status == "Best Friend":
            return "best-friend-img"
        elif status == "Active Friend":
            return "active-friend-img"
        elif status == "Inactive Friend":
            return "inactive-friend-img"
        else:
            return "ex-friend-img"
    
    # First display BFFs (Soul Mates) in their own section
    st.subheader("💚 BFFs / Soul Mates 💚")
    bff_df = friends_df[(friends_df["status"] == "Best Friend") & (friends_df["soulmate"] == True)]
    
    if len(bff_df) > 0:
        # Layout for mobile-friendly display
        num_columns = 5
        columns = st.columns(num_columns)
        
        for i, (_, friend) in enumerate(bff_df.iterrows()):
            col_idx = i % num_columns
            with columns[col_idx]:
                # Apply appropriate CSS class
                css_class = get_css_class(friend["status"])
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                st.image(friend['image'], width=50)
                st.markdown('</div>', unsafe_allow_html=True)
                st.caption(f"{friend['name']} ⭐")
                st.caption(f"{friend['neighborhood']}")
    
    # Then display other best friends (non-soulmates)
    st.subheader("🟢 Best Friends")
    best_df = friends_df[(friends_df["status"] == "Best Friend") & (~friends_df["soulmate"].fillna(False))]
    
    if len(best_df) > 0:
        # Layout for mobile-friendly display
        num_columns = 5
        columns = st.columns(num_columns)
        
        for i, (_, friend) in enumerate(best_df.iterrows()):
            col_idx = i % num_columns
            with columns[col_idx]:
                css_class = get_css_class(friend["status"])
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                st.image(friend['image'], width=45)
                st.markdown('</div>', unsafe_allow_html=True)
                st.caption(f"{friend['name']}")
                st.caption(f"{friend['neighborhood']}")
    
    # Active Friends
    st.subheader("🔵 Active Friends")
    active_df = friends_df[friends_df["status"] == "Active Friend"]
    
    if len(active_df) > 0:
        num_columns = 5
        columns = st.columns(num_columns)
        
        for i, (_, friend) in enumerate(active_df.iterrows()):
            col_idx = i % num_columns
            with columns[col_idx]:
                css_class = get_css_class(friend["status"])
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                st.image(friend['image'], width=40)
                st.markdown('</div>', unsafe_allow_html=True)
                st.caption(f"{friend['name']}")
                st.caption(f"{friend['neighborhood']}")
    
    # Inactive Friends
    st.subheader("🟠 Inactive Friends")
    inactive_df = friends_df[friends_df["status"] == "Inactive Friend"]
    
    if len(inactive_df) > 0:
        num_columns = 5
        columns = st.columns(num_columns)
        
        for i, (_, friend) in enumerate(inactive_df.iterrows()):
            col_idx = i % num_columns
            with columns[col_idx]:
                css_class = get_css_class(friend["status"])
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                st.image(friend['image'], width=40)
                st.markdown('</div>', unsafe_allow_html=True)
                st.caption(f"{friend['name']}")
                st.caption(f"{friend['neighborhood']}")
    
    # Ex Friends
    st.subheader("🔴 Ex-Friends")
    ex_df = friends_df[friends_df["status"] == "Ex-Friend"]
    
    if len(ex_df) > 0:
        num_columns = 5
        columns = st.columns(num_columns)
        
        for i, (_, friend) in enumerate(ex_df.iterrows()):
            col_idx = i % num_columns
            with columns[col_idx]:
                css_class = get_css_class(friend["status"])
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                st.image(friend['image'], width=35)  # Smaller for ex-friends
                st.markdown('</div>', unsafe_allow_html=True)
                st.caption(f"{friend['name']}")
                st.caption(f"{friend['neighborhood']}")

with tab3:
    # Analytics with simplified view
    analytics_tab1, analytics_tab2 = st.tabs(["Timeline", "Statistics"])
    
    with analytics_tab1:
        # Friendship growth over time
        years = ["2022", "2023", "2024", "2025"]
        friends_count = [12, 20, 26, total_friends]
        
        # Format dates
        dates = [f"{year}-01-01" for year in years]
        
        time_data = {
            'date': pd.to_datetime(dates),
            'friend_count': friends_count
        }
        growth_df = pd.DataFrame(time_data)
        
        st.subheader("Friendship Growth")
        st.line_chart(growth_df.set_index('date'))
        
    with analytics_tab2:
        # Create two columns for key charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Status breakdown
            status_counts = friends_df["status"].value_counts()
            st.subheader("Status Breakdown")
            st.bar_chart(status_counts)
        
        with col2:
            # Yearly breakdown
            year_df = friends_df[friends_df["since"] != "Birth"]
            year_counts = year_df["since"].value_counts().sort_index()
            st.subheader("Friends Made Each Year")
            st.bar_chart(year_counts)
        
        # Friendship longevity
        st.subheader("Friendship Longevity")
        
        def categorize_longevity(since):
            if since == "Birth":
                return "Lifelong"
            elif since == "2022":
                return "3+ Years"
            elif since == "2023":
                return "2+ Years"
            elif since == "2024":
                return "1+ Year"
            else:
                return "New (<1 Year)"
        
        friends_df["longevity"] = friends_df["since"].apply(categorize_longevity)
        longevity_counts = friends_df["longevity"].value_counts()
        longevity_order = ["Lifelong", "3+ Years", "2+ Years", "1+ Year", "New (<1 Year)"]
        longevity_df = pd.DataFrame({"Longevity": longevity_order, "Count": [longevity_counts.get(x, 0) for x in longevity_order]})
        st.bar_chart(longevity_df.set_index("Longevity"))

# Ultra-minimal footer
st.markdown("<div style='text-align:center;font-size:0.7rem;'>Felix's Friendship Tracker © 2025</div>", unsafe_allow_html=True)

# Fix the C-style comment at the beginning of the file