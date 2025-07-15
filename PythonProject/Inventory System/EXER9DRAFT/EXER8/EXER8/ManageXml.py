import xml.etree.ElementTree as ET
import os

class XMLHandler:
    def __init__(self, file_name=r"C:\EXER9DRAFT\database.xml"):
        self.file_name = file_name
        self.create_xml_file_if_not_exists()

    def create_xml_file_if_not_exists(self):
            if not os.path.exists(self.file_name):
                root = ET.Element("Data")
                ET.SubElement(root, "CustomersData")
                products_data = ET.SubElement(root, "ProductsData")
                ET.SubElement(products_data, "Table2Data")
                ET.SubElement(root, "SuppliersData")
                ET.SubElement(root, "OrdersData")
                cost = ET.SubElement(root, "Cost")
                ET.SubElement(cost, "Labor_Cost").text = "0"
                ET.SubElement(cost, "Overhead_Cost").text = "0"
                ET.SubElement(cost, "Desired_Profit").text = "0"
                tree = ET.ElementTree(root)
                tree.write(self.file_name, encoding="utf-8", xml_declaration=True)
            else:
                tree = ET.parse(self.file_name)
                root = tree.getroot()
                if root.find("CustomersData") is None:
                    ET.SubElement(root, "CustomersData")
                products_data = root.find("ProductsData")
                if products_data is None:
                    products_data = ET.SubElement(root, "ProductsData")
                if products_data.find("Table2Data") is None:
                    ET.SubElement(products_data, "Table2Data")
                if root.find("SuppliersData") is None:
                    ET.SubElement(root, "SuppliersData")
                if root.find("OrdersData") is None:
                    ET.SubElement(root, "OrdersData")
                if root.find("Cost") is None:
                    cost = ET.SubElement(root, "Cost")
                    ET.SubElement(cost, "Labor_Cost").text = "0"
                    ET.SubElement(cost, "Overhead_Cost").text = "0"
                    ET.SubElement(cost, "Desired_Profit").text = "0"
                tree.write(self.file_name)

    def get_highest_id_plus_one(self, records):
        if not records:
            return "1"
        max_id = "0"
        for record in records:
            record_id = record.get("ID", "0")
            if int(record_id) > int(max_id):
                max_id = record_id
        return str(int(max_id) + 1)

    def generate_ids(self, product_data, products, tree):
        product_id = None
        prod_id = None
        existing_products = []
        for p in products:
            if (p.get("Product Type") == product_data.get("Product Type") and
                p.get("Product Description") == product_data.get("Product Description")):
                existing_products.append(p)
        if existing_products:
            product_id = existing_products[0]["ID"]
            table2_data = tree.getroot().find("ProductsData/Table2Data")
            max_prod_id = 0
            for b in table2_data.findall("Batch"):
                if b.get("ProductID") == product_id:
                    b_prod_id = int(b.find("ProdID").text or "0")
                    if b_prod_id > max_prod_id:
                        max_prod_id = b_prod_id
            prod_id = str(max_prod_id + 1)
        else:
            product_id = self.get_highest_id_plus_one(products)
            prod_id = "1"
        return product_id, prod_id

    def add_customer(self, customer_data):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        customers_data = root.find("CustomersData")
        customers = self.get_all_customers()
        new_id = self.get_highest_id_plus_one(customers)
        customer = ET.SubElement(customers_data, "Customer")
        customer.set("ID", new_id)
        for key in customer_data:
            value = customer_data[key]
            if value:
                elem = ET.SubElement(customer, key.replace(" ", "_"))
                elem.text = value
        tree.write(self.file_name)
        return new_id

    def update_customer(self, customer_id, customer_data):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        customers_data = root.find("CustomersData")
        for customer in customers_data.findall("Customer"):
            if customer.get("ID") == customer_id:
                for key in customer_data:
                    value = customer_data[key]
                    if value:
                        elem = customer.find(key.replace(" ", "_"))
                        if elem is None:
                            elem = ET.SubElement(customer, key.replace(" ", "_"))
                        elem.text = value
                tree.write(self.file_name)
                return True
        return False

    def delete_customer(self, customer_id):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        customers_data = root.find("CustomersData")
        for customer in customers_data.findall("Customer"):
            if customer.get("ID") == customer_id:
                customers_data.remove(customer)
                tree.write(self.file_name)
                return True
        return False

    def get_all_customers(self):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        customers_data = root.find("CustomersData")
        customers = []
        for customer in customers_data.findall("Customer"):
            customer_dict = {"ID": customer.get("ID")}
            for elem in customer:
                customer_dict[elem.tag.replace("_", " ")] = elem.text or ""
            customers.append(customer_dict)
        return customers

    def add_supplier(self, supplier_data):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        suppliers_data = root.find("SuppliersData")
        suppliers = self.get_all_suppliers()
        new_id = self.get_highest_id_plus_one(suppliers)
        supplier = ET.SubElement(suppliers_data, "Supplier")
        supplier.set("ID", new_id)
        for key in supplier_data:
            value = supplier_data[key]
            if value:
                elem = ET.SubElement(supplier, key.replace(" ", "_"))
                elem.text = value
        tree.write(self.file_name)
        return new_id

    def update_supplier(self, supplier_id, supplier_data):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        suppliers_data = root.find("SuppliersData")
        for supplier in suppliers_data.findall("Supplier"):
            if supplier.get("ID") == supplier_id:
                for key in supplier_data:
                    value = supplier_data[key]
                    if value:
                        elem = supplier.find(key.replace(" ", "_"))
                        if elem is None:
                            elem = ET.SubElement(supplier, key.replace(" ", "_"))
                        elem.text = value
                tree.write(self.file_name)
                return True
        return False

    def delete_supplier(self, supplier_id):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        suppliers_data = root.find("SuppliersData")
        for supplier in suppliers_data.findall("Supplier"):
            if supplier.get("ID") == supplier_id:
                suppliers_data.remove(supplier)
                tree.write(self.file_name)
                return True
        return False

    def get_all_suppliers(self):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        suppliers_data = root.find("SuppliersData")
        suppliers = []
        for supplier in suppliers_data.findall("Supplier"):
            supplier_dict = {"ID": supplier.get("ID")}
            for elem in supplier:
                supplier_dict[elem.tag.replace("_", " ")] = elem.text or ""
            suppliers.append(supplier_dict)
        return suppliers

    def add_order(self, order_data):
            tree = ET.parse(self.file_name)
            root = tree.getroot()
            orders_data = root.find("OrdersData")
            orders = self.get_all_orders()
            new_id = self.get_highest_id_plus_one(orders)
            order = ET.SubElement(orders_data, "Order")
            order.set("OrderID", new_id)
            # Add all fields except Orders
            fields = ["CustomerID", "prodID", "Product Type", "Product Description", 
                      "Quantity", "Unit Price", "Total Price", "Date Received"]
            for key in fields:
                value = order_data.get(key, "")
                if value:
                    elem = ET.SubElement(order, key.replace(" ", "_"))
                    elem.text = value
            # Add Orders element with Quantity value after Date_Received
            quantity = order_data.get("Quantity", "0")
            orders_elem = ET.Element("Orders")
            orders_elem.text = quantity
            # Insert Orders after Date_Received
            date_received_elem = order.find("Date_Received")
            if date_received_elem is not None:
                children = list(order)
                date_index = children.index(date_received_elem)
                order.insert(date_index + 1, orders_elem)
            else:
                order.append(orders_elem)
            tree.write(self.file_name, encoding="utf-8", xml_declaration=True)
            return new_id

    def update_order(self, order_id, order_data):
            tree = ET.parse(self.file_name)
            root = tree.getroot()
            orders_data = root.find("OrdersData")
            for order in orders_data.findall("Order"):
                if order.get("OrderID") == order_id:
                    # Update existing fields
                    for key in order_data:
                        value = order_data[key]
                        if value:
                            elem = order.find(key.replace(" ", "_"))
                            if elem is None:
                                elem = ET.SubElement(order, key.replace(" ", "_"))
                            elem.text = value
                    # Update or add Orders element with Quantity value
                    quantity = order_data.get("Quantity", "0")
                    orders_elem = order.find("Orders")
                    if orders_elem is None:
                        orders_elem = ET.Element("Orders")
                        date_received_elem = order.find("Date_Received")
                        if date_received_elem is not None:
                            children = list(order)
                            date_index = children.index(date_received_elem)
                            order.insert(date_index + 1, orders_elem)
                        else:
                            order.append(orders_elem)
                    orders_elem.text = quantity
                    tree.write(self.file_name, encoding="utf-8", xml_declaration=True)
                    return True
            return False

    def delete_order(self, order_id):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        orders_data = root.find("OrdersData")
        for order in orders_data.findall("Order"):
            if order.get("OrderID") == order_id:
                orders_data.remove(order)
                tree.write(self.file_name)
                return True
        return False

    def get_all_orders(self):
            tree = ET.parse(self.file_name)
            root = tree.getroot()
            orders_data = root.find("OrdersData")
            orders = []
            for order in orders_data.findall("Order"):
                order_dict = {"OrderID": order.get("OrderID")}
                for elem in order:
                    order_dict[elem.tag.replace("_", " ")] = elem.text or ""
                orders.append(order_dict)
            return orders

    def add_product(self, product_data):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        products_data = root.find("ProductsData")
        table2_data = products_data.find("Table2Data")
        products = self.get_all_products()
        product_fields = ["Product Type", "Product Description", "Supplier", "Threshold"]
        batch_fields = ["Supplier", "Quantity", "Unit Cost", "Date Received"]
        product_id, prod_id = self.generate_ids(product_data, products, tree)
        existing_product = None
        for product in products_data.findall("Product"):
            if product.get("ID") == product_id:
                existing_product = product
                break
        if not existing_product:
            product = ET.SubElement(products_data, "Product")
            product.set("ID", product_id)
            for field in product_fields:
                value = product_data.get(field, "")
                if value:
                    elem = ET.SubElement(product, field.replace(" ", "_"))
                    elem.text = value
        # Count existing batches for this product_id
        batch_count = 0
        for b in table2_data.findall("Batch"):
            if b.get("ProductID") == product_id:
                batch_count += 1
        # Set batch number: 1 for new products, next number for existing
        batch_number = str(1 if batch_count == 0 else batch_count + 1)
        # Create new batch
        batch = ET.SubElement(table2_data, "Batch")
        batch.set("ProductID", product_id)
        ET.SubElement(batch, "ProdID").text = prod_id
        ET.SubElement(batch, "BatchNumber").text = batch_number
        for field in batch_fields:
            value = product_data.get(field, "")
            if value:
                elem = ET.SubElement(batch, field.replace(" ", "_"))
                elem.text = value
        tree.write(self.file_name)
        return product_id, prod_id

    def update_product(self, product_id, updated_data, batch_number=None):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        products_data = root.find("ProductsData")
        table2_data = products_data.find("Table2Data")
        product_updated = False
        for product in products_data.findall("Product"):
            if product.get("ID") == product_id:
                for key in updated_data:
                    value = updated_data[key]
                    if value:
                        elem = product.find(key.replace(" ", "_"))
                        if elem is None:
                            elem = ET.SubElement(product, key.replace(" ", "_"))
                        elem.text = value
                product_updated = True
                break
        if batch_number:
            for batch in table2_data.findall("Batch"):
                batch_num_elem = batch.find("BatchNumber")
                if (batch_num_elem is not None and
                    batch.get("ProductID") == product_id and
                    batch_num_elem.text == batch_number):
                    for key in updated_data:
                        value = updated_data[key]
                        if value:
                            elem = batch.find(key.replace(" ", "_"))
                            if elem is None:
                                elem = ET.SubElement(batch, key.replace(" ", "_"))
                            elem.text = value
                    tree.write(self.file_name)
                    return True
        if product_updated:
            tree.write(self.file_name)
            return True
        return False

    def update_batch_quantity(self, product_id, batch_number, new_quantity):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        table2_data = root.find("ProductsData/Table2Data")
        for batch in table2_data.findall("Batch"):
            batch_num_elem = batch.find("BatchNumber")
            if (batch.get("ProductID") == product_id and
                batch_num_elem is not None and
                batch_num_elem.text == batch_number):
                quantity_elem = batch.find("Quantity")
                if quantity_elem is None:
                    quantity_elem = ET.SubElement(batch, "Quantity")
                quantity_elem.text = str(new_quantity)
                tree.write(self.file_name)
                return True
        print(f"Warning: No batch found with ProductID={product_id} and BatchNumber={batch_number}")
        return False

    def delete_product(self, product_id):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        products_data = root.find("ProductsData")
        table2_data = products_data.find("Table2Data")
        for product in products_data.findall("Product"):
            if product.get("ID") == product_id:
                products_data.remove(product)
                for batch in table2_data.findall("Batch"):
                    if batch.get("ProductID") == product_id:
                        table2_data.remove(batch)
                tree.write(self.file_name)
                return True
        return False

    def get_all_products(self):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        products_data = root.find("ProductsData")
        table2_data = products_data.find("Table2Data")
        products = []
        for product in products_data.findall("Product"):
            product_dict = {"ID": product.get("ID"), "Table2Entries": []}
            for elem in product:
                product_dict[elem.tag.replace("_", " ")] = elem.text or ""
            for batch in table2_data.findall("Batch"):
                if batch.get("ProductID") == product.get("ID"):
                    batch_dict = {"ProductID": batch.get("ProductID")}
                    for elem in batch:
                        if elem.tag == "ProdID":
                            batch_dict["ProdID"] = elem.text or ""
                        elif elem.tag == "BatchNumber":
                            batch_dict["BatchNumber"] = elem.text or ""
                        else:
                            batch_dict[elem.tag.replace("_", " ")] = elem.text or ""
                    product_dict["Table2Entries"].append(batch_dict)
            products.append(product_dict)
        return products

    def update_costs(self, cost_data):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        cost = root.find("Cost")
        for key in cost_data:
            value = cost_data[key]
            if value:
                elem = cost.find(key.replace(" ", "_"))
                if elem is None:
                    elem = ET.SubElement(cost, key.replace(" ", "_"))
                elem.text = value
        tree.write(self.file_name)
        return True

    def get_costs(self):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        cost = root.find("Cost")
        cost_dict = {}
        for elem in cost:
            cost_dict[elem.tag.replace("_", " ")] = elem.text or "0"
        return cost_dict
