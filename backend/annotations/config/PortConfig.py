from flask import Flask
import os

class PortConfig:
    @staticmethod
    def get_port():
        return int(os.environ.get("PORT", 5002))

    @staticmethod
    def run(app: Flask):
        port = PortConfig.get_port()
        is_production = os.environ.get("RENDER", False) or os.environ.get("PRODUCTION", False)
        app.run(host="0.0.0.0", port=port, debug=not is_production)