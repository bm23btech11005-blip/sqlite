#!/usr/bin/env python3
"""
Prompt: Generate complex SQL queries that join multiple tables and produce meaningful business insights.

Create queries that demonstrate:
- INNER JOINs across multiple tables
- LEFT/RIGHT JOINs for comprehensive data analysis
- Aggregate functions (COUNT, SUM, AVG, MAX, MIN)
- GROUP BY and HAVING clauses
- Subqueries and CTEs
- Window functions for advanced analytics

Business questions to answer:
1. Top customers by total purchase amount
2. Best-selling products by category
3. Monthly sales trends
4. Customer order frequency analysis
5. Product performance metrics
6. Revenue analysis by category and time period
"""

import sqlite3
import pandas as pd
from datetime import datetime

class EcommerceAnalytics:
    def __init__(self, db_path="ecommerce.db"):
        self.db_path = db_path
    
    def execute_query(self, query, description):
        """Execute a query and return results with description"""
        conn = sqlite3.connect(self.db_path)
        try:
            df = pd.read_sql_query(query, conn)
            print(f"\n{'='*60}")
            print(f"QUERY: {description}")
            print(f"{'='*60}")
            print(f"SQL:\n{query}")
            print(f"\nRESULTS:")
            print(df.to_string(index=False))
            print(f"\nRows returned: {len(df)}")
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()
    
    def top_customers_by_revenue(self):
        """Find top 10 customers by total purchase amount"""
        query = """
        SELECT 
            c.id,
            c.name,
            c.email,
            COUNT(o.id) as total_orders,
            SUM(o.total_amount) as total_spent,
            AVG(o.total_amount) as avg_order_value,
            MAX(o.order_date) as last_order_date
        FROM customers c
        INNER JOIN orders o ON c.id = o.customer_id
        WHERE o.status != 'cancelled'
        GROUP BY c.id, c.name, c.email
        ORDER BY total_spent DESC
        LIMIT 10
        """
        return self.execute_query(query, "Top 10 Customers by Total Revenue")
    
    def best_selling_products_by_category(self):
        """Find best-selling products in each category"""
        query = """
        WITH product_sales AS (
            SELECT 
                p.id,
                p.name,
                c.name as category_name,
                SUM(oi.quantity) as total_quantity_sold,
                SUM(oi.quantity * oi.unit_price) as total_revenue,
                COUNT(DISTINCT oi.order_id) as orders_count
            FROM products p
            INNER JOIN categories c ON p.category_id = c.id
            INNER JOIN order_items oi ON p.id = oi.product_id
            INNER JOIN orders o ON oi.order_id = o.id
            WHERE o.status != 'cancelled'
            GROUP BY p.id, p.name, c.name
        ),
        ranked_products AS (
            SELECT *,
                ROW_NUMBER() OVER (PARTITION BY category_name ORDER BY total_revenue DESC) as rank
            FROM product_sales
        )
        SELECT 
            category_name,
            name as product_name,
            total_quantity_sold,
            total_revenue,
            orders_count
        FROM ranked_products
        WHERE rank <= 3
        ORDER BY category_name, rank
        """
        return self.execute_query(query, "Top 3 Best-Selling Products by Category")
    
    def monthly_sales_trends(self):
        """Analyze monthly sales trends"""
        query = """
        SELECT 
            strftime('%Y-%m', o.order_date) as month,
            COUNT(o.id) as total_orders,
            COUNT(DISTINCT o.customer_id) as unique_customers,
            SUM(o.total_amount) as total_revenue,
            AVG(o.total_amount) as avg_order_value,
            SUM(oi.quantity) as total_items_sold
        FROM orders o
        INNER JOIN order_items oi ON o.id = oi.order_id
        WHERE o.status != 'cancelled'
        GROUP BY strftime('%Y-%m', o.order_date)
        ORDER BY month DESC
        LIMIT 12
        """
        return self.execute_query(query, "Monthly Sales Trends (Last 12 Months)")
    
    def customer_order_frequency_analysis(self):
        """Analyze customer ordering patterns"""
        query = """
        WITH customer_stats AS (
            SELECT 
                c.id,
                c.name,
                c.registration_date,
                COUNT(o.id) as total_orders,
                SUM(o.total_amount) as total_spent,
                MIN(o.order_date) as first_order_date,
                MAX(o.order_date) as last_order_date,
                JULIANDAY(MAX(o.order_date)) - JULIANDAY(MIN(o.order_date)) as days_between_first_last
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled'
            GROUP BY c.id, c.name, c.registration_date
        )
        SELECT 
            CASE 
                WHEN total_orders = 0 THEN 'No Orders'
                WHEN total_orders = 1 THEN 'One-time Buyer'
                WHEN total_orders BETWEEN 2 AND 5 THEN 'Occasional Buyer'
                WHEN total_orders BETWEEN 6 AND 10 THEN 'Regular Customer'
                ELSE 'VIP Customer'
            END as customer_segment,
            COUNT(*) as customer_count,
            AVG(total_spent) as avg_total_spent,
            AVG(total_orders) as avg_orders_per_customer
        FROM customer_stats
        GROUP BY customer_segment
        ORDER BY 
            CASE customer_segment
                WHEN 'VIP Customer' THEN 1
                WHEN 'Regular Customer' THEN 2
                WHEN 'Occasional Buyer' THEN 3
                WHEN 'One-time Buyer' THEN 4
                WHEN 'No Orders' THEN 5
            END
        """
        return self.execute_query(query, "Customer Segmentation by Order Frequency")
    
    def product_performance_metrics(self):
        """Comprehensive product performance analysis"""
        query = """
        SELECT 
            p.id,
            p.name,
            c.name as category,
            p.price,
            p.stock_quantity,
            COALESCE(SUM(oi.quantity), 0) as total_sold,
            COALESCE(SUM(oi.quantity * oi.unit_price), 0) as total_revenue,
            COALESCE(COUNT(DISTINCT oi.order_id), 0) as orders_count,
            CASE 
                WHEN SUM(oi.quantity) IS NULL THEN 'No Sales'
                WHEN SUM(oi.quantity) < 5 THEN 'Low Performer'
                WHEN SUM(oi.quantity) BETWEEN 5 AND 20 THEN 'Average Performer'
                ELSE 'High Performer'
            END as performance_category,
            ROUND(
                COALESCE(SUM(oi.quantity * oi.unit_price), 0) / 
                NULLIF(SUM(oi.quantity), 0), 2
            ) as avg_selling_price
        FROM products p
        INNER JOIN categories c ON p.category_id = c.id
        LEFT JOIN order_items oi ON p.id = oi.product_id
        LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
        GROUP BY p.id, p.name, c.name, p.price, p.stock_quantity
        ORDER BY total_revenue DESC
        """
        return self.execute_query(query, "Product Performance Metrics")
    
    def revenue_analysis_by_category_and_period(self):
        """Revenue analysis by category and time period"""
        query = """
        SELECT 
            c.name as category,
            strftime('%Y-%m', o.order_date) as month,
            COUNT(DISTINCT o.id) as orders_count,
            SUM(oi.quantity) as items_sold,
            SUM(oi.quantity * oi.unit_price) as revenue,
            AVG(oi.unit_price) as avg_item_price,
            COUNT(DISTINCT o.customer_id) as unique_customers
        FROM categories c
        INNER JOIN products p ON c.id = p.category_id
        INNER JOIN order_items oi ON p.id = oi.product_id
        INNER JOIN orders o ON oi.order_id = o.id
        WHERE o.status != 'cancelled'
        GROUP BY c.name, strftime('%Y-%m', o.order_date)
        HAVING revenue > 0
        ORDER BY month DESC, revenue DESC
        """
        return self.execute_query(query, "Revenue Analysis by Category and Month")
    
    def cross_selling_analysis(self):
        """Find products frequently bought together"""
        query = """
        WITH order_product_pairs AS (
            SELECT DISTINCT
                oi1.product_id as product1_id,
                oi2.product_id as product2_id,
                oi1.order_id
            FROM order_items oi1
            INNER JOIN order_items oi2 ON oi1.order_id = oi2.order_id
            INNER JOIN orders o ON oi1.order_id = o.id
            WHERE oi1.product_id < oi2.product_id
            AND o.status != 'cancelled'
        )
        SELECT 
            p1.name as product1,
            p2.name as product2,
            c1.name as category1,
            c2.name as category2,
            COUNT(*) as times_bought_together,
            ROUND(COUNT(*) * 100.0 / (
                SELECT COUNT(DISTINCT order_id) 
                FROM order_items 
                WHERE product_id = p1.id
            ), 2) as cross_sell_rate_percent
        FROM order_product_pairs opp
        INNER JOIN products p1 ON opp.product1_id = p1.id
        INNER JOIN products p2 ON opp.product2_id = p2.id
        INNER JOIN categories c1 ON p1.category_id = c1.id
        INNER JOIN categories c2 ON p2.category_id = c2.id
        GROUP BY p1.id, p2.id, p1.name, p2.name, c1.name, c2.name
        HAVING times_bought_together >= 3
        ORDER BY times_bought_together DESC
        LIMIT 15
        """
        return self.execute_query(query, "Cross-Selling Analysis - Products Frequently Bought Together")

def main():
    """Run all analytics queries"""
    
    # Check if database exists
    try:
        analytics = EcommerceAnalytics()
        
        print("ECOMMERCE DATABASE ANALYTICS REPORT")
        print("Generated on:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Run all analytics
        analytics.top_customers_by_revenue()
        analytics.best_selling_products_by_category()
        analytics.monthly_sales_trends()
        analytics.customer_order_frequency_analysis()
        analytics.product_performance_metrics()
        analytics.revenue_analysis_by_category_and_period()
        analytics.cross_selling_analysis()
        
        print(f"\n{'='*60}")
        print("ANALYTICS REPORT COMPLETED")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to run the data generation and ingestion scripts first:")
        print("1. python generate_ecommerce_data.py")
        print("2. python ingest_to_database.py")

if __name__ == "__main__":
    main()