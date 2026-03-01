from dataclasses import is_dataclass, fields
from typing import get_origin, get_args, List, Any

class SwaggerStructureResponse:
    
    @staticmethod
    def build_schema(type_hint):
        """
        Recursively builds a Swagger/OpenAPI JSON schema from a Python type hint.
        Handles: Dataclasses, List[T], DataResponseParameter[T], and primitives.
        """
        try:
            origin = get_origin(type_hint)
            args = get_args(type_hint)
            
            if origin is list or origin is List:
                item_type = args[0] if args else Any
                return {
                    "type": "array",
                    "items": SwaggerStructureResponse.build_schema(item_type)
                }
                
            type_name = getattr(type_hint, "__name__", "")
            if type_name in ["DataResponseParameter", "ListResponseParameter", "PageResponseParameter"]:
                inner_type = args[0] if args else Any
                return {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "default": True},
                        "message": {"type": "string"},
                        "data": SwaggerStructureResponse.build_schema(inner_type),
                        "errors": {
                            "type": "array", 
                            "items": {
                                "type": "object",
                                "properties": {
                                    "code": {"type": "integer"},
                                    "title": {"type": "string"},
                                    "message": {"type": "string"}
                                }
                            }
                        }
                    }
                }

            if is_dataclass(type_hint):
                props = {}
                for field in fields(type_hint):
                    props[field.name] = SwaggerStructureResponse.build_schema(field.type)
                return {
                    "type": "object",
                    "properties": props
                }

            if type_hint == int: return {"type": "integer"}
            if type_hint == str: return {"type": "string"}
            if type_hint == bool: return {"type": "boolean"}
            if type_hint == float: return {"type": "number"}
            
            return {"type": "string"}
        except Exception:
            return {"type": "object"}

    @staticmethod
    def generate_responses(meta_method, existing_responses=None):
        """
        Generates standard 200, 400, 500 response schemas.
        Inspects 'return' annotation to build the 200 schema.
        """
        responses = existing_responses or {}

        def create_error_schema(code_example, message_example):
            return {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "default": False},
                    "message": {"type": "string"},
                    "data": {"type": "object", "nullable": True},
                    "errors": {
                        "type": "array", 
                        "items": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "integer", "example": code_example},
                                "title": {"type": "string", "example": "Error Title"},
                                "message": {"type": "string", "example": message_example}
                            }
                        }
                    }
                }
            }

        # Default 200
        if "200" not in responses:
            return_annotation = meta_method.__annotations__.get('return')
            if return_annotation:
                schema = SwaggerStructureResponse.build_schema(return_annotation)
                responses["200"] = {
                    "description": "Successful operation",
                    "schema": schema
                }
            else:
                 responses["200"] = {"description": "Successful operation"}
        
        # Default 400
        if "400" not in responses:
            responses["400"] = {
                "description": "Bad Request",
                "schema": create_error_schema(400, "Detailed bad request message")
            }

        # Default 500
        if "500" not in responses:
            responses["500"] = {
                "description": "Internal Server Error",
                "schema": create_error_schema(500, "Internal Server Error")
            }
            
        return responses
