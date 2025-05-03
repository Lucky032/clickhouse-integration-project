# backend/app.py
from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from clickhouse_client import get_client

app = Flask(__name__, template_folder='../frontend/templates')

# Configure where uploaded files will be stored temporarily
app.config['UPLOAD_FOLDER'] = 'backend/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'json'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the user has selected a file
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    
    # If no file is selected, return error
    if file.filename == '':
        return 'No selected file', 400

    # Check if the file is allowed
    if file and allowed_file(file.filename):
        # Save the file temporarily
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        try:
            # Read the file into a Pandas DataFrame (depending on file type)
            if filename.endswith('.csv'):
                data = pd.read_csv(filename)
            elif filename.endswith('.json'):
                data = pd.read_json(filename)

            # Example: Get connection to ClickHouse
            host = 'your_clickhouse_host'
            port = 8443
            database = 'your_database'
            user = 'your_user'
            jwt_token = 'your_jwt_token'

            client = get_client(host, port, database, user, jwt_token)

            # Insert data into ClickHouse
            rows = data.values.tolist()
            columns = list(data.columns)

            # Create an insert query
            insert_query = f"INSERT INTO {database}.{columns[0]} ({', '.join(columns)}) VALUES"

            # Execute the query to insert the data
            client.execute(insert_query, rows)

            return 'File uploaded and data inserted successfully!', 200
        except Exception as e:
            return f"Error processing the file: {str(e)}", 500
    else:
        return 'Invalid file format. Only CSV or JSON files are allowed.', 400

if __name__ == '__main__':
    app.run(debug=True)
