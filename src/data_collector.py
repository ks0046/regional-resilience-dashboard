import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class EconomicDataCollector:
    def __init__(self):
        self.census_api_key = os.getenv('CENSUS_API_KEY')
        self.bls_api_key = os.getenv('BLS_API_KEY')
        
        # Major metro areas for quick implementation
        self.metro_areas = {
            'New York-Newark-Jersey City, NY-NJ-PA': '35620',
            'Los Angeles-Long Beach-Anaheim, CA': '31080',
            'Chicago-Naperville-Elgin, IL-IN-WI': '16980',
            'Dallas-Fort Worth-Arlington, TX': '19100',
            'Houston-The Woodlands-Sugar Land, TX': '26420',
            'Washington-Arlington-Alexandria, DC-VA-MD-WV': '47900',
            'Philadelphia-Camden-Wilmington, PA-NJ-DE-MD': '37980',
            'Miami-Fort Lauderdale-West Palm Beach, FL': '33100',
            'Atlanta-Sandy Springs-Roswell, GA': '12060',
            'Boston-Cambridge-Newton, MA-NH': '14460',
            'Phoenix-Mesa-Scottsdale, AZ': '38060',
            'San Francisco-Oakland-Hayward, CA': '41860',
            'Riverside-San Bernardino-Ontario, CA': '40140',
            'Detroit-Warren-Dearborn, MI': '19820',
            'Seattle-Tacoma-Bellevue, WA': '42660',
            'Minneapolis-St. Paul-Bloomington, MN-WI': '33460',
            'San Diego-Carlsbad, CA': '41740',
            'Tampa-St. Petersburg-Clearwater, FL': '45300',
            'Denver-Aurora-Lakewood, CO': '19740',
            'Baltimore-Columbia-Towson, MD': '12580'
        }
        
    def get_census_data(self):
        """Fetch Census ACS 5-year data for metro areas"""
        # Basic demographics and economic indicators
        variables = {
            'B01003_001E': 'total_population',
            'B19013_001E': 'median_household_income',
            'B25077_001E': 'median_home_value',
            'B15003_022E': 'bachelors_degree',
            'B08301_010E': 'public_transportation'
        }
        
        var_string = ','.join(variables.keys())
        
        data = []
        for metro_name, metro_code in self.metro_areas.items():
            url = f"https://api.census.gov/data/2021/acs/acs5?get={var_string}&for=metropolitan%20statistical%20area%2Fmicropolitan%20statistical%20area:{metro_code}&key={self.census_api_key}"
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    json_data = response.json()
                    if len(json_data) > 1:  # Has data beyond header
                        row_data = json_data[1]
                        metro_data = {
                            'metro_name': metro_name,
                            'metro_code': metro_code
                        }
                        
                        for i, var_code in enumerate(variables.keys()):
                            metro_data[variables[var_code]] = str(row_data[i]) if row_data[i] != '-999999999' else "0"
                        
                        data.append(metro_data)
                        print(f"✓ Collected data for {metro_name}")
                    
            except Exception as e:
                print(f"Error collecting data for {metro_name}: {str(e)}")
                
        return pd.DataFrame(data)
    
    def get_bls_unemployment_data(self):
        """Fetch BLS unemployment data for metro areas"""
        # Sample unemployment series IDs for major metros (this would normally be more comprehensive)
        unemployment_series = {
            'New York-Newark-Jersey City, NY-NJ-PA': 'LAUMT355620000000003',
            'Los Angeles-Long Beach-Anaheim, CA': 'LAUMT063108000000003',
            'Chicago-Naperville-Elgin, IL-IN-WI': 'LAUMT171698000000003',
            'Dallas-Fort Worth-Arlington, TX': 'LAUMT481910000000003',
            'Houston-The Woodlands-Sugar Land, TX': 'LAUMT482642000000003'
        }
        
        unemployment_data = []
        
        for metro_name, series_id in unemployment_series.items():
            # Mock data for quick implementation - in real app would call BLS API
            unemployment_data.append({
                'metro_name': metro_name,
                'unemployment_rate': 4.2 + (hash(metro_name) % 3),  # Mock data between 4.2-7.2%
                'unemployment_change_1yr': -0.5 + (hash(metro_name) % 2)  # Mock change
            })
            
        return pd.DataFrame(unemployment_data)
    
    def create_sample_economic_diversity_data(self):
        """Create sample economic diversity metrics"""
        diversity_data = []
        
        for metro_name in self.metro_areas.keys():
            # Mock economic diversity score (in real app would calculate from industry data)
            diversity_score = 50 + (hash(metro_name) % 40)  # Score 50-90
            
            diversity_data.append({
                'metro_name': metro_name,
                'economic_diversity_score': diversity_score,
                'top_industry_share': 0.15 + (hash(metro_name) % 20) / 100  # 15-35% share
            })
            
        return pd.DataFrame(diversity_data)
    
    def collect_all_data(self):
        """Collect and merge all economic data"""
        print("Collecting Census data...")
        census_data = self.get_census_data()
        
        print("Collecting unemployment data...")
        unemployment_data = self.get_bls_unemployment_data()
        
        print("Creating economic diversity data...")
        diversity_data = self.create_sample_economic_diversity_data()
        
        # Merge all datasets
        merged_data = census_data
        
        if not unemployment_data.empty:
            merged_data = merged_data.merge(unemployment_data, on='metro_name', how='left')
            
        if not diversity_data.empty:
            merged_data = merged_data.merge(diversity_data, on='metro_name', how='left')
        
        # Clean and convert data types
        numeric_columns = ['total_population', 'median_household_income', 'median_home_value', 
                          'bachelors_degree', 'public_transportation', 'unemployment_rate',
                          'unemployment_change_1yr', 'economic_diversity_score', 'top_industry_share']
        
        for col in numeric_columns:
            if col in merged_data.columns:
                merged_data[col] = pd.to_numeric(merged_data[col], errors='coerce')
        
        return merged_data

if __name__ == "__main__":
    collector = EconomicDataCollector()
    data = collector.collect_all_data()
    
    # Save to data directory
    os.makedirs('data', exist_ok=True)
    data.to_csv('data/metro_economic_data.csv', index=False)
    print(f"\nData collection complete. Saved {len(data)} metro areas to ../data/metro_economic_data.csv")
    print(data.head())