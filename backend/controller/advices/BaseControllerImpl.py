from flask import Blueprint
from flask_cors import CORS
import inspect
import functools
import yaml
import json
from dataclasses import is_dataclass, asdict

def BaseControllerImpl(import_name=__name__):
    target_cls = None
    if inspect.isclass(import_name):
        target_cls = import_name
        import_name = __name__

    def decorator(cls):
        prefix = None
        for base in cls.__mro__:
            if hasattr(base, "__controller_prefix__"):
                prefix = base.__controller_prefix__
                break

        bp = Blueprint(cls.__name__.lower(), import_name, url_prefix=prefix)
        CORS(bp, resources={r"/*": {"origins": "*"}})

        instance = cls()
        existing_routes = set()

        for attr_name in dir(instance):
            if attr_name.startswith("_"):
                continue

            actual_method = getattr(instance, attr_name)
            if not callable(actual_method):
                continue

            meta_method = None
            for base in cls.__mro__:
                if hasattr(base, attr_name):
                    candidate = getattr(base, attr_name)
                    if hasattr(candidate, "__http_method__"):
                        meta_method = candidate
                        break

            if meta_method:
                method = getattr(meta_method, "__http_method__", None)
                path = getattr(meta_method, "__route_path__", None)
                route_kwargs = getattr(meta_method, "__route_kwargs__", {})

                # Convert Spring Boot style {param} to Flask style <param>
                if path:
                    import re
                    path = re.sub(r'\{(\w+)\}', r'<\1>', path)


                # --- SWAGGER INJECTION ---
                swagger_info = getattr(meta_method, "__swagger_info__", {})
                if swagger_info:
                    swag = {}

                    tags = []
                    tag_name = swagger_info.get("tagName")
                    if tag_name:
                        tags.append(tag_name)

                    if tags:
                        swag["tags"] = tags

                    if swagger_info.get("summary"):
                        swag["summary"] = swagger_info["summary"]
                    if swagger_info.get("description"):
                        swag["description"] = swagger_info["description"]

                    from backend.annotations.config.SwaggerStructureRequest import SwaggerStructureRequest
                    params = SwaggerStructureRequest.get_parameters(meta_method, swagger_info.get("params"))
                    if params:
                        swag["parameters"] = params

                    consumes = swagger_info.get("consumes")
                    if consumes:
                        swag["consumes"] = consumes
                    produces = swagger_info.get("produces")
                    if produces:
                        swag["produces"] = produces

                    from backend.annotations.config.SwaggerStructureResponse import SwaggerStructureResponse
                    initial_responses = swagger_info.get("responses", {})
                    responses = SwaggerStructureResponse.generate_responses(meta_method, initial_responses)

                    swag["responses"] = responses

                    def create_wrapper(method_to_wrap, swag_data):
                        import functools
                        from flask import request, jsonify
                        from dataclasses import is_dataclass, asdict
                        import inspect

                        sig = inspect.signature(method_to_wrap)
                        dataclass_param_name = None
                        dataclass_type = None

                        for name, param in sig.parameters.items():
                             if name == 'self': continue
                             if is_dataclass(param.annotation):
                                 dataclass_param_name = name
                                 dataclass_type = param.annotation
                                 break

                        @functools.wraps(method_to_wrap)
                        def wrapper(*args, **kwargs):
                            if dataclass_param_name and dataclass_type:
                                # Force JSON parsing even without Content-Type header
                                # This allows Postman to work without explicitly setting Content-Type
                                json_body = request.get_json(force=True, silent=True) or {}
                                try:
                                    dto_instance = dataclass_type(**json_body)
                                    if hasattr(dto_instance, '__post_init__'):
                                        dto_instance.__post_init__()
                                    kwargs[dataclass_param_name] = dto_instance
                                except ValueError as ve:
                                     return jsonify({
                                         "success": False,
                                         "message": "Validation Error",
                                         "errors": [{"code": 400, "title": "Validation Error", "message": str(ve)}]
                                     }), 400
                                except TypeError as te:
                                     # Structure Error - Add detailed logging
                                     import traceback
                                     print(f"[DEBUG] TypeError during dataclass instantiation:")
                                     print(f"[DEBUG] Dataclass type: {dataclass_type}")
                                     print(f"[DEBUG] JSON body: {json_body}")
                                     print(f"[DEBUG] Error: {te}")
                                     print(f"[DEBUG] Traceback: {traceback.format_exc()}")
                                     return jsonify({
                                         "success": False,
                                         "message": "Invalid Request Format",
                                         "errors": [{"code": 400, "title": "Type Error", "message": str(te)}]
                                     }), 400
                                except Exception as e:
                                     import traceback
                                     print(f"[DEBUG] Unexpected error during dataclass instantiation:")
                                     print(f"[DEBUG] Error type: {type(e)}")
                                     print(f"[DEBUG] Error: {e}")
                                     print(f"[DEBUG] Traceback: {traceback.format_exc()}")
                                     return jsonify({
                                         "success": False,
                                         "message": "Bad Request",
                                         "errors": [{"code": 400, "title": "Bad Request", "message": str(e)}]
                                     }), 400


                            try:
                                result = method_to_wrap(*args, **kwargs)
                            except Exception as e:
                                return jsonify({
                                    "success": False,
                                    "message": "Internal Server Error",
                                    "errors": [{"code": 500, "title": "Internal Error", "message": str(e)}]
                                }), 500

                            if is_dataclass(result):
                                # Recursive asdict untuk handle nested dataclass
                                def recursive_asdict(obj):
                                    """Recursively convert dataclass to dict, handling nested structures"""
                                    if is_dataclass(obj) and not isinstance(obj, type):
                                        # Convert dataclass instance to dict
                                        print(f"[ASDICT] Converting dataclass: {type(obj).__name__}")
                                        try:
                                            obj_dict = asdict(obj)
                                            print(f"[ASDICT] Successfully converted {type(obj).__name__}")
                                        except Exception as e:
                                            print(f"[ASDICT ERROR] Failed to convert {type(obj).__name__}: {e}")
                                            import traceback
                                            print(traceback.format_exc())
                                            raise

                                        result_dict = {}
                                        for field_name, field_value in obj_dict.items():
                                            result_dict[field_name] = recursive_asdict(field_value)
                                        return result_dict
                                    elif isinstance(obj, list):
                                        return [recursive_asdict(item) for item in obj]
                                    elif isinstance(obj, dict):
                                        return {k: recursive_asdict(v) for k, v in obj.items()}
                                    else:
                                        return obj

                                try:
                                    print(f"[SERIALIZATION] Starting serialization of {type(result).__name__}")
                                    serialized = recursive_asdict(result)
                                    print(f"[SERIALIZATION] Successfully serialized")
                                    return jsonify(serialized)
                                except Exception as e:
                                    print(f"[SERIALIZATION ERROR] {str(e)}")
                                    import traceback
                                    print(traceback.format_exc())
                                    return jsonify({
                                        "success": False,
                                        "message": "Serialization Failed",
                                        "data": None,
                                        "errors": [{
                                            "code": "SERIALIZATION_ERROR",
                                            "title": "Serialization Failed",
                                            "message": str(e)
                                        }]
                                    }), 500

                            return result


                        wrapper.swag = swag_data
                        doc_content = method_to_wrap.__doc__ or ""
                        wrapper.__doc__ = f"{doc_content}\n---\n{yaml.dump(swag_data)}"
                        return wrapper

                    view_func_to_register = create_wrapper(actual_method, swag)
                else:
                    view_func_to_register = actual_method
                # --- SWAGGER INJECTION ---

                key = (method, path)
                if key not in existing_routes:
                    bp.add_url_rule(path, view_func=view_func_to_register, methods=[method], **route_kwargs)
                    existing_routes.add(key)

        cls.__blueprint__ = bp
        return cls

    if target_cls:
        return decorator(target_cls)
    return decorator
