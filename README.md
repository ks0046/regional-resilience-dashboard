# Regional Economic Resilience Dashboard

A functional prototype demonstrating core RAG + economic data analysis capabilities for regional economic policy analysis.

## 🚀 Features

### 1. Data Collection & Analysis
- **Census Data Integration**: Pulls real-time data from U.S. Census Bureau ACS 5-year estimates
- **Economic Indicators**: Population, income, education, and housing metrics
- **Resilience Scoring**: Composite scoring algorithm based on employment stability, economic diversity, income resilience, and human capital

### 2. Policy Analysis (RAG System)
- **Document Search**: TF-IDF based similarity search across policy documents
- **AI-Powered Insights**: OpenAI GPT-3.5-turbo powered policy recommendations
- **Source Citations**: Transparent sourcing of policy recommendations

### 3. Interactive Dashboard
- **Regional Overview**: Detailed metro area analysis with radar charts
- **Comparative Analysis**: Side-by-side comparison of multiple metros
- **Policy Insights**: Query-based policy recommendations with RAG system

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.12+
- OpenAI API key
- U.S. Census API key
- BLS API key (optional)

### Installation
```bash
# Clone and setup
cd regional_resilience_dashboard
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements_minimal.txt

# Create .env file with your API keys
cp .env.example .env
# Edit .env with your API keys
```

### Run the Complete Pipeline
```bash
# 1. Collect and process data
python src/data_collector.py

# 2. Calculate resilience scores
python src/resilience_scorer.py

# 3. Test RAG system
python src/rag_system.py

# 4. Launch dashboard
streamlit run app.py
```

## 📊 Dashboard Pages

### Regional Overview
- Metro area selector
- Resilience score dashboard
- Component breakdown (radar chart)
- Key economic indicators
- Generated insights

### Comparative Analysis
- Multi-metro selection
- Side-by-side resilience scores
- Component comparison charts
- Detailed comparison table

### Policy Insights
- RAG-powered Q&A system
- Sample policy questions
- AI-generated recommendations
- Source document citations

## 🎯 Core Capabilities Demonstrated

### Economic Data Integration
- Real-time Census API integration
- Data cleaning and normalization
- Multi-source data fusion
- Resilience scoring methodology

### RAG System Implementation
- Document vectorization (TF-IDF)
- Semantic similarity search
- Context-aware response generation
- Source attribution

### Policy Analysis
- Economic development strategies
- Regional resilience frameworks
- Manufacturing and rural development
- Urban resilience approaches

## 📈 Sample Metro Areas Analyzed
- New York-Newark-Jersey City, NY-NJ-PA
- Los Angeles-Long Beach-Anaheim, CA
- Chicago-Naperville-Elgin, IL-IN-WI
- Dallas-Fort Worth-Arlington, TX
- Houston-The Woodlands-Sugar Land, TX
- Washington-Arlington-Alexandria, DC-VA-MD-WV
- Philadelphia-Camden-Wilmington, PA-NJ-DE-MD
- Miami-Fort Lauderdale-West Palm Beach, FL
- Atlanta-Sandy Springs-Roswell, GA
- Boston-Cambridge-Newton, MA-NH
- And 10 more major metro areas...

## 🔍 Policy Documents Included
1. EDA Regional Development Strategy
2. Federal Reserve Regional Economic Outlook
3. Manufacturing Resilience Policy
4. Rural Economic Development Strategies
5. Urban Resilience Framework

## 🛠 Technology Stack
- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **API Integration**: Requests
- **AI/RAG**: OpenAI GPT-3.5, scikit-learn
- **Search**: TF-IDF vectorization

## 📝 Sample Queries for Policy Insights
- "What strategies promote economic diversification in regions?"
- "How can manufacturing contribute to regional resilience?"
- "What are the main challenges for rural economic development?"
- "How do urban areas build economic resilience?"
- "What role does workforce development play in regional resilience?"


## 🔧 Architecture

```
regional_resilience_dashboard/
├── src/
│   ├── data_collector.py     # Census/BLS API integration
│   ├── resilience_scorer.py   # Scoring algorithm
│   └── rag_system.py         # RAG implementation
├── data/
│   ├── metro_economic_data.csv
│   └── metro_resilience_scores.csv
├── docs/policies/            # Policy documents
├── app.py                   # Streamlit dashboard
└── README.md
```

## 🎯 Key Metrics
- **20+ Metro Areas**: Comprehensive coverage of major U.S. regions
- **4 Core Components**: Employment, diversity, income, human capital
- **5 Policy Documents**: Covering federal, regional, and local strategies
- **3 Dashboard Pages**: Overview, comparison, policy insights
- **Real-time Data**: Live Census Bureau integration

This prototype demonstrates the technical feasibility and policy value of combining economic data analysis with AI-powered policy insights for regional development applications.
