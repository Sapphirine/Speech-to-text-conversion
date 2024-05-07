from flask import Flask, render_template, request 
import os  
import speech_recognition as sr  
from audiodenoising import denoise 

app = Flask(__name__)  

# Define constants for file upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to convert speech to text
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, could not understand audio"
    except sr.RequestError as e:
        return "Could not get results; {0}".format(e)

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')  # Render HTML template

# Route for processing uploaded file
@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']
    if file.filename == '':
        return "No file selected"

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        text = speech_to_text(filepath)
        return render_template('index.html', text=text, audio_file=filename)  # Render HTML template with results

    return "Invalid file format"

# Run the application
if __name__ == "__main__":
    app.run(debug=True) 