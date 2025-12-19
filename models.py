from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import json

class FunctionSignature(BaseModel):
    input_params: List[str]  # Имена входных параметров x
    output_type: str         # Тип выхода (например, "float", "list")
    param_names: List[str]   # Имена параметров λ

class FunctionMetadata(BaseModel):
    name: str
    signature: FunctionSignature
    description: Optional[str] = None

class FunctionDefinition(BaseModel):
    metadata: FunctionMetadata
    code: str  # Исходный код функции в виде строки

class FunctionExecutionRequest(BaseModel):
    function_name: str
    inputs: Dict[str, Any]      # x
    parameters: Dict[str, Any]  # λ

class FunctionExecutionResponse(BaseModel):
    result: Any
    function_name: str
    executed_at: str