import streamlit as st
from datetime import date
from Database import con

from customers import Customers
from sales import Sales
from SalesItem import SalesItem
from products import Products

# Initialize table if they dont exist
def initialize_tables():
  try:
    Customers.create_table()
    Sales.create_table()
    SalesItem.create_table()
    Products.create_table()
    con.commit()
  except Exception as e:
    con.rollback()
    print("Error initializing tables:",e)

# Initialize tables
initialize_tables()

# App Configuration
st.set_page_config(
    page_title="Sales Management System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Title
st.title("🛒 Sales Management System")
st.markdown("---")

# Sidebar Navigation
st.sidebar.title("📋 Navigation")
st.sidebar.markdown("---")

menu_options = [
    "🏠 Dashboard",
    "👥 Manage Customers",
    "📦 Manage Products",
    "💰 Manage Sales",
    "📊 View Reports",
    "🗄️ Database Management"
]

selected_menu = st.sidebar.radio("Select a section:", menu_options)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use this sidebar to navigate between different sections of the application.")

# Main Content Area
if selected_menu == "🏠 Dashboard":
    st.header("Dashboard")
    st.write("Welcome to the Sales Management System!")
    
    col1, col2, col3 = st.columns(3)
    
    try:
        customers = Customers.get_all_customers()
        products = Products.get_all_products()
        sales = Sales.view_sales()
        
        customers_count = len(customers) if customers else 0
        products_count = len(products) if products else 0
        sales_count = len(sales) if sales else 0
    except:
        customers_count = 0
        products_count = 0
        sales_count = 0
    
    with col1:
        st.metric("Total Customers", customers_count)
    with col2:
        st.metric("Total Products", products_count)
    with col3:
        st.metric("Total Sales", sales_count)
    
elif selected_menu == "👥 Manage Customers":
    st.header("Customer Management")
    
    # Tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Customer", "✏️ Update Customer", "🗑️ Delete Customer", "📋 View All"])
    
    # Add Customer Tab
    with tab1:
        st.subheader("Add New Customer")
        with st.form("add_customer_form", clear_on_submit=True):
            name = st.text_input("Customer Name*", placeholder="Enter customer name")
            contact = st.text_input("Contact Number*", placeholder="Enter contact number")
            submit = st.form_submit_button("Add Customer")
            
            if submit:
                if name and contact:
                    try:
                        Customers.insert_customer(name, contact)
                        st.success(f"✅ Customer '{name}' added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                else:
                    st.warning("⚠️ Please fill all required fields!")
    
    # Update Customer Tab
    with tab2:
        st.subheader("Update Customer")
        customers = Customers.get_all_customers()
        
        if customers:
            customer_options = {f"ID: {c[0]} - {c[1]}": c[0] for c in customers}
            selected_customer = st.selectbox("Select Customer", list(customer_options.keys()))
            customer_id = customer_options[selected_customer]
            
            current_customer = [c for c in customers if c[0] == customer_id][0]
            
            with st.form("update_customer_form"):
                new_name = st.text_input("New Name", value=current_customer[1])
                new_contact = st.text_input("New Contact", value=current_customer[2])
                update_submit = st.form_submit_button("Update Customer")
                
                if update_submit:
                    try:
                        Customers.update_customer(customer_id, new_name, new_contact)
                        st.success(f"✅ Customer updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        else:
            st.info("No customers found. Add some customers first!")
    
    # Delete Customer Tab
    with tab3:
        st.subheader("Delete Customer")
        customers = Customers.get_all_customers()
        
        if customers:
            customer_options = {f"ID: {c[0]} - {c[1]}": c[0] for c in customers}
            selected_customer = st.selectbox("Select Customer to Delete", list(customer_options.keys()))
            customer_id = customer_options[selected_customer]
            
            if st.button("🗑️ Delete Customer", type="primary"):
                try:
                    Customers.delete_customer(customer_id)
                    st.success(f"✅ Customer deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.info("No customers found.")
    
    # View All Tab
    with tab4:
        st.subheader("All Customers")
        customers = Customers.get_all_customers()
        
        if customers:
            import pandas as pd
            df = pd.DataFrame(customers, columns=["ID", "Name", "Contact"])
            st.dataframe(df, use_container_width=True)
            st.success(f"Total Customers: {len(customers)}")
        else:
            st.info("No customers found in the database.")
    
elif selected_menu == "📦 Manage Products":
    st.header("Product Management")
    
    # Tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Product", "✏️ Update Product", "🗑️ Delete Product", "📋 View All"])
    
    # Add Product Tab
    with tab1:
        st.subheader("Add New Product")
        with st.form("add_product_form", clear_on_submit=True):
            name = st.text_input("Product Name*", placeholder="Enter product name")
            description = st.text_area("Description*", placeholder="Enter product description")
            price = st.number_input("Price*", min_value=0.0, step=0.01, format="%.2f")
            quantity = st.number_input("Quantity*", min_value=0, step=1)
            submit = st.form_submit_button("Add Product")
            
            if submit:
                if name and description and price > 0 and quantity >= 0:
                    try:
                        Products.insert_products(name, description, price, quantity)
                        st.success(f"✅ Product '{name}' added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                else:
                    st.warning("⚠️ Please fill all required fields!")
    
    # Update Product Tab
    with tab2:
        st.subheader("Update Product")
        products = Products.get_all_products()
        
        if products:
            product_options = {f"ID: {p[0]} - {p[1]}": p[0] for p in products}
            selected_product = st.selectbox("Select Product", list(product_options.keys()))
            product_id = product_options[selected_product]
            
            current_product = [p for p in products if p[0] == product_id][0]
            
            with st.form("update_product_form"):
                new_name = st.text_input("Product Name", value=current_product[1])
                new_description = st.text_area("Description", value=current_product[2])
                new_price = st.number_input("Price", value=float(current_product[3]), step=0.01, format="%.2f")
                new_quantity = st.number_input("Quantity", value=int(current_product[4]), step=1)
                update_submit = st.form_submit_button("Update Product")
                
                if update_submit:
                    try:
                        Products.update_products(product_id, new_name, new_description, new_price, new_quantity)
                        st.success(f"✅ Product updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        else:
            st.info("No products found. Add some products first!")
    
    # Delete Product Tab
    with tab3:
        st.subheader("Delete Product")
        products = Products.get_all_products()
        
        if products:
            product_options = {f"ID: {p[0]} - {p[1]}": p[0] for p in products}
            selected_product = st.selectbox("Select Product to Delete", list(product_options.keys()))
            product_id = product_options[selected_product]
            
            if st.button("🗑️ Delete Product", type="primary"):
                try:
                    Products.delete_products(product_id)
                    st.success(f"✅ Product deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.info("No products found.")
    
    # View All Tab
    with tab4:
        st.subheader("All Products")
        products = Products.get_all_products()
        
        if products:
            import pandas as pd
            df = pd.DataFrame(products, columns=["ID", "Name", "Description", "Price", "Quantity"])
            st.dataframe(df, use_container_width=True)
            st.success(f"Total Products: {len(products)}")
        else:
            st.info("No products found in the database.")
    
elif selected_menu == "💰 Manage Sales":
    st.header("Sales Management")
    
    # Tabs for different operations
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "➕ Insert Sale", 
        "📝 Insert Sale Items",
        "✏️ Update Sale", 
        "🗑️ Delete Sale", 
        "📋 View All Sales",
        "🛒 View Sale Items"
    ])
    
    # Insert Sale Tab
    with tab1:
        st.subheader("Insert New Sale")
        with st.form("add_sale_form", clear_on_submit=True):
            customers = Customers.get_all_customers()
            if customers:
                customer_options = {f"{c[1]} (ID: {c[0]})": c[0] for c in customers}
                selected_customer = st.selectbox("Customer*", list(customer_options.keys()))
                customer_id = customer_options[selected_customer]
            else:
                st.warning("⚠️ No customers available. Please add customers first!")
                customer_id = None
            
            sale_date = st.date_input("Sale Date*", value=date.today())
            total_amount = st.number_input("Total Amount*", min_value=0.0, step=0.01, format="%.2f")
            submit = st.form_submit_button("💾 Insert Sale")
            
            if submit:
                if customer_id and total_amount > 0:
                    try:
                        Sales.insert_sale(customer_id, sale_date, total_amount)
                        st.success(f"✅ Sale inserted successfully!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                else:
                    st.warning("⚠️ Please fill all required fields!")
    
    # Insert Sale Items Tab
    with tab2:
        st.subheader("Insert Sale Items")
        st.write("Add individual items to a sale transaction")
        
        with st.form("add_sale_item_form", clear_on_submit=True):
            # Select Sale
            sales = Sales.view_sales()
            if sales:
                sale_options = {f"Sale ID: {s[0]} - Customer: {s[1]} - Date: {s[2]}": s[0] for s in sales}
                selected_sale = st.selectbox("Select Sale*", list(sale_options.keys()))
                sale_id = sale_options[selected_sale]
            else:
                st.warning("⚠️ No sales available. Please insert a sale first!")
                sale_id = None
            
            # Select Product
            products = Products.get_all_products()
            if products:
                product_options = {f"{p[1]} (ID: {p[0]}) - Stock: {p[4]} - Price: ${p[3]}": p[0] for p in products}
                selected_product = st.selectbox("Select Product*", list(product_options.keys()))
                product_id = product_options[selected_product]
                
                # Get selected product price
                selected_product_data = [p for p in products if p[0] == product_id][0]
                product_price = float(selected_product_data[3])
            else:
                st.warning("⚠️ No products available. Please add products first!")
                product_id = None
                product_price = 0.0
            
            quantity = st.number_input("Quantity*", min_value=1, step=1, value=1)
            price = st.number_input("Price*", min_value=0.01, step=0.01, format="%.2f", value=product_price)
            
            submit_item = st.form_submit_button("💾 Insert Sale Item")
            
            if submit_item:
                if sale_id and product_id and quantity > 0 and price > 0:
                    try:
                        cur = con.cursor()
                        cur.execute(
                            """INSERT INTO salesitem(sale_id, product_id, quantity, price) 
                               VALUES(%s, %s, %s, %s)""",
                            (sale_id, product_id, quantity, price)
                        )
                        con.commit()
                        cur.close()
                        st.success(f"✅ Sale item inserted successfully!")
                        st.info(f"Total: ${quantity * price:.2f}")
                        st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"❌ Error: {e}")
                else:
                    st.warning("⚠️ Please fill all required fields!")
    
    # Update Sale Tab
    with tab3:
        st.subheader("Update Sale")
        sales = Sales.view_sales()
        
        if sales:
            sale_options = {f"Sale ID: {s[0]} - Customer: {s[1]} - Amount: ${s[3]}": s[0] for s in sales}
            selected_sale = st.selectbox("Select Sale", list(sale_options.keys()))
            sale_id = sale_options[selected_sale]
            
            current_sale = [s for s in sales if s[0] == sale_id][0]
            
            with st.form("update_sale_form"):
                customers = Customers.get_all_customers()
                customer_options = {f"{c[1]} (ID: {c[0]})": c[0] for c in customers}
                current_customer = f"Customer ID: {current_sale[1]}"
                selected_customer = st.selectbox("Customer", list(customer_options.keys()))
                new_customer_id = customer_options[selected_customer]
                
                new_date = st.date_input("Sale Date", value=current_sale[2])
                new_total = st.number_input("Total Amount", value=float(current_sale[3]), step=0.01, format="%.2f")
                update_submit = st.form_submit_button("Update Sale")
                
                if update_submit:
                    try:
                        Sales.update_sale(sale_id, new_customer_id, new_date, new_total)
                        st.success(f"✅ Sale updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        else:
            st.info("No sales found. Record some sales first!")
    
    # Delete Sale Tab
    with tab4:
        st.subheader("Delete Sale")
        sales = Sales.view_sales()
        
        if sales:
            sale_options = {f"Sale ID: {s[0]} - Customer: {s[1]} - Amount: ${s[3]}": s[0] for s in sales}
            selected_sale = st.selectbox("Select Sale to Delete", list(sale_options.keys()))
            sale_id = sale_options[selected_sale]
            
            if st.button("🗑️ Delete Sale", type="primary"):
                try:
                    Sales.delete_sale(sale_id)
                    st.success(f"✅ Sale deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.info("No sales found.")
    
    # View All Sales Tab
    with tab5:
        st.subheader("All Sales")
        sales = Sales.view_sales()
        
        if sales:
            import pandas as pd
            df = pd.DataFrame(sales, columns=["ID", "Customer ID", "Date", "Total Amount"])
            st.dataframe(df, use_container_width=True)
            st.success(f"Total Sales: {len(sales)}")
            st.metric("Total Revenue", f"${sum([s[3] for s in sales]):.2f}")
        else:
            st.info("No sales found in the database.")
    
    # View Sale Items Tab
    with tab6:
        st.subheader("All Sale Items")
        
        try:
            cur = con.cursor()
            cur.execute("""
                SELECT si.id, si.sale_id, si.product_id, p.name, si.quantity, si.price, 
                       (si.quantity * si.price) as total
                FROM salesitem si
                LEFT JOIN products p ON si.product_id = p.id
                ORDER BY si.id DESC
            """)
            sale_items = cur.fetchall()
            cur.close()
            
            if sale_items:
                import pandas as pd
                df = pd.DataFrame(sale_items, columns=[
                    "Item ID", "Sale ID", "Product ID", "Product Name", 
                    "Quantity", "Price", "Total"
                ])
                st.dataframe(df, use_container_width=True)
                st.success(f"Total Sale Items: {len(sale_items)}")
                
                # Summary
                col1, col2 = st.columns(2)
                with col1:
                    total_items = sum([item[4] for item in sale_items])
                    st.metric("Total Items Sold", total_items)
                with col2:
                    total_value = sum([item[6] for item in sale_items])
                    st.metric("Total Value", f"${total_value:.2f}")
            else:
                st.info("No sale items found. Insert some sale items first!")
        except Exception as e:
            st.error(f"❌ Error loading sale items: {e}")
    
elif selected_menu == "📊 View Reports":
    st.header("Reports & Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📊 Sales Summary", "📈 Sales by Date Range", "🏆 Top Products"])
    
    # Sales Summary
    with tab1:
        st.subheader("Sales Summary")
        col1, col2, col3 = st.columns(3)
        
        try:
            customers = Customers.get_all_customers()
            products = Products.get_all_products()
            sales = Sales.view_sales()
            
            with col1:
                st.metric("Total Customers", len(customers) if customers else 0)
            with col2:
                st.metric("Total Products", len(products) if products else 0)
            with col3:
                st.metric("Total Sales", len(sales) if sales else 0)
            
            if sales:
                total_revenue = sum([s[3] for s in sales])
                avg_sale = total_revenue / len(sales)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Revenue", f"${total_revenue:.2f}")
                with col2:
                    st.metric("Average Sale", f"${avg_sale:.2f}")
                
                # Recent Sales
                st.subheader("Recent Sales")
                import pandas as pd
                df = pd.DataFrame(sales[-10:], columns=["ID", "Customer ID", "Date", "Total Amount"])
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading summary: {e}")
    
    # Sales by Date Range
    with tab2:
        st.subheader("Sales by Date Range")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date.today())
        with col2:
            end_date = st.date_input("End Date", value=date.today())
        
        if st.button("Generate Report"):
            try:
                total = Sales.total_sales_by_date(start_date, end_date)
                if total:
                    st.success(f"Total Sales: ${total:.2f}")
                else:
                    st.info("No sales found in this date range.")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Top Products
    with tab3:
        st.subheader("Top Selling Products")
        
        try:
            top_products = Sales.top_selling_products()
            if top_products:
                import pandas as pd
                df = pd.DataFrame(top_products, columns=["Product ID", "Total Quantity"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No sales data available yet.")
        except Exception as e:
            st.error(f"Error: {e}")

elif selected_menu == "🗄️ Database Management":
    st.header("Database Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Create Tables", "🔍 View Table Data", "📊 Table Info", "🔧 Operations"])
    
    # Create Tables Tab
    with tab1:
        st.subheader("Initialize Database Tables")
        st.write("Create all required tables in the database.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 Create Customers Table", use_container_width=True):
                try:
                    Customers.create_table()
                    st.success("✅ Customers table created successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            
            if st.button("📦 Create Products Table", use_container_width=True):
                try:
                    Products.create_table()
                    st.success("✅ Products table created successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        with col2:
            if st.button("💰 Create Sales Table", use_container_width=True):
                try:
                    Sales.create_table()
                    st.success("✅ Sales table created successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            
            if st.button("📝 Create SalesItem Table", use_container_width=True):
                try:
                    SalesItem.create_table()
                    st.success("✅ SalesItem table created successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        st.markdown("---")
        if st.button("🚀 Create All Tables", type="primary", use_container_width=True):
            try:
                Customers.create_table()
                Products.create_table()
                Sales.create_table()
                SalesItem.create_table()
                st.success("✅ All tables created successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # View Table Data Tab
    with tab2:
        st.subheader("View Table Data")
        
        table_selection = st.selectbox("Select Table", ["Customers", "Products", "Sales", "SalesItem"])
        
        if st.button("📊 Load Data"):
            try:
                import pandas as pd
                
                if table_selection == "Customers":
                    data = Customers.get_all_customers()
                    if data:
                        df = pd.DataFrame(data, columns=["ID", "Name", "Contact"])
                        st.dataframe(df, use_container_width=True)
                        st.info(f"Total Records: {len(data)}")
                    else:
                        st.warning("No data found in Customers table")
                
                elif table_selection == "Products":
                    data = Products.get_all_products()
                    if data:
                        df = pd.DataFrame(data, columns=["ID", "Name", "Description", "Price", "Quantity"])
                        st.dataframe(df, use_container_width=True)
                        st.info(f"Total Records: {len(data)}")
                    else:
                        st.warning("No data found in Products table")
                
                elif table_selection == "Sales":
                    data = Sales.view_sales()
                    if data:
                        df = pd.DataFrame(data, columns=["ID", "Customer ID", "Date", "Total Amount"])
                        st.dataframe(df, use_container_width=True)
                        st.info(f"Total Records: {len(data)}")
                    else:
                        st.warning("No data found in Sales table")
                
                elif table_selection == "SalesItem":
                    cur = con.cursor()
                    cur.execute("SELECT * FROM salesitem")
                    data = cur.fetchall()
                    cur.close()
                    if data:
                        df = pd.DataFrame(data, columns=["ID", "Sale ID", "Product ID", "Quantity", "Price"])
                        st.dataframe(df, use_container_width=True)
                        st.info(f"Total Records: {len(data)}")
                    else:
                        st.warning("No data found in SalesItem table")
                
            except Exception as e:
                st.error(f"❌ Error loading data: {e}")
    
    # Table Info Tab
    with tab3:
        st.subheader("Table Structure Information")
        
        st.markdown("""
        ### 📋 Customers Table
        - **ID**: Serial Primary Key (Auto-increment)
        - **Name**: VARCHAR(100) - Customer name
        - **Contact**: VARCHAR(15) - Contact number
        
        ### 📦 Products Table
        - **ID**: Serial Primary Key (Auto-increment)
        - **Name**: VARCHAR(50) - Product name
        - **Description**: TEXT - Product description
        - **Price**: DECIMAL(10,2) - Product price
        - **Quantity**: INTEGER - Stock quantity
        
        ### 💰 Sales Table
        - **ID**: Serial Primary Key (Auto-increment)
        - **Customer ID**: INTEGER - References Customers(id)
        - **Date**: DATE - Sale date
        - **Total Amount**: DECIMAL(10,2) - Total sale amount
        - **Foreign Key**: customer_id → Customers(id) ON DELETE CASCADE
        
        ### 📝 SalesItem Table
        - **ID**: Serial Primary Key (Auto-increment)
        - **Sale ID**: INTEGER - References Sales(id)
        - **Product ID**: INTEGER - References Products(id)
        - **Quantity**: INTEGER - Quantity sold
        - **Price**: DECIMAL(10,2) - Price at time of sale
        - **Foreign Keys**: 
          - sale_id → Sales(id) ON DELETE CASCADE
          - product_id → Products(id) ON DELETE CASCADE
        """)
    
    # Operations Tab
    with tab4:
        st.subheader("Available Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 👥 Customers Operations
            - ➕ **Create** - Add new customer
            - 📖 **Read** - View all customers
            - ✏️ **Update** - Modify customer details
            - 🗑️ **Delete** - Remove customer
            
            ### 📦 Products Operations
            - ➕ **Create** - Add new product
            - 📖 **Read** - View all products
            - ✏️ **Update** - Modify product details
            - 🗑️ **Delete** - Remove product
            """)
        
        with col2:
            st.markdown("""
            ### 💰 Sales Operations
            - ➕ **Create** - Record new sale
            - 📖 **Read** - View all sales
            - ✏️ **Update** - Modify sale details
            - 🗑️ **Delete** - Remove sale
            
            ### 📊 Reports Operations
            - 📈 Sales by date range
            - 🏆 Top selling products
            - 💹 Total revenue calculation
            """)
        
        st.markdown("---")
        st.info("💡 All operations are available through the respective management sections in the sidebar.")

