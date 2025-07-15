import tkinter as tk
from tkinter import ttk, messagebox
from ManageXml import XMLHandler
from datetime import datetime

# Global variable to store selected customer ID from MyCustomers
selected_customer_id = None

class MyCustomers:
    def __init__(self):
        self.xml_handler = XMLHandler(file_name=r"C:\EXER9DRAFT\database.xml")
        self.style_config = {
            "bg": "#f0f0f0",
            "btn_bg": "#4CAF50",
            "btn_fg": "white",
            "header_bg": "#e0e0e0",
            "selected_row_bg": "#d3e4cd",
            "font": ("Courier", 10),
            "header_font": ("Courier", 10, "bold"),
            "title_font": ("Courier", 12, "bold"),
        }
        self.product_window = None
        self.supplier_window = None
        self.product_form = None
        self.selected_row = None
        self.selected_order_row = None
        self.selected_prod_id = None
        self.cached_orders = None
        self.current_prod_id_order = []  # Track current table composite key order
        self.setup_ui()

    def setup_ui(self):
        self.MyWindow = tk.Tk()
        self.MyWindow.title("Customer Form")
        self.MyWindow.geometry("1000x600")
        self.MyWindow.resizable(True, True)
        self.MyWindow.configure(bg=self.style_config["bg"])
        self.MyWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        menubar = tk.Menu(self.MyWindow)
        self.MyWindow.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Products", command=self.open_products_form)
        file_menu.add_command(label="Open Suppliers", command=self.open_suppliers_form)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        label = tk.Label(
            self.MyWindow,
            text="Customer System",
            height=1,
            bg=self.style_config["header_bg"],
            anchor="center",
            font=self.style_config["title_font"],
        )
        label.grid(column=0, row=0, columnspan=3, pady=10, sticky="n")

        self.form_frame = tk.Frame(self.MyWindow, bg=self.style_config["bg"])
        self.form_frame.grid(column=0, row=1, padx=20, pady=10, sticky="w")

        labels = ["ID", "Name", "Address", "Contact", "Email", "Birthday", "Gender"]
        self.text_vars = []
        self.entry_widgets = []
        i = 0
        for text in labels:
            lbl = tk.Label(
                self.form_frame,
                text=text,
                height=1,
                bg=self.style_config["header_bg"],
                anchor="w",
                font=self.style_config["font"],
            )
            lbl.grid(column=0, row=i, padx=10, pady=5, sticky="w")
            var = tk.StringVar()
            self.text_vars.append(var)
            entry = tk.Entry(
                self.form_frame,
                textvariable=var,
                width=30,
                state="readonly" if text == "ID" else "normal",
                font=self.style_config["font"],
            )
            entry.grid(column=1, row=i, pady=5, padx=10)
            self.entry_widgets.append(entry)
            i = i + 1

        self.btn_frame = tk.Frame(self.form_frame, bg=self.style_config["bg"])
        self.btn_frame.grid(column=0, row=len(labels), columnspan=2, pady=10)

        buttons = [
            ("Save", self.save_customer),
            ("Edit", self.edit_customer),
            ("Delete", self.delete_selected_customer),
            ("Add Order", self.add_order),
            ("Delete Order", self.delete_order),
        ]
        i = 0
        for button_info in buttons:
            text = button_info[0]
            command = button_info[1]
            btn = tk.Button(
                self.btn_frame,
                text=text,
                bg=self.style_config["btn_bg"],
                fg=self.style_config["btn_fg"],
                width=10,
                height=1,
                command=command,
                font=self.style_config["font"],
            )
            btn.grid(column=i, row=0, pady=5, padx=5, sticky="w")
            i = i + 1

        self.output_frame = tk.Frame(self.MyWindow, bg=self.style_config["bg"])
        self.output_frame.grid(column=1, row=1, padx=20, pady=10, sticky="nsew")
        i = 0
        while i < 8:
            self.output_frame.grid_columnconfigure(i, weight=1)
            i = i + 1
        i = 0
        while i < 20:
            self.output_frame.grid_rowconfigure(i, weight=1)
            i = i + 1

        self.fields = ["ID", "Name", "Address", "Contact", "Email", "Birthday", "Gender"]
        self.OrderFields = ["ProdID", "Product Type", "Product Description", "Quantity", "Unit Price", "Total Price", "Date Received", "Orders"]
        self.table_entry_widgets = []
        self.order_entry_widgets = []
        self.order_prod_ids = []
        self.order_order_ids = []

        self.load_customers()

    def load_customers(self):
        for widget in self.output_frame.winfo_children():
            if int(widget.grid_info().get("row", 0)) <= len(self.customers) + 1:
                widget.destroy()
        self.table_entry_widgets = []

        i = 0
        for field in self.fields:
            header = tk.Label(
                self.output_frame,
                text=field,
                bg=self.style_config["header_bg"],
                font=self.style_config["header_font"],
                borderwidth=1,
                relief="solid",
                width=12,
            )
            header.grid(row=0, column=i, padx=1, pady=1, sticky="nsew")
            i = i + 1

        self.customers = self.xml_handler.get_all_customers()
        print(f"Loaded customers: {[customer['ID'] for customer in self.customers]}")
        row_index = 1
        for customer in self.customers:
            row_entries = []
            col_index = 0
            for field in self.fields:
                var = tk.StringVar(value=customer.get(field, ""))
                entry = tk.Entry(
                    self.output_frame,
                    textvariable=var,
                    state="readonly",
                    width=12,
                    borderwidth=1,
                    relief="solid",
                    font=self.style_config["font"],
                    bg=self.style_config["selected_row_bg"] if self.selected_row == row_index-1 else "white",
                    cursor="hand2",
                )
                entry.grid(row=row_index, column=col_index, padx=1, pady=1, sticky="nsew")
                entry.bind("<Button-1>", lambda e, r=row_index-1: self.on_entry_select(r))
                row_entries.append(entry)
                col_index = col_index + 1
            self.table_entry_widgets.append(row_entries)
            row_index = row_index + 1

        if self.selected_row is not None and 0 <= self.selected_row < len(self.customers):
            self.load_orders(len(self.customers) + 2)
        else:
            self.clear_orders(len(self.customers) + 2)

    def clear_orders(self, start_row):
        for widget in self.output_frame.grid_slaves():
            if int(widget.grid_info()["row"]) >= start_row:
                widget.destroy()
        self.order_entry_widgets = []
        self.order_prod_ids = []
        self.order_order_ids = []

    def load_orders(self, start_row):
        self.clear_orders(start_row)
        self.order_entry_widgets = []
        self.order_prod_ids = []
        self.order_order_ids = []

        if self.cached_orders is None:
            self.cached_orders = self.xml_handler.get_all_orders()
        orders = self.cached_orders

        customer_id = None
        if self.selected_row is not None and 0 <= self.selected_row < len(self.customers):
            customer_id = self.customers[self.selected_row]["ID"]
            filtered_orders = []
            for order in orders:
                if order.get("CustomerID") == customer_id:
                    filtered_orders.append(order)
            orders = filtered_orders
        else:
            orders = []

        print(f"Loaded orders for customer {customer_id if customer_id else 'none'}: {[order['OrderID'] for order in orders]}")

        # Aggregate orders by composite key (prodID, Product Type, Product Description)
        product_orders = {}
        for order in orders:
            prod_id = order.get("prodID", "")
            product_type = order.get("Product Type", "")
            product_desc = order.get("Product Description", "")
            if not prod_id:
                print(f"Warning: Order {order['OrderID']} has no prodID, skipping")
                continue
            composite_key = (prod_id, product_type, product_desc)
            if composite_key not in product_orders:
                product_orders[composite_key] = {
                    "ProdID": prod_id,
                    "Product Type": product_type,
                    "Product Description": product_desc,
                    "Quantity": 0,
                    "Unit Price": order.get("Unit Price", "0"),
                    "Date Received": order.get("Date Received", ""),
                    "OrderIDs": [],
                }
            quantity = int(order.get("Quantity", "0") or "0")
            product_orders[composite_key]["Quantity"] = product_orders[composite_key]["Quantity"] + quantity
            product_orders[composite_key]["Unit Price"] = order.get("Unit Price", "0")
            product_orders[composite_key]["Date Received"] = order.get("Date Received", "")
            order_id = order.get("OrderID", "")
            if order_id:
                product_orders[composite_key]["OrderIDs"].append(order_id)

        # Maintain order of products in the table
        self.current_prod_id_order = []
        for key in product_orders:
            self.current_prod_id_order.append(key)
        print(f"Product order: {self.current_prod_id_order}")

        # Create table headers
        col_index = 0
        for field in self.OrderFields:
            header = tk.Label(
                self.output_frame,
                text=field,
                bg=self.style_config["header_bg"],
                font=self.style_config["header_font"],
                borderwidth=1,
                relief="solid",
                width=12,
            )
            header.grid(row=start_row, column=col_index, padx=1, pady=1, sticky="nsew")
            col_index = col_index + 1

        # Populate table rows
        row_index = start_row + 1
        for composite_key in self.current_prod_id_order:
            product = product_orders[composite_key]
            total_price = int(product["Quantity"]) * int(product["Unit Price"] or "0")
            row_entries = []
            col_index = 0
            for field in self.OrderFields:
                if field == "Quantity":
                    value = str(product["Quantity"])
                elif field == "Total Price":
                    value = str(total_price)
                elif field == "Orders":
                    value = str(len(product["OrderIDs"]))
                else:
                    value = product.get(field, "")
                var = tk.StringVar(value=value)
                entry = tk.Entry(
                    self.output_frame,
                    textvariable=var,
                    state="readonly",
                    width=12,
                    borderwidth=1,
                    relief="solid",
                    font=self.style_config["font"],
                    bg=self.style_config["selected_row_bg"] if composite_key == self.selected_prod_id else "white",
                    cursor="hand2",
                )
                entry.grid(row=row_index, column=col_index, padx=1, pady=1, sticky="nsew")
                entry.bind("<Button-1>", lambda e, r=row_index-(start_row+1), key=composite_key: self.on_order_select(r, key))
                row_entries.append(entry)
                col_index = col_index + 1
            self.order_entry_widgets.append(row_entries)
            self.order_prod_ids.append(composite_key)
            self.order_order_ids.append(product["OrderIDs"][:])
            print(f"Row {row_index-(start_row+1)}: CompositeKey={composite_key}, OrderIDs={product['OrderIDs']}, Quantity={product['Quantity']}")
            row_index = row_index + 1

    def on_entry_select(self, row):
        global selected_customer_id
        if 0 <= row < len(self.customers):
            customer = self.customers[row]
            i = 0
            for field in self.fields:
                self.text_vars[i].set(customer.get(field, ""))
                i = i + 1
            self.selected_row = row
            self.selected_order_row = None
            self.selected_prod_id = None
            selected_customer_id = customer["ID"]
            self.load_customers()

    def on_order_select(self, row, composite_key):
        print(f"Selected order row: {row}, CompositeKey={composite_key}")
        self.selected_order_row = row
        self.selected_prod_id = composite_key
        i = 0
        for row_entries in self.order_entry_widgets:
            bg = self.style_config["selected_row_bg"] if i == row else "white"
            for entry in row_entries:
                entry.configure(bg=bg)
            i = i + 1

    def add_order(self):
        global selected_customer_id
        if self.selected_row is None:
            messagebox.showwarning("Warning", "Please select a customer first!")
            return

        if not self.product_form or not self.product_window or not self.product_window.winfo_exists():
            self.open_products_form()
            messagebox.showwarning("Warning", "Product Form opened. Please select a product and batch.")
            return

        if self.product_form.selected_row is None or self.product_form.selected_batch_row is None:
            messagebox.showwarning("Warning", "Please select a product and batch in the Product Form!")
            return

        product_data = self.product_form.get_selected_product_data()
        if not product_data:
            messagebox.showerror("Error", "Failed to retrieve product data!")
            return

        customer_id = self.customers[self.selected_row]["ID"]
        prod_id = product_data["ProdID"]
        product_type = product_data["Product Type"]
        product_desc = product_data["Product Description"]

        if self.cached_orders is None:
            self.cached_orders = self.xml_handler.get_all_orders()
        customer_orders = []
        for order in self.cached_orders:
            if (order.get("CustomerID") == customer_id and
                order.get("prodID") == prod_id and
                order.get("Product Type") == product_type and
                order.get("Product Description") == product_desc):
                customer_orders.append(order)
        if len(customer_orders) >= 10:
            messagebox.showwarning("Warning", "Maximum order limit of 10 reached for this product!")
            return

        batch_quantity_str = self.product_form.products[self.product_form.selected_row]["Table2Entries"][self.product_form.selected_batch_row].get("Quantity", "0") or "0"
        if not self.product_form.is_valid_integer(batch_quantity_str):
            messagebox.showerror("Error", "Invalid quantity in selected batch!")
            return
        batch_quantity = int(batch_quantity_str)

        if batch_quantity <= 0:
            messagebox.showinfo("Out of Stock", "Product out of stock!")
            return

        selected_batch = self.product_form.products[self.product_form.selected_row]["Table2Entries"][self.product_form.selected_batch_row]
        unit_cost = int(selected_batch.get("Unit Cost", "0") or "0")
        costs = self.xml_handler.get_costs()
        labor_cost = int(costs.get("Labor Cost", "0") or "0")
        overhead_cost = int(costs.get("Overhead Cost", "0") or "0")
        desired_profit = int(costs.get("Desired Profit", "0") or "0")
        unit_price = unit_cost + labor_cost + overhead_cost + desired_profit

        order_data = {
            "CustomerID": customer_id,
            "prodID": prod_id,
            "Product Type": product_type,
            "Product Description": product_desc,
            "Quantity": "1",
            "Unit Price": str(unit_price),
            "Total Price": str(unit_price),
            "Date Received": datetime.now().strftime("%Y-%m-%d"),
        }

        order_id = self.xml_handler.add_order(order_data)
        if order_id:
            product_id = self.product_form.products[self.product_form.selected_row]["ID"]
            batch_number = selected_batch.get("BatchNumber", "")
            new_quantity = batch_quantity - 1
            self.xml_handler.update_batch_quantity(product_id, batch_number, new_quantity)
            selected_batch["Quantity"] = str(new_quantity)
            
            self.cached_orders = None
            self.load_customers()
            self.product_form.load_products()
            messagebox.showinfo("Success", f"Order added with ID: {order_id} for Customer ID: {customer_id}")
        else:
            messagebox.showerror("Error", "Failed to add order")

    def delete_order(self):
        if self.selected_row is None:
            messagebox.showwarning("Warning", "Please select a customer!")
            return

        if self.selected_order_row is None or self.selected_prod_id is None or self.selected_order_row >= len(self.order_prod_ids):
            messagebox.showwarning("Warning", "Please select an order to delete!")
            return

        if not self.product_form or not self.product_window or not self.product_window.winfo_exists():
            messagebox.showwarning("Warning", "Product Form must be open to delete an order!")
            return

        customer_id = self.customers[self.selected_row]["ID"]
        composite_key = self.selected_prod_id
        prod_id = composite_key[0]
        product_type = composite_key[1]
        product_desc = composite_key[2]

        if self.cached_orders is None:
            self.cached_orders = self.xml_handler.get_all_orders()
        orders = []
        for order in self.cached_orders:
            if (order.get("CustomerID") == customer_id and
                order.get("prodID") == prod_id and
                order.get("Product Type") == product_type and
                order.get("Product Description") == product_desc):
                orders.append(order)

        if not orders:
            messagebox.showwarning("Warning", "No orders remain for this product!")
            self.selected_order_row = None
            self.selected_prod_id = None
            self.load_customers()
            return

        # Find the order to reduce (most recent by Date Received)
        order_to_reduce = None
        latest_date = "1970-01-01"
        for order in orders:
            date_received = order.get("Date Received", "1970-01-01")
            if datetime.strptime(date_received, "%Y-%m-%d") > datetime.strptime(latest_date, "%Y-%m-%d"):
                latest_date = date_received
                order_to_reduce = order
        if not order_to_reduce:
            messagebox.showerror("Error", "No valid order found to reduce!")
            return

        order_id = order_to_reduce.get("OrderID", "")
        current_qty = int(order_to_reduce.get("Quantity", "1") or "1")
        quantity_change = 1  # Increment the batch quantity when reducing

        # Reduce the order quantity
        new_qty = current_qty - 1
        unit_price = int(order_to_reduce.get("Unit Price", "0") or "0")
        new_total_price = new_qty * unit_price
        order_to_reduce["Quantity"] = str(new_qty)
        order_to_reduce["Total Price"] = str(new_total_price)

        # Update the UI
        qty_index = 0
        for field in self.OrderFields:
            if field == "Quantity":
                break
            qty_index = qty_index + 1
        self.order_entry_widgets[self.selected_order_row][qty_index].config(state="normal")
        self.order_entry_widgets[self.selected_order_row][qty_index].delete(0, tk.END)
        self.order_entry_widgets[self.selected_order_row][qty_index].insert(0, str(new_qty))
        self.order_entry_widgets[self.selected_order_row][qty_index].config(state="readonly")

        total_price_index = 0
        for field in self.OrderFields:
            if field == "Total Price":
                break
            total_price_index = total_price_index + 1
        self.order_entry_widgets[self.selected_order_row][total_price_index].config(state="normal")
        self.order_entry_widgets[self.selected_order_row][total_price_index].delete(0, tk.END)
        self.order_entry_widgets[self.selected_order_row][total_price_index].insert(0, str(new_total_price))
        self.order_entry_widgets[self.selected_order_row][total_price_index].config(state="readonly")

        # If quantity is now 0, remove the order
        if new_qty == 0:
            self.cached_orders = [order for order in self.cached_orders if order != order_to_reduce]
            for entry in self.order_entry_widgets[self.selected_order_row]:
                entry.destroy()
            self.order_entry_widgets.pop(self.selected_order_row)
            self.order_prod_ids.pop(self.selected_order_row)
            self.order_order_ids.pop(self.selected_order_row)
            self.current_prod_id_order = [key for key in self.current_prod_id_order if key != composite_key]
            self.xml_handler.delete_order(order_id)

        # Find the corresponding batch in MyProducts to update its quantity
        product = None
        batch = None
        for p in self.product_form.products:
            if (p.get("Product Type") == product_type and
                p.get("Product Description") == product_desc):
                for b in p["Table2Entries"]:
                    if (b.get("ProdID") == prod_id and
                        b.get("Product Type", product_type) == product_type and
                        b.get("Product Description", product_desc) == product_desc):
                        product = p
                        batch = b
                        break
                if batch:
                    break
        if product and batch:
            current_batch_qty = int(batch.get("Quantity", "0") or "0")
            new_batch_qty = current_batch_qty + quantity_change
            batch["Quantity"] = str(new_batch_qty)
            product_id = product["ID"]
            batch_number = batch.get("BatchNumber", "")
            print(f"Updating batch: ProductID={product_id}, BatchNumber={batch_number}, ProdID={prod_id}, Old Quantity={current_batch_qty}, New Quantity={new_batch_qty}")
            if self.xml_handler.update_batch_quantity(product_id, batch_number, new_batch_qty):
                print(f"Batch quantity updated successfully in XML")
            else:
                print(f"Warning: Failed to update batch quantity in XML")
            # Update MyProducts UI
            self.product_form.products = self.xml_handler.get_all_products()  # Force reload from XML
            self.product_form.load_products()
            # Find the updated product in MyProducts
            updated_product = None
            for p in self.product_form.products:
                if p["ID"] == product_id:
                    updated_product = p
                    break
            if updated_product:
                self.product_form.refresh_table2(updated_product)
            else:
                print(f"Warning: Product ID {product_id} not found in MyProducts after update")
        else:
            print(f"Warning: No matching batch found for ProdID={prod_id}, Product Type={product_type}, Product Description={product_desc}")

        # Update XML if quantity is not 0
        if new_qty > 0:
            order_data = {
                "CustomerID": customer_id,
                "prodID": prod_id,
                "Product Type": product_type,
                "Product Description": product_desc,
                "Quantity": str(new_qty),
                "Unit Price": str(unit_price),
                "Total Price": str(new_total_price),
                "Date Received": order_to_reduce.get("Date Received", ""),
            }
            if self.xml_handler.update_order(order_id, order_data):
                print(f"Order ID={order_id} updated successfully in XML")
            else:
                print(f"Warning: Failed to update Order ID={order_id} in XML")

        # Refresh UI
        self.load_customers()
        self.selected_order_row = None
        self.selected_prod_id = None

        messagebox.showinfo("Success", "Order quantity reduced!")

    def save_customer(self):
        customer_data = {
            "Name": self.text_vars[1].get(),
            "Address": self.text_vars[2].get(),
            "Contact": self.text_vars[3].get(),
            "Email": self.text_vars[4].get(),
            "Birthday": self.text_vars[5].get(),
            "Gender": self.text_vars[6].get(),
        }
        new_id = self.xml_handler.add_customer(customer_data)
        if new_id is not None:
            self.text_vars[0].set(new_id)
            self.cached_orders = None
            messagebox.showinfo("Success", f"Customer added with ID: {new_id}")
            self.load_customers()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to add customer")

    def edit_customer(self):
        if self.selected_row is None or self.selected_row >= len(self.customers):
            messagebox.showwarning("Warning", "Please select a customer to edit!")
            return
        customer_id = self.customers[self.selected_row]["ID"]
        customer_data = {
            "Name": self.text_vars[1].get(),
            "Address": self.text_vars[2].get(),
            "Contact": self.text_vars[3].get(),
            "Email": self.text_vars[4].get(),
            "Birthday": self.text_vars[5].get(),
            "Gender": self.text_vars[6].get(),
        }
        if self.xml_handler.update_customer(customer_id, customer_data):
            messagebox.showinfo("Success", f"Customer ID: {customer_id} updated successfully!")
            self.load_customers()
        else:
            messagebox.showerror("Error", "Failed to update customer")

    def delete_selected_customer(self):
        if self.selected_row is None or self.selected_row >= len(self.customers):
            messagebox.showwarning("Warning", "Please select a customer to delete!")
            return
        customer_id = self.customers[self.selected_row]["ID"]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?"):
            if self.xml_handler.delete_customer(customer_id):
                messagebox.showinfo("Success", "Customer deleted successfully!")
                self.load_customers()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to delete customer")

    def open_products_form(self):
        from Products import MyProducts
        if self.product_form is None or not self.product_window or not self.product_window.winfo_exists():
            self.product_window = tk.Toplevel(self.MyWindow)
            self.product_form = MyProducts(self.product_window)
        else:
            self.product_window.lift()

    def open_suppliers_form(self):
        from Suppliers import MySuppliers
        if self.supplier_window is None or not self.supplier_window.winfo_exists():
            self.supplier_window = tk.Toplevel(self.MyWindow)
            MySuppliers(self.supplier_window)
        else:
            self.supplier_window.lift()

    def clear_form(self):
        for var in self.text_vars:
            var.set("")
        self.selected_row = None
        self.selected_order_row = None
        self.selected_prod_id = None

    def on_closing(self):
        if self.product_window and self.product_window.winfo_exists():
            self.product_window.destroy()
        if self.supplier_window and self.supplier_window.winfo_exists():
            self.supplier_window.destroy()
        self.MyWindow.destroy()

    def run(self):
        self.MyWindow.mainloop()

if __name__ == "__main__":
    app = MyCustomers()
    app.run()
