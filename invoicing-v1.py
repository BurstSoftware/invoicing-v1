import streamlit as st
from fpdf import FPDF
import datetime
import base64
from io import BytesIO

def create_pdf(invoice_data):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "INVOICE", 0, 1, "C")
    
    # Company Details
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Your Company Name", 0, 1)
    pdf.cell(0, 10, "123 Business Street", 0, 1)
    pdf.cell(0, 10, "City, State ZIP", 0, 1)
    pdf.cell(0, 10, "Email: your@email.com", 0, 1)
    pdf.ln(10)
    
    # Invoice Details
    pdf.cell(0, 10, f"Invoice #: {invoice_data['invoice_number']}", 0, 1)
    pdf.cell(0, 10, f"Date: {invoice_data['date']}", 0, 1)
    pdf.ln(10)
    
    # Client Details
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Bill To:", 0, 1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, invoice_data['client_name'], 0, 1)
    pdf.cell(0, 10, invoice_data['client_address'], 0, 1)
    pdf.cell(0, 10, invoice_data['client_email'], 0, 1)
    pdf.ln(10)
    
    # Items Table
    pdf.set_font("Arial", "B", 12)
    pdf.cell(80, 10, "Description", 1, 0)
    pdf.cell(40, 10, "Quantity", 1, 0)
    pdf.cell(40, 10, "Unit Price", 1, 0)
    pdf.cell(30, 10, "Total", 1, 1)
    
    pdf.set_font("Arial", size=12)
    total = 0
    for item in invoice_data['items']:
        total_line = item['quantity'] * item['price']
        total += total_line
        pdf.cell(80, 10, item['description'], 1, 0)
        pdf.cell(40, 10, str(item['quantity']), 1, 0)
        pdf.cell(40, 10, f"${item['price']:.2f}", 1, 0)
        pdf.cell(30, 10, f"${total_line:.2f}", 1, 1)
    
    # Total
    pdf.set_font("Arial", "B", 12)
    pdf.cell(160, 10, "Total", 1, 0, "R")
    pdf.cell(30, 10, f"${total:.2f}", 1, 1)
    
    return pdf.output(dest="S").encode("latin-1")

def create_download_link(pdf_content, filename):
    b64 = base64.b64encode(pdf_content).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download Invoice PDF</a>'
    return href

def main():
    st.title("Simple Invoice Generator")
    
    # Invoice Details
    invoice_number = st.text_input("Invoice Number", f"INV-{datetime.datetime.now().strftime('%Y%m%d')}")
    date = st.date_input("Invoice Date", datetime.datetime.now())
    
    # Client Details
    st.subheader("Client Information")
    client_name = st.text_input("Client Name")
    client_address = st.text_area("Client Address")
    client_email = st.text_input("Client Email")
    
    # Items
    st.subheader("Items")
    num_items = st.number_input("Number of Items", min_value=1, max_value=10, value=1)
    
    items = []
    for i in range(num_items):
        with st.expander(f"Item {i+1}"):
            description = st.text_input(f"Description {i+1}", key=f"desc_{i}")
            quantity = st.number_input(f"Quantity {i+1}", min_value=1, key=f"qty_{i}")
            price = st.number_input(f"Unit Price {i+1}", min_value=0.0, format="%.2f", key=f"price_{i}")
            items.append({
                "description": description,
                "quantity": quantity,
                "price": price
            })
    
    # Generate Invoice
    if st.button("Generate Invoice"):
        invoice_data = {
            "invoice_number": invoice_number,
            "date": date.strftime("%Y-%m-%d"),
            "client_name": client_name,
            "client_address": client_address,
            "client_email": client_email,
            "items": items
        }
        
        pdf_content = create_pdf(invoice_data)
        st.markdown(create_download_link(pdf_content, f"invoice_{invoice_number}.pdf"), unsafe_allow_html=True)
        
        # Display total
        total = sum(item["quantity"] * item["price"] for item in items)
        st.success(f"Invoice generated successfully! Total: ${total:.2f}")

if __name__ == "__main__":
    main()
