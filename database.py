"""
Thrift Store Management System - Database Backend
This module handles all database connections and operations
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional, Tuple
import pandas as pd
from datetime import datetime

class ThriftStoreDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        """Initialize database connection parameters"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = None) -> bool:
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return False
    
    def fetch_query(self, query: str, params: tuple = None) -> List[tuple]:
        """Execute SELECT queries and return results"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
    
    def fetch_df(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Fetch query results as pandas DataFrame"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            cursor.close()
            return pd.DataFrame(results, columns=columns)
        except Error as e:
            print(f"Error fetching dataframe: {e}")
            return pd.DataFrame()
    
    # ==================== CUSTOMER OPERATIONS ====================
    
    def add_customer(self, first_name: str, last_name: str, phone: str, email: str) -> Tuple[bool, str]:
        """Add new customer using stored procedure"""
        try:
            cursor = self.connection.cursor()
            cursor.callproc('sp_AddCustomer', [first_name, last_name, phone, email])
            
            for result in cursor.stored_results():
                row = result.fetchone()
                message = row[1] if row else "Customer added successfully"
            
            self.connection.commit()
            cursor.close()
            return True, message
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {str(e)}"
    
    def get_all_customers(self) -> pd.DataFrame:
        """Get all customers with their contact info"""
        query = """
        SELECT c.CustomerID, c.FirstName, c.LastName, 
               cp.Phone, ce.Email
        FROM Tb_Customer c
        LEFT JOIN Tb_CustomerPhone cp ON c.CustomerID = cp.CustomerID
        LEFT JOIN Tb_CustomerEmail ce ON c.CustomerID = ce.CustomerID
        ORDER BY c.CustomerID DESC
        """
        return self.fetch_df(query)
    
    def get_customer_purchase_history(self, customer_id: int) -> pd.DataFrame:
        """Get purchase history for a customer"""
        try:
            cursor = self.connection.cursor()
            cursor.callproc('sp_CustomerPurchaseHistory', [customer_id])
            
            for result in cursor.stored_results():
                columns = [desc[0] for desc in result.description]
                data = result.fetchall()
                df = pd.DataFrame(data, columns=columns)
            
            cursor.close()
            return df if not df.empty else pd.DataFrame()
        except Error as e:
            print(f"Error: {e}")
            return pd.DataFrame()
    
    # ==================== ITEM OPERATIONS ====================
    
    def get_all_items(self) -> pd.DataFrame:
        """Get all items with category info"""
        query = """
        SELECT i.ItemID, i.Name, i.Condition, i.Price, 
               c.CategoryName, inv.QuantityAvailable, inv.Location
        FROM Tb_Item i
        JOIN Tb_Category c ON i.CategoryID = c.CategoryID
        LEFT JOIN Tb_Inventory inv ON i.ItemID = inv.ItemID
        ORDER BY i.ItemID DESC
        """
        return self.fetch_df(query)
    
    def add_item(self, name: str, condition: str, price: float, 
                 category_id: int, supplier_id: int = None) -> Tuple[bool, str]:
        """Add new item"""
        query = """
        INSERT INTO Tb_Item (Name, `Condition`, Price, CategoryID, SupplierID)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (name, condition, price, category_id, supplier_id))
            item_id = cursor.lastrowid
            self.connection.commit()
            cursor.close()
            return True, f"Item added successfully with ID: {item_id}"
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {str(e)}"
    
    def update_item_price(self, item_id: int, new_price: float) -> Tuple[bool, str]:
        """Update item price using stored procedure"""
        try:
            cursor = self.connection.cursor()
            cursor.callproc('sp_UpdateItemPrice', [item_id, new_price])
            
            for result in cursor.stored_results():
                row = result.fetchone()
                message = row[0] if row else "Price updated successfully"
            
            self.connection.commit()
            cursor.close()
            return True, message
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {str(e)}"
    
    def get_low_stock_items(self, threshold: int = 5) -> pd.DataFrame:
        """Get low stock items using stored procedure"""
        try:
            cursor = self.connection.cursor()
            cursor.callproc('sp_LowStockAlert', [threshold])
            
            for result in cursor.stored_results():
                columns = [desc[0] for desc in result.description]
                data = result.fetchall()
                df = pd.DataFrame(data, columns=columns)
            
            cursor.close()
            return df if not df.empty else pd.DataFrame()
        except Error as e:
            print(f"Error: {e}")
            return pd.DataFrame()
    
    # ==================== INVENTORY OPERATIONS ====================
    
    def add_inventory(self, item_id: int, quantity: int, location: str) -> Tuple[bool, str]:
        """Add or update inventory"""
        query = """
        INSERT INTO Tb_Inventory (ItemID, QuantityAvailable, Location)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE QuantityAvailable = QuantityAvailable + %s
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (item_id, quantity, location, quantity))
            self.connection.commit()
            cursor.close()
            return True, "Inventory updated successfully"
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {str(e)}"
    
    # ==================== TRANSACTION OPERATIONS ====================
    
    def create_transaction(self, customer_id: int, employee_id: int, 
                          payment_mode: str) -> Tuple[bool, int, str]:
        """Create new transaction"""
        now = datetime.now()
        try:
            cursor = self.connection.cursor()
            cursor.callproc('sp_ProcessTransaction', 
                          [customer_id, employee_id, payment_mode, 
                           now.day, now.month, now.year])
            
            trans_id = None
            for result in cursor.stored_results():
                row = result.fetchone()
                trans_id = row[0] if row else None
            
            self.connection.commit()
            cursor.close()
            
            if trans_id:
                return True, trans_id, "Transaction created successfully"
            return False, 0, "Failed to create transaction"
        except Error as e:
            self.connection.rollback()
            return False, 0, f"Error: {str(e)}"
    
    def add_transaction_item(self, transaction_id: int, item_id: int, 
                            quantity: int) -> Tuple[bool, str]:
        """Add item to transaction"""
        try:
            cursor = self.connection.cursor()
            cursor.callproc('sp_AddTransactionItem', [transaction_id, item_id, quantity])
            
            for result in cursor.stored_results():
                row = result.fetchone()
                message = row[0] if row else "Item added to transaction"
            
            self.connection.commit()
            cursor.close()
            return True, message
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {str(e)}"
    
    def get_sales_report(self, start_year: int, start_month: int, 
                        end_year: int, end_month: int) -> pd.DataFrame:
        """Get sales report for date range"""
        try:
            cursor = self.connection.cursor()
            cursor.callproc('sp_SalesReport', 
                          [start_year, start_month, end_year, end_month])
            
            for result in cursor.stored_results():
                columns = [desc[0] for desc in result.description]
                data = result.fetchall()
                df = pd.DataFrame(data, columns=columns)
            
            cursor.close()
            return df if not df.empty else pd.DataFrame()
        except Error as e:
            print(f"Error: {e}")
            return pd.DataFrame()
    
    # ==================== CATEGORY OPERATIONS ====================
    
    def get_all_categories(self) -> pd.DataFrame:
        """Get all categories"""
        query = "SELECT CategoryID, CategoryName, Description FROM Tb_Category"
        return self.fetch_df(query)
    
    # ==================== EMPLOYEE OPERATIONS ====================
    
    def get_all_employees(self) -> pd.DataFrame:
        """Get all employees"""
        query = """
        SELECT e.EmployeeID, e.FirstName, e.LastName, e.Role, e.Salary
        FROM Tb_Employee e
        ORDER BY e.EmployeeID
        """
        return self.fetch_df(query)
    
    # ==================== DONATION OPERATIONS ====================
    
    def add_donation(self, donor_id: int, employee_id: int, 
                    estimated_value: float) -> Tuple[bool, str]:
        """Add new donation"""
        now = datetime.now()
        try:
            cursor = self.connection.cursor()
            cursor.callproc('sp_AddDonation', 
                          [donor_id, employee_id, estimated_value, 
                           now.day, now.month, now.year])
            
            for result in cursor.stored_results():
                row = result.fetchone()
                message = row[1] if row else "Donation recorded successfully"
            
            self.connection.commit()
            cursor.close()
            return True, message
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {str(e)}"
    
    def get_all_donors(self) -> pd.DataFrame:
        """Get all donors"""
        query = """
        SELECT d.DonorID, d.FirstName, d.LastName, dp.Phone
        FROM Tb_Donor d
        LEFT JOIN Tb_DonorPhone dp ON d.DonorID = dp.DonorID
        ORDER BY d.DonorID
        """
        return self.fetch_df(query)
    
    # ==================== ANALYTICS FUNCTIONS ====================
    
    def get_customer_total_purchases(self, customer_id: int) -> float:
        """Get customer's total purchase amount"""
        query = "SELECT fn_CustomerTotalPurchases(%s) AS total"
        result = self.fetch_query(query, (customer_id,))
        return float(result[0][0]) if result else 0.0
    
    def get_category_inventory_value(self, category_id: int) -> float:
        """Get total inventory value for a category"""
        query = "SELECT fn_CategoryInventoryValue(%s) AS value"
        result = self.fetch_query(query, (category_id,))
        return float(result[0][0]) if result else 0.0
    
    def get_employee_sales_total(self, employee_id: int) -> float:
        """Get employee's total sales processed"""
        query = "SELECT fn_EmployeeSalesTotal(%s) AS total"
        result = self.fetch_query(query, (employee_id,))
        return float(result[0][0]) if result else 0.0
    
    # ==================== DASHBOARD ANALYTICS ====================
    
    def get_dashboard_stats(self) -> Dict:
        """Get key statistics for dashboard"""
        stats = {}
        
        # Total Customers
        result = self.fetch_query("SELECT COUNT(*) FROM Tb_Customer")
        stats['total_customers'] = result[0][0] if result else 0
        
        # Total Items
        result = self.fetch_query("SELECT COUNT(*) FROM Tb_Item")
        stats['total_items'] = result[0][0] if result else 0
        
        # Total Transactions
        result = self.fetch_query("SELECT COUNT(*) FROM Tb_Transaction")
        stats['total_transactions'] = result[0][0] if result else 0
        
        # Total Revenue
        result = self.fetch_query("SELECT COALESCE(SUM(TotalAmount), 0) FROM Tb_Transaction")
        stats['total_revenue'] = float(result[0][0]) if result else 0.0
        
        # Low Stock Count
        result = self.fetch_query("SELECT COUNT(*) FROM Tb_Inventory WHERE QuantityAvailable <= 5")
        stats['low_stock_count'] = result[0][0] if result else 0
        
        return stats
