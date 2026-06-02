import streamlit as st
import pandas as pd

# Set up page configuration
st.set_page_config(
    page_title="Team Scorecard Dashboard",
    page_icon="📊",
    layout="wide"
)

# 1. Access the Google Sheet
# Converting the standard edit URL into an export CSV URL
SHEET_ID = "1M1TY5TTPoaTlc4JiYPtS4YV7J7Y8DgQ0kUqbvR86S7s"
GID = "315475186"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=3600)  # Caches data for 1 hour to keep it fast, updates automatically
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        # Clean up column names (strip whitespace)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error connecting to Google Sheet: {e}")
        return None

df = load_data()

if df is not None:
    # 2. Sidebar Configuration for Filtering
    st.sidebar.header("Filter Options")
    
    # ASSUMPTION: Your sheet has a column named 'Name' or 'Team Member'. 
    # Change 'Name' below to match your exact column header for the 22 people.
    name_column = 'Name' 
    
    if name_column in df.columns:
        team_members = sorted(df[name_column].dropna().unique())
        selected_member = st.sidebar.selectbox("Select Your Name:", team_members)
        
        # Filter the dataframe for the selected individual
        user_data = df[df[name_column] == selected_member]
        
        # 3. Main Dashboard UI
        st.title(f"📊 Scorecard: {selected_member}")
        st.markdown("---")
        
        # Example Metric Display (Customize these based on your sheet's actual columns)
        # Let's assume you have 'KPI 1', 'KPI 2', and 'Feedback Score' columns
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
        # Display their filtered rows neatly in a table
        st.dataframe(user_data, use_container_width=True, hide_index=True)
        
    else:
        st.warning(f"Could not find the column '{name_column}' in your sheet.")
        st.markdown("### Preview of raw data headers found:")
        st.write(list(df.columns))
        st.info("Please modify the `name_column` variable in the code to match one of the headers above.")