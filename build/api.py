from fastapi import UploadFile, File, status, Form, Query
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from template import service as template_service
from template import schema
import os
import uuid
from zipfile import ZipFile

build_router = InferringRouter()
IMAGEDIR = "./build/projects/"


@cbv(build_router)
class ProductAPI:
    @build_router.post("/registry/upload", status_code=201)
    async def upload(self, file: UploadFile = File(...)):

        uuids = uuid.uuid4()
        file.filename = f"{uuids}.zip"
        contents = await file.read()
        
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)
        
        os.mkdir(os.path.join(IMAGEDIR, f"{uuids}"))

        with ZipFile(f"{IMAGEDIR}{file.filename}", 'r') as zip:
            zip.printdir()
            zip.extractall(f"{IMAGEDIR}/{uuids}")

        os.remove(f"{IMAGEDIR}{file.filename}")

        os.system(f"docker-compose -f {IMAGEDIR}/{uuids}/docker-compose.yml up -d")

        # TODO: Gen UUID Save in to db

        return {"file_name": file.filename}

    # @build_router.get("/test")
    # async def zip(self, name: str):
    #     with ZipFile(f"{IMAGEDIR}{name}", 'r') as zip:
    #         zip.printdir()
    #         print('Extracting all the files now...')
    #         zip.extractall(f"{IMAGEDIR}")
    #         print('Done!')
    #     return 'Done!'
