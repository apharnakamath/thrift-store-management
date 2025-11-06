"""
Thrift Store Management System - Streamlit Frontend
Main application interface
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database import ThriftStoreDB

# Page configuration
st.set_page_config(
    page_title="Thrift Store Management",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-msg {
        color: #28a745;
        font-weight: bold;
    }
    .error-msg {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for database connection
if 'db' not in st.session_state:
    st.session_state.db = None
    st.session_state.connected = False

# Database connection sidebar
with st.sidebar:
    st.header("🔐 Database Connection")
    
    if not st.session_state.connected:
        with st.form("db_connection"):
            host = st.text_input("Host", value="localhost")
            user = st.text_input("Username", value="root")
            password = st.text_input("Password", type="default")
            database = st.text_input("Database", value="MINIPROJECT_DBMS")
            
            if st.form_submit_button("Connect"):
                db = ThriftStoreDB(host, user, password, database)
                if db.connect():
                    st.session_state.db = db
                    st.session_state.connected = True
                    st.success("Connected successfully!")
                    st.rerun()
                else:
                    st.error("Connection failed!")
    else:
        st.success("✅ Connected to Database")
        if st.button("Disconnect"):
            if st.session_state.db:
                st.session_state.db.disconnect()
            st.session_state.connected = False
            st.session_state.db = None
            st.rerun()
    
    st.divider()
    
    # Navigation
    if st.session_state.connected:
        st.header(" Navigation")
        page = st.radio(
            "Select Module",
            [" Dashboard", " Customers", " Inventory", 
             " Transactions", " Donations", " Reports"],
            label_visibility="collapsed"
        )
    else:
        page = " Dashboard"

# Main content
if not st.session_state.connected:
    st.markdown("<div class='main-header'> Thrift Store Management System</div>", 
                unsafe_allow_html=True)
    st.info(" Please connect to the database using the sidebar")
    
    st.markdown("###  Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Customer Management**")
        st.write("• Add new customers")
        st.write("• View purchase history")
        st.write("• Track customer spending")
    
    with col2:
        st.markdown("**Inventory Control**")
        st.write("• Manage items & stock")
        st.write("• Low stock alerts")
        st.write("• Price management")
    
    with col3:
        st.markdown("**Sales & Reports**")
        st.write("• Process transactions")
        st.write("• Sales analytics")
        st.write("• Donation tracking")

else:
    db = st.session_state.db
    
    # ==================== DASHBOARD ====================
    if page == " Dashboard":
        st.markdown("<div class='main-header'> Dashboard</div>", unsafe_allow_html=True)
        
        # Get statistics
        stats = db.get_dashboard_stats()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Customers", stats['total_customers'])
        with col2:
            st.metric("Total Items", stats['total_items'])
        with col3:
            st.metric("Total Transactions", stats['total_transactions'])
        with col4:
            st.metric("Total Revenue", f"₹{stats['total_revenue']:,.2f}")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⚠️ Low Stock Alert")
            if stats['low_stock_count'] > 0:
                st.warning(f"{stats['low_stock_count']} items are low on stock!")
                low_stock_df = db.get_low_stock_items(5)
                if not low_stock_df.empty:
                    st.dataframe(low_stock_df, use_container_width=True)
            else:
                st.success("All items are well stocked!")
        
        with col2:
            st.subheader(" Recent Transactions")
            current_date = datetime.now()
            recent_trans = db.get_sales_report(
                current_date.year, current_date.month,
                current_date.year, current_date.month
            )
            if not recent_trans.empty:
                st.dataframe(recent_trans.head(10), use_container_width=True)
            else:
                st.info("No transactions this month")
    
    # ==================== CUSTOMERS ====================
    elif page == " Customers":
        st.markdown("<div class='main-header'>👥 Customer Management</div>", 
                    unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📋 View Customers", "➕ Add Customer", "🔍 Customer Details"])
        
        with tab1:
            st.subheader("All Customers")
            customers_df = db.get_all_customers()
            if not customers_df.empty:
                st.dataframe(customers_df, use_container_width=True, hide_index=True)
            else:
                st.info("No customers found")
        
        with tab2:
            st.subheader("Add New Customer")
            with st.form("add_customer_form"):
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name*")
                    phone = st.text_input("Phone Number*")
                with col2:
                    last_name = st.text_input("Last Name*")
                    email = st.text_input("Email*")
                
                submitted = st.form_submit_button("Add Customer")
                
                if submitted:
                    if first_name and last_name and phone and email:
                        success, message = db.add_customer(first_name, last_name, phone, email)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("Please fill all required fields")
        
        with tab3:
            st.subheader("Customer Purchase History")
            customers_df = db.get_all_customers()
            if not customers_df.empty:
                customer_options = {
                    f"{row['FirstName']} {row['LastName']} (ID: {row['CustomerID']})": row['CustomerID']
                    for _, row in customers_df.iterrows()
                }
                selected_customer = st.selectbox("Select Customer", options=customer_options.keys())
                
                if selected_customer and st.button("View History"):
                    customer_id = customer_options[selected_customer]
                    
                    # Show total purchases
                    total = db.get_customer_total_purchases(customer_id)
                    st.metric("Total Purchases", f"₹{total:,.2f}")
                    
                    # Show purchase history
                    history = db.get_customer_purchase_history(customer_id)
                    if not history.empty:
                        st.dataframe(history, use_container_width=True, hide_index=True)
                    else:
                        st.info("No purchase history found")
            else:
                st.info("No customers available")
    
    # ==================== INVENTORY ====================
    elif page == " Inventory":
        st.markdown("<div class='main-header'> Inventory Management</div>", 
                    unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 View Items", "➕ Add Item", "💰 Update Price", "📥 Add Stock"])
        
        with tab1:
            st.subheader("All Items")
            items_df = db.get_all_items()
            if not items_df.empty:
                st.dataframe(items_df, use_container_width=True, hide_index=True)
            else:
                st.info("No items found")
        
        with tab2:
            st.subheader("Add New Item")
            categories_df = db.get_all_categories()
            
            with st.form("add_item_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    item_name = st.text_input("Item Name*")
                    condition = st.selectbox("Condition*", 
                        ["New", "Like New", "Good", "Fair", "Poor"])
                    price = st.number_input("Price*", min_value=0.0, step=0.01)
                
                with col2:
                    if not categories_df.empty:
                        category_options = {
                            row['CategoryName']: row['CategoryID']
                            for _, row in categories_df.iterrows()
                        }
                        selected_category = st.selectbox("Category*", options=category_options.keys())
                        category_id = category_options[selected_category]
                    else:
                        st.error("No categories available")
                        category_id = None
                
                submitted = st.form_submit_button("Add Item")
                
                if submitted and item_name and category_id:
                    success, message = db.add_item(item_name, condition, price, category_id)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        
        with tab3:
            st.subheader("Update Item Price")
            items_df = db.get_all_items()
            
            if not items_df.empty:
                item_options = {
                    f"{row['Name']} - Current: ₹{row['Price']} (ID: {row['ItemID']})": row['ItemID']
                    for _, row in items_df.iterrows()
                }
                
                selected_item = st.selectbox("Select Item", options=item_options.keys())
                new_price = st.number_input("New Price", min_value=0.0, step=0.01)
                
                if st.button("Update Price"):
                    item_id = item_options[selected_item]
                    success, message = db.update_item_price(item_id, new_price)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.info("No items available")
        
        with tab4:
            st.subheader("Add Inventory Stock")
            items_df = db.get_all_items()
            
            if not items_df.empty:
                with st.form("add_inventory_form"):
                    item_options = {
                        f"{row['Name']} (ID: {row['ItemID']})": row['ItemID']
                        for _, row in items_df.iterrows()
                    }
                    
                    selected_item = st.selectbox("Select Item", options=item_options.keys())
                    quantity = st.number_input("Quantity to Add", min_value=1, step=1)
                    location = st.text_input("Storage Location", value="Main Store")
                    
                    submitted = st.form_submit_button("Add to Inventory")
                    
                    if submitted:
                        item_id = item_options[selected_item]
                        success, message = db.add_inventory(item_id, quantity, location)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
            else:
                st.info("No items available")
    
    # ==================== TRANSACTIONS ====================
    elif page == " Transactions":
        st.markdown("<div class='main-header'>🛒 Transaction Processing</div>", 
                    unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["➕ New Transaction", "📋 View Transactions"])
        
        with tab1:
            st.subheader("Process New Sale")
            
            customers_df = db.get_all_customers()
            employees_df = db.get_all_employees()
            items_df = db.get_all_items()
            
            if customers_df.empty or employees_df.empty or items_df.empty:
                st.error("Please ensure customers, employees, and items are available")
            else:
                # Transaction header
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    customer_options = {
                        f"{row['FirstName']} {row['LastName']}": row['CustomerID']
                        for _, row in customers_df.iterrows()
                    }
                    selected_customer = st.selectbox("Customer", options=customer_options.keys())
                    customer_id = customer_options[selected_customer]
                
                with col2:
                    employee_options = {
                        f"{row['FirstName']} {row['LastName']} ({row['Role']})": row['EmployeeID']
                        for _, row in employees_df.iterrows()
                    }
                    selected_employee = st.selectbox("Employee", options=employee_options.keys())
                    employee_id = employee_options[selected_employee]
                
                with col3:
                    payment_mode = st.selectbox("Payment Mode", ["Cash", "Card", "UPI", "Check"])
                
                st.divider()
                
                # Initialize cart in session state
                if 'cart' not in st.session_state:
                    st.session_state.cart = []
                
                # Add items to cart
                st.subheader("Add Items to Cart")
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    item_options = {
                        f"{row['Name']} - ₹{row['Price']} (Stock: {row['QuantityAvailable']})": 
                        (row['ItemID'], row['Price'], row['QuantityAvailable'])
                        for _, row in items_df.iterrows()
                        if row['QuantityAvailable'] > 0
                    }
                    selected_item = st.selectbox("Select Item", options=item_options.keys())
                
                with col2:
                    quantity = st.number_input("Qty", min_value=1, value=1)
                
                with col3:
                    st.write("")
                    st.write("")
                    if st.button("Add to Cart"):
                        item_id, price, available = item_options[selected_item]
                        if quantity <= available:
                            st.session_state.cart.append({
                                'item_id': item_id,
                                'name': selected_item.split(' - ')[0],
                                'quantity': quantity,
                                'unit_price': price,
                                'line_total': price * quantity
                            })
                            st.success("Item added to cart!")
                        else:
                            st.error(f"Only {available} units available!")
                
                # Display cart
                if st.session_state.cart:
                    st.subheader("Shopping Cart")
                    cart_df = pd.DataFrame(st.session_state.cart)
                    st.dataframe(cart_df, use_container_width=True, hide_index=True)
                    
                    total = sum(item['line_total'] for item in st.session_state.cart)
                    st.metric("Total Amount", f"₹{total:,.2f}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Complete Transaction", type="primary"):
                            # Create transaction
                            success, trans_id, message = db.create_transaction(
                                customer_id, employee_id, payment_mode
                            )
                            
                            if success:
                                # Add items to transaction
                                all_success = True
                                for item in st.session_state.cart:
                                    item_success, item_msg = db.add_transaction_item(
                                        trans_id, item['item_id'], item['quantity']
                                    )
                                    if not item_success:
                                        all_success = False
                                        st.error(f"Error adding {item['name']}: {item_msg}")
                                
                                if all_success:
                                    st.success(f"Transaction completed! ID: {trans_id}")
                                    st.session_state.cart = []
                                    st.rerun()
                            else:
                                st.error(message)
                    
                    with col2:
                        if st.button("Clear Cart"):
                            st.session_state.cart = []
                            st.rerun()
        
        with tab2:
            st.subheader("Transaction History")
            current_date = datetime.now()
            
            col1, col2 = st.columns(2)
            with col1:
                month = st.selectbox("Month", range(1, 13), index=current_date.month-1)
            with col2:
                year = st.number_input("Year", min_value=2020, max_value=2030, 
                                      value=current_date.year)
            
            if st.button("View Transactions"):
                trans_df = db.get_sales_report(year, month, year, month)
                if not trans_df.empty:
                    st.dataframe(trans_df, use_container_width=True, hide_index=True)
                    st.metric("Total Sales", f"₹{trans_df['TotalAmount'].sum():,.2f}")
                else:
                    st.info("No transactions found for this period")
    
    # ==================== DONATIONS ====================
    elif page == " Donations":
        st.markdown("<div class='main-header'> Donation Management</div>", 
                    unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["➕ Record Donation", "📋 View Donors"])
        
        with tab1:
            st.subheader("Record New Donation")
            
            donors_df = db.get_all_donors()
            employees_df = db.get_all_employees()
            
            with st.form("add_donation_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if not donors_df.empty:
                        donor_options = {
                            f"{row['FirstName']} {row['LastName']}": row['DonorID']
                            for _, row in donors_df.iterrows()
                        }
                        selected_donor = st.selectbox("Donor", options=donor_options.keys())
                        donor_id = donor_options[selected_donor]
                    else:
                        st.error("No donors available")
                        donor_id = None
                
                with col2:
                    if not employees_df.empty:
                        employee_options = {
                            f"{row['FirstName']} {row['LastName']}": row['EmployeeID']
                            for _, row in employees_df.iterrows()
                        }
                        selected_employee = st.selectbox("Handled By", options=employee_options.keys())
                        employee_id = employee_options[selected_employee]
                    else:
                        st.error("No employees available")
                        employee_id = None
                
                estimated_value = st.number_input("Estimated Value (₹)", min_value=0.0, step=10.0)
                
                submitted = st.form_submit_button("Record Donation")
                
                if submitted and donor_id and employee_id:
                    success, message = db.add_donation(donor_id, employee_id, estimated_value)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        
        with tab2:
            st.subheader("All Donors")
            donors_df = db.get_all_donors()
            if not donors_df.empty:
                st.dataframe(donors_df, use_container_width=True, hide_index=True)
            else:
                st.info("No donors found")
    
    # ==================== REPORTS ====================
    elif page == " Reports":
        st.markdown("<div class='main-header'> Reports & Analytics</div>", 
                    unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📈 Sales Report", "📦 Inventory Report", "👤 Employee Performance"])
        
        with tab1:
            st.subheader("Sales Report")
            col1, col2, col3, col4 = st.columns(4)
            
            current_date = datetime.now()
            with col1:
                start_month = st.selectbox("Start Month", range(1, 13), index=0)
            with col2:
                start_year = st.number_input("Start Year", min_value=2020, 
                                            value=current_date.year)
            with col3:
                end_month = st.selectbox("End Month", range(1, 13), 
                                        index=current_date.month-1)
            with col4:
                end_year = st.number_input("End Year", min_value=2020, 
                                          value=current_date.year)
            
            if st.button("Generate Report"):
                report_df = db.get_sales_report(start_year, start_month, end_year, end_month)
                if not report_df.empty:
                    st.dataframe(report_df, use_container_width=True, hide_index=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Transactions", len(report_df))
                    with col2:
                        st.metric("Total Revenue", f"₹{report_df['TotalAmount'].sum():,.2f}")
                    with col3:
                        st.metric("Average Transaction", 
                                f"₹{report_df['TotalAmount'].mean():,.2f}")
                else:
                    st.info("No sales data for selected period")
        
        with tab2:
            st.subheader("Inventory Report")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Low Stock Items**")
                low_stock = db.get_low_stock_items(10)
                if not low_stock.empty:
                    st.dataframe(low_stock, use_container_width=True, hide_index=True)
                else:
                    st.success("No low stock items")
            
            with col2:
                st.markdown("**Category Inventory Value**")
                categories_df = db.get_all_categories()
                if not categories_df.empty:
                    category_values = []
                    for _, cat in categories_df.iterrows():
                        value = db.get_category_inventory_value(cat['CategoryID'])
                        category_values.append({
                            'Category': cat['CategoryName'],
                            'Inventory Value': f"₹{value:,.2f}"
                        })
                    st.dataframe(pd.DataFrame(category_values), 
                               use_container_width=True, hide_index=True)
        
        with tab3:
            st.subheader("Employee Performance")
            employees_df = db.get_all_employees()
            
            if not employees_df.empty:
                emp_performance = []
                for _, emp in employees_df.iterrows():
                    sales_total = db.get_employee_sales_total(emp['EmployeeID'])
                    emp_performance.append({
                        'Employee': f"{emp['FirstName']} {emp['LastName']}",
                        'Role': emp['Role'],
                        'Total Sales': f"₹{sales_total:,.2f}"
                    })
                
                perf_df = pd.DataFrame(emp_performance)
                st.dataframe(perf_df, use_container_width=True, hide_index=True)
            else:
                st.info("No employee data available")
