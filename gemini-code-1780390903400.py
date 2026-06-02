import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Set up page configuration
st.set_page_config(
    page_title="Team Scorecard Dashboard",
    page_icon="📊",
    layout="wide"
)

# 1. Access the Google Sheet Securely
# Paste your full Google Sheet URL below
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1M1TY5TTPoaTlc4JiYPtS4YV7J7Y8DgQ0kUqbvR86S7s/edit?gid=315475186#gid=315475186"

@st.cache_data(ttl=3600)  # Caches data for 1 hour
def load_data():
    try:
        # Uses Streamlit's built-in Sheets connection
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=SPREADSHEET_URL, ttl="1h")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error connecting to Google Sheet: {e}")
        return None

df = load_data()

if df is not None:
    # 2. Sidebar Configuration for Filtering
    st.sidebar.header("Filter Options")
    
    # Change 'Name' below to match your exact column header for the 22 people.
    name_column = 'Name' 
    
    if name_column in df.columns:
        team_members = sorted(df[name_column].dropna().unique())
        selected_member = st.sidebar.selectbox("Select Your Name:", team_members)
        
        user_data = df[df[name_column] == selected_member]
        
        # 3. Main Dashboard UI
        st.title(f"📊 Scorecard: {selected_member}")
        st.markdown("---")
        
        cols = st.columns(3)
        with cols[0]:
            if 'Feedback Score' in df.columns:
                score = user_data['Feedback Score'].values[0]
                st.metric(label="Latest Feedback Score", value=f"{score}")
            else:
                st.info("Add a 'Feedback Score' column to see summary metrics.")
                
        with cols[1]:
            if 'Tasks Completed' in df.columns:
                tasks = user_data['Tasks Completed'].values[0]
                st.metric(label="Tasks Completed", value=f"{tasks}")
                
        with cols[2]:
            st.metric(label="Total Records", value=len(user_data))
            
        st.markdown("### Your Detailed Feedback History")
        st.dataframe(user_data, use_container_width=True, hide_index=True)
        
    else:
        st.warning(f"Could not find the column '{name_column}' in your sheet.")
        st.markdown("### Preview of raw data headers found:")
        st.write(list(df.columns))
