import shutil
import datetime
import pandas as pd
import uvicorn
import xml.etree.ElementTree as ET
from fastapi import FastAPI, UploadFile, File, Form, Request, Response
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
import os
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadXlsxFile/")
async def create_upload_file(projectName: str, file: UploadFile, request):
    ts = datetime.datetime.now().strftime("%m%d_%H%M%S")
    path = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename)
    await save_upload_file(file, path)
    df = pd.read_excel(path)
    print(df)
    data = df.to_json(orient='split')
    print(data)
    return {"data": data}

@app.post("/uploadXmlFile/")
async def create_upload_file(projectName: str, file: UploadFile, request):
    ts = datetime.datetime.now().strftime("%m%d_%H%M%S")
    path = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename)
    await save_upload_file(file, path)
    xml_data = open(path, 'r').read()
    root = ET.XML(xml_data)  # Parse XML

    data = []
    cols = []
    for i, child in enumerate(root):
        data.append([subchild.text for subchild in child])
        cols.append(child.tag)

    df = pd.DataFrame(data).T  # Write in DF and transpose it
    df.columns = cols  # Update column names
    data = df.to_json(orient='split')
    print(data)
    return {"data": data}

@app.post("/uploadJsonfile/")
async def create_upload_file(projectName: str, file: UploadFile, request):
    ts = datetime.datetime.now().strftime("%m%d_%H%M%S")
    path = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename)
    await save_upload_file(file, path)
    df = open(path, 'r').read()
    print(df)
    return {df}

@app.post("/uploadfile/")
async def create_upload_file(projectName: str, file: UploadFile, request):
    ts = datetime.datetime.now().strftime("%m%d_%H%M%S")
    path = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename)
    await save_upload_file(file, path)
    return {"filename": file.filename}


async def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        upload_file.file.seek(0)
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


if __name__ == '_main_':
    uvicorn.run(app, host="0.0.0.0", port=8888)