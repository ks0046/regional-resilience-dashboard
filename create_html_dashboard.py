#!/usr/bin/env python3
"""
Create a static HTML dashboard as alternative to Streamlit
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Load data
data = pd.read_csv('data/metro_resilience_scores.csv')

# Create HTML dashboard
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Regional Economic Resilience Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .card {{ background: white; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .metrics {{ display: flex; justify-content: space-around; flex-wrap: wrap; }}
        .metric {{ text-align: center; padding: 10px; }}
        .metric h3 {{ margin: 0; color: #1e3a8a; }}
        .metric p {{ margin: 5px 0 0 0; font-size: 14px; color: #666; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f8f9fa; font-weight: bold; }}
        .high {{ background-color: #d4edda; }}
        .moderate {{ background-color: #fff3cd; }}
        .low {{ background-color: #f8d7da; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏙️ Regional Economic Resilience Dashboard</h1>
            <p>Analysis of economic resilience across major U.S. metropolitan areas</p>
        </div>
        
        <div class="card">
            <h2>📊 Overview</h2>
            <div class="metrics">
                <div class="metric">
                    <h3>{len(data)}</h3>
                    <p>Metropolitan Areas Analyzed</p>
                </div>
                <div class="metric">
                    <h3>{data['resilience_score'].mean():.1f}</h3>
                    <p>Average Resilience Score</p>
                </div>
                <div class="metric">
                    <h3>{data['resilience_score'].max():.1f}</h3>
                    <p>Highest Score</p>
                </div>
                <div class="metric">
                    <h3>{data['resilience_category'].value_counts().to_dict()}</h3>
                    <p>Category Distribution</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🏆 Top Performing Metropolitan Areas</h2>
            <div id="resilience-chart" style="height: 500px;"></div>
        </div>

        <div class="card">
            <h2>📋 Detailed Rankings</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Metropolitan Area</th>
                        <th>Resilience Score</th>
                        <th>Category</th>
                        <th>Employment Score</th>
                        <th>Diversity Score</th>
                    </tr>
                </thead>
                <tbody>
"""

# Add table rows
for i, (_, row) in enumerate(data.sort_values('resilience_score', ascending=False).iterrows(), 1):
    category_class = row['resilience_category'].lower().replace(' ', '-')
    html_content += f"""
                    <tr class="{category_class}">
                        <td>{i}</td>
                        <td>{row['metro_name']}</td>
                        <td>{row['resilience_score']:.1f}</td>
                        <td>{row['resilience_category']}</td>
                        <td>{row.get('employment_stability_score', 'N/A')}</td>
                        <td>{row.get('diversity_score', 'N/A')}</td>
                    </tr>
    """

# Create chart data
chart_data = data.nlargest(10, 'resilience_score')
chart_json = {
    'data': [{
        'x': chart_data['resilience_score'].tolist(),
        'y': chart_data['metro_name'].tolist(),
        'type': 'bar',
        'orientation': 'h',
        'marker': {'color': '#3b82f6'}
    }],
    'layout': {
        'title': 'Resilience Scores by Metropolitan Area',
        'xaxis': {'title': 'Resilience Score'},
        'yaxis': {'title': 'Metropolitan Area'},
        'margin': {'l': 300, 'r': 50, 't': 80, 'b': 50}
    }
}

html_content += f"""
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>🎯 About This Dashboard</h2>
            <p>This dashboard analyzes economic resilience across major U.S. metropolitan areas using:</p>
            <ul>
                <li><strong>Employment Stability</strong> - Based on unemployment rates and trends</li>
                <li><strong>Economic Diversity</strong> - Measure of sector diversification</li>
                <li><strong>Income Resilience</strong> - Household income levels and growth</li>
                <li><strong>Human Capital</strong> - Education levels and workforce quality</li>
            </ul>
            <p>Data sources: U.S. Census Bureau, Bureau of Labor Statistics</p>
        </div>
    </div>

    <script>
        // Create the resilience chart
        const chartData = {json.dumps(chart_json)};
        Plotly.newPlot('resilience-chart', chartData.data, chartData.layout, {{responsive: true}});
    </script>
</body>
</html>
"""

# Save HTML file
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ HTML Dashboard created: dashboard.html")
print("📱 Open dashboard.html in your browser to view the dashboard")
print("🎯 This provides all the key insights without Streamlit dependencies")