from backend.annotations.config.AppConfig import AppConfig
from flask import Flask, jsonify
from flask_cors import CORS

# Initialize Flask app as pure API server
app = Flask(__name__)

# Enable CORS for all origins (needed for Ngrok public access)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Allow all domains (including Ngrok)
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Initialize backend config
AppConfig.init(app)

# Health check endpoint
@app.route('/')
def index():
    """API health check"""
    return jsonify({
        "status": "ok",
        "message": "Flask API Server is running",
        "version": "1.0.0",
        "endpoints": {
            "api_docs": "/apidocs",
            "health": "/",
            "api_base": "/api/v1"
        }
    })

# API health check
@app.route('/health')
def health():
    """Detailed health check"""
    return jsonify({
        "status": "healthy",
        "service": "AI Classification API",
        "timestamp": "2026-01-03"
    })

if __name__ == "__main__":
    AppConfig.run(app)
