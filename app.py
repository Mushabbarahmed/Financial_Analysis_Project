from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
import io
from models import probe_model_5l_profit

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'json'}

# Function to check if the uploaded file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # Read the file in memory using BytesIO
        file_content = file.read()
        data = json.load(io.BytesIO(file_content))

        # Process the data
        results = probe_model_5l_profit(data['data'])

        return redirect(url_for('results', results=json.dumps(results)))

    return redirect(request.url)

@app.route('/results')
def results():
    results = request.args.get('results', None)
    if results:
        return render_template('results.html', results=json.loads(results))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
