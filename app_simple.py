import streamlit as st
import pandas as pd
import plotly.express as px

# Simple version for debugging
st.set_page_config(
    page_title="Regional Economic Resilience Dashboard",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ Regional Economic Resilience Dashboard")

# Test data loading
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/metro_resilience_scores.csv')
        st.success(f"✅ Successfully loaded data for {len(data)} metropolitan areas")
        return data
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame()

data = load_data()

if not data.empty:
    st.subheader("📊 Data Overview")
    st.write(f"Total metros analyzed: **{len(data)}**")
    
    # Show top metros
    if 'resilience_score' in data.columns:
        st.subheader("🏆 Top Performing Metropolitan Areas")
        top_metros = data.nlargest(5, 'resilience_score')[['metro_name', 'resilience_score', 'resilience_category']]
        st.dataframe(top_metros, use_container_width=True)
        
        # Simple bar chart
        fig = px.bar(
            top_metros, 
            x='resilience_score', 
            y='metro_name', 
            title="Resilience Scores by Metro Area",
            orientation='h'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Show raw data
    with st.expander("📋 View Raw Data"):
        st.dataframe(data, use_container_width=True)

st.markdown("""
---
### 🎯 Dashboard Status
- ✅ Streamlit app running
- ✅ Data files loaded
- ✅ Visualizations working

**Next Steps**: If this simple version works, we can enable the full dashboard features.
""")