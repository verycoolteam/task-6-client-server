import os
import json
from typing import Dict, List, Optional
from models import FunctionDefinition, FunctionMetadata

FUNCTIONS_DIR = "functions"

os.makedirs(FUNCTIONS_DIR, exist_ok=True)

class FunctionStorage:
    def __init__(self):
        self.functions: Dict[str, FunctionDefinition] = {}
        self.load_all()

    def load_all(self):
        for filename in os.listdir(FUNCTIONS_DIR):
            if filename.endswith(".json"):
                func_name = filename[:-5]
                with open(os.path.join(FUNCTIONS_DIR, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.functions[func_name] = FunctionDefinition(**data)

    def save_function(self, func_def: FunctionDefinition):
        filename = os.path.join(FUNCTIONS_DIR, f"{func_def.metadata.name}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(func_def.dict(), f, indent=2, ensure_ascii=False)
        self.functions[func_def.metadata.name] = func_def

    def get_function(self, name: str) -> Optional[FunctionDefinition]:
        return self.functions.get(name)

    def list_functions(self) -> List[str]:
        return list(self.functions.keys())

    def delete_function(self, name: str) -> bool:
        if name in self.functions:
            del self.functions[name]
            filename = os.path.join(FUNCTIONS_DIR, f"{name}.json")
            if os.path.exists(filename):
                os.remove(filename)
            return True
        return False