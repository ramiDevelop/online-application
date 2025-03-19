import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st
from io import BytesIO

# Custom Styling
st.markdown("""
    <style>
        body { background-color: #f5f7fa; }
        .title { text-align: center; color: #2c3e50; font-size: 32px; font-weight: bold; }
        .subheader { color: #34495e; font-size: 24px; font-weight: bold; padding-top: 10px; border-bottom: 2px solid #2980b9; padding-bottom: 5px; }
        .stButton>button { background-color: #2980b9; color: white; border-radius: 5px; padding: 10px; font-size: 16px; border: none; transition: all 0.3s ease; }
        .stButton>button:hover { background-color: #1c6ea4; }
        .divider { border-top: 3px solid #2980b9; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

# Send Email Function
def send_email(subject, body, attachments):
    sender_email = "hahadigital2020@gmail.com"
    recipient_email = "hahadigital2020@gmail.com"
    email_password = st.secrets["email"]["EMAIL_PASSWORD"]

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    for attachment in attachments:
        if attachment is not None:
            file_name = attachment.name
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={file_name}")
            msg.attach(part)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, email_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
    st.success("✅ Your application has been submitted successfully!")

# Title
st.markdown('<h1 class="title">Hahas Heating and Cooling Employment Application</h1>', unsafe_allow_html=True)

# Personal Information
st.markdown('<div class="subheader">Personal Information</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("First Name")
with col2:
    last_name = st.text_input("Last Name")
col1, col2 = st.columns(2)
with col1:
    ssn = st.text_input("Social Security Number", type="password")
with col2:
    email = st.text_input("Email Address")
address = st.text_input("Address")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Employment Details
st.markdown('<div class="subheader">Employment Details</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    position = st.text_input("Position Applied For")
with col2:
    desired_pay = st.text_input("Desired Pay")
start_date = st.date_input("Start Date")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Education
st.markdown('<div class="subheader">Education</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    degree = st.text_input("Degree")
with col2:
    school_name = st.text_input("School Name")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Work Experience
st.markdown('<div class="subheader">Work Experience (Last 2 Jobs)</div>', unsafe_allow_html=True)
jobs = []
for i in range(1, 3):
    st.subheader(f"Job {i}")
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input(f"Company Name (Job {i})", key=f"company_{i}")
        job_title = st.text_input(f"Job {i} Title", key=f"job_{i}_title")
    with col2:
        job_start_date = st.date_input(f"Job {i} Start Date", key=f"job_{i}_start")
        job_end_date = st.date_input(f"Job {i} End Date", key=f"job_{i}_end")
    with col3:
        ending_wage = st.text_input(f"Ending Wage (Job {i})", key=f"wage_{i}")
    jobs.append((company_name, job_title, job_start_date, job_end_date, ending_wage))
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Banking Information
st.markdown('<div class="subheader">Banking Information</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    bank_name = st.text_input("Bank Name")
    bank_account = st.text_input("Bank Account Number", type="password")
    retype_bank_account = st.text_input("Retype Bank Account Number", type="password")
with col2:
    routing_number = st.text_input("Routing Number", type="password")
    retype_routing_number = st.text_input("Retype Routing Number", type="password")
    account_type = st.selectbox("Account Type", ["Checking", "Savings"])
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Additional Questions
st.markdown('<div class="subheader">Other Information</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    veteran_status = st.selectbox("Are you a Veteran?", ["Yes", "No"])
with col2:
    can_lift = st.selectbox("Can you lift 20 lbs?", ["Yes", "No"])
with col3:
    disability_status = st.selectbox("Do you have a disability?", ["Yes", "No"])
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# File Uploads
st.markdown('<div class="subheader">Upload Your Documents</div>', unsafe_allow_html=True)
id_file = st.file_uploader("Upload ID", type=["pdf", "jpg", "png"])
ssn_file = st.file_uploader("Upload Social Security Card", type=["pdf", "jpg", "png"])
epa_osha_file = st.file_uploader("Upload EPA/OSHA Licenses", type=["pdf", "jpg", "png"])

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Confirmation Checkbox
confirmation = st.checkbox("I confirm that all information provided is accurate and that I am fully responsible for any misleading or incorrect financial information. Hahas Heating and Cooling is not responsible for any applicant-provided errors.")

# Submit button with validation
if st.button("Submit Application"):
    if not all([first_name, last_name, ssn, email, address]):
        st.error("❌ Please fill all required fields: Name, SSN, Email, and Address.")
    elif not confirmation:
        st.error("❌ Please confirm the information accuracy before submitting.")
    else:
        email_subject = f"{first_name} {last_name} Employment Application"
        email_body = f"""
        <html>
        <body>
            <h2>Employment Application</h2>

            <h3>Personal Information</h3>
            <p><strong>Name:</strong> {first_name} {last_name}</p>
            <p><strong>SSN:</strong> {ssn}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Address:</strong> {address}</p>

            <h3>Employment Details</h3>
            <p><strong>Position Applied For:</strong> {position}</p>
            <p><strong>Desired Pay:</strong> {desired_pay}</p>
            <p><strong>Start Date:</strong> {start_date}</p>

            <h3>Education</h3>
            <p><strong>Degree:</strong> {degree}</p>
            <p><strong>School Name:</strong> {school_name}</p>

            <h3>Work Experience</h3>
            <ul>
                {''.join(f"<li><strong>Company:</strong> {job[0]}, <strong>Title:</strong> {job[1]}, <strong>Start:</strong> {job[2]}, <strong>End:</strong> {job[3]}, <strong>Ending Wage:</strong> {job[4]}</li>" for job in jobs)}
            </ul>

            <h3>Banking Information</h3>
            <p><strong>Bank Name:</strong> {bank_name}</p>
            <p><strong>Account Type:</strong> {account_type}</p>
            <p><strong>Bank Account Number:</strong> {bank_account}</p>
            <p><strong>Routing Number:</strong> {routing_number}</p>

            <h3>Other Information</h3>
            <p><strong>Veteran:</strong> {veteran_status}</p>
            <p><strong>Can lift 20 lbs:</strong> {can_lift}</p>
            <p><strong>Disability:</strong> {disability_status}</p>
        </body>
        </html>
        """
        attachments = [f for f in [id_file, ssn_file, epa_osha_file] if f is not None]
        send_email(email_subject, email_body, attachments)
