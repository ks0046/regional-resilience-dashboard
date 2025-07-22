import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Regional Economic Resilience Dashboard",
    page_icon="🏙️",
    layout="wide"
)

# Load data with error handling
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/metro_resilience_scores.csv')
        return data, None
    except Exception as e:
        return pd.DataFrame(), str(e)

def main():
    st.title("🏙️ Regional Economic Resilience Dashboard")
    st.markdown("*Analysis of economic resilience across major U.S. metropolitan areas*")
    
    # Load data
    data, error = load_data()
    
    if error:
        st.error(f"Error loading data: {error}")
        st.stop()
    
    if data.empty:
        st.warning("No data available")
        st.stop()
    
    # Sidebar navigation
    st.sidebar.title("Dashboard Sections")
    page = st.sidebar.radio("Select:", ["Overview", "Rankings", "Comparisons"])
    
    if page == "Overview":
        show_overview(data)
    elif page == "Rankings":
        show_rankings(data)
    elif page == "Comparisons":
        show_comparisons(data)

def show_overview(data):
    st.header("📊 Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Metro Areas", len(data))
    
    with col2:
        st.metric("Average Resilience", f"{data['resilience_score'].mean():.1f}")
    
    with col3:
        st.metric("Highest Score", f"{data['resilience_score'].max():.1f}")
    
    with col4:
        st.metric("Lowest Score", f"{data['resilience_score'].min():.1f}")
    
    # Category distribution
    st.subheader("Resilience Category Distribution")
    category_counts = data['resilience_category'].value_counts()
    
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="Distribution by Resilience Category"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_rankings(data):
    st.header("🏆 Metro Area Rankings")
    
    # Top performers chart
    st.subheader("Resilience Scores by Metro Area")
    
    sorted_data = data.sort_values('resilience_score', ascending=True)
    
    fig = px.bar(
        sorted_data,
        x='resilience_score',
        y='metro_name',
        color='resilience_category',
        orientation='h',
        title="Resilience Scores by Metropolitan Area",
        color_discrete_map={
            'Very High': '#2E8B57',
            'High': '#32CD32', 
            'Moderate': '#FFD700',
            'Low': '#FF8C00',
            'Very Low': '#DC143C'
        }
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.subheader("Detailed Rankings")
    
    display_data = sorted_data[['metro_name', 'resilience_score', 'resilience_category']].copy()
    display_data = display_data.sort_values('resilience_score', ascending=False)
    display_data.index = range(1, len(display_data) + 1)
    
    st.dataframe(display_data, use_container_width=True)

def show_comparisons(data):
    st.header("🔍 Metro Area Comparisons")
    
    # Metro selector
    selected_metros = st.multiselect(
        "Select metros to compare:",
        data['metro_name'].tolist(),
        default=data.nlargest(3, 'resilience_score')['metro_name'].tolist()
    )
    
    if len(selected_metros) < 2:
        st.warning("Please select at least 2 metropolitan areas for comparison.")
        return
    
    comparison_data = data[data['metro_name'].isin(selected_metros)]
    
    # Comparison bar chart
    st.subheader("Resilience Score Comparison")
    
    fig = px.bar(
        comparison_data.sort_values('resilience_score'),
        x='resilience_score',
        y='metro_name',
        title="Selected Metro Areas - Resilience Scores",
        orientation='h'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Component comparison (if available)
    component_cols = ['employment_stability_score', 'diversity_score', 
                     'income_resilience_score', 'human_capital_score']
    
    available_components = [col for col in component_cols if col in comparison_data.columns]
    
    if available_components:
        st.subheader("Component Score Comparison")
        
        # Reshape data for plotting
        plot_data = []
        for _, row in comparison_data.iterrows():
            for component in available_components:
                if pd.notna(row[component]):
                    plot_data.append({
                        'Metro': row['metro_name'],
                        'Component': component.replace('_score', '').replace('_', ' ').title(),
                        'Score': row[component]
                    })
        
        if plot_data:
            plot_df = pd.DataFrame(plot_data)
            
            fig = px.bar(
                plot_df,
                x='Component',
                y='Score',
                color='Metro',
                barmode='group',
                title="Component Scores by Metro Area"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Comparison table
    st.subheader("Side-by-Side Comparison")
    
    display_cols = ['metro_name', 'resilience_score', 'resilience_category']
    if available_components:
        display_cols.extend(available_components)
    
    comparison_table = comparison_data[display_cols].sort_values('resilience_score', ascending=False)
    st.dataframe(comparison_table, use_container_width=True)

if __name__ == "__main__":
    main()