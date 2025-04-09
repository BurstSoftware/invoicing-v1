import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# Function to create downloadable file link
def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}.txt">Download {file_label}</a>'
    return href

# Function to ensure items is a valid list
def ensure_valid_items():
    if 'items' not in st.session_state or not isinstance(st.session_state.items, list):
        st.session_state.items = []

# Function to add an item safely
def add_item(description, quantity, unit_price):
    ensure_valid_items()
    new_item = {
        'description': str(description),
        'quantity': int(quantity),
        'unit_price': float(unit_price),
        'total': float(quantity * unit_price)
    }
    st.session_state.items.append(new_item)

# Function to display items
def display_items():
    ensure_valid_items()
    items = st.session_state.items
    try:
        if items and all(isinstance(item, dict) for item in items):
            df = pd.DataFrame(items)
            st.dataframe(df.style.format({'unit_price': '${:.2f}', 'total': '${:.2f}'}))

            total_amount = sum(float(item['total']) for item in items)
            st.write(f"**Total Amount: ${total_amount:.2f}**")
        else:
            st.info("No valid items to display.")
    except ValueError as e:
        st.error(f"Error displaying items: {str(e)}. Resetting items.")
        st.session_state.items = []
    except Exception as e:
        st.error(f"Unexpected error in display: {str(e)}. Resetting items.")
        st.session_state.items = []

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

    # Ensure items is initialized
    ensure_valid_items()

    # Invoice Items
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
            add_item(description, quantity, unit_price)
            st.success(f"Added item: {description}")

    # Display items
    display_items()

    # Clear items button
    if st.button("Clear All Items"):
        st.session_state.items = []
        st.experimental_rerun()

    # Generate Invoice
    if st.button("Generate Invoice"):
        ensure_valid_items()
        items = st.session_state.items  # Work with a local copy
        if not items:
            st.warning("Please add at least one item before generating an invoice.")
        else:
            try:
                # Explicitly check if items is iterable and a list
                if not isinstance(items, list):
                    raise TypeError("Items is not a list, something went wrong with the state.")
                
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
                
                # Double-check before iterating
                if not hasattr(items, '__iter__') or callable(items):
                    raise TypeError("Items is a method or non-iterable object.")
                
                for item in items:
                    if not isinstance(item, dict):
                        raise ValueError("Invalid item format detected")
                    invoice_text += f"{item['description']} | Qty: {item['quantity']} | ${item['unit_price']:.2f} | ${item['total']:.2f}\n"
                    
                total_amount = sum(float(item['total']) for item in items)
                invoice_text += f"\nTOTAL: ${total_amount:.2f}"

                # Convert to bytes for download
                invoice_bytes = invoice_text.encode('utf-8')
                
                # Download link
                st.markdown(
                    get_binary_file_downloader_html(invoice_bytes, f"Invoice_{invoice_date}"),
                    unsafe_allow_html=True
                )
            except TypeError as e:
                st.error(f"Type error in invoice generation: {str(e)}. Resetting items.")
                st.session_state.items = []
            except ValueError as e:
                st.error(f"Value error in invoice generation: {str(e)}. Resetting items.")
                st.session_state.items = []
            except Exception as e:
                st.error(f"Unexpected error in invoice generation: {str(e)}. Resetting items.")
                st.session_state.items = []

if __name__ == "__main__":
    main()
