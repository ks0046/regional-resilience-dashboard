import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sys
import os

# Add src directory to path for imports
sys.path.append('src')
from rag_system import SimpleRAG

# Page configuration
st.set_page_config(
    page_title="Regional Economic Resilience Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/metro_resilience_scores.csv')
        return data
    except FileNotFoundError:
        st.error("Data file not found. Please run data collection and scoring scripts first.")
        return pd.DataFrame()

# Initialize RAG system
@st.cache_resource
def init_rag():
    return SimpleRAG()

# Main app
def main():
    st.title("🏙️ Regional Economic Resilience Dashboard")
    st.markdown("*Analyzing economic resilience across major U.S. metropolitan areas*")
    
    # Load data
    data = load_data()
    if data.empty:
        st.stop()
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ["Regional Overview", "Comparative Analysis", "Policy Insights"]
    )
    
    # Page routing
    if page == "Regional Overview":
        show_regional_overview(data)
    elif page == "Comparative Analysis":
        show_comparative_analysis(data)
    elif page == "Policy Insights":
        show_policy_insights()

def show_regional_overview(data):
    st.header("Regional Overview")
    
    # Metro selector
    selected_metro = st.selectbox(
        "Select a Metropolitan Area:",
        data['metro_name'].tolist(),
        index=0
    )
    
    # Filter data for selected metro
    metro_data = data[data['metro_name'] == selected_metro].iloc[0]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Resilience Score",
            f"{metro_data['resilience_score']:.1f}",
            help="Composite score based on employment, diversity, income, and human capital"
        )
    
    with col2:
        st.metric(
            "Resilience Category",
            metro_data['resilience_category'],
            help="Classification based on overall resilience score"
        )
    
    with col3:
        st.metric(
            "Unemployment Rate",
            f"{metro_data['unemployment_rate']:.1f}%",
            help="Current unemployment rate"
        )
    
    with col4:
        st.metric(
            "Economic Diversity Score",
            f"{metro_data['economic_diversity_score']:.1f}",
            help="Measure of economic sector diversification"
        )
    
    # Detailed breakdown
    st.subheader("Resilience Component Breakdown")
    
    # Create radar chart
    categories = ['Employment Stability', 'Economic Diversity', 'Income Resilience', 'Human Capital']
    values = [
        metro_data['employment_stability_score'],
        metro_data['diversity_score'],
        metro_data['income_resilience_score'],
        metro_data['human_capital_score']
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=selected_metro,
        line_color='rgb(32, 201, 151)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Resilience Components Radar Chart",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Economic indicators
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Economic Indicators")
        metrics_data = {
            'Metric': ['Total Population', 'Median Household Income', 'Median Home Value'],
            'Value': [
                f"{metro_data['total_population']:,.0f}" if pd.notna(metro_data['total_population']) else "N/A",
                f"${metro_data['median_household_income']:,.0f}" if pd.notna(metro_data['median_household_income']) else "N/A",
                f"${metro_data['median_home_value']:,.0f}" if pd.notna(metro_data['median_home_value']) else "N/A"
            ]
        }
        st.table(pd.DataFrame(metrics_data))
    
    with col2:
        st.subheader("Resilience Insights")
        insights = generate_metro_insights(metro_data)
        for insight in insights:
            st.info(insight)

def show_comparative_analysis(data):
    st.header("Comparative Analysis")
    
    # Metro selector for comparison
    st.subheader("Select Metropolitan Areas to Compare")
    selected_metros = st.multiselect(
        "Choose metros (2-5 recommended):",
        data['metro_name'].tolist(),
        default=data.nlargest(3, 'resilience_score')['metro_name'].tolist()
    )
    
    if len(selected_metros) < 2:
        st.warning("Please select at least 2 metropolitan areas for comparison.")
        return
    
    # Filter data
    comparison_data = data[data['metro_name'].isin(selected_metros)]
    
    # Side-by-side comparison
    st.subheader("Resilience Scores Comparison")
    
    fig = px.bar(
        comparison_data.sort_values('resilience_score', ascending=True),
        y='metro_name',
        x='resilience_score',
        color='resilience_category',
        title="Overall Resilience Scores",
        labels={'resilience_score': 'Resilience Score', 'metro_name': 'Metropolitan Area'},
        color_discrete_map={
            'Very High': '#2E8B57',
            'High': '#32CD32',
            'Moderate': '#FFD700',
            'Low': '#FF8C00',
            'Very Low': '#DC143C'
        }
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Component comparison
    st.subheader("Component Score Comparison")
    
    components = ['employment_stability_score', 'diversity_score', 'income_resilience_score', 'human_capital_score']
    component_names = ['Employment Stability', 'Economic Diversity', 'Income Resilience', 'Human Capital']
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=component_names,
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    for i, (component, name) in enumerate(zip(components, component_names)):
        row = i // 2 + 1
        col = i % 2 + 1
        
        fig.add_trace(
            go.Bar(
                x=comparison_data['metro_name'],
                y=comparison_data[component],
                name=name,
                showlegend=False
            ),
            row=row, col=col
        )
    
    fig.update_layout(height=600, title_text="Detailed Component Comparison")
    st.plotly_chart(fig, use_container_width=True)
    
    # Rankings table
    st.subheader("Detailed Comparison Table")
    
    display_columns = ['metro_name', 'resilience_score', 'resilience_category',
                      'employment_stability_score', 'diversity_score',
                      'income_resilience_score', 'human_capital_score']
    
    comparison_table = comparison_data[display_columns].sort_values('resilience_score', ascending=False)
    st.dataframe(comparison_table, use_container_width=True)

def show_policy_insights():
    st.header("Policy Insights & Recommendations")
    
    # Initialize RAG system
    try:
        rag = init_rag()
    except Exception as e:
        st.error(f"Could not initialize policy analysis system: {str(e)}")
        return
    
    st.markdown("""
    Ask questions about regional economic resilience policies and strategies. 
    The system will search through policy documents and provide evidence-based recommendations.
    """)
    
    # Sample questions
    st.subheader("Sample Questions")
    sample_queries = rag.get_sample_queries()
    
    cols = st.columns(2)
    for i, query in enumerate(sample_queries):
        col = cols[i % 2]
        if col.button(f"📋 {query}", key=f"sample_{i}"):
            st.session_state.query_input = query
    
    # Query input
    query = st.text_area(
        "Enter your policy question:",
        value=st.session_state.get('query_input', ''),
        height=100,
        placeholder="e.g., What strategies can help rural areas build economic resilience?"
    )
    
    # Clear query state
    if 'query_input' in st.session_state:
        del st.session_state.query_input
    
    if st.button("Get Policy Insights", type="primary"):
        if query.strip():
            with st.spinner("Analyzing policy documents..."):
                try:
                    result = rag.generate_response(query)
                    
                    st.subheader("📊 Policy Analysis")
                    st.write(result['response'])
                    
                    if result['sources']:
                        st.subheader("📚 Sources")
                        for source in result['sources']:
                            st.info(f"📄 {source}")
                
                except Exception as e:
                    st.error(f"Error generating insights: {str(e)}")
        else:
            st.warning("Please enter a question.")
    
    # Policy document library
    st.subheader("📖 Available Policy Documents")
    
    documents = [
        "EDA Regional Development Strategy",
        "Federal Reserve Regional Economic Outlook",
        "Manufacturing Resilience Policy",
        "Rural Economic Development Strategies",
        "Urban Resilience Framework"
    ]
    
    for doc in documents:
        st.info(f"📄 {doc}")

def generate_metro_insights(metro_data):
    """Generate insights for a specific metro area"""
    insights = []
    
    # Resilience category insight
    if metro_data['resilience_category'] in ['Very High', 'High']:
        insights.append("🟢 This metropolitan area demonstrates strong economic resilience across multiple indicators.")
    elif metro_data['resilience_category'] == 'Moderate':
        insights.append("🟡 This metropolitan area shows moderate resilience with room for improvement in key areas.")
    else:
        insights.append("🔴 This metropolitan area faces resilience challenges that require targeted interventions.")
    
    # Employment insight
    if metro_data['unemployment_rate'] < 4.0:
        insights.append("💼 Low unemployment rate indicates strong labor market conditions.")
    elif metro_data['unemployment_rate'] > 7.0:
        insights.append("⚠️ High unemployment suggests labor market challenges requiring attention.")
    
    # Economic diversity insight
    if metro_data['economic_diversity_score'] > 70:
        insights.append("🏭 High economic diversity provides protection against sector-specific shocks.")
    elif metro_data['economic_diversity_score'] < 50:
        insights.append("📊 Limited economic diversity may increase vulnerability to industry downturns.")
    
    return insights

if __name__ == "__main__":
    main()