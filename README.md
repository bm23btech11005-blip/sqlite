# Ecommerce Data Analysis Exercise

This project demonstrates a complete data pipeline for ecommerce analytics using Python and SQLite, created as part of the Cursor IDE (A-SDLC) exercise.

## Overview

The exercise consists of three main components:
1. **Data Generation**: Create synthetic ecommerce data
2. **Database Ingestion**: Store data in a relational SQLite database
3. **Analytics Queries**: Generate complex SQL queries with joins and business insights

## Project Structure

```
├── generate_ecommerce_data.py    # Generates synthetic ecommerce data
├── ingest_to_database.py         # Creates database schema and ingests data
├── generate_sql_queries.py       # Runs complex analytics queries
├── run_complete_exercise.py      # Orchestrates the entire workflow
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Generated Data

The system creates realistic ecommerce data including:

- **Categories** (10): Electronics, Clothing, Books, etc.
- **Customers** (100): Names, emails, addresses, registration dates
- **Products** (50): Names, prices, stock quantities, descriptions
- **Orders** (200): Customer orders with dates, amounts, status
- **Order Items** (400+): Individual items within orders

## Database Schema

The SQLite database includes properly structured tables with:
- Primary and foreign key constraints
- Data validation checks
- Performance indexes
- Referential integrity

## Analytics Queries

The system generates comprehensive business insights:

1. **Top Customers by Revenue** - Identify highest-value customers
2. **Best-Selling Products by Category** - Product performance analysis
3. **Monthly Sales Trends** - Time-based revenue analysis
4. **Customer Segmentation** - Order frequency patterns
5. **Product Performance Metrics** - Comprehensive product analysis
6. **Revenue by Category and Period** - Category performance over time
7. **Cross-Selling Analysis** - Products frequently bought together

## Installation & Usage

### Prerequisites
- Python 3.7+
- pip package manager

### Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

### Run Complete Exercise
```bash
python run_complete_exercise.py
```

### Run Individual Components
```bash
# Generate data only
python generate_ecommerce_data.py

# Ingest data only (requires data file)
python ingest_to_database.py

# Run analytics only (requires database)
python generate_sql_queries.py
```

## Output Files

- `ecommerce_data.json` - Generated synthetic data
- `ecommerce.db` - SQLite database with all tables and data

## Key Features

### Data Generation
- Realistic customer profiles using Faker library
- Product catalog across multiple categories
- Order patterns with realistic relationships
- Proper data relationships and constraints

### Database Design
- Normalized relational schema
- Foreign key constraints
- Performance indexes
- Data validation rules

### Analytics Capabilities
- Multi-table joins (INNER, LEFT, RIGHT)
- Aggregate functions (COUNT, SUM, AVG, MAX, MIN)
- Window functions for advanced analytics
- Common Table Expressions (CTEs)
- Subqueries for complex analysis
- Business intelligence insights

## Sample Query Results

The analytics provide insights such as:
- Customer lifetime value rankings
- Product performance by category
- Seasonal sales trends
- Customer behavior segmentation
- Cross-selling opportunities
- Revenue optimization insights

## Technical Implementation

- **Language**: Python 3
- **Database**: SQLite
- **Libraries**: Faker (data generation), Pandas (data analysis)
- **SQL Features**: Complex joins, window functions, CTEs, aggregations

## Exercise Completion

This project fulfills all requirements of the Cursor IDE exercise:
- ✅ Synthetic ecommerce data generation (~5 files worth of data)
- ✅ SQLite database creation and data ingestion
- ✅ Complex SQL queries with multiple table joins
- ✅ Comprehensive output and analysis
- ✅ Ready for Git repository push

## Next Steps

To extend this project, consider:
- Adding data visualization with matplotlib/plotly
- Implementing real-time data updates
- Adding more complex business rules
- Creating a web dashboard
- Implementing machine learning models for predictions