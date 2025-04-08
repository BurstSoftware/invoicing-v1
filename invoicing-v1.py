import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# Function to create downloadable PDF link (simplified version)
def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/pdf;base64,{bin_str}" download="{file_label}.pdf">Download {file_label}</a>'
    return href

# Main app
def main():
    st.title("Simple Invoice Generator")

    # Company Info
    st.header("Your Company Information")
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Company Name", "ABC Company")
        company_email = st.text_input("Email", "contact@abccompany.com")
    with col2:
        company_address = st.text_area("Address", "123 Business Street\nCity, State 12345")
        invoice_date = st.date_input("Invoice Date", datetime.now())

    # Client Info
    st.header("Client Information")
    col3, col4 = st.columns(2)
    with col3:
        client_name = st.text_input("Client Name", "John Doe")
        client_email = st.text_input("Client Email", "john.doe@email.com")
    with col4:
        client_address = st.text_area("Client Address", "456 Client Road\nCity, State 67890")

    # Invoice Items
    st.header("Invoice Items")
    if 'items' not in st.session_state:
        st.session_state.items = []

    with st.form(key='item_form', clear_on_submit=True):
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            description = st.text_input("Description")
        with col6:
            quantity = st.number_input("Quantity", min_value=1, value=1)
        with col7:
            unit_price = st.number_input("Unit Price", min_value=0.0, format="%.2f")
        with col8:
            st.write("")  # Empty space for alignment
            submit_button = st.form_submit_button("Add Item")

        if submit_button and description:
            st.session_state.items.append({
                'description': description,
                'quantity': quantity,
                'unit_price': unit_price,
                'total': quantity * unit_price
            })

    # Display items
    if st.session_state.items:
        df = pd.DataFrame(st.session_state.items)
        st.dataframe(df.style.format({'unit_price': '${:.2f}', 'total': '${:.2f}'}))

        # Calculate total
        total_amount = sum(item['total'] for item in st.session_state.items)
        st.write(f"**Total Amount: ${total_amount:.2f}**")

        # Clear items button
        if st.button("Clear All Items"):
            st.session_state.items = []
            st.experimental_rerun()

    # Generate Invoice
    if st.button("Generate Invoice"):
        # Create simple text-based invoice
        invoice_text = f"""
        INVOICE
        Date: {invoice_date}

        From:
        {company_name}
        {company_address}
        {company_email}

        To:
        {client_name}
        {client_address}
        {client_email}

        Items:
        """
        
        for item in st.session_state.items:
            invoice_text += f"{item['description']} | Qty: {item['quantity']} | ${item['unit_price']:.2f} | ${item['total']:.2f}\n"
            
        invoice_text += f"\nTOTAL: ${total_amount:.2f}"

        # Convert to bytes for download
        invoice_bytes = invoice_text.encode('utf-8')
        
        # Download link
        st.markdown(
            get_binary_file_downloader_html(invoice_bytes, f"Invoice_{invoice_date}"),
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
