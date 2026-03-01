from functools import wraps
from typing import List, Optional

def OptionsEndpoint(
    value: str = "/",
    path: Optional[str] = None,
    name: str = "",
    tagName: str = "",
    summary: str = "",
    description: str = "",
    group: object = None,
    consumes: Optional[List[str]] = None,
    produces: Optional[List[str]] = None,
    params: Optional[List[str]] = None,
    headers: Optional[List[str]] = None,
    **kwargs
):
    def decorator(func):
        func.__http_method__ = "OPTIONS"
        func.__route_path__ = path if path is not None else value
        
        func.__swagger_info__ = {
            "name": name,
            "tagName": tagName,
            "summary": summary,
            "description": description,
            "group": group,
            "consumes": consumes,
            "produces": produces,
            "params": params,
            "headers": headers
        }
        
        func.__route_kwargs__ = kwargs
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
