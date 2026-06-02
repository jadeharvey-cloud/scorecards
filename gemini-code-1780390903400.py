@st.cache_data(ttl=3600)
def load_data():
    try:
        # Reads the file directly from your GitHub instead of Google Sheets
        df = pd.read_csv("data.csv")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None
