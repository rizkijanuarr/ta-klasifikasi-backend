from flask import Flask
from backend.annotations.config.RegisteredController import RegisteredController
from backend.annotations.config.SwaggerConfig import SwaggerConfig
from backend.annotations.config.PortConfig import PortConfig

class AppConfig:
    
    @staticmethod
    def init(app: Flask):
        RegisteredController.auto_register_blueprints(app)
        SwaggerConfig.init(app)

    @staticmethod
    def run(app: Flask):
        PortConfig.run(app)
