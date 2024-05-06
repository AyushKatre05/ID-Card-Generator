import textwrap
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import csv
import qrcode
from datetime import datetime

# Function to generate ID card
def generate_id_card(name, gender, dob, blood_group, mobile_no, address, profile_image):
    # Generate unique ID number
    id_number = random.randint(1000000, 9000000)
    
    # Create ID card image
    image = Image.new('RGB', (500, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font_bold = ImageFont.truetype('arialbd.ttf', size=16)
    font_regular = ImageFont.truetype('arial.ttf', size=16)
    
    # Add blue background with black outline
    draw.rectangle([(10, 10), (490, 290)], fill="#3498db", outline="black", width=2)
    
    # Add ID number
    draw.text((20, 20), f"ID: {id_number}", fill="white", font=font_bold)
    
    # Add user details
    draw.text((20, 50), f"Name:", fill="black", font=font_bold)
    draw.text((150, 50), f"{name}", fill="black", font=font_regular)
    draw.text((20, 80), f"Gender:", fill="black", font=font_bold)
    draw.text((150, 80), f"{gender}", fill="black", font=font_regular)
    draw.text((20, 110), f"DOB:", fill="black", font=font_bold)
    draw.text((150, 110), f"{dob}", fill="black", font=font_regular)
    draw.text((20, 140), f"Blood Group:", fill="black", font=font_bold)
    draw.text((150, 140), f"{blood_group}", fill="black", font=font_regular)
    draw.text((20, 170), f"Mobile No:", fill="black", font=font_bold)
    draw.text((150, 170), f"{mobile_no}", fill="black", font=font_regular)
    draw.text((20, 200), f"Address:", fill="black", font=font_bold)
    address_lines = textwrap.wrap(address, width=40)
    # Adjust y_offset for text wrapping
    y_offset = 200
    line_spacing = 3  # Additional spacing between lines
    for line in address_lines:
        draw.text((150, y_offset), line, fill="black", font=font_regular)
        y_offset += 20 + line_spacing  # Manually adjust y_offset for each line

    # Add profile image if uploaded
    if profile_image:
        profile_image.thumbnail((80, 80))  # Resize profile image
        image.paste(profile_image, (400, 20))
    
    # Generate QR code with user information
    qr_data = f"ID: {id_number}\nName: {name}\nGender: {gender}\nDOB: {dob}\nBlood Group: {blood_group}\nMobile No: {mobile_no}\nAddress: {address}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image = qr_image.resize((80, 80))
    image.paste(qr_image, (400, 110))
    
    return image, id_number

# Function to validate input
def validate_input(name, gender, dob, blood_group, mobile_no, address, profile_image):
    # Perform validation here
    if not name or not gender or not dob or not blood_group or not mobile_no or not address:
        st.error("All fields are mandatory.")
        return False
    
    if gender not in ["Male", "Female"]:
        st.error("Please select a valid gender.")
        return False
    
    if not mobile_no.isdigit():
        st.error("Mobile Number should contain only numbers.")
        return False
    
    # Perform additional validation...
    
    return True

# Function to save data to CSV
def save_to_csv(id_number, name, gender, dob, blood_group, mobile_no, address):
    with open('data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([id_number, name, gender, dob, blood_group, mobile_no, address, datetime.now()])

def main():
    st.title("Simple ID Card Generator")
    st.write("Fill out the following details to generate your ID card:")
    
    # Input fields
    name = st.text_input("Enter Full Name:")
    gender = st.selectbox("Select Gender:", ["Male", "Female"])
    dob = st.date_input("Enter Date of Birth:", min_value=datetime(1920, 1, 1), max_value=datetime.now())
    blood_group = st.selectbox("Select Blood Group:", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    mobile_no = st.text_input("Enter Mobile Number:")
    address = st.text_area("Enter Address:")
    profile_image = st.file_uploader("Upload Profile Picture:", type=["jpg", "jpeg", "png"])
    
    # Validation
    if st.button("Generate ID Card"):
        if validate_input(name, gender, dob, blood_group, mobile_no, address, profile_image):
            # Convert uploaded image to PIL format
            profile_image_pil = None
            if profile_image:
                profile_image_pil = Image.open(profile_image)
            
            # Format date of birth
            formatted_dob = dob.strftime("%d-%m-%Y")
            
            # Generate ID card
            id_card, id_number = generate_id_card(name, gender, formatted_dob, blood_group, mobile_no, address, profile_image_pil)
            st.image(id_card, caption=f"ID Card for {name}", use_column_width=True)
            
            # Save data to CSV
            save_to_csv(id_number, name, gender, formatted_dob, blood_group, mobile_no, address)
            
            # Download link for ID card image
            st.markdown(f"Download your ID card [here](data:image/png;base64,{id_number}).")

if __name__ == "__main__":
    main()
