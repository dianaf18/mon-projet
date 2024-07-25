from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from google.cloud import speech_v1p1beta1 as speech
import io
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Charger les credentials de Google Cloud depuis le fichier .env
load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Fonction pour transcrire l'audio en temps réel
def transcribe_streaming(stream):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream)

    responses = client.streaming_recognize(config=streaming_config, requests=requests)
    return responses

@socketio.on('audio_stream')
def handle_audio_stream(audio_data):
    # Transcrire les données audio
    responses = transcribe_streaming(audio_data)
    for response in responses:
        for result in response.results:
            if result.is_final:
                text = result.alternatives[0].transcript
                # Traiter et organiser le texte
                organized_text = process_text(text)
                # Envoyer le texte organisé au frontend
                emit('transcription', {'data': organized_text})

# Fonction pour traiter le texte et extraire les informations clés
def process_text(text):
    # Placeholder pour le traitement NLP
    return text

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
import os
print("Current working directory:", os.getcwd())

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from google.cloud import speech_v1p1beta1 as speech
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Load Google Cloud credentials from the .env file
load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Function to transcribe audio in real-time
def transcribe_streaming(stream):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream)

    responses = client.streaming_recognize(config=streaming_config, requests=requests)
    return responses

@socketio.on('audio_stream')
def handle_audio_stream(audio_data):
    # Transcribe audio data
    responses = transcribe_streaming(audio_data)
    for response in responses:
        for result in response.results:
            if result.is_final:
                text = result.alternatives[0].transcript
                # Process and organize the text
                organized_text = process_text(text)
                # Emit the organized text to the frontend
                emit('transcription', {'data': organized_text})

# Function to process text and extract key information
def process_text(text):
    # Placeholder for NLP processing
    return text

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
