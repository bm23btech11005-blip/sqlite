#!/usr/bin/env python3
"""
Complete Ecommerce Data Exercise Runner

This script runs the complete exercise:
1. Generates synthetic ecommerce data
2. Creates SQLite database and ingests data
3. Runs complex SQL queries with joins and analytics
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(f"Return code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: {script_name} not found!")
        return False

def check_requirements():
    """Check if required packages are installed"""
    try:
        import faker
        import pandas
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def main():
    """Run the complete exercise"""
    print("ECOMMERCE DATA EXERCISE - COMPLETE WORKFLOW")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Step 1: Generate synthetic data
    success = run_script("generate_ecommerce_data.py", 
                        "Generating Synthetic Ecommerce Data")
    if not success:
        print("Failed to generate data. Stopping.")
        return
    
    # Step 2: Ingest data into database
    success = run_script("ingest_to_database.py", 
                        "Ingesting Data into SQLite Database")
    if not success:
        print("Failed to ingest data. Stopping.")
        return
    
    # Step 3: Run analytics queries
    success = run_script("generate_sql_queries.py", 
                        "Running SQL Analytics Queries")
    if not success:
        print("Failed to run queries. Stopping.")
        return
    
    print(f"\n{'='*60}")
    print("EXERCISE COMPLETED SUCCESSFULLY!")
    print(f"{'='*60}")
    print("\nFiles created:")
    print("- ecommerce_data.json (synthetic data)")
    print("- ecommerce.db (SQLite database)")
    print("\nScripts available:")
    print("- generate_ecommerce_data.py")
    print("- ingest_to_database.py") 
    print("- generate_sql_queries.py")

if __name__ == "__main__":
    main()