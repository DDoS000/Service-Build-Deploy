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

# class Role(str, enum.Enum):
#     USER = 'USER'
#     ADMIN = 'ADMIN'
#     STORE = 'STORE'


# class Registered_by(str, enum.Enum):
#     EMAIL = 'EMAIL'
#     FACEBOOK = 'FACEBOOK'


# users = Table(
#     "users", metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("email", String(50), nullable=False),
#     Column("name", String(50), nullable=False),
#     Column("registered_at", DateTime(timezone=True), server_default=func.now()),
#     Column("registered_by", Enum(Registered_by), nullable=False,
#            server_default=f"{Registered_by.FACEBOOK.value}"),
#     Column("password", String(200), nullable=False),
#     Column("role", Enum(Role), nullable=False,
#            server_default=f"{Role.USER.value}"),
#     Column("phone", String(10), nullable=False),
#     Column("status", String(1), nullable=False, server_default='1')
# )

# line_notify = Table(
#     "line_notify", metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("stores_id", Integer, ForeignKey("stores.id"), nullable=False),
#     Column("token", String(100), nullable=False),
#     Column("code", String(30), nullable=False),
# )


# class store_status(str, enum.Enum):
#     VERIFIED = 'VERIFIED'
#     BAN = 'BAN'
#     WAITING = 'WAITING'


# stores = Table(
#     "stores", metadata,
#     Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("name", String(50), nullable=False),
#     Column("status", Enum(store_status), nullable=False,
#            server_default=f"{store_status.WAITING.value}"),
#     Column("created_at", DateTime(timezone=True), server_default=func.now()),
#     Column("address", TEXT, nullable=False),
#     Column("amphoe", String(60), nullable=False),  # ตําบล
#     Column("district", String(60), nullable=False),  # อำเภอ
#     Column("province", String(60), nullable=False),  # จังหวัด
#     Column("postcode", String(10), nullable=False),  # รหัสไปรษณีย์
#     Column("latitude", String(20), nullable=False),
#     Column("longitude", String(20), nullable=False),
#     Column("facebook", TEXT, nullable=False),
#     Column("phone", String(20), nullable=False),
#     Column("description", TEXT, nullable=False),
#     Column("image", TEXT, nullable=False),
#     Column("open_status", Boolean, nullable=False,
#            server_default='0'),  # 0=False 1=True
#     Column("open_time", DateTime, nullable=False),
#     Column("close_time", DateTime, nullable=False),
#     Column("open_day", TEXT, nullable=False),
#     Column("rating", String(50), nullable=True, server_default='0'),
#     Column("rating_count", String(50), nullable=True, server_default='0'),
#     Column("rating_average", String(50), nullable=True, server_default='0'),
#     Column("pay_half", Boolean, nullable=False),  # 0=False 1=True
#     Column("pay_cash", Boolean, nullable=False),  # 0=False 1=True
# )

# store_banking = Table(
#     "store_banking", metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("store_id", Integer, ForeignKey("stores.id"), nullable=False),
#     Column("bank_name", String(50), nullable=False),
#     Column("bank_number", String(50), nullable=False),
#     Column("bank_owner", String(50), nullable=False),
# )


# class pd_shipping(str, enum.Enum):
#     PREORDER = 'PREORDER'
#     DELIVERY = 'DELIVERY'


# #  Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
# products_preorders = Table(
#     "products_preorders", metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("stores_id", Integer, ForeignKey("stores.id"), nullable=False),
#     Column("pd_title", String(50), nullable=False),
#     Column("pd_image", TEXT, nullable=True),
#     Column("pd_price", Integer, nullable=False),
#     Column("pd_category", String(50), nullable=False),
#     Column("pd_amount", Integer, nullable=False),
#     Column("pd_option", JSON, nullable=False),
#     Column("pd_delivery_round", JSON, nullable=False),
#     Column("pd_shipping", Enum(pd_shipping), nullable=False),
#     Column("pd_open", Boolean, nullable=False,
#            server_default='1'),  # 0=False 1=True
#     Column("create_at", DateTime(timezone=True), server_default=func.now()),
# )

# category = Table(
#     "category", metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("category_name", String(50), nullable=False),  # 0=False 1=True
# )

# class oreder_status(str, enum.Enum):
#     AWAITING_PAYMENT = 'AWAITING_PAYMENT'
#     FINISHED_PAYMENT = 'FINISHED_PAYMENT'
#     WAITING = 'WAITING'
#     CONFIRM = 'CONFIRM'
#     SENDING = 'SENDING'
#     CANCEL_BY_USER = 'CANCEL_BY_USER'
#     CANCEL_BY_STORE = 'CANCEL_BY_STORE'

# order_poreorders = Table(
#     "order_preorders", metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("stores_id", Integer, ForeignKey("stores.id"), nullable=False),
#     Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
#     Column("state", Enum(oreder_status), nullable=False, server_default=f"{oreder_status.WAITING.value}"),
#     Column("product", JSON, nullable=False),
#     Column("pd_amount", Integer, nullable=False),
#     Column("od_price", Integer, nullable=False),
#     Column("create_at", DateTime(timezone=True), server_default=func.now())
# )

# user_address = Table(
#     "user_addres", metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
#     Column("location_name", String(60), nullable=False),
#     Column("address", TEXT, nullable=False),
#     Column("amphoe", String(60), nullable=False),  # ตําบล
#     Column("district", String(60), nullable=False),  # อำเภอ
#     Column("province", String(60), nullable=False),  # จังหวัด
#     Column("postcode", String(10), nullable=False),  # รหัสไปรษณีย์
#     Column("name_customer", String(100), nullable=False),
# )
