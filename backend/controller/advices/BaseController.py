from flask import Blueprint
from flask_cors import CORS
from typing import Callable

def create_blueprint(name: str, import_name: str = __name__) -> Blueprint:
    bp = Blueprint(name, import_name)
    CORS(bp, resources={r"/*": {"origins": "*"}})
    return bp

def register_route(bp: Blueprint, rule: str, methods: list, handler: Callable):
    bp.route(rule, methods=methods)(handler)

def BaseController(*, name: str = "", value: str = "", import_name: str = __name__):
    def decorator(cls):
        
        cls.__controller_prefix__ = value

        import inspect
        if inspect.isabstract(cls):
            return cls

        bp_name = name or cls.__name__.lower()
        bp = Blueprint(bp_name, import_name, url_prefix=(value or None))
        CORS(bp, resources={r"/*": {"origins": "*"}})
        
        instance = cls()
        for attr_name in dir(instance):
            attr = getattr(instance, attr_name)
            method = getattr(attr, "__http_method__", None)
            path = getattr(attr, "__route_path__", None)
            if method and path is not None:
                route_kwargs = getattr(attr, "__route_kwargs__", {})
                bp.add_url_rule(path, view_func=attr, methods=[method], **route_kwargs)
        cls.__blueprint__ = bp
        return cls
    return decorator
