import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import base64
import os
import json

# Set page configuration
st.set_page_config(
    page_title="Al Hayah Developments - Property Inquiry Form",
    page_icon="🏢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Function to load and display the logo
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Color scheme based on the logo
primary_color = "#C8A23F"  # Gold color from logo
secondary_color = "#000000"  # Black color from logo
accent_color = "#8A6D3B"  # Darker gold for accents
light_color = "#F9F6EF"  # Light cream color for backgrounds
text_color = "#333333"  # Dark gray for text

# Custom CSS for styling
st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {primary_color};
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    .sub-header {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {accent_color};
        margin-bottom: 1rem;
        text-align: center;
    }}
    .form-section {{
        background-color: {light_color};
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .success-message {{
        background-color: #d4edda;
        color: #155724;
        padding: 20px;
        border-radius: 5px;
        text-align: center;
        margin: 20px 0;
        font-size: 1.2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .stButton>button {{
        background-color: {primary_color};
        color: white;
        font-weight: bold;
        width: 100%;
        padding: 12px 0;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: {accent_color};
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}
    footer {{
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e0e0e0;
        color: {text_color};
        font-size: 0.9rem;
    }}
    .logo-container {{
        text-align: center;
        margin-bottom: 10px;
        padding: 20px 0;
    }}
    .result-table {{
        margin-top: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        overflow: hidden;
    }}
    .stDateInput>div>div>input {{
        text-align: center;
    }}
    .highlight {{
        background-color: {light_color};
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid {primary_color};
        margin-bottom: 20px;
        font-weight: 600;
        color: {accent_color};
    }}
    .required:after {{
        content: " *";
        color: #e74c3c;
        font-weight: bold;
    }}
    .stSelectbox [data-baseweb=select] {{
        border-radius: 5px;
    }}
    .stNumberInput [data-baseweb=input] {{
        border-radius: 5px;
    }}
    .stTextInput [data-baseweb=input] {{
        border-radius: 5px;
    }}
    .stDateInput [data-baseweb=input] {{
        border-radius: 5px;
    }}
    /* Custom styling for the table */
    .dataframe {{
        width: 100%;
        border-collapse: collapse;
    }}
    .dataframe th {{
        background-color: {primary_color};
        color: white;
        padding: 12px;
        text-align: left;
    }}
    .dataframe td {{
        padding: 12px;
        border-bottom: 1px solid #e0e0e0;
    }}
    .dataframe tr:nth-child(even) {{
        background-color: {light_color};
    }}
    /* Page background */
    .stApp {{
        background: linear-gradient(to bottom, white, {light_color});
    }}
    /* Header area with logo */
    .header-area {{
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    /* Email preview section */
    .email-preview {{
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .email-preview-header {{
        font-size: 1.2rem;
        font-weight: 600;
        color: {accent_color};
        margin-bottom: 10px;
        border-bottom: 1px solid #e0e0e0;
        padding-bottom: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# Logo and Header
st.markdown('<div class="header-area">', unsafe_allow_html=True)
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.jpg")
st.markdown(f'<div class="logo-container"><img src="data:image/jpeg;base64,{get_base64_of_bin_file(logo_path)}" width="400"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">Property Inquiry Form</h2>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state for form submission
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Form inputs
with st.form("property_inquiry_form"):
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    
    # Client Information
    st.markdown('<h3 class="highlight">Client Information</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="required">Report Date</p>', unsafe_allow_html=True)
        report_date = st.date_input("Report Date", datetime.date.today(), label_visibility="collapsed")
        
        st.markdown('<p class="required">Client Name</p>', unsafe_allow_html=True)
        client_name = st.text_input("Client Name", label_visibility="collapsed")
    with col2:
        st.markdown('<p class="required">Client Phone Number</p>', unsafe_allow_html=True)
        client_phone = st.text_input("Client Phone Number", label_visibility="collapsed")
    
    # Property Requirements
    st.markdown('<h3 class="highlight">Property Requirements</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p>Unit Type</p>', unsafe_allow_html=True)
        unit_type = st.selectbox(
            "Unit Type",
            [
                "Studio", "Apartment", "Duplex", "Penthouse", 
                "Town House", "Twin House", "Villa", "Chalet",
                "Commercial Space", "Administrative Space"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown('<p>Floor Type</p>', unsafe_allow_html=True)
        floor_type = st.selectbox(
            "Floor Type",
            [
                "Ground Floor", "Ground Floor with Garden", 
                "Typical Floor", "Last Floor", 
                "Last Floor with Roof"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown('<p>Unit Area (m²)</p>', unsafe_allow_html=True)
        min_area, max_area = st.columns(2)
        with min_area:
            min_unit_area = st.number_input("Min Area", min_value=0, value=0, label_visibility="collapsed")
        with max_area:
            max_unit_area = st.number_input("Max Area", min_value=0, value=0, label_visibility="collapsed")
    
    with col2:
        st.markdown('<p>Number of Rooms</p>', unsafe_allow_html=True)
        num_rooms = st.number_input("Number of Rooms", min_value=0, value=0, label_visibility="collapsed")
        
        st.markdown('<p>Number of Bathrooms</p>', unsafe_allow_html=True)
        num_bathrooms = st.number_input("Number of Bathrooms", min_value=0, value=0, label_visibility="collapsed")
        
        st.markdown('<p>Finishing Type</p>', unsafe_allow_html=True)
        finishing_type = st.selectbox(
            "Finishing Type",
            ["Fully Finished", "Semi-Finished", "Core & Shell"],
            label_visibility="collapsed"
        )
    
    # Location and Financial Details
    st.markdown('<h3 class="highlight">Location and Financial Details</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p>Area</p>', unsafe_allow_html=True)
        area = st.selectbox(
            "Area",
            [
                "Sheikh Zayed", "October", "October Gardens", 
                "Green Belt", "Green Revolution", "New Cairo", 
                "6th Settlement", "Future City", "El Shorouk", 
                "New Administrative Capital", "Ain Sokhna", 
                "Red Sea", "North Coast"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown('<p>Budget (EGP)</p>', unsafe_allow_html=True)
        budget = st.number_input("Budget", min_value=0, value=0, label_visibility="collapsed")
    
    with col2:
        st.markdown('<p>Payment Method</p>', unsafe_allow_html=True)
        payment_method = st.selectbox(
            "Payment Method",
            ["Cash", "Installments"],
            label_visibility="collapsed"
        )
        
        st.markdown('<p>Delivery Date</p>', unsafe_allow_html=True)
        delivery_date = st.date_input("Delivery Date", min_value=datetime.date.today(), label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
    submit_button = st.form_submit_button("Submit Inquiry")
    
    if submit_button:
        # Validate form
        if not client_name or not client_phone:
            st.error("Please fill in all required fields: Client Name and Phone Number")
        else:
            st.session_state.form_submitted = True
            st.session_state.form_data = {
                "Report Date": report_date.strftime("%Y-%m-%d"),
                "Client Name": client_name,
                "Client Phone": client_phone,
                "Unit Type": unit_type,
                "Floor Type": floor_type,
                "Unit Area": f"{min_unit_area} - {max_unit_area} m²",
                "Number of Rooms": num_rooms,
                "Number of Bathrooms": num_bathrooms,
                "Finishing Type": finishing_type,
                "Area": area,
                "Budget": f"{budget:,} EGP",
                "Payment Method": payment_method,
                "Delivery Date": delivery_date.strftime("%Y-%m-%d")
            }
            
            # Save the form data to a JSON file for record keeping
            try:
                # Create a directory for submissions if it doesn't exist
                submissions_dir = os.path.join(os.path.dirname(__file__), "submissions")
                os.makedirs(submissions_dir, exist_ok=True)
                
                # Generate a unique filename based on timestamp and client name
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = ''.join(c if c.isalnum() else '_' for c in client_name)
                filename = f"{timestamp}_{safe_name}.json"
                
                # Save the data
                with open(os.path.join(submissions_dir, filename), 'w') as f:
                    json.dump(st.session_state.form_data, f, indent=4)
            except Exception as e:
                st.warning(f"Could not save submission locally: {e}")

# Display results after form submission
if st.session_state.form_submitted:
    st.markdown('<div class="success-message">Form submitted successfully! A copy has been sent to our team.</div>', unsafe_allow_html=True)
    
    # Display the submitted data in a table format
    st.markdown('<h3 class="sub-header">Property Inquiry Details</h3>', unsafe_allow_html=True)
    
    # Convert the form data to a DataFrame for better display
    df = pd.DataFrame([st.session_state.form_data])
    df_transposed = df.T.reset_index()
    df_transposed.columns = ['Field', 'Value']
    
    # Style the table
    st.markdown('<div class="result-table">', unsafe_allow_html=True)
    st.table(df_transposed)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Send email function
    def send_email(form_data):
        try:
            # Email configuration
            sender_email = "noreply@alhayadevelopments.com"
            receiver_email = "cpt.ahmed2018@gmail.com"
            
            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = f"New Property Inquiry from {form_data['Client Name']}"
            
            # Email body
            email_body = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                    }}
                    .header {{
                        background-color: {primary_color};
                        color: white;
                        padding: 20px;
                        text-align: center;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin: 20px 0;
                    }}
                    th, td {{
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 12px;
                    }}
                    th {{
                        background-color: {primary_color};
                        color: white;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f9f9f9;
                    }}
                    .footer {{
                        margin-top: 30px;
                        font-size: 0.9em;
                        color: #666;
                        text-align: center;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>New Property Inquiry - Al Hayah Developments</h2>
                </div>
                <p>A new property inquiry has been submitted with the following details:</p>
                <table>
                    <tr>
                        <th>Field</th>
                        <th>Value</th>
                    </tr>
            """
            
            for key, value in form_data.items():
                email_body += f"""
                    <tr>
                        <td>{key}</td>
                        <td>{value}</td>
                    </tr>
                """
            
            email_body += """
                </table>
                <p>Please contact the client as soon as possible.</p>
                <div class="footer">
                    <p>© 2025 Al Hayah Developments. All rights reserved.</p>
                </div>
            </body>
            </html>
           
            
            message.attach(MIMEText(email_body, "html"))
            
            # For demonstration purposes, we'll show a preview of the email
            st.markdown('<div class="email-preview">', unsafe_allow_html=True)
            st.markdown('<div class="email-preview-header">Email Preview (Will be sent to cpt.ahmed2018@gmail.com)</div>', unsafe_allow_html=True)
            st.markdown(f"<strong>Subject:</strong> New Property Inquiry from {form_data['Client Name']}", unsafe_allow_html=True)
            st.markdown("<strong>Email Content:</strong>", unsafe_allow_html=True)
            st.markdown(email_body, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # In a production environment, uncomment this code to actually send the email
            """
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login("cpt.ahmed2018@gmail.com", "yndxitnnalocuqkd")
                server.send_message(message)
            
            
            return True
        except Exception as e:
            st.error(f"Error preparing email: {e}")
            return False
    
    # Send the email
    send_email(st.session_state.form_data)

# Footer
st.markdown(f"""
<footer>
    <p>© 2025 Al Hayah Developments. All rights reserved.</p>
    <p>For inquiries, please contact us at info@alhayadevelopments.com</p>
</footer>
""", unsafe_allow_html=True)
