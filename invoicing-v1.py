import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# Function to create downloadable file link
def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}.txt">Download {file_label}</a>'
    return href

# Main app
def main():
    st.title("Simple Invoice Generator")

    # Always start with a fresh list, regardless of previous state
    st.session_state.items = getattr(st.session_state, 'items', [])  # Default to empty list if not set
    if not isinstance(st.session_state.items, list):
        st.session_state.items = []  # Force reset if corrupted
    items = st.session_state.items[:]  # Use slice to create a shallow copy safely

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

    # Invoice Items Form
    st.header("Invoice Items")
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
            new_item = {
                'description': str(description),
                'quantity': int(quantity),
                'unit_price': float(unit_price),
                'total': float(quantity * unit_price)
            }
            items.append(new_item)
            st.session_state.items = items  # Sync back to session state
            st.success(f"Added item: {description}")

    # Display items
    if items:
        try:
            df = pd.DataFrame(items)
            st.dataframe(df.style.format({'unit_price': '${:.2f}', 'total': '${:.2f}'}))

            total_amount = sum(item['total'] for item in items)
            st.write(f"**Total Amount: ${total_amount:.2f}**")
        except Exception as e:
            st.error(f"Error displaying items: {str(e)}. Clearing items.")
            items.clear()
            st.session_state.items = items
    else:
        st.info("No items added yet.")

    # Clear items button
    if st.button("Clear All Items"):
        items.clear()
        st.session_state.items = items
        st.experimental_rerun()

    # Generate Invoice
    if st.button("Generate Invoice"):
        if not items:
            st.warning("Please add at least one item before generating an invoice.")
        else:
            try:
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
                for item in items:
                    invoice_text += f"{item['description']} | Qty: {item['quantity']} | ${item['unit_price']:.2f} | ${item['total']:.2f}\n"
                
                total_amount = sum(item['total'] for item in items)
                invoice_text += f"\nTOTAL: ${total_amount:.2f}"

                invoice_bytes = invoice_text.encode('utf-8')
                st.markdown(
                    get_binary_file_downloader_html(invoice_bytes, f"Invoice_{invoice_date}"),
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Error generating invoice: {str(e)}. Clearing items.")
                items.clear()
                st.session_state.items = items

if __name__ == "__main__":
    main()
