from fastapi import UploadFile
from uuid import uuid4
from os import makedirs 
from os.path import splitext , join
from shutil import copyfileobj

from api.configs.settings import settings


def save_file(file : UploadFile , dirPath : str)->str:
    ext = splitext(file.filename)[1]
    filename = f"{uuid4().hex}{ext}"
    filePath = join(dirPath , filename)
    absoluteFilePath = join(settings.UPLOAD_DIR , filePath)
    makedirs(join(settings.UPLOAD_DIR , dirPath) ,exist_ok=True)
    
    with open(absoluteFilePath , "wb") as buffer:
        copyfileobj(file.file , buffer)
    
    return filePath