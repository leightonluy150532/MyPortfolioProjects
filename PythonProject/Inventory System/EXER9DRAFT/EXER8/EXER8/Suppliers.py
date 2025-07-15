import tkinter as tk
from tkinter import ttk, messagebox
from ManageXml import XMLHandler

class MySuppliers:
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
        self.setup_ui()

    def setup_ui(self):
        self.window = self.parent_window
        self.window.title("Supplier Form")
        self.window.geometry("1000x600")
        self.window.resizable(True, True)
        self.window.configure(bg=self.style_config["bg"])

        # Menu Bar
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.window.destroy)

        # Title Label
        label = tk.Label(
            self.window,
            text="Supplier System",
            height=1,
            bg=self.style_config["header_bg"],
            anchor="center",
            font=self.style_config["title_font"],
        )
        label.grid(column=0, row=0, columnspan=3, pady=10, sticky="n")

        # Form Frame
        self.form_frame = tk.Frame(self.window, bg=self.style_config["bg"])
        self.form_frame.grid(column=0, row=1, padx=20, pady=10, sticky="w")

        labels = ["ID", "Name", "Contact", "Address"]
        self.text_vars = []
        for i, text in enumerate(labels):
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

        # Button Frame
        self.btn_frame = tk.Frame(self.form_frame, bg=self.style_config["bg"])
        self.btn_frame.grid(column=0, row=len(labels), columnspan=2, pady=10)

        save_btn = tk.Button(
            self.btn_frame,
            text="Save",
            bg=self.style_config["btn_bg"],
            fg=self.style_config["btn_fg"],
            width=10,
            height=1,
            command=self.save_supplier,
            font=self.style_config["font"],
        )
        save_btn.grid(column=0, row=0, pady=5, padx=5, sticky="w")
        edit_btn = tk.Button(
            self.btn_frame,
            text="Edit",
            bg=self.style_config["btn_bg"],
            fg=self.style_config["btn_fg"],
            width=10,
            height=1,
            command=self.edit_supplier,
            font=self.style_config["font"],
        )
        edit_btn.grid(column=1, row=0, pady=5, padx=5, sticky="w")
        delete_btn = tk.Button(
            self.btn_frame,
            text="Delete",
            bg=self.style_config["btn_bg"],
            fg=self.style_config["btn_fg"],
            width=10,
            height=1,
            command=self.delete_supplier,
            font=self.style_config["font"],
        )
        delete_btn.grid(column=2, row=0, pady=5, padx=5, sticky="w")

        # Output Frame for Table
        self.output_frame = tk.Frame(self.window, bg=self.style_config["bg"])
        self.output_frame.grid(column=1, row=1, padx=20, pady=10, sticky="nsew")

        self.fields = ["ID","Name", "Contact", "Address"]
        self.entry_widgets = []

        self.load_suppliers()

    def load_suppliers(self):
        for widget in self.output_frame.winfo_children():
            widget.destroy()

        # Display table directly in output_frame without Canvas or Scrollbar
        for col, field in enumerate(self.fields):
            header = tk.Label(
                self.output_frame,
                text=field,
                bg=self.style_config["header_bg"],
                font=self.style_config["header_font"],
                borderwidth=1,
                relief="solid",
                width=15,
            )
            header.grid(row=0, column=col, padx=1, pady=1, sticky="nsew")

        self.suppliers = self.xml_handler.get_all_suppliers()
        self.entry_widgets = []
        for row, supplier in enumerate(self.suppliers, start=1):
            row_entries = []
            for col, field in enumerate(self.fields):
                var = tk.StringVar(value=supplier.get(field, ""))
                entry = tk.Entry(
                    self.output_frame,
                    textvariable=var,
                    state="readonly",
                    width=15,
                    borderwidth=1,
                    relief="solid",
                    font=self.style_config["font"],
                )
                entry.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                entry.bind("<Button-1>", lambda e, r=row-1: self.on_entry_select(r))
                row_entries.append(entry)
            self.entry_widgets.append(row_entries)

    def on_entry_select(self, row):
        if 0 <= row < len(self.suppliers):
            supplier = self.suppliers[row]
            for i, field in enumerate(["ID"] + self.fields):
                self.text_vars[i].set(supplier.get(field, ""))
            self.selected_row = row

    def delete_supplier_row(self, row):
        if 0 <= row < len(self.suppliers):
            supplier_id = self.suppliers[row]["ID"]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this supplier?"):
                if self.xml_handler.delete_supplier(supplier_id):
                    messagebox.showinfo("Success", "Supplier deleted successfully!")
                    self.refresh_table()
                    self.clear_form()
                else:
                    messagebox.showerror("Error", "Failed to delete supplier")

    def save_supplier(self):
        supplier_data = {
            "ID": self.text_vars[0].get(),
            "Name": self.text_vars[1].get(),
            "Contact": self.text_vars[2].get(),
            "Address": self.text_vars[3].get(),
        }
        if self.selected_row is not None and self.selected_row < len(self.suppliers):
            if self.xml_handler.update_supplier(supplier_data["ID"], supplier_data):
                messagebox.showinfo("Success", "Supplier updated successfully!")
                self.refresh_table()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to update supplier")
        else:
            new_id = self.xml_handler.add_supplier(supplier_data)
            if new_id is not None:
                self.text_vars[0].set(new_id)
                messagebox.showinfo("Success", "Supplier added successfully!")
                self.refresh_table()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to add supplier")

    def edit_supplier(self):
        if self.selected_row is not None:
            messagebox.showinfo("Edit Mode", "Modify the fields and click Save to update.")
        else:
            messagebox.showwarning("No Selection", "Please select a supplier to edit.")

    def delete_supplier(self):
        if self.selected_row is None or self.selected_row >= len(self.suppliers):
            messagebox.showwarning("Warning", "Please select a supplier to delete first!")
            return
        self.delete_supplier_row(self.selected_row)

    def refresh_table(self):
        self.load_suppliers()
        self.selected_row = None

    def clear_form(self):
        for var in self.text_vars:
            var.set("")
        self.selected_row = None
