#!/usr/bin/env python3
"""
Regional Economic Resilience Dashboard - Demo Script
Quick demonstration of the full pipeline
"""

import subprocess
import sys
import time
import os

def run_command(command, description):
    """Run a command and handle output"""
    print(f"\n🔄 {description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout:
                print(result.stdout[:500])  # Show first 500 chars
        else:
            print(f"❌ Error in {description}")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Exception in {description}: {str(e)}")
        return False
    
    return True

def main():
    """Run the complete demo pipeline"""
    print("🏙️ Regional Economic Resilience Dashboard - Demo")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('src/data_collector.py'):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found. Please create it with your API keys:")
        print("OPENAI_API_KEY=your_key_here")
        print("CENSUS_API_KEY=your_key_here") 
        print("BLS_API_KEY=your_key_here")
        sys.exit(1)
    
    print("📋 Demo Pipeline Steps:")
    print("1. Data Collection (Census API)")
    print("2. Resilience Scoring")
    print("3. RAG System Test")
    print("4. Dashboard Launch")
    print()
    
    # Step 1: Data Collection
    if not run_command("python src/data_collector.py", "Collecting economic data from Census API"):
        print("Stopping demo due to data collection failure")
        return
    
    time.sleep(2)
    
    # Step 2: Resilience Scoring
    if not run_command("python src/resilience_scorer.py", "Calculating resilience scores"):
        print("Stopping demo due to scoring failure")
        return
    
    time.sleep(2)
    
    # Step 3: RAG System Test
    print("\n🔄 Testing RAG System")
    print("Running: Quick RAG test")
    print("-" * 50)
    
    try:
        from src.rag_system import SimpleRAG
        rag = SimpleRAG()
        
        # Test query
        result = rag.generate_response("What strategies promote economic diversification?")
        print("✅ RAG System Test Passed")
        print(f"Sample response preview: {result['response'][:200]}...")
        print(f"Sources found: {len(result['sources'])}")
        
    except Exception as e:
        print(f"❌ RAG System Test Failed: {str(e)}")
        print("Dashboard will still work with limited policy features")
    
    time.sleep(2)
    
    # Step 4: Dashboard Launch
    print("\n🚀 Launching Dashboard")
    print("=" * 30)
    print("Dashboard will open at: http://localhost:8501")
    print("Features available:")
    print("  • Regional Overview - Select and analyze metro areas")
    print("  • Comparative Analysis - Compare multiple metros")
    print("  • Policy Insights - RAG-powered Q&A system")
    print()
    print("Press Ctrl+C to stop the dashboard")
    print("-" * 50)
    
    try:
        # Launch Streamlit
        subprocess.run("streamlit run app.py", shell=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped. Demo complete!")

if __name__ == "__main__":
    main()