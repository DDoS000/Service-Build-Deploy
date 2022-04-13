import json
import socket

import docker
from utils.dbUtil import database


# * Get Docker Api
client = docker.APIClient(base_url='tcp://localhost:2375')


async def get_setting():
    query = "SELECT * FROM settings"
    return await database.fetch_one(query)


async def get_all_pj_ports():
    query = "SELECT PJ_PORTS_MAP FROM registrys"
    return await database.fetch_all(query)


def create_new_registrys(user_id, PJ_NAME, PJ_DESC, PJ_PORTS_MAP):
    query = "INSERT INTO registrys (user_id, PJ_NAME, PJ_DESC, PJ_PORTS_MAP)VALUES (:user_id, :PJ_NAME, :PJ_DESC, :PJ_PORTS_MAP)"
    return database.execute(query, values={'user_id': user_id, 'PJ_NAME': PJ_NAME, 'PJ_DESC': PJ_DESC, 'PJ_PORTS_MAP': json.dumps(PJ_PORTS_MAP, ensure_ascii=False)})


def get_all_registrys():
    query = "SELECT * FROM registrys"
    return database.fetch_all(query)


def check_registrys_uuid(id):
    query = "SELECT PJ_UUID FROM registrys WHERE id=:id"
    return database.fetch_one(query, values={'id': id})


async def CHECK_FREE_PORT_IN_RANGE(PJ_PORTS_MAP):
    # port=8070, max_port=9000, port_in_use=[8081, 8082, 8083, 8084]

    # เช็คPort ที่ต้องการจาก json port ที่เป็น public
    desired_port = 0
    for i in PJ_PORTS_MAP:
        if i['port'] == "public":
            desired_port += 1

    free_port = []
    port_black_list = []

    # เช็คPort ที่ใช้ไปแล้วจากของPJ จาก DB
    pj_port = await get_all_pj_ports()
    for all_port in pj_port:
        for one_port in json.loads(all_port[0]):
            if one_port.get('port_number'):
                port_black_list.append(one_port.get('port_number'))

    # เช็คPort ที่ใช้ไปแล้วจาก docker
    for i in client.containers(all=True):
        for s in i['Ports']:
            if s.get('PublicPort'):
                port_black_list.append(s.get('PublicPort'))

    # เช็คPort ที่ติดblacklist จาก DB
    st = await get_setting()
    port = int(st.start_port)
    for ports in json.loads(st.Port_black_list):
        port_black_list.append(ports)
    print("port_black_list", sorted(port_black_list))

    # เช็คPort ที่ว่างในเครืองเซิฟ
    while port <= int(st.end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if port in port_black_list:
                port += 1
                # print("inblacklist", port)
                continue

            if s.connect_ex(('localhost', port)) == 0:
                # print(f"inUse {port}")
                port += 1
            else:
                # print(f"Free Port{port}")
                if port in port_black_list:
                    pass
                    # print(f"Ports in blacklist {port}")
                else:
                    free_port.append(port)
                if len(free_port) == desired_port:
                    free_port_in_use = 0
                    for i in PJ_PORTS_MAP:
                        if i['port'] == "public":
                            i['port_number'] = free_port[free_port_in_use]
                            free_port_in_use += 1
                    return PJ_PORTS_MAP
                else:
                    port += 1
