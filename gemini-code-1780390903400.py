import streamlit as st
import pandas as pd

# 1. Setup page configuration
st.set_page_config(
    page_title="Team Scorecard Dashboard",
    page_icon="📊",
    layout="wide"
)

# 2. Load the data from your uploaded GitHub CSV file
@st.cache_data(ttl=3600)
def load_data():
    try:
        # Reads the data.csv file you upload to GitHub
        df = pd.read_csv("data.csv")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Could not find or read 'data.csv'. Make sure you uploaded it to GitHub! Error details: {e}")
        return None

df = load_data()

if df is not None:
    # 3. Sidebar Filter Configuration
    st.sidebar.header("Filter Options")
    
    # ⚠️ CHANGE 'Name' to match your spreadsheet's exact team name column header if needed
    name_column = 'Name' 
    
    if name_column in df.columns:
        team_members = sorted(df[name_column].dropna().unique())
        selected_member = st.sidebar.selectbox("Select Your Name:", team_members)
        
        # Filter rows for the selected person
        user_data = df[df[name_column] == selected_member]
        
        # 4. Main Dashboard UI
        st.title(f"📊 Scorecard: {selected_member}")
        st.markdown("---")
        
        st.markdown("### Your Detailed Feedback History")
        st.dataframe(user_data, use_container_width=True, hide_index=True)
    else:
        st.warning(f"Could not find the column '{name_column}' in your file.")
        st.markdown("### Columns actually found in your data.csv:")
        st.write(list(df.columns))
        st.info("Please edit app.py on GitHub and change `name_column = 'Name'` to match one of the headers above.")
        
