import os
import importlib
import inspect
from flask import Flask

class RegisteredController:
    
    @staticmethod
    def auto_register_blueprints(app: Flask):
        """
        Dynamically scans backend/controller/**/impl/*.py for classes with __blueprint__.
        """
        project_root = os.getcwd() # Assumes running from root of project
        base_dir = os.path.join(project_root, "backend", "controller")
        
        if not os.path.exists(base_dir):
            print(f"Warning: Controller directory not found at {base_dir}")
            return

        for root, dirs, files in os.walk(base_dir):
            # We strictly only want to look inside directories named 'impl'
            # Note: os.walk yields root as the full path. We check if the path ends with /impl
            # or if 'impl' is part of the path structure we care about.
            
            # Use logic: only load modules if they are inside an 'impl' package
            rel_dir = os.path.relpath(root, project_root)
            path_parts = rel_dir.split(os.sep)
            
            if "impl" not in path_parts:
                continue
                
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    # Construct module path: backend.controller.v1.impl.SomeController
                    file_path = os.path.join(root, file)
                    rel_file_path = os.path.relpath(file_path, project_root)
                    module_name = rel_file_path.replace(os.sep, ".")[:-3] # Strip .py
                    
                    try:
                        module = importlib.import_module(module_name)
                        
                        # Inspect classes in the module
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            # Check if it has __blueprint__ (added by BaseControllerImpl)
                            if hasattr(obj, "__blueprint__"):
                                # Check if it's already registered to avoid double registration issues (Flask handles this but good to be clean)
                                # Simple check: is it in existing blueprints?
                                # Actually Flask blueprint registration is idempotent-ish but errors on name collision if object different.
                                # Here we just register.
                                print(f"  [Auto-Register] Blueprint: {name}")
                                app.register_blueprint(obj.__blueprint__)
                                
                    except Exception as e:
                        print(f"  [Error] Failed to load module {module_name}: {e}")