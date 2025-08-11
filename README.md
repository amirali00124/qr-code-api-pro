# QR Code Generator API

A comprehensive, professional QR Code Generator API designed for RapidAPI monetization. Generate high-quality QR codes with advanced customization options.

## 🚀 Features

- **8 QR Code Types**: URL, Text, Email, Phone, SMS, vCard, WiFi, Location
- **Multiple Formats**: PNG, SVG, PDF output
- **Advanced Customization**: Colors, shapes, error correction levels
- **Professional Design**: Bootstrap-based demo interface
- **RapidAPI Ready**: Pre-configured for marketplace integration
- **Competitive Pricing**: 5-tier pricing structure starting with 500 free requests

## 🎯 Pricing Strategy

- **Free**: 500 requests/month
- **Starter**: $5/mo - 2,000 requests + $0.05 overage
- **Basic**: $7/mo - 5,000 requests + $0.03 overage  
- **Pro**: $12.99/mo - 15,000 requests + $0.02 overage
- **Ultra**: $49/mo - 100,000 requests + $0.01 overage

## 📁 Project Structure

```
├── app.py              # Main Flask application
├── qr_generator.py     # QR code generation logic
├── main.py             # Application entry point
├── templates/          # HTML templates
│   ├── index.html      # Demo interface
│   └── api_docs.html   # API documentation
├── static/             # CSS/JS assets
├── Procfile           # Deployment configuration
└── render.yaml        # Render deployment config
```

## 🛠 Deployment

### GitHub + Render (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "QR Code API ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**:
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration
   - Your API will be live at `https://your-app-name.onrender.com`

3. **List on RapidAPI**:
   - Use your Render URL as the base URL
   - Import the API documentation from `/docs` endpoint
   - Set up the 5-tier pricing structure

### Alternative: Railway/Fly.io

The `Procfile` is compatible with Railway and other platforms supporting Python deployments.

## 🔧 Local Development

```bash
# Install dependencies
pip install flask flask-cors gunicorn qrcode[pil] pillow reportlab

# Run locally
python main.py

# Access demo: http://localhost:5000
# Access docs: http://localhost:5000/docs
```

## 📊 API Endpoints

- `POST /api/v1/qr/url` - Generate URL QR codes
- `POST /api/v1/qr/text` - Generate text QR codes  
- `POST /api/v1/qr/email` - Generate email QR codes
- `POST /api/v1/qr/phone` - Generate phone QR codes
- `POST /api/v1/qr/sms` - Generate SMS QR codes
- `POST /api/v1/qr/vcard` - Generate vCard contact QR codes
- `POST /api/v1/qr/wifi` - Generate WiFi QR codes
- `POST /api/v1/qr/location` - Generate location QR codes

## 💼 RapidAPI Integration

All endpoints include RapidAPI-compatible headers and rate limiting information. The API is designed to be immediately compatible with RapidAPI's marketplace requirements.

## 🎨 Demo Interface

Professional demo interface featuring:
- Interactive QR code generator
- Real-time preview
- Customization options
- Download functionality
- Responsive design
- API documentation

## 📈 Competitive Advantages

- **40% cheaper** than similar APIs
- **500 free requests** vs competitors' 100-200
- **All QR types included** in every plan
- **Professional design** and documentation
- **Multiple output formats**
- **Advanced customization options**

---

Ready for deployment and RapidAPI monetization! 🚀