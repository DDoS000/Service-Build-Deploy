from email.policy import default
import json
from sre_constants import SUCCESS
from typing import Text
from xml.etree.ElementInclude import default_loader
from pydantic import BaseModel, EmailStr
import enum

from sqlalchemy import Column, DateTime, String, Table, ForeignKey, Boolean, \
    Enum, Index, func, JSON, MetaData, Integer, TEXT, Sequence, CHAR, text
from sqlalchemy.sql.expression import null

metadata = MetaData()


class Status_build(str, enum.Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    WAIT = "WAIT"
    RUNNING = "RUNNING"


registrys = Table(
    "registrys", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer),
    Column("PJ_UUID", TEXT),
    Column("PJ_NAME", TEXT),
    Column("PJ_DESC", TEXT),
    Column("PJ_PORTS_MAP", JSON),
    Column("status", Enum(Status_build)),
)

setting = Table(
    "settings", metadata,
    Column("Port_black_list", JSON),  # default=[]
    Column("Max_Port", Integer),  # default=65535
    Column("start_port", Integer),  # default=1024
    Column("end_port", Integer),  # default=65535
)