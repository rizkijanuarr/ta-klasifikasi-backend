from flask import Flask
from flasgger import Swagger

class SwaggerConfig:
    @staticmethod
    def init(app: Flask):
        app.config['SWAGGER'] = {
            'title': 'Tugas Akhir API',
            'uiversion': 3
        }
        Swagger(app)