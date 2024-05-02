from flask import Flask, request, jsonify, url_for
from rembg import remove
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Set the directory where processed images will be saved
UPLOAD_FOLDER = 'static/uploads'

# Create the directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure the upload folder for Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/remove-background', methods=['POST'])
def remove_background():
    # Get the uploaded image file
    uploaded_file = request.files.get('image')
    
    if uploaded_file:
        # Generate a unique filename using a timestamp and secure the filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        original_filename = secure_filename(uploaded_file.filename)
        unique_filename = f"{timestamp}_{original_filename}"
        
        # Define the input path and output path for the uploaded image
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Read the uploaded file as bytes
        input_image_bytes = uploaded_file.read()
        
        # Remove the background using rembg
        output_image_bytes = remove(input_image_bytes)
        
        # Define the output file path (change extension to .png)
        output_filename = f"{os.path.splitext(unique_filename)[0]}_bg_removed.png"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Save the output image as a PNG file
        with open(output_path, 'wb') as output_file:
            output_file.write(output_image_bytes)
        
        # Generate the URL to the output file
        output_url = url_for('static', filename=f'uploads/{output_filename}', _external=True)
        
        # Return a JSON response with the output URL
        return jsonify({"output_url": output_url})
    
    # Return an error message if no file is uploaded
    return jsonify({"error": "No image uploaded."}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
