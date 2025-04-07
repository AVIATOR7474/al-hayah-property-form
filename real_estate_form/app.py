import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json

# Set page configuration
st.set_page_config(
    page_title="Al Hayah Developments - Property Inquiry Form",
    page_icon="🏢",
    layout="centered"
)

# Initialize session state for form submission
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Simple header
st.title("Al Hayah Developments")
st.header("Property Inquiry Form")

# Define email sending function
def send_inquiry_email(form_data):
    try:
        # Email configuration
        sender_email = "noreply@alhayadevelopments.com"
        receiver_email = "cpt.ahmed2018@gmail.com"
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"New Property Inquiry from {form_data['Client Name']}"
        
        # Create simple email body
        email_text = "A new property inquiry has been submitted with the following details:\n\n"
        for key, value in form_data.items():
            email_text += f"{key}: {value}\n"
        email_text += "\nPlease contact the client as soon as possible."
        
        # Attach the text content to the email
        message.attach(MIMEText(email_text, "plain"))
        
        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("cpt.ahmed2018@gmail.com", "yndxitnnalocuqkd")
            server.send_message(message)
        
        return True
    except Exception as e:
        return False

# Display form or results based on submission status
if not st.session_state.form_submitted:
    # Client Information
    st.subheader("Client Information")
    report_date = st.date_input("Report Date", datetime.date.today())
    client_name = st.text_input("Client Name")
    client_phone = st.text_input("Client Phone Number")
    
    # Property Requirements
    st.subheader("Property Requirements")
    unit_type = st.selectbox(
        "Unit Type",
        [
            "Studio", "Apartment", "Duplex", "Penthouse", 
            "Town House", "Twin House", "Villa", "Chalet",
            "Commercial Space", "Administrative Space"
        ]
    )
    
    floor_type = st.selectbox(
        "Floor Type",
        [
            "Ground Floor", "Ground Floor with Garden", 
            "Typical Floor", "Last Floor", 
            "Last Floor with Roof"
        ]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        min_unit_area = st.number_input("Min Area (m²)", min_value=0, value=0)
    with col2:
        max_unit_area = st.number_input("Max Area (m²)", min_value=0, value=0)
    
    num_rooms = st.number_input("Number of Rooms", min_value=0, value=0)
    num_bathrooms = st.number_input("Number of Bathrooms", min_value=0, value=0)
    
    finishing_type = st.selectbox(
        "Finishing Type",
        ["Fully Finished", "Semi-Finished", "Core & Shell"]
    )
    
    # Location and Financial Details
    st.subheader("Location and Financial Details")
    area = st.selectbox(
        "Area",
        [
            "Sheikh Zayed", "October", "October Gardens", 
            "Green Belt", "Green Revolution", "New Cairo", 
            "6th Settlement", "Future City", "El Shorouk", 
            "New Administrative Capital", "Ain Sokhna", 
            "Red Sea", "North Coast"
        ]
    )
    
    budget = st.number_input("Budget (EGP)", min_value=0, value=0)
    
    payment_method = st.selectbox(
        "Payment Method",
        ["Cash", "Installments"]
    )
    
    delivery_date = st.date_input("Delivery Date", min_value=datetime.date.today())
    
    # Submit button
    if st.button("Submit Inquiry"):
        # Validate form
        if not client_name or not client_phone:
            st.error("Please fill in all required fields: Client Name and Phone Number")
        else:
            # Store form data
            form_data = {
                "Report Date": report_date.strftime("%Y-%m-%d"),
                "Client Name": client_name,
                "Client Phone": client_phone,
                "Unit Type": unit_type,
                "Floor Type": floor_type,
                "Unit Area": f"{min_unit_area} - {max_unit_area} m²",
                "Number of Rooms": str(num_rooms),
                "Number of Bathrooms": str(num_bathrooms),
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
                    json.dump(form_data, f, indent=4)
            except Exception:
                pass  # Silently handle file saving errors
            
            # Send email silently
            try:
                send_inquiry_email(form_data)
            except:
                pass
            
            # Store data in session state for display
            st.session_state.form_data = form_data
            st.session_state.form_submitted = True
            
            # Show success message
            st.success("Form submitted successfully! A copy has been sent to our team.")
            
            # Display the submitted data in a simple format
            st.subheader("Property Inquiry Details")
            for key, value in form_data.items():
                st.write(f"**{key}:** {value}")

else:
    # Display success message
    st.success("Form submitted successfully! A copy has been sent to our team.")
    
    # Display the submitted data in a simple format
    st.subheader("Property Inquiry Details")
    for key, value in st.session_state.form_data.items():
        st.write(f"**{key}:** {value}")
    
    # Add a button to submit another inquiry
    if st.button("Submit Another Inquiry"):
        st.session_state.form_submitted = False

# Simple footer
st.write("---")
st.write("© 2025 Al Hayah Developments. All rights reserved.")
st.write("For inquiries, please contact us @ Mobile Number - 01288359654")
