from flask import request, jsonify
from dataclasses import asdict
from backend.controller.advices.BaseControllerImpl import BaseControllerImpl
from backend.controller.v1.HealthControllerV1 import HealthControllerV1

@BaseControllerImpl
class HealthControllerImplV1(HealthControllerV1):
    
    def __init__(self):
        pass

    def health_check(self):
        return jsonify({"status": "ok"})
