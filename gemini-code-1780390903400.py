import streamlit as st
import pandas as pd

st.set_page_config(page_title="Team Scorecard Dashboard", page_icon="📊", layout="wide")

# The public URL that streams your sheet data directly into the app
SHEET_ID = "1M1TY5TTPoaTlc4JiYPtS4YV7J7Y8DgQ0kUqbvR86S7s"
GID = "315475186"
GVIZ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={GID}"

@st.cache_data(ttl=3600) # Updates automatically every hour
def load_data():
    try:
        df = pd.read_csv(GVIZ_URL)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

df = load_data()

if df is not None:
    st.sidebar.header("Filter Options")
    
    # ⚠️ CRITICAL: Check your Google Sheet. 
    # Change 'Name' below to match the EXACT header of your team column (e.g., 'Agent', 'Team Member')
    name_column = 'Name' 
    
    if name_column in df.columns:
        team_members = sorted(df[name_column].dropna().unique())
        selected_member = st.sidebar.selectbox("Select Your Name:", team_members)
        user_data = df[df[name_column] == selected_member]
        
        st.title(f"📊 Scorecard: {selected_member}")
        st.markdown("---")
        
        st.markdown("### Your Detailed Feedback History")
        st.dataframe(user_data, use_container_width=True, hide_index=True)
    else:
        st.warning(f"Could not find the column '{name_column}' in your sheet.")
        st.markdown("### Columns actually found in your sheet:")
        st.write(list(df.columns))
        st.info("Please edit this file on GitHub and change the `name_column` variable to match one of the exact headers above.")
