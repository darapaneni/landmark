import streamlit as st
from fpdf import FPDF
import datetime

# Function to create the PDF
def create_pdf(sale_deed_details):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt="SALE DEED", ln=True, align='C')

    # Sale Deed Content
    pdf.set_font('Arial', '', 10)
    for line in sale_deed_details:
        pdf.multi_cell(100, 10, line)

    # Save PDF
    pdf_output = "sale_deed.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Title of the app
st.title("Sale Deed Form")

if __name__ == '__main__':
    # Initialize session state for authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # Default credentials
    DEFAULT_USERNAME = "narayana"
    DEFAULT_EMAIL = "darapaneni@gmail.com"
    DEFAULT_PASSWORD = "123"

    # Login page
    if not st.session_state.authenticated:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")

        if st.button("Login"):
            if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD and email == DEFAULT_EMAIL:
                st.session_state.authenticated = True
                st.success("Login successful!")
            else:
                st.error("Invalid credentials. Please try again.")

    # Main app
    if st.session_state.authenticated:
        # Form for user input
        with st.form("sale_deed_form"):
            st.header("Seller's Information")
            seller_name = st.text_input("Seller's Full Name", "")
            seller_age = st.number_input("Seller's Age", min_value=18, max_value=100, value=30)
            seller_occupation = st.text_input("Seller's Occupation", "")
            seller_address = st.text_area("Seller's Address", "")
            seller_aadhar = st.text_input("Seller's Aadhar No.", "")

            st.header("Buyer's Information")
            buyer_name = st.text_input("Buyer's Full Name", "")
            buyer_age = st.number_input("Buyer's Age", min_value=18, max_value=100, value=30)
            buyer_occupation = st.text_input("Buyer's Occupation", "")
            buyer_address = st.text_area("Buyer's Address", "")
            buyer_aadhar = st.text_input("Buyer's Aadhar No.", "")

            st.header("Property Information")
            survey_no = st.text_input("Survey No.", "")
            village_name = st.text_input("Village Name", "")
            mandal_name = st.text_input("Mandal Name", "")
            district_name = st.text_input("District Name", "")
            sale_price = st.number_input("Sale Price (INR)", min_value=0, value=0)
            amount_in_words = st.text_input("Amount in Words", "")

            st.header("Payment Information")
            advance_amount = st.number_input("Advance Amount (INR)", min_value=0, value=0)
            balance_amount = st.number_input("Balance Amount (INR)", min_value=0, value=0)
            payment_date = st.date_input("Date of Payment", datetime.date.today())

            st.header("Additional Information")
            location = st.text_input("Location of Deed Execution", "")
            registration_days = st.number_input("Number of Days for Registration", min_value=1, max_value=365, value=30)
            sub_registrar_location = st.text_input("Location of Sub-Registrar's Office", "")

            # Submit button
            submitted = st.form_submit_button("Generate Sale Deed PDF")

        # On form submission
        if submitted:
            # Format the sale deed details
            sale_deed_details = [
                f"This Sale Deed is made and executed on this {datetime.date.today().strftime('%d')} day of {datetime.date.today().strftime('%B')}, {datetime.date.today().year}, at {location}, Andhra Pradesh, India.",
                "",
                "BETWEEN",
                f"1. Seller(s):\n   - Name: {seller_name}\n   - Age: {seller_age}\n   - Occupation: {seller_occupation}\n   - Address: {seller_address}\n   - Aadhar No.: {seller_aadhar}",
                "",
                f"AND\n2. Buyer(s):\n   - Name: {buyer_name}\n   - Age: {buyer_age}\n   - Occupation: {buyer_occupation}\n   - Address: {buyer_address}\n   - Aadhar No.: {buyer_aadhar}",
                "",
                "WHEREAS:",
                f"1. The Seller is the absolute owner of the agricultural land bearing Survey No. {survey_no}, situated at {village_name}, {mandal_name}, {district_name}, Andhra Pradesh, hereinafter referred to as the 'Scheduled Property'.",
                f"2. The Seller has agreed to sell and the Buyer has agreed to purchase the Scheduled Property for a total sale consideration of RS: {sale_price} (Rupees {amount_in_words} only) on the terms and conditions hereinafter set forth.",
                "3. The Seller assures that the Scheduled Property is free from all encumbrances, charges, liens, mortgages, or any other claims and that the Seller has a clear and marketable title to the Scheduled Property.",
                "",
                "NOW THIS DEED WITNESSETH AS FOLLOWS:",
                f"1. Sale Consideration: The total sale consideration for the Scheduled Property is RS: {sale_price} (Rupees {amount_in_words} only).",
                f"2. Payment: The Buyer has paid the Seller a sum of RS: {advance_amount} as advance payment on {payment_date.strftime('%d-%m-%Y')}, and the balance amount of RS: {balance_amount} shall be paid at the time of registration.",
                f"3. Registration: The parties agree to present this Sale Deed for registration at the Sub-Registrar's office at {sub_registrar_location} within {registration_days} days."
            ]

            # Generate PDF
            pdf_file = create_pdf(sale_deed_details)

            # Display success message and download link
            st.success("Sale Deed PDF generated successfully!")
            st.download_button("Download Sale Deed PDF", data=open(pdf_file, "rb"), file_name="sale_deed.pdf")
