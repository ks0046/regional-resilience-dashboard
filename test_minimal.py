import streamlit as st

st.title("🔧 Minimal Test App")
st.write("If you can see this, Streamlit is working!")

# Test 1: Basic functionality
st.header("Test 1: Basic Streamlit")
st.success("✅ Streamlit is running")

# Test 2: Data loading
st.header("Test 2: Data Loading")
try:
    import pandas as pd
    data = pd.read_csv('data/metro_resilience_scores.csv')
    st.success(f"✅ Data loaded: {len(data)} rows")
    st.write(data.head())
except Exception as e:
    st.error(f"❌ Data loading failed: {str(e)}")

# Test 3: Plotly
st.header("Test 3: Plotly")
try:
    import plotly.express as px
    import numpy as np
    
    # Simple test chart
    x = [1, 2, 3, 4]
    y = [10, 11, 12, 13]
    fig = px.bar(x=x, y=y, title="Test Chart")
    st.plotly_chart(fig)
    st.success("✅ Plotly working")
except Exception as e:
    st.error(f"❌ Plotly failed: {str(e)}")

st.write("---")
st.write("**What do you see?** Tell me which tests pass/fail.")