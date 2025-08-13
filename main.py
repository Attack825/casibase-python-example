# Copyright 2025 The Casibase Authors. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from casibase_python_sdk.store import Store
from casibase_python_sdk.record import Record
from casibase_python_sdk.task import Task
import logging

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Casibase Python API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/web", StaticFiles(directory="./web/dist", html=True), name="web")


# Serve index.html for root path
@app.get("/", include_in_schema=False)
async def index(request: Request):
    dist_dir = os.path.abspath(os.path.join(os.getcwd(), "./web/dist"))
    return FileResponse(os.path.join(dist_dir, "index.html"))


class RecordCreate(BaseModel):
    owner: str
    name: str
    createdTime: str
    organization: Optional[str] = None
    clientIp: Optional[str] = None
    userAgent: Optional[str] = None
    user: Optional[str] = None
    method: Optional[str] = None
    requestUri: Optional[str] = None
    action: Optional[str] = None
    language: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "owner": "admin",
                "name": "a5d92f93-e0b9-48e0-a4d0-dc21d7908fe8",
                "createdTime": "2024-03-19T10:00:00Z",
            }
        }


class StoreCreate(BaseModel):
    owner: str
    name: str
    createdTime: str
    displayName: str
    storageProvider: Optional[str] = None
    storageSubpath: Optional[str] = None
    modelProvider: Optional[str] = None
    embeddingProvider: Optional[str] = None
    state: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "owner": "admin",
                "name": "store_7lxjmh",
                "createdTime": "2024-03-19T10:00:00Z",
                "displayName": "store_7lxjmh",
                "storageProvider": "provider-storage-built-in",
            }
        }


class TaskCreate(BaseModel):
    owner: str
    name: str
    createdTime: str
    displayName: str
    provider: Optional[str] = None
    type: Optional[str] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    status: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "owner": "admin",
                "name": "task_uhbf8m",
                "createdTime": "2024-03-19T10:00:00Z",
                "displayName": "task_uhbf8m",
            }
        }


sdk = Config.SDK


# API Routes
@app.get("/api/get-records", tags=["records"], summary="get records")
async def get_records(page_size: str = "100", p: str = "1"):
    try:
        records = sdk.get_records(page_size, p)
        return {
            "status": "success",
            "data": {
                "items": [record.__dict__ for record in records],
                "total": len(records),
            },
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/get-record", tags=["records"], summary="get record")
async def get_record(id: str):
    try:
        record = sdk.get_record(id)
        return {"status": "success", "data": record.__dict__ if record else None}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/add-record", tags=["records"], summary="add record")
async def add_record(record_data: RecordCreate):
    try:
        record = Record.from_dict(record_data.model_dump())
        result = sdk.add_record(record)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/update-record", tags=["records"], summary="update record")
async def update_record(record_data: RecordCreate):
    try:
        record = Record.from_dict(record_data.model_dump())
        result = sdk.update_record(record)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/delete-record", tags=["records"], summary="delete record")
async def delete_record(id: str):
    try:
        record = sdk.get_record(id)
        if record:
            result = sdk.delete_record(record)
            return {"status": "success", "data": result}
        return {"status": "error", "message": "Record not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/get-stores", tags=["stores"], summary="get stores")
async def get_stores(page_size: int = 10, p: int = 1):
    try:
        stores = sdk.get_stores(page_size, p)
        return {
            "status": "success",
            "data": {
                "items": [store.__dict__ for store in stores],
                "total": len(stores),
            },
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/get-store", tags=["stores"], summary="get store")
async def get_store(id: str):
    try:
        owner, name = id.split("/")
        store = sdk.get_store(owner, name)
        return {"status": "success", "data": store.__dict__ if store else None}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/add-store", tags=["stores"], summary="add store")
async def add_store(store_data: StoreCreate):
    try:
        store = Store.from_dict(store_data.model_dump())
        if store_data.storageProvider:
            store.storageProvider = store_data.storageProvider
        if store_data.storageSubpath:
            store.storageSubpath = store_data.storageSubpath
        result = sdk.add_store(store)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/update-store", tags=["stores"], summary="update store")
async def update_store(store_data: StoreCreate):
    try:
        store = Store.from_dict(store_data.model_dump())
        if store_data.storageProvider:
            store.storageProvider = store_data.storageProvider
        if store_data.storageSubpath:
            store.storageSubpath = store_data.storageSubpath
        result = sdk.update_store(store)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/delete-store", tags=["stores"], summary="delete store")
async def delete_store(id: str):
    try:
        owner, name = id.split("/")
        store = sdk.get_store(owner, name)
        if store:
            result = sdk.delete_store(store)
            return {"status": "success", "data": result}
        return {"status": "error", "message": "Store not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/get-tasks", tags=["tasks"], summary="get tasks")
async def get_tasks(owner: str):
    try:
        tasks = sdk.get_tasks(owner)
        return {"status": "success", "data": [task.__dict__ for task in tasks]}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/get-task", tags=["tasks"], summary="get task")
async def get_task(id: str):
    try:
        owner, name = id.split("/")
        task = sdk.get_task(owner, name)
        return {"status": "success", "data": task.__dict__ if task else None}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/add-task", tags=["tasks"], summary="add task")
async def add_task(task_data: TaskCreate):
    try:
        task = Task.from_dict(task_data.model_dump())
        if task_data.provider:
            task.provider = task_data.provider
        if task_data.type:
            task.type = task_data.type
        result = sdk.add_task(task)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/update-task", tags=["tasks"], summary="update task")
async def update_task(task_data: TaskCreate):
    try:
        task = Task.from_dict(task_data.model_dump())
        if task_data.provider:
            task.provider = task_data.provider
        if task_data.type:
            task.type = task_data.type
        result = sdk.update_task(task)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/delete-task", tags=["tasks"], summary="delete task")
async def delete_task(id: str):
    try:
        owner, name = id.split("/")
        task = sdk.get_task(owner, name)
        if task:
            result = sdk.delete_task(task)
            return {"status": "success", "data": result}
        return {"status": "error", "message": "Task not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/{path:path}", include_in_schema=False)
async def serve_static(request: Request, path: str):
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")

    dist_dir = os.path.abspath(os.path.join(os.getcwd(), "./web/dist"))
    file_path = os.path.join(dist_dir, path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse(os.path.join(dist_dir, "index.html"))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
