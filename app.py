import os
import logging
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from qr_generator import QRCodeGenerator
from keep_alive import start_keep_alive
import json
import traceback
import atexit
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")
CORS(app)

# Initialize QR Code Generator
qr_gen = QRCodeGenerator()

# Start keep-alive service only in production (Render environment)
if os.environ.get('RENDER'):
    start_keep_alive()
    logging.info("Keep-alive service started for Render deployment")

@app.route('/')
def index():
    """Demo interface for the QR Code API"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring and keep-alive"""
    return jsonify({
        'status': 'healthy',
        'service': 'QR Code Generator API',
        'timestamp': str(datetime.now()),
        'version': '1.0.0'
    }), 200

@app.route('/docs')
def api_docs():
    """API documentation page"""
    return render_template('api_docs.html')

@app.route('/api/v1/qr/url', methods=['POST'])
def generate_url_qr():
    """Generate QR code for URL"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        # Extract parameters
        url = data['url']
        options = data.get('options', {})
        
        # Generate QR code
        result = qr_gen.generate_url_qr(url, options)
        
        # Add rate limiting headers for RapidAPI
        response = jsonify(result)
        response.headers['X-RateLimit-Limit'] = '1000'
        response.headers['X-RateLimit-Remaining'] = '999'
        
        return response
        
    except Exception as e:
        logging.error(f"Error generating URL QR code: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500

@app.route('/api/v1/qr/text', methods=['POST'])
def generate_text_qr():
    """Generate QR code for plain text"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        options = data.get('options', {})
        
        result = qr_gen.generate_text_qr(text, options)
        
        response = jsonify(result)
        response.headers['X-RateLimit-Limit'] = '1000'
        response.headers['X-RateLimit-Remaining'] = '999'
        
        return response
        
    except Exception as e:
        logging.error(f"Error generating text QR code: {str(e)}")
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500

@app.route('/api/v1/qr/email', methods=['POST'])
def generate_email_qr():
    """Generate QR code for email"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
        
        email = data['email']
        subject = data.get('subject', '')
        message = data.get('message', '')
        options = data.get('options', {})
        
        result = qr_gen.generate_email_qr(email, subject, message, options)
        
        response = jsonify(result)
        response.headers['X-RateLimit-Limit'] = '1000'
        response.headers['X-RateLimit-Remaining'] = '999'
        
        return response
        
    except Exception as e:
        logging.error(f"Error generating email QR code: {str(e)}")
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500

@app.route('/api/v1/qr/phone', methods=['POST'])
def generate_phone_qr():
    """Generate QR code for phone number"""
    try:
        data = request.get_json()
        
        if not data or 'phone' not in data:
            return jsonify({'error': 'Phone number is required'}), 400
        
        phone = data['phone']
        options = data.get('options', {})
        
        result = qr_gen.generate_phone_qr(phone, options)
        
        response = jsonify(result)
        response.headers['X-RateLimit-Limit'] = '1000'
        response.headers['X-RateLimit-Remaining'] = '999'
        
        return response
        
    except Exception as e:
        logging.error(f"Error generating phone QR code: {str(e)}")
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500

@app.route('/api/v1/qr/sms', methods=['POST'])
def generate_sms_qr():
    """Generate QR code for SMS"""
    try:
        data = request.get_json()
        
        if not data or 'phone' not in data:
            return jsonify({'error': 'Phone number is required'}), 400
        
        phone = data['phone']
        message = data.get('message', '')
        options = data.get('options', {})
        
        result = qr_gen.generate_sms_qr(phone, message, options)
        
        response = jsonify(result)
        response.headers['X-RateLimit-Limit'] = '1000'
        response.headers['X-RateLimit-Remaining'] = '999'
        
        return response
        
    except Exception as e:
        logging.error(f"Error generating SMS QR code: {str(e)}")
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500

@app.route('/api/v1/qr/vcard', methods=['POST'])
def generate_vcard_qr():
    """Generate QR code for vCard contact"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'vCard data is required'}), 400
        
        vcard_data = {
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'organization': data.get('organization', ''),
            'phone_work': data.get('phone_work', ''),
            'phone_mobile': data.get('phone_mobile', ''),
            'email': data.get('email', ''),
            'website': data.get('website', ''),
            'street': data.get('street', ''),
            'city': data.get('city', ''),
            'state': data.get('state', ''),
            'zipcode': data.get('zipcode', ''),
            'country': data.get('country', '')
        }
        
        options = data.get('options', {})
        
        result = qr_gen.generate_vcard_qr(vcard_data, options)
        
        response = jsonify(result)
        response.headers['X-RateLimit-Limit'] = '1000'
        response.headers['X-RateLimit-Remaining'] = '999'
        
        return response
        
    except Exception as e:
        logging.error(f"Error generating vCard QR code: {str(e)}")
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500

@app.route('/api/v1/qr/wifi', methods=['POST'])
def generate_wifi_qr():
    """Generate QR code for WiFi connection"""
    try:
        data = request.get_json()
        
        if not data or 'ssid' not in data:
            return jsonify({'error': 'SSID is required'}), 400
        
        ssid = data['ssid']
        password = data.get('password', '')
        encryption = data.get('encryption', 'WPA')  # WPA, WEP, or nopass
        options = data.get('options', {})
        
        result = qr_gen.generate_wifi_qr(ssid, password, encryption, options)
        
        response = jsonify(result)
        response.headers['X-RateLimit-Limit'] = '1000'
        response.headers['X-RateLimit-Remaining'] = '999'
        
        return response
        
    except Exception as e:
        logging.error(f"Error generating WiFi QR code: {str(e)}")
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500

@app.route('/api/v1/qr/location', methods=['POST'])
def generate_location_qr():
    """Generate QR code for location coordinates"""
    try:
        data = request.get_json()
        
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Latitude and longitude are required'}), 400
        
        latitude = data['latitude']
        longitude = data['longitude']
        options = data.get('options', {})
        
        result = qr_gen.generate_location_qr(latitude, longitude, options)
        
        response = jsonify(result)
        response.headers['X-RateLimit-Limit'] = '1000'
        response.headers['X-RateLimit-Remaining'] = '999'
        
        return response
        
    except Exception as e:
        logging.error(f"Error generating location QR code: {str(e)}")
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
