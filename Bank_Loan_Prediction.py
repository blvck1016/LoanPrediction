import streamlit as st
from PIL import Image
import pickle
import mysql.connector
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient



# Load the model
with open('./Model/ML_Model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

def get_key_vault_secret(https://keykey.managedhsm.azure.net, keykey):
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=vault_url, credential=credential)

    try:
        secret = secret_client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        print(f"Error retrieving secret '{secret_name}' from Key Vault: {e}")
        return None


# Function to create a MySQL connection
def create_connection():
    
    mysql_host = 'medproject.mysql.database.azure.com'
    mysql_user = 'ifmpwbxopa@medproject'
    mysql_password = '1VRSAF7B6311Z1TV$'
    mysql_db = 'apploan-database'

    return mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_db
    )

# Function to create a loan_data table
def create_loan_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loan_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_no VARCHAR(255),
            full_name VARCHAR(255),
            prediction INT
        )
    """)
    connection.commit()

# Function to insert loan data into the database
def insert_loan_data(connection, account_no, fn, prediction):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO loan_data (account_no, full_name, prediction)
        VALUES (%s, %s, %s)
    """, (account_no, fn, prediction))
    connection.commit()
    
    # Function to upload a file to Azure Blob Storage
def upload_to_blob_storage(file_content, file_name):
    connection_string = 'DefaultEndpointsProtocol=https;AccountName=datamed;AccountKey=Tf/4H6710/Z6qrmNycf3X6Y6tZ59qWb3ILNrJYxPIfIJwDMX+SRdJ469pmy1wJey23G3nLL0mnRU+AStM/VznQ==;EndpointSuffix=core.windows.net'
    container_name = 'blob'

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Upload file
    blob_client = container_client.get_blob_client(file_name)
    blob_client.upload_blob(file_content)

def run():
    # Apply styling with HTML and CSS
    st.markdown(
        """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f0f0f0;  /* Light gray background */
            }
            .container {
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background-color: #ffffff;  /* White container background */
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .header {
                text-align: center;
                font-size: 32px;
                color: #3498db;  /* Blue color for header */
                margin-bottom: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Main content
  

    # Logo image
    img1 = Image.open('bank.jpg').resize((700, 350))
    st.image(img1, use_column_width=False)

    # Title
    st.markdown("<div class='header'>Bank Loan Prediction</div>", unsafe_allow_html=True)
    

    # User inputs
    account_no = st.text_input('Account number')
    fn = st.text_input('Full Name')

    # Dropdowns for categorical features
    gen = st.selectbox("Gender", ('Female', 'Male'))
    mar = st.selectbox("Marital Status", ('No', 'Yes'))
    dep = st.selectbox("Dependents", ('No', 'One', 'Two', 'More than Two'))
    edu = st.selectbox("Education", ('Not Graduate', 'Graduate'))
    emp = st.selectbox("Employment Status", ('Job', 'Business', 'Unemployed'))
    prop = st.selectbox("Property Area", ('Rural', 'Semi-Urban', 'Urban'))
    cred = st.selectbox("Credit Score", ('Between 300 to 500', 'Above 500'))

    # Numeric inputs
    mon_income = st.number_input("Applicant's Monthly Income($)", value=0)
    co_mon_income = st.number_input("Co-Applicant's Monthly Income($)", value=0)
    loan_amt = st.number_input("Loan Amount", value=0)

    # Dropdown for loan duration
    dur_options = ['2 Month', '6 Month', '8 Month', '1 Year', '16 Month']
    dur = st.selectbox("Loan Duration", dur_options)

    if st.button("Submit"):
        # Mapping duration to months
        duration_mapping = {'2 Month': 60, '6 Month': 180, '8 Month': 240, '1 Year': 360, '16 Month': 480}
        duration = duration_mapping.get(dur, 0)

        # Features for prediction
        features = [[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]]
        print(features)

        # Make prediction
        prediction = model.predict(features)
        
        if prediction == 0:
            st.error(f"Hello: {fn} || Account number: {account_no} || "
                     "According to our calculations, you will not get the loan from the bank.")
        else:
            st.success(f"Hello: {fn} || Account number: {account_no} || "
                       "Congratulations!! You will get the loan from the bank.")
            
            # Create loan_data table if not exists
            create_loan_table(mysql_connection)

            # Insert loan data into the database
            insert_loan_data(mysql_connection, account_no, fn, prediction)

            # Close MySQL connection
            mysql_connection.close()
            
            # Close the main content div
    st.markdown("</div>", unsafe_allow_html=True)

# Run the Streamlit app
run()
