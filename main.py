import shutil
import datetime
import pandas as pd
import uvicorn
import xml.etree.ElementTree as ET
from fastapi import FastAPI, UploadFile, File, Form, Request, Response
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from pip._vendor.requests.packages import package
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
    # print(df)
    data = df.to_json(orient='split')
    # print(data)
    return {"data": data}

@app.post("/convertxlsxtocsv/")
async def create_upload_file(projectName: str, file: UploadFile, request):
    ts = datetime.datetime.now().strftime("%m%d_%H%M%S")
    path = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename)
    await save_upload_file(file, path)
    path2 = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename+".csv")
    df = pd.read_excel(path)
    # print(df)
    df.to_csv(path2)
    data = df.to_json(orient='split')
    # print(data)
    return {"data": data}

@app.post("/convertjsontoxml/")
async def create_upload_file(projectName: str, file: UploadFile, request):
    ts = datetime.datetime.now().strftime("%m%d_%H%M%S")
    path = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename)
    await save_upload_file(file, path)
    df = pd.read_json(path, orient='index')
    path2 = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename+".xml")
    df.to_xml(path2)
    data = df.to_json(orient='split')
    return {"data": data}

@app.post("/convertxmltoxlsx/")
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
    path2 = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename+".xlsx")

    # print(df)
    df.to_excel(path2)
    data = df.to_json(orient='split')
    # print(data)
    return {"data": data}

@app.post("/convertcsvtojson/")
async def create_upload_file(projectName: str, file: UploadFile, request):
    ts = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    path = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename)
    await save_upload_file(file, path)
    path2 = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename + ".json")
    # csvpath = Path('D:/output/'  + ts + '_' + file.filename + ".json")
    csvfile= file.filename
    df = pd.read_csv(path)
    df.to_json(path2)
    data = df.to_json(orient='split')
    return {"filename": file.filename,"csvdata": data}

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
    # print(data)
    return {"data": data}

@app.post("/uploadJsonfile/")
async def create_upload_file(projectName: str, file: UploadFile, request):
    ts = datetime.datetime.now().strftime("%m%d_%H%M%S")
    path = Path('D:/aryabhatta/training' + '/Regression/' + projectName + '/data/' + ts + '_' + file.filename)
    await save_upload_file(file, path)
    df = open(path, 'r').read()
    # print(df)
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