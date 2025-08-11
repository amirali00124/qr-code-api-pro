# QR Code Generator API

A professional QR code generation API with customization options, multiple content types, and demo interface designed for RapidAPI monetization.

## Features

- **Multiple QR Code Types**: URL, Text, Email, Phone, SMS, vCard, WiFi, Location
- **Advanced Customization**: Colors, shapes, sizes, error correction levels
- **Multiple Output Formats**: PNG, SVG, PDF
- **Professional Demo Interface**: Interactive web interface for testing
- **RapidAPI Ready**: Optimized for marketplace deployment
- **Keep-Alive Functionality**: Prevents Render free tier from sleeping

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

3. Open http://localhost:5000 in your browser

### Deployment on Render

1. Push this code to your GitHub repository
2. Connect to Render and deploy
3. Set environment variables:
   - `SESSION_SECRET`: Auto-generate
   - `RENDER`: Set to "true"

See `DEPLOYMENT.md` for detailed deployment instructions.

## API Endpoints

### Generate QR Code for URL
```
POST /api/v1/qr/url
```

**Request Body:**
```json
{
  "url": "https://example.com",
  "options": {
    "foreground_color": "#000000",
    "background_color": "#ffffff",
    "module_drawer": "square",
    "error_correction": "M",
    "format": "PNG",
    "size": 10
  }
}
```

### Health Check
```
GET /health
```

## Project Structure

```
├── app.py              # Main Flask application
├── main.py             # Application entry point
├── qr_generator.py     # QR code generation logic
├── keep_alive.py       # Keep-alive service for Render
├── templates/          # HTML templates
├── static/             # CSS and JavaScript files
├── render.yaml         # Render deployment config
├── Procfile            # Process configuration
├── runtime.txt         # Python version
└── requirements.txt    # Python dependencies
```

## Pricing Strategy

Competitive 5-tier pricing structure for RapidAPI:

- **Free**: $0/mo - 500 requests/month
- **Starter**: $5/mo - 2,000 requests + overage
- **Basic**: $7/mo - 5,000 requests + overage
- **Pro**: $12.99/mo - 15,000 requests + overage
- **Ultra**: $49/mo - 100,000 requests + overage

## Keep-Alive Feature

This project includes an automatic keep-alive service that:

- Pings the `/health` endpoint every 5 minutes
- Only runs in production (when `RENDER` environment variable is set)
- Prevents Render free tier from sleeping due to inactivity
- Includes comprehensive logging for monitoring

## License

This project is ready for commercial use and RapidAPI marketplace deployment.