import tkinter as tk
from tkinter import ttk, messagebox
from ManageXml import XMLHandler
from datetime import datetime

# Global variable to store selected customer ID from MyCustomers
selected_customer_id = None

class MyProducts:
    def __init__(self, parent_window):
        self.parent_window = parent_window
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
        self.selected_row = None
        self.selected_batch_row = None
        self.setup_ui()
        self.activate()

    def activate(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.text_vars[7].set(current_date)

    def setup_ui(self):
        self.window = self.parent_window
        self.window.title("Product Form")
        self.window.geometry("1000x600")
        self.window.resizable(True, True)
        self.window.configure(bg=self.style_config["bg"])

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.window.destroy)

        label = tk.Label(
            self.window,
            text="Product System",
            height=1,
            bg=self.style_config["header_bg"],
            anchor="center",
            font=self.style_config["title_font"],
        )
        label.grid(column=0, row=0, columnspan=3, pady=10, sticky="n")

        self.form_frame = tk.Frame(self.window, bg=self.style_config["bg"])
        self.form_frame.grid(column=0, row=1, padx=20, pady=10, sticky="w")

        self.text_vars = []
        labels = ["ID", "Product Type", "Product Description", "Supplier", "Threshold", "Unit Cost", "Quantity", "Date Received"]
        for i, text in enumerate(labels):
            lbl = tk.Label(
                self.form_frame,
                text=text,
                height=1,
                bg=self.style_config["header_bg"],
                anchor="w",
                font=self.style_config["font"],
            )
            var = tk.StringVar()
            self.text_vars.append(var)
            entry = tk.Entry(
                self.form_frame,
                textvariable=var,
                width=30,
                state="readonly" if i == 0 else "normal",
                font=self.style_config["font"],
            )
            lbl.grid(column=0, row=i, padx=10, pady=5, sticky="w")
            entry.grid(column=1, row=i, pady=5, padx=10)

        self.text_var2 = []
        cost_labels = ["Labor Cost", "Overhead Cost", "Desired Profit"]
        for i, text in enumerate(cost_labels):
            lbl = tk.Label(
                self.form_frame,
                text=text,
                height=1,
                bg=self.style_config["header_bg"],
                anchor="w",
                font=self.style_config["font"],
            )
            var = tk.StringVar()
            self.text_var2.append(var)
            entry = tk.Entry(
                self.form_frame,
                textvariable=var,
                width=30,
                font=self.style_config["font"],
            )
            lbl.grid(column=0, row=i+8, padx=10, pady=5, sticky="w")
            entry.grid(column=1, row=i+8, pady=5, padx=10)

        self.btn_frame = tk.Frame(self.form_frame, bg=self.style_config["bg"])
        self.btn_frame.grid(column=0, row=11, columnspan=2, pady=10)

        buttons = [
            ("STOCKIN", self.save_product),
            ("Edit", self.edit_product),
            ("Delete", self.delete_product),
            ("Save", self.update_product),
            ("Add Order", self.add_order),
        ]
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(
                self.btn_frame,
                text=text,
                bg=self.style_config["btn_bg"] if text != "Save" else "orange",
                fg=self.style_config["btn_fg"],
                width=10,
                height=1,
                command=command,
                font=self.style_config["font"],
            )
            btn.grid(column=i, row=0, pady=5, padx=5, sticky="w")

        self.output_frame = tk.Frame(self.window, bg=self.style_config["bg"])
        self.output_frame.grid(column=1, row=1, padx=20, pady=10, sticky="nsew")
        self.output_frame.grid_columnconfigure(tuple(range(8)), weight=1)
        self.output_frame.grid_rowconfigure(tuple(range(20)), weight=1)

        self.fields = ["ID", "Product Type", "Product Description", "TOT Quantity", "TOT COST", "TOT PRICE", "TOT Orders"]
        self.field2 = ["PROD ID", "BatchNumber", "SUPPLIER", "QUANTITY", "UNITCOST", "UNIT PRICE", "DATE Received", "Orders"]
        self.entry_widgets = []
        self.entry_widgets2 = []

        self.load_products()

    def calculate_product_totals(self, product):
        total_quantity = 0
        total_cost = 0
        total_price = 0
        costs = self.xml_handler.get_costs()
        overhead_cost = int(costs.get("Overhead Cost", "0") or "0")
        desired_profit = int(costs.get("Desired Profit", "0") or "0")
        labor_cost = int(costs.get("Labor Cost", "0") or "0")
        for batch in product["Table2Entries"]:
            quantity = int(batch.get("Quantity", "0") or "0")
            unit_cost = int(batch.get("Unit Cost", "0") or "0")
            total_quantity += quantity
            total_cost += unit_cost
            unit_price = unit_cost + overhead_cost + desired_profit + labor_cost
            total_price += unit_price
        print(f"Calculated totals for product {product.get('ID', '')}: Quantity={total_quantity}, Cost={total_cost}, Price={total_price}")
        return total_quantity, total_cost, total_price

    def load_products(self):
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        self.entry_widgets = []
        self.entry_widgets2 = []

        # Set up headers for Table 1
        for col_index in range(len(self.fields)):
            header = tk.Label(
                self.output_frame,
                text=self.fields[col_index],
                bg=self.style_config["header_bg"],
                font=self.style_config["header_font"],
                borderwidth=1,
                relief="solid",
                width=15,
            )
            header.grid(row=0, column=col_index, padx=1, pady=1, sticky="nsew")

        self.products = self.xml_handler.get_all_products()
        orders = self.xml_handler.get_all_orders()
        print(f"Loaded products: {[product['ID'] for product in self.products]}")
        for product in self.products:
            product["Table2Entries"] = sorted(product["Table2Entries"], key=lambda x: int(x.get("ProdID", "0")))

        # Populate Table 1 with product data
        row = 1
        for product in self.products:
            total_quantity, total_cost, total_price = self.calculate_product_totals(product)
            # Count orders for this product based on Product Type and Product Description
            product_type = product.get("Product Type", "")
            product_desc = product.get("Product Description", "")
            product_orders = len([
                order for order in orders
                if order.get("Product Type", "") == product_type and
                   order.get("Product Description", "") == product_desc
            ])
            row_entries = []
            for col in range(len(self.fields)):
                field = self.fields[col]
                if field == "TOT Quantity":
                    value = str(total_quantity)
                elif field == "TOT COST":
                    value = str(total_cost)
                elif field == "TOT PRICE":
                    value = str(total_price)
                elif field == "TOT Orders":
                    value = str(product_orders)
                else:
                    value = product.get(field, "")
                var = tk.StringVar(value=value)
                entry = tk.Entry(
                    self.output_frame,
                    textvariable=var,
                    state="readonly",
                    width=15,
                    borderwidth=1,
                    relief="solid",
                    font=self.style_config["font"],
                    cursor="hand2",
                    bg=self.style_config["selected_row_bg"] if self.selected_row == row-1 else "white",
                )
                entry.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                entry.bind("<Button-1>", lambda e, r=row-1: self.on_entry_select(r))
                row_entries.append(entry)
            self.entry_widgets.append(row_entries)
            row += 1

        # Set up headers for Table 2
        start_row = len(self.products) + 2
        for col_index in range(len(self.field2)):
            header = tk.Label(
                self.output_frame,
                text=self.field2[col_index],
                bg=self.style_config["header_bg"],
                font=self.style_config["header_font"],
                borderwidth=1,
                relief="solid",
                width=15,
            )
            header.grid(row=start_row, column=col_index, padx=1, pady=1, sticky="nsew")

        # Refresh Table 2 if a product is selected
        if self.selected_row is not None:
            self.refresh_table2(self.products[self.selected_row])

    def refresh_table2(self, product):
        start_row = len(self.products) + 2
        for widget in self.output_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > start_row:
                widget.destroy()
        self.entry_widgets2 = []

        costs = self.xml_handler.get_costs()
        overhead_cost = int(costs.get("Overhead Cost", "0") or "0")
        desired_profit = int(costs.get("Desired Profit", "0") or "0")
        labor_cost = int(costs.get("Labor Cost", "0") or "0")
        orders = self.xml_handler.get_all_orders()
        product_id = product.get("ID", "")
        product_type = product.get("Product Type", "")
        product_desc = product.get("Product Description", "")
        table2_entries = sorted(product["Table2Entries"], key=lambda x: int(x.get("ProdID", "0")))

        row_index = start_row + 1
        for entry in table2_entries:
            row_entries = []
            # Count orders for this batch based on ProdID, Product Type, and Product Description
            batch_orders = len([
                order for order in orders
                if order.get("prodID", "") == entry.get("ProdID", "") and
                   order.get("Product Type", "") == product_type and
                   order.get("Product Description", "") == product_desc
            ])
            for col_index in range(len(self.field2)):
                field = self.field2[col_index]
                if field == "PROD ID":
                    value = entry.get("ProdID", "")
                elif field == "BatchNumber":
                    value = entry.get("BatchNumber", "")
                elif field == "SUPPLIER":
                    value = entry.get("Supplier", "")
                elif field == "QUANTITY":
                    value = entry.get("Quantity", "")
                elif field == "UNITCOST":
                    value = entry.get("Unit Cost", "")
                elif field == "UNIT PRICE":
                    unit_cost = int(entry.get("Unit Cost", "0") or "0")
                    unit_price = unit_cost + overhead_cost + desired_profit + labor_cost
                    value = str(unit_price)
                elif field == "DATE Received":
                    value = entry.get("Date Received", "")
                elif field == "Orders":
                    value = str(batch_orders)
                else:
                    value = ""
                var = tk.StringVar(value=value)
                entry_widget = tk.Entry(
                    self.output_frame,
                    textvariable=var,
                    state="readonly",
                    width=15,
                    borderwidth=1,
                    relief="solid",
                    font=self.style_config["font"],
                    cursor="hand2",
                    bg=self.style_config["selected_row_bg"] if self.selected_batch_row == row_index-(start_row+1) else "white",
                )
                entry_widget.grid(row=row_index, column=col_index, padx=1, pady=1, sticky="nsew")
                if self.selected_row is not None:
                    entry_widget.bind("<Button-1>", lambda e, r=row_index-(start_row+1): self.on_batch_select(r))
                row_entries.append(entry_widget)
            self.entry_widgets2.append(row_entries)
            print(f"Batch row {row_index-(start_row+1)}: ProdID={entry.get('ProdID', '')}, Type={product_type}, Desc={product_desc}, Orders={batch_orders}")
            row_index += 1
    def on_entry_select(self, row):
        if 0 <= row < len(self.products):
            self.selected_row = row
            product = self.products[row]
            for field_index, field in enumerate(["ID", "Product Type", "Product Description", "Supplier", "Threshold"]):
                self.text_vars[field_index].set(product.get(field, ""))
            latest_entry = product["Table2Entries"][-1] if product["Table2Entries"] else {}
            self.text_vars[5].set(latest_entry.get("Unit Cost", ""))
            self.text_vars[6].set(latest_entry.get("Quantity", ""))
            self.text_vars[7].set(latest_entry.get("Date Received", ""))
            costs = self.xml_handler.get_costs()
            for cost_index, field in enumerate(["Labor Cost", "Overhead Cost", "Desired Profit"]):
                self.text_var2[cost_index].set(costs.get(field, ""))
            self.selected_batch_row = None
            self.load_products()
            self.refresh_table2(product)

    def on_batch_select(self, batch_row):
        if self.selected_row is None:
            messagebox.showwarning("Warning", "Please select a product in Table 1 first!")
            return
        if 0 <= batch_row < len(self.products[self.selected_row]["Table2Entries"]):
            self.selected_batch_row = batch_row
            entry = self.products[self.selected_row]["Table2Entries"][batch_row]
            self.text_vars[3].set(entry.get("Supplier", ""))
            self.text_vars[5].set(entry.get("Unit Cost", ""))
            self.text_vars[6].set(entry.get("Quantity", ""))
            self.text_vars[7].set(entry.get("Date Received", ""))
            self.refresh_table2(self.products[self.selected_row])

    def add_order(self):
        global selected_customer_id
        if self.selected_row is None or self.selected_batch_row is None:
            messagebox.showwarning("Warning", "Please select a product and a batch first!")
            return
        if selected_customer_id is None:
            messagebox.showwarning("Warning", "Please select a customer in the Customer Form first!")
            return

        product = self.products[self.selected_row]
        batch = product["Table2Entries"][self.selected_batch_row]
        batch_quantity = int(batch.get("Quantity", "0") or "0")

        if batch_quantity <= 0:
            messagebox.showerror("Error", "No stock available for this batch!")
            return

        prod_id = batch.get("ProdID", "")
        costs = self.xml_handler.get_costs()
        unit_cost = int(batch.get("Unit Cost", "0") or "0")
        labor_cost = int(costs.get("Labor Cost", "0") or "0")
        overhead_cost = int(costs.get("Overhead Cost", "0") or "0")
        desired_profit = int(costs.get("Desired Profit", "0") or "0")
        unit_price = unit_cost + labor_cost + overhead_cost + desired_profit

        order_data = {
            "CustomerID": selected_customer_id,
            "prodID": prod_id,
            "Product Type": product.get("Product Type", ""),
            "Product Description": product.get("Product Description", ""),
            "Quantity": "1",
            "Unit Price": str(unit_price),
            "Total Price": str(unit_price),
            "Date Received": datetime.now().strftime("%Y-%m-%d"),
        }

        order_id = self.xml_handler.add_order(order_data)
        if order_id:
            new_quantity = batch_quantity - 1
            self.xml_handler.update_batch_quantity(product["ID"], batch["BatchNumber"], new_quantity)
            batch["Quantity"] = str(new_quantity)
            self.load_products()
            self.refresh_table2(product)
            messagebox.showinfo("Success", f"Order added with ID: {order_id} for Customer ID: {selected_customer_id}")
        else:
            messagebox.showerror("Error", "Failed to add order")

    def is_valid_integer(self, value):
        if not isinstance(value, str):
            return False
        value = value.strip()
        if not value:
            return False
        if value[0] in '-+':
            value = value[1:]
        return value.isdigit()

    def update_order_count(self, prod_id, delta):
        found = False
        for product in self.products:
            for batch in product["Table2Entries"]:
                batch_prod_id = batch.get("ProdID", "")
                if batch_prod_id == prod_id:
                    print(f"Updating batch for ProdID {prod_id}: ProductID={product['ID']}, BatchNumber={batch['BatchNumber']}, Previous Quantity={batch['Quantity']}")
                    current_qty = int(batch.get("Quantity", "0") or "0")
                    new_qty = max(0, current_qty + delta)
                    batch["Quantity"] = str(new_qty)
                    self.xml_handler.update_batch_quantity(product["ID"], batch["BatchNumber"], new_qty)
                    print(f"Updated Quantity to {new_qty} for ProdID {prod_id}")
                    found = True
                    break
            if found:
                break
        if not found:
            print(f"Warning: ProdID {prod_id} not found in products for update_order_count")
        self.load_products()

    def save_product(self):
        product_data = {
            "ID": self.text_vars[0].get(),
            "Product Type": self.text_vars[1].get(),
            "Product Description": self.text_vars[2].get(),
            "Supplier": self.text_vars[3].get(),
            "Threshold": self.text_vars[4].get(),
            "Unit Cost": self.text_vars[5].get(),
            "Quantity": self.text_vars[6].get(),
            "Date Received": self.text_vars[7].get(),
        }
        cost_data = {
            "Labor Cost": self.text_var2[0].get(),
            "Overhead Cost": self.text_var2[1].get(),
            "Desired Profit": self.text_var2[2].get(),
        }
        print(f"Saving product data: {product_data}, cost data: {cost_data}")
        if not all([product_data[key] for key in ["Product Type", "Product Description", "Supplier", "Quantity", "Unit Cost"]]):
            messagebox.showerror("Error", "Required fields are missing!")
            return

        # Refresh product list to check for existing products
        self.products = self.xml_handler.get_all_products()
        existing_product = None
        for p in self.products:
            if p.get("Product Type") == product_data["Product Type"] and p.get("Product Description") == product_data["Product Description"]:
                existing_product = p
                break

        # Determine BatchNumber
        if existing_product:
            product_id = existing_product["ID"]
            batch_count = len(existing_product["Table2Entries"])
            batch_number = str(batch_count + 1)
        else:
            product_id = self.xml_handler.get_highest_id_plus_one(self.products)
            batch_number = "1"

        # ProdID is assigned by XMLHandler.generate_ids
        batch_data = {
            "BatchNumber": batch_number,
            "Supplier": product_data["Supplier"],
            "Unit Cost": product_data["Unit Cost"],
            "Quantity": product_data["Quantity"],
            "Date Received": product_data["Date Received"],
        }
        product_data["Table2Entries"] = [batch_data] if not existing_product else existing_product.get("Table2Entries", []) + [batch_data]

        result = self.xml_handler.add_product(product_data)
        if result:
            product_id, prod_id = result
            self.text_vars[0].set(product_id)
            self.xml_handler.update_costs(cost_data)
            messagebox.showinfo("Success", f"Product added with ID: {product_id}, PROD ID: {prod_id}, Batch Number: {batch_number}")
            print(f"Product saved successfully: ID={product_id}, PROD ID={prod_id}, Batch Number={batch_number}")
            self.load_products()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to add product")
    def edit_product(self):
        if self.selected_row is None or self.selected_batch_row is None:
            messagebox.showwarning("Warning", "Please select a product and batch to edit!")
            return
        product = self.products[self.selected_row]
        product_id = product["ID"]
        batch_number = product["Table2Entries"][self.selected_batch_row]["BatchNumber"]
        updated_data = {
            "Supplier": self.text_vars[3].get(),
            "Unit Cost": self.text_vars[5].get(),
            "Quantity": self.text_vars[6].get(),
            "Date Received": self.text_vars[7].get(),
        }
        cost_data = {
            "Labor Cost": self.text_var2[0].get(),
            "Overhead Cost": self.text_var2[1].get(),
            "Desired Profit": self.text_var2[2].get(),
        }
        if not all([updated_data[key] for key in ["Supplier", "Unit Cost", "Quantity", "Date Received"]]):
            messagebox.showerror("Error", "All fields must be filled!")
            return
        if self.xml_handler.update_product(product_id, updated_data, batch_number=batch_number):
            self.xml_handler.update_costs(cost_data)
            messagebox.showinfo("Success", "Batch updated successfully!")
            self.load_products()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to update batch")

    def update_product(self):
        if self.selected_row is None:
            messagebox.showwarning("Warning", "Please select a product to edit!")
            return
        product_id = self.products[self.selected_row]["ID"]
        updated_data = {
            "Product Type": self.text_vars[1].get(),
            "Product Description": self.text_vars[2].get(),
            "Supplier": self.text_vars[3].get(),
            "Threshold": self.text_vars[4].get(),
        }
        cost_data = {
            "Labor Cost": self.text_var2[0].get(),
            "Overhead Cost": self.text_var2[1].get(),
            "Desired Profit": self.text_var2[2].get(),
        }
        if self.xml_handler.update_product(product_id, updated_data):
            self.xml_handler.update_costs(cost_data)
            messagebox.showinfo("Success", "Product updated successfully!")
            self.load_products()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to update product")

    def delete_product(self):
        if self.selected_row is None:
            messagebox.showwarning("Warning", "Please select a product to delete!")
            return
        product_id = self.products[self.selected_row]["ID"]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
            if self.xml_handler.delete_product(product_id):
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.load_products()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to delete product")

    def get_selected_product_data(self):
        if self.selected_row is None or self.selected_batch_row is None:
            return None
        if 0 <= self.selected_row < len(self.products):
            product = self.products[self.selected_row]
            if 0 <= self.selected_batch_row < len(product["Table2Entries"]):
                batch = product["Table2Entries"][self.selected_batch_row]
                costs = self.xml_handler.get_costs()
                unit_cost = int(batch.get("Unit Cost", "0") or "0")
                labor_cost = int(costs.get("Labor Cost", "0") or "0")
                overhead_cost = int(costs.get("Overhead Cost", "0") or "0")
                desired_profit = int(costs.get("Desired Profit", "0") or "0")
                unit_price = unit_cost + labor_cost + overhead_cost + desired_profit
                return {
                    "ProdID": batch.get("ProdID", ""),
                    "Product Type": product.get("Product Type", ""),
                    "Product Description": product.get("Product Description", ""),
                    "Unit Price": str(unit_price),
                }
        return None

    def clear_form(self):
        for var in self.text_vars:
            var.set("")
        self.selected_row = None
        self.selected_batch_row = None
        self.activate()
