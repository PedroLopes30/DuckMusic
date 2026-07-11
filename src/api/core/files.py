from fastapi import UploadFile
from uuid import uuid4
from os import makedirs 
from os.path import splitext , join , getsize
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

def get_file_path(file_name : str)->str:
    return join(settings.UPLOAD_DIR , file_name)

def get_file_chunk(file_name : str , start : int , end : int , size_block : int = 1024 * 64 ):
    with open(get_file_path(file_name) , "rb") as file:
        file.seek(start)
        remaining_bytes = end - start + 1
        while remaining_bytes:
            block = min(size_block , remaining_bytes)
            data = file.read(block)
            if not data:
                break
            
            remaining_bytes -= len(data)
            yield data
            
def get_file_size(file_name  : str) -> int:
    path = get_file_path(file_name)
    return getsize(path)