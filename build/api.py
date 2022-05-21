import asyncio
import json
import os
import re
import subprocess
import sys
import threading
import uuid
from zipfile import ZipFile

from fastapi import BackgroundTasks, File, Form, UploadFile, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic.types import Json

from build import service

build_router = InferringRouter()
IMAGEDIR = "./build/projects/"


# async def build(uuids, file):
#     file.filename = f"{uuids}.zip"
#     contents = await file.read()
#     with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
#         f.write(contents)
#     os.mkdir(os.path.join(IMAGEDIR, f"{uuids}"))
#     with ZipFile(f"{IMAGEDIR}{file.filename}", 'r') as zip:
#         # zip.printdir()
#         zip.extractall(f"{IMAGEDIR}/{uuids}")
#     os.remove(f"{IMAGEDIR}{file.filename}")
#     with open(f"{IMAGEDIR}/{uuids}/log.log", 'wb') as f:
#         process = subprocess.Popen(f"docker-compose -f {IMAGEDIR}/{uuids}/docker-compose.yml up -d",
#                                    shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, start_new_session=True)
#         for c in iter(lambda: process.stdout.read(1), b''):
#             sys.stdout.buffer.write(c)
#             f.write(c)


async def step_fuction(pj_id, uuids):
    check_pj_uuid = await service.check_registrys_uuid(pj_id)
    if(check_pj_uuid.PJ_UUID):
        print("PJ_UUID", check_pj_uuid.PJ_UUID)
    # return uuids
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)

    # loop.run_until_complete(build(uuids, file))
    # loop.close()


# def create_Thread(uuids, file):
#     threading.Thread(
#         name=uuids, target=lambda: step_fuction(uuids, file)).start()


async def unzips(uuids, file):
    file.filename = f"{uuids}.zip"
    contents = await file.read()
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    os.mkdir(os.path.join(IMAGEDIR, f"{uuids}"))
    with ZipFile(f"{IMAGEDIR}{file.filename}", 'r') as zip:
        # zip.printdir()
        zip.extractall(f"{IMAGEDIR}/{uuids}")
    os.remove(f"{IMAGEDIR}{file.filename}")
    return uuids


async def build_test(uuids):
    with open(f"{IMAGEDIR}/{uuids}/log.log", 'wb') as f:
        process = subprocess.Popen(f"docker-compose -f {IMAGEDIR}/{uuids}/docker-compose.yml up -d",
                                   shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, start_new_session=True)
    for c in iter(lambda: process.stdout.read(1), b''):
        sys.stdout.buffer.write(c)
        f.write(c)
    return


@cbv(build_router)
class Upload_build:
    @build_router.post("/registry/upload", status_code=201)
    async def upload(self,
                     background_tasks: BackgroundTasks,
                     pj_id: int = Form(...),
                     #  file: UploadFile = File(...)
                     ):
        uuids = uuid.uuid4()

        # background_tasks.add_task(step_fuction, pj_id, uuids, file)
        background_tasks.add_task(step_fuction, pj_id, uuids)
        # TODO: Save in to db

        return f"Create"

    @build_router.post("/registry/create_pj", status_code=201)
    async def create_project(self,
                             user_id: int = Form(...),
                             PJ_NAME: str = Form(...),
                             PJ_DESC: str = Form(...),
                             PJ_PORTS_MAP: Json = Form(...)
                             ):

        result_port = await service.CHECK_FREE_PORT_IN_RANGE(PJ_PORTS_MAP)
        PJ_ID = await service.create_new_registrys(user_id, PJ_NAME, PJ_DESC, result_port)
        return {
            "status_code": status.HTTP_201_CREATED,
            "detail": 'create registrys successfully',
            "data": {"PJ_ID": PJ_ID, "PJ_NAME": PJ_NAME, "PJ_DESC": PJ_DESC, "PJ_PORTS_MAP": result_port}
        }

    @build_router.get("/registrys")
    async def registrys(self):
        datas = await service.get_all_registrys()
        return {
            "status_code": status.HTTP_200_OK,
            "data": datas
        }

    # @build_router.get("/test_cmd")
    # async def cmd(self, command: str):
    #     with open('test.log', 'wb') as f:
    #         process = subprocess.Popen(
    #             command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, start_new_session=True)

    #         for c in iter(lambda: process.stdout.read(1), b''):
    #             sys.stdout.buffer.write(c)
    #             f.write(c)

    # @build_router.get("/test")
    # async def zip(self, name: str):
    #     with ZipFile(f"{IMAGEDIR}{name}", 'r') as zip:
    #         zip.printdir()
    #         print('Extracting all the files now...')
    #         zip.extractall(f"{IMAGEDIR}")
    #         print('Done!')
    #     return 'Done!'

    # @build_router.post("/registry/test", status_code=201)
    # async def zip(self, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    #     if not file:
    #         return {"message": "No upload file sent"}
    #     else:
    #         uuids = uuid.uuid4()
    #         # background_tasks.add_task(unzips, uuids, file)
    #         return {"message": "upload task" "{uuids}"}

    # @build_router.post("/registry/check_port", status_code=200)
    # async def check_port(self):
    #     result = await service.CHECK_FREE_PORT_IN_RANGE(3)
    #     return result
