from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import datetime
from storage import FunctionStorage
from executor import execute_function
from models import (
    FunctionDefinition,
    FunctionMetadata,
    FunctionExecutionRequest,
    FunctionExecutionResponse
)

app = FastAPI(title="Parametric Function Manager", version="1.0")

storage = FunctionStorage()

@app.get("/")
async def root():
    return {"message": "Welcome to Parametric Function Manager"}

@app.post("/functions/", response_model=FunctionMetadata)
async def create_function(func_def: FunctionDefinition):
    if func_def.metadata.name in storage.functions:
        raise HTTPException(status_code=409, detail="Функция с таким именем уже существует")
    storage.save_function(func_def)
    return func_def.metadata

@app.get("/functions/{function_name}", response_model=FunctionDefinition)
async def get_function(function_name: str):
    func = storage.get_function(function_name)
    if not func:
        raise HTTPException(status_code=404, detail="Функция не найдена")
    return func

@app.get("/functions/", response_model=List[FunctionMetadata])
async def list_functions():
    return [f.metadata for f in storage.functions.values()]

@app.put("/functions/{function_name}", response_model=FunctionMetadata)
async def update_function(function_name: str, func_def: FunctionDefinition):
    if func_def.metadata.name != function_name:
        raise HTTPException(status_code=400, detail="Имя функции в метаданных не совпадает с URL")
    if function_name not in storage.functions:
        raise HTTPException(status_code=404, detail="Функция не найдена")
    storage.save_function(func_def)
    return func_def.metadata

@app.delete("/functions/{function_name}")
async def delete_function(function_name: str):
    if not storage.delete_function(function_name):
        raise HTTPException(status_code=404, detail="Функция не найдена")
    return {"message": f"Функция '{function_name}' удалена"}

@app.post("/execute/", response_model=FunctionExecutionResponse)
async def execute_function_endpoint(request: FunctionExecutionRequest):
    func = storage.get_function(request.function_name)
    if not func:
        raise HTTPException(status_code=404, detail="Функция не найдена")

    try:
        result = execute_function(func, request.inputs, request.parameters)
        return FunctionExecutionResponse(
            result=result,
            function_name=request.function_name,
            executed_at=datetime.datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/functions/{function_name}/info", response_model=FunctionMetadata)
async def get_function_info(function_name: str):
    func = storage.get_function(function_name)
    if not func:
        raise HTTPException(status_code=404, detail="Функция не найдена")
    return func.metadata