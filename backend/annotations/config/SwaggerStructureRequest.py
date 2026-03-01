import inspect
from dataclasses import is_dataclass, fields

class SwaggerStructureRequest:
    @staticmethod
    def get_parameters(meta_method, existing_params=None):
        """
        Generates Swagger parameters.
        If 'existing_params' (from annotation) is provided, it takes precedence.
        Otherwise, auto-detects 'body' parameter from Dataclass type signals in method signature.
        """
        if existing_params:
             return existing_params
             
        try:
            sig = inspect.signature(meta_method)
            auto_params = []
            
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue

                annotation = param.annotation
                if is_dataclass(annotation):
                    schema_props = {}
                    for field in fields(annotation):
                        ftype = field.type
                        prop_type = "string"
                        if ftype == int: 
                            prop_type = "integer"
                        elif ftype == bool: 
                            prop_type = "boolean"
                        elif ftype == float: 
                            prop_type = "number"
                        
                        schema_props[field.name] = {"type": prop_type}
                    
                    auto_params.append({
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": schema_props
                        }
                    })
            
            if auto_params:
                return auto_params
                
        except Exception as e:
            print(f"SwaggerStructureRequest Auto-detect failed: {e}")
            
        return None
