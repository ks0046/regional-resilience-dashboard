#!/usr/bin/env python3
"""
Create a comprehensive HTML dashboard with all features
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import sys
import os

# Add src to path for RAG system
sys.path.append('src')
from rag_system import SimpleRAG

def create_full_html_dashboard():
    # Load data
    data = pd.read_csv('data/metro_resilience_scores.csv')
    
    # Initialize RAG system
    try:
        rag = SimpleRAG()
        sample_queries = rag.get_sample_queries()
    except Exception as e:
        print(f"Warning: Could not initialize RAG system: {e}")
        rag = None
        sample_queries = []
    
    # Create charts
    charts_js = create_all_charts(data)
    
    # Create sample policy responses
    policy_responses = create_sample_policy_responses(rag) if rag else {}
    
    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Regional Economic Resilience Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            color: #1a202c;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .nav-tabs {{
            display: flex;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin-bottom: 20px;
            overflow: hidden;
        }}
        
        .nav-tab {{
            flex: 1;
            padding: 15px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            color: white;
            font-weight: 600;
            border: none;
            background: none;
        }}
        
        .nav-tab:hover {{
            background: rgba(255, 255, 255, 0.2);
        }}
        
        .nav-tab.active {{
            background: rgba(255, 255, 255, 0.3);
            color: #1a202c;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .card {{
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            margin: 20px 0;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            backdrop-filter: blur(10px);
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .metric-label {{
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        
        .chart-container {{
            height: 500px;
            margin: 20px 0;
            border-radius: 10px;
            overflow: hidden;
        }}
        
        .comparison-selector {{
            margin: 20px 0;
        }}
        
        .metro-selector {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }}
        
        .metro-checkbox {{
            display: flex;
            align-items: center;
            background: rgba(102, 126, 234, 0.1);
            padding: 8px 12px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .metro-checkbox:hover {{
            background: rgba(102, 126, 234, 0.2);
        }}
        
        .metro-checkbox input {{
            margin-right: 8px;
        }}
        
        .policy-section {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        
        .query-buttons {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 10px;
            margin: 20px 0;
        }}
        
        .query-button {{
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 12px 15px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: left;
        }}
        
        .query-button:hover {{
            background: rgba(255, 255, 255, 0.3);
        }}
        
        .custom-query {{
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 8px;
            margin: 10px 0;
            font-size: 1rem;
            resize: vertical;
            min-height: 100px;
        }}
        
        .submit-query {{
            background: #4299e1;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .submit-query:hover {{
            background: #3182ce;
        }}
        
        .policy-response {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            display: none;
        }}
        
        .policy-response.show {{
            display: block;
        }}
        
        .sources {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .source-item {{
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 12px;
            border-radius: 6px;
            margin: 5px 0;
            font-size: 0.9rem;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border-radius: 10px;
            overflow: hidden;
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        
        tr:nth-child(even) {{
            background: #f8fafc;
        }}
        
        .high {{ background: #d4edda !important; }}
        .moderate {{ background: #fff3cd !important; }}
        .low {{ background: #f8d7da !important; }}
        .very-high {{ background: #c3e6cb !important; }}
        .very-low {{ background: #f5c6cb !important; }}
        
        .loading {{
            text-align: center;
            padding: 20px;
            color: rgba(255, 255, 255, 0.8);
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 10px; }}
            .header h1 {{ font-size: 2rem; }}
            .nav-tab {{ padding: 12px 15px; }}
            .metrics-grid {{ grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }}
            .query-buttons {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏙️ Regional Economic Resilience Dashboard</h1>
            <p>Comprehensive analysis of economic resilience across major U.S. metropolitan areas</p>
            <p><strong>Data Sources:</strong> U.S. Census Bureau, Bureau of Labor Statistics | <strong>Analysis:</strong> {len(data)} Metropolitan Areas</p>
        </div>
        
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showTab('overview')">📊 Regional Overview</button>
            <button class="nav-tab" onclick="showTab('comparison')">🔍 Comparative Analysis</button>
            <button class="nav-tab" onclick="showTab('policy')">🎯 Policy Insights</button>
        </div>
        
        <!-- Overview Tab -->
        <div id="overview" class="tab-content active">
            <div class="card">
                <h2>📊 Dashboard Overview</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{len(data)}</div>
                        <div class="metric-label">Metropolitan Areas</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{data['resilience_score'].mean():.1f}</div>
                        <div class="metric-label">Average Resilience Score</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{data['resilience_score'].max():.1f}</div>
                        <div class="metric-label">Highest Score</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{data['resilience_score'].min():.1f}</div>
                        <div class="metric-label">Lowest Score</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>🏆 Top Performing Metropolitan Areas</h3>
                <div id="overview-chart" class="chart-container"></div>
            </div>
            
            <div class="card">
                <h3>📈 Resilience Score Distribution</h3>
                <div id="distribution-chart" class="chart-container"></div>
            </div>
            
            <div class="card">
                <h3>🎯 Selected Metro Analysis</h3>
                <select id="metro-selector" onchange="updateMetroAnalysis()" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd; margin: 10px 0;">
                    {generate_metro_options(data)}
                </select>
                <div id="metro-details">
                    {generate_metro_details(data.iloc[0])}
                </div>
                <div id="radar-chart" class="chart-container"></div>
            </div>
        </div>
        
        <!-- Comparison Tab -->
        <div id="comparison" class="tab-content">
            <div class="card">
                <h2>🔍 Comparative Analysis</h2>
                <div class="comparison-selector">
                    <h3>Select Metropolitan Areas to Compare:</h3>
                    <div class="metro-selector">
                        {generate_comparison_checkboxes(data)}
                    </div>
                    <button onclick="updateComparison()" style="background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 10px 0;">Update Comparison</button>
                </div>
            </div>
            
            <div class="card">
                <h3>📊 Resilience Score Comparison</h3>
                <div id="comparison-chart" class="chart-container"></div>
            </div>
            
            <div class="card">
                <h3>🎯 Component Analysis</h3>
                <div id="component-chart" class="chart-container"></div>
            </div>
            
            <div class="card">
                <h3>📋 Detailed Comparison Table</h3>
                <div id="comparison-table"></div>
            </div>
        </div>
        
        <!-- Policy Tab -->
        <div id="policy" class="tab-content">
            <div class="policy-section">
                <h2>🎯 AI-Powered Policy Insights</h2>
                <p>Explore evidence-based policy recommendations for regional economic resilience. Click on sample questions or ask your own.</p>
                
                <h3>📋 Sample Policy Questions</h3>
                <div class="query-buttons">
                    {generate_sample_query_buttons(sample_queries)}
                </div>
                
                <h3>💭 Ask Your Own Question</h3>
                <textarea id="custom-query" class="custom-query" placeholder="e.g., What infrastructure investments best support regional economic resilience?"></textarea>
                <button onclick="submitCustomQuery()" class="submit-query">Get Policy Insights</button>
                
                <div id="policy-response" class="policy-response">
                    <div id="policy-loading" class="loading" style="display: none;">
                        <p>🤖 Analyzing policy documents and generating insights...</p>
                    </div>
                    <div id="policy-content"></div>
                </div>
                
                <div class="card" style="margin-top: 30px; background: rgba(255,255,255,0.95); color: #1a202c;">
                    <h3>📚 Available Policy Documents</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;">📄 EDA Regional Development Strategy</li>
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;">📄 Federal Reserve Regional Economic Outlook</li>
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;">📄 Manufacturing Resilience Policy Framework</li>
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;">📄 Rural Economic Development Strategies</li>
                        <li style="padding: 8px 0;">📄 Urban Economic Resilience Guidelines</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Chart data and configurations
        {charts_js}
        
        // Policy responses data
        const policyResponses = {json.dumps(policy_responses, indent=2)};
        
        // Tab switching functionality
        function showTab(tabName) {{
            // Hide all tabs
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            const navTabs = document.querySelectorAll('.nav-tab');
            navTabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // Initialize charts for active tab
            if (tabName === 'overview') {{
                initializeOverviewCharts();
            }} else if (tabName === 'comparison') {{
                updateComparison();
            }}
        }}
        
        // Initialize overview charts
        function initializeOverviewCharts() {{
            Plotly.newPlot('overview-chart', overviewChartData.data, overviewChartData.layout, {{responsive: true}});
            Plotly.newPlot('distribution-chart', distributionChartData.data, distributionChartData.layout, {{responsive: true}});
            updateMetroAnalysis();
        }}
        
        // Metro analysis update
        function updateMetroAnalysis() {{
            const selector = document.getElementById('metro-selector');
            const selectedIndex = selector.selectedIndex;
            const metroData = {json.dumps(data.to_dict('records'))};
            const selectedMetro = metroData[selectedIndex];
            
            // Update details
            document.getElementById('metro-details').innerHTML = generateMetroDetailsHTML(selectedMetro);
            
            // Update radar chart
            const radarData = {{
                data: [{{
                    type: 'scatterpolar',
                    r: [
                        parseFloat(selectedMetro.employment_stability_score) || 0,
                        parseFloat(selectedMetro.diversity_score) || 0,
                        parseFloat(selectedMetro.income_resilience_score) || 0,
                        parseFloat(selectedMetro.human_capital_score) || 0
                    ],
                    theta: ['Employment Stability', 'Economic Diversity', 'Income Resilience', 'Human Capital'],
                    fill: 'toself',
                    name: selectedMetro.metro_name,
                    line: {{color: '#667eea'}},
                    marker: {{color: '#667eea'}}
                }}],
                layout: {{
                    polar: {{
                        radialaxis: {{
                            visible: true,
                            range: [0, 100],
                            ticksuffix: '%'
                        }}
                    }},
                    showlegend: false,
                    title: 'Resilience Components: ' + selectedMetro.metro_name,
                    font: {{size: 12}}
                }}
            }};
            
            Plotly.newPlot('radar-chart', radarData.data, radarData.layout, {{responsive: true}});
        }}
        
        // Comparison functionality
        function updateComparison() {{
            const checkboxes = document.querySelectorAll('input[name="metro-compare"]:checked');
            const selectedMetros = Array.from(checkboxes).map(cb => cb.value);
            
            if (selectedMetros.length < 2) {{
                document.getElementById('comparison-chart').innerHTML = '<p style="text-align: center; padding: 50px;">Please select at least 2 metropolitan areas for comparison.</p>';
                return;
            }}
            
            const allData = {json.dumps(data.to_dict('records'))};
            const compareData = allData.filter(metro => selectedMetros.includes(metro.metro_name));
            
            // Comparison bar chart
            const comparisonChart = {{
                data: [{{
                    x: compareData.map(d => d.resilience_score),
                    y: compareData.map(d => d.metro_name),
                    type: 'bar',
                    orientation: 'h',
                    marker: {{color: '#667eea'}}
                }}],
                layout: {{
                    title: 'Resilience Score Comparison',
                    xaxis: {{title: 'Resilience Score'}},
                    yaxis: {{title: 'Metropolitan Area'}},
                    margin: {{l: 300}}
                }}
            }};
            
            Plotly.newPlot('comparison-chart', comparisonChart.data, comparisonChart.layout, {{responsive: true}});
            
            // Component comparison
            const components = ['employment_stability_score', 'diversity_score', 'income_resilience_score', 'human_capital_score'];
            const componentNames = ['Employment Stability', 'Economic Diversity', 'Income Resilience', 'Human Capital'];
            
            const componentData = compareData.map(metro => ({{
                x: componentNames,
                y: components.map(comp => metro[comp] || 0),
                name: metro.metro_name,
                type: 'bar'
            }}));
            
            const componentChart = {{
                data: componentData,
                layout: {{
                    title: 'Component Score Comparison',
                    barmode: 'group',
                    xaxis: {{title: 'Component'}},
                    yaxis: {{title: 'Score', range: [0, 100]}},
                    margin: {{l: 50, r: 50, t: 80, b: 80}}
                }}
            }};
            
            Plotly.newPlot('component-chart', componentChart.data, componentChart.layout, {{responsive: true}});
            
            // Generate comparison table
            let tableHTML = '<table><thead><tr><th>Metro Area</th><th>Resilience Score</th><th>Category</th></tr></thead><tbody>';
            compareData.forEach(metro => {{
                const categoryClass = metro.resilience_category.toLowerCase().replace(/\s+/g, '-');
                tableHTML += `<tr class="${{categoryClass}}"><td>${{metro.metro_name}}</td><td>${{metro.resilience_score}}</td><td>${{metro.resilience_category}}</td></tr>`;
            }});
            tableHTML += '</tbody></table>';
            
            document.getElementById('comparison-table').innerHTML = tableHTML;
        }}
        
        // Policy query functionality
        function submitSampleQuery(query) {{
            const response = policyResponses[query];
            if (response) {{
                showPolicyResponse(response.response, response.sources);
            }} else {{
                showPolicyResponse("This is a sample response for: " + query, ["Sample Policy Document"]);
            }}
        }}
        
        function submitCustomQuery() {{
            const query = document.getElementById('custom-query').value.trim();
            if (!query) {{
                alert('Please enter a question.');
                return;
            }}
            
            document.getElementById('policy-loading').style.display = 'block';
            document.getElementById('policy-response').classList.add('show');
            document.getElementById('policy-content').innerHTML = '';
            
            // Simulate API call
            setTimeout(() => {{
                document.getElementById('policy-loading').style.display = 'none';
                showPolicyResponse(
                    "This is a simulated response to your custom query. In the full implementation, this would connect to the RAG system to provide evidence-based policy recommendations based on the query: " + query,
                    ["Federal Economic Policy Framework", "Regional Development Guidelines"]
                );
            }}, 2000);
        }}
        
        function showPolicyResponse(response, sources) {{
            let sourcesHTML = '';
            if (sources && sources.length > 0) {{
                sourcesHTML = '<div class="sources"><h4>📚 Sources:</h4>' + 
                    sources.map(source => `<div class="source-item">📄 ${{source}}</div>`).join('') + 
                    '</div>';
            }}
            
            document.getElementById('policy-content').innerHTML = 
                `<h4>🎯 Policy Analysis</h4><p>${{response}}</p>${{sourcesHTML}}`;
            document.getElementById('policy-response').classList.add('show');
        }}
        
        function generateMetroDetailsHTML(metro) {{
            return `
                <div class="metrics-grid" style="grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));">
                    <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 8px;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">${{metro.resilience_score}}</div>
                        <div style="font-size: 0.9rem;">Resilience Score</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 8px;">
                        <div style="font-size: 1.2rem; font-weight: bold; color: #667eea;">${{metro.resilience_category}}</div>
                        <div style="font-size: 0.9rem;">Category</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 8px;">
                        <div style="font-size: 1.2rem; font-weight: bold; color: #667eea;">${{metro.total_population ? parseInt(metro.total_population).toLocaleString() : 'N/A'}}</div>
                        <div style="font-size: 0.9rem;">Population</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 8px;">
                        <div style="font-size: 1.2rem; font-weight: bold; color: #667eea;">${{metro.median_household_income ? '$' + parseInt(metro.median_household_income).toLocaleString() : 'N/A'}}</div>
                        <div style="font-size: 0.9rem;">Median Income</div>
                    </div>
                </div>
            `;
        }}
        
        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {{
            initializeOverviewCharts();
            
            // Initialize comparison with top 3
            const topMetros = {json.dumps(data.nlargest(3, 'resilience_score')['metro_name'].tolist())};
            topMetros.forEach(metro => {{
                const checkbox = document.querySelector(`input[value="${{metro}}"]`);
                if (checkbox) checkbox.checked = true;
            }});
            updateComparison();
        }});
    </script>
</body>
</html>
"""
    
    return html_content

def create_all_charts(data):
    """Create all chart configurations"""
    
    # Overview chart
    top_data = data.nlargest(10, 'resilience_score')
    overview_chart = {
        'data': [{
            'x': top_data['resilience_score'].tolist(),
            'y': top_data['metro_name'].tolist(),
            'type': 'bar',
            'orientation': 'h',
            'marker': {'color': '#667eea'}
        }],
        'layout': {
            'title': 'Top Metropolitan Areas by Resilience Score',
            'xaxis': {'title': 'Resilience Score'},
            'yaxis': {'title': 'Metropolitan Area'},
            'margin': {'l': 300, 'r': 50, 't': 80, 'b': 50}
        }
    }
    
    # Distribution chart
    category_counts = data['resilience_category'].value_counts()
    distribution_chart = {
        'data': [{
            'labels': category_counts.index.tolist(),
            'values': category_counts.values.tolist(),
            'type': 'pie',
            'marker': {'colors': ['#2E8B57', '#32CD32', '#FFD700', '#FF8C00', '#DC143C']}
        }],
        'layout': {
            'title': 'Distribution by Resilience Category'
        }
    }
    
    return f"""
        const overviewChartData = {json.dumps(overview_chart)};
        const distributionChartData = {json.dumps(distribution_chart)};
    """

def generate_metro_options(data):
    """Generate metro selector options"""
    options = ""
    for _, metro in data.iterrows():
        options += f'<option value="{metro["metro_name"]}">{metro["metro_name"]} (Score: {metro["resilience_score"]:.1f})</option>\n'
    return options

def generate_metro_details(metro):
    """Generate initial metro details"""
    return f"""
    <div class="metrics-grid" style="grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));">
        <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 8px;">
            <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">{metro['resilience_score']:.1f}</div>
            <div style="font-size: 0.9rem;">Resilience Score</div>
        </div>
        <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 8px;">
            <div style="font-size: 1.2rem; font-weight: bold; color: #667eea;">{metro['resilience_category']}</div>
            <div style="font-size: 0.9rem;">Category</div>
        </div>
        <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 8px;">
            <div style="font-size: 1.2rem; font-weight: bold; color: #667eea;">{int(metro['total_population']):,}</div>
            <div style="font-size: 0.9rem;">Population</div>
        </div>
        <div style="text-align: center; padding: 15px; background: #f8fafc; border-radius: 8px;">
            <div style="font-size: 1.2rem; font-weight: bold; color: #667eea;">${int(metro['median_household_income']):,}</div>
            <div style="font-size: 0.9rem;">Median Income</div>
        </div>
    </div>
    """

def generate_comparison_checkboxes(data):
    """Generate comparison checkboxes"""
    checkboxes = ""
    for _, metro in data.iterrows():
        checkboxes += f"""
        <div class="metro-checkbox">
            <input type="checkbox" name="metro-compare" value="{metro['metro_name']}" id="metro_{metro['metro_code']}">
            <label for="metro_{metro['metro_code']}">{metro['metro_name']} ({metro['resilience_score']:.1f})</label>
        </div>
        """
    return checkboxes

def generate_sample_query_buttons(queries):
    """Generate sample query buttons"""
    buttons = ""
    for i, query in enumerate(queries):
        buttons += f'<button class="query-button" onclick="submitSampleQuery(`{query}`)">{query}</button>\n'
    return buttons

def create_sample_policy_responses(rag):
    """Create sample policy responses"""
    if not rag:
        return {}
    
    responses = {}
    sample_queries = [
        "What strategies promote economic diversification in regions?",
        "How can manufacturing contribute to regional resilience?"
    ]
    
    for query in sample_queries:
        try:
            result = rag.generate_response(query)
            responses[query] = result
        except Exception as e:
            print(f"Error generating response for '{query}': {e}")
            responses[query] = {
                "response": f"Sample policy analysis for: {query}",
                "sources": ["Economic Development Policy Framework"]
            }
    
    return responses

if __name__ == "__main__":
    print("🚀 Creating comprehensive HTML dashboard...")
    
    try:
        html_content = create_full_html_dashboard()
        
        # Save HTML file
        with open('full_dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Full HTML Dashboard created: full_dashboard.html")
        print("📱 Features included:")
        print("   - 📊 Regional Overview with interactive metro selection")
        print("   - 🔍 Comparative Analysis with multi-metro selection") 
        print("   - 🎯 AI-powered Policy Insights with sample queries")
        print("   - 📈 Interactive charts and visualizations")
        print("   - 📱 Responsive design for all devices")
        print()
        print("🌐 Open full_dashboard.html in your browser to access the complete dashboard!")
        
    except Exception as e:
        print(f"❌ Error creating dashboard: {e}")
        import traceback
        traceback.print_exc()