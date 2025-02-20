from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from datetime import datetime
from utils.language_handler import _get_language_from_header
from services.damage_detection import DamageDetection

# Upload API Key
load_dotenv()

# Flask App
app = Flask(__name__)

# Create DamageDetection Object
damage_detection_instance = DamageDetection()

# Home Page (Web UI)
@app.route('/')
def index():
    return render_template('index.html')

# Damage Assessment API
@app.route('/detect-damage', methods=['POST'])
def detect_damage_endpoint():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({'error': 'İki farklı görsel yüklenmelidir'}), 400

    file1 = request.files['image1']
    file2 = request.files['image2']

    if file1.filename == '' or file2.filename == '':
        return jsonify({'error': 'Seçili dosya yok'}), 400

    if file1 and file2:
        # Get language from header
        accept_language_header = request.headers.get('Accept-Language', 'tr-tr')  # Default Turkish
        language = _get_language_from_header(accept_language_header)  # Use language detection function

        # Save files temporarily
        image_path1 = f"./temp_{datetime.now().strftime('%Y%m%d%H%M%S')}_1.jpg"
        image_path2 = f"./temp_{datetime.now().strftime('%Y%m%d%H%M%S')}_2.jpg"
        file1.save(image_path1)
        file2.save(image_path2)

        try:
            # Analyze by sending two images to the OpenAI API
            content, usage = damage_detection_instance.analyze_damage(image_path1, image_path2, language)

            # Delete temporary files
            os.remove(image_path1)
            os.remove(image_path2)

            return jsonify({
                "content": content,
                "usage": usage
            })

        except Exception as e:
            os.remove(image_path1)
            os.remove(image_path2)
            return jsonify({'error': str(e)}), 500

# Run Flask Application
if __name__ == '__main__':
    app.run(debug=True)
