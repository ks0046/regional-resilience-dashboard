import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

class ResilienceScorer:
    def __init__(self):
        self.scaler = MinMaxScaler()
        
    def calculate_resilience_scores(self, data):
        """Calculate composite resilience scores for metro areas"""
        df = data.copy()
        
        # Remove rows with insufficient data
        required_columns = ['unemployment_rate', 'economic_diversity_score', 
                          'median_household_income', 'total_population']
        df = df.dropna(subset=required_columns)
        
        if df.empty:
            print("Warning: No complete data available for scoring")
            return df
        
        # Calculate component scores (0-100 scale)
        
        # 1. Employment Stability Score (inverse of unemployment rate)
        df['employment_stability_score'] = self._calculate_employment_score(df)
        
        # 2. Economic Diversity Score (already provided)
        df['diversity_score'] = df['economic_diversity_score']
        
        # 3. Income Resilience Score
        df['income_resilience_score'] = self._calculate_income_score(df)
        
        # 4. Human Capital Score (education levels)
        df['human_capital_score'] = self._calculate_human_capital_score(df)
        
        # Calculate weighted composite resilience score
        weights = {
            'employment_stability_score': 0.30,
            'diversity_score': 0.25,
            'income_resilience_score': 0.25,
            'human_capital_score': 0.20
        }
        
        df['resilience_score'] = (
            df['employment_stability_score'] * weights['employment_stability_score'] +
            df['diversity_score'] * weights['diversity_score'] +
            df['income_resilience_score'] * weights['income_resilience_score'] +
            df['human_capital_score'] * weights['human_capital_score']
        )
        
        # Round scores
        score_columns = ['employment_stability_score', 'diversity_score', 
                        'income_resilience_score', 'human_capital_score', 'resilience_score']
        
        for col in score_columns:
            df[col] = df[col].round(1)
        
        # Add resilience categories
        df['resilience_category'] = df['resilience_score'].apply(self._categorize_resilience)
        
        return df
    
    def _calculate_employment_score(self, df):
        """Calculate employment stability score (lower unemployment = higher score)"""
        # Invert unemployment rate and scale to 0-100
        max_unemployment = df['unemployment_rate'].max()
        min_unemployment = df['unemployment_rate'].min()
        
        if max_unemployment == min_unemployment:
            return pd.Series([75.0] * len(df), index=df.index)
        
        # Invert so lower unemployment = higher score
        employment_scores = 100 - ((df['unemployment_rate'] - min_unemployment) / 
                                 (max_unemployment - min_unemployment) * 100)
        
        return employment_scores
    
    def _calculate_income_score(self, df):
        """Calculate income resilience score based on median household income"""
        if df['median_household_income'].max() == df['median_household_income'].min():
            return pd.Series([50.0] * len(df), index=df.index)
        
        # Normalize income to 0-100 scale
        income_scores = ((df['median_household_income'] - df['median_household_income'].min()) /
                        (df['median_household_income'].max() - df['median_household_income'].min()) * 100)
        
        return income_scores
    
    def _calculate_human_capital_score(self, df):
        """Calculate human capital score based on education levels"""
        if 'bachelors_degree' not in df.columns:
            return pd.Series([50.0] * len(df), index=df.index)
        
        # Calculate education rate (bachelors degree holders / total population)
        df_temp = df.copy()
        df_temp['education_rate'] = df_temp['bachelors_degree'] / df_temp['total_population'] * 100
        
        if df_temp['education_rate'].max() == df_temp['education_rate'].min():
            return pd.Series([50.0] * len(df), index=df.index)
        
        # Normalize to 0-100 scale
        education_scores = ((df_temp['education_rate'] - df_temp['education_rate'].min()) /
                           (df_temp['education_rate'].max() - df_temp['education_rate'].min()) * 100)
        
        return education_scores
    
    def _categorize_resilience(self, score):
        """Categorize resilience scores"""
        if score >= 80:
            return "Very High"
        elif score >= 70:
            return "High"
        elif score >= 60:
            return "Moderate"
        elif score >= 50:
            return "Low"
        else:
            return "Very Low"
    
    def get_top_metros(self, df, n=10, metric='resilience_score'):
        """Get top N metros by specified metric"""
        return df.nlargest(n, metric)[['metro_name', metric, 'resilience_category']]
    
    def get_resilience_summary(self, df):
        """Get summary statistics for resilience scores"""
        summary = {
            'total_metros': len(df),
            'avg_resilience_score': df['resilience_score'].mean().round(1),
            'highest_score': df['resilience_score'].max(),
            'lowest_score': df['resilience_score'].min(),
            'category_distribution': df['resilience_category'].value_counts().to_dict()
        }
        return summary

if __name__ == "__main__":
    # Load the data
    data = pd.read_csv('data/metro_economic_data.csv')
    
    # Calculate resilience scores
    scorer = ResilienceScorer()
    scored_data = scorer.calculate_resilience_scores(data)
    
    # Save scored data
    scored_data.to_csv('data/metro_resilience_scores.csv', index=False)
    
    # Display results
    print("Resilience Scoring Complete!")
    print(f"Processed {len(scored_data)} metro areas")
    
    print("\nTop 10 Most Resilient Metro Areas:")
    top_metros = scorer.get_top_metros(scored_data, 10)
    print(top_metros.to_string(index=False))
    
    print("\nResilience Summary:")
    summary = scorer.get_resilience_summary(scored_data)
    for key, value in summary.items():
        if key != 'category_distribution':
            print(f"{key}: {value}")
    
    print("\nResilience Category Distribution:")
    for category, count in summary['category_distribution'].items():
        print(f"{category}: {count}")