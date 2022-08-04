from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
import yaml

from . import ssh
from . import utils

import os
os.chdir('./backend')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test():
    return {'test_result': 'kslee'}

@app.on_event("startup")
@app.get("/reload_id")
def read_info():
    global server_ids
    server_ids = utils.read_server_ids('/app/config/server_ids.conf')

@app.on_event("startup")
@repeat_every(seconds=60*30)
@app.get("/space/refresh")
def ssh_space():
    result = ssh.get_spaces(server_ids)
    ctime = utils.getTime()
    with open('logs/space_%s.yaml' % ctime, 'w') as fp:
        yaml.dump(result, fp, sort_keys=False)
    return {'time': ctime, 'data': result}

@app.on_event("startup")
@repeat_every(seconds=60*30)
@app.get("/memory/refresh")
def ssh_memory():
    result = ssh.get_memories(server_ids)
    ctime = utils.getTime()
    with open('logs/memory_%s.yaml' % ctime, 'w') as fp:
        yaml.dump(result, fp, sort_keys=False)
    return {'time': ctime, 'data': result}

@app.on_event("startup")
@repeat_every(seconds=60*30)
@app.get("/gpu/refresh")
def ssh_memory():
    result = ssh.get_gpus(server_ids)
    ctime = utils.getTime()
    with open('logs/gpu_%s.yaml' % ctime, 'w') as fp:
        yaml.dump(result, fp, sort_keys=False)
    return {'time': ctime, 'data': result}

@app.on_event("startup")
@repeat_every(seconds=60*30)
@app.get("/container/refresh")
def ssh_container():
    result = ssh.get_containers(server_ids)
    print('GET CONTAINER:', result)
    ctime = utils.getTime()
    with open('logs/container_%s.yaml' % ctime, 'w') as fp:
        yaml.dump(result, fp, sort_keys=False)
    return {'time': ctime, 'data': result}

@app.get("/space")
def read_space():
    fname = utils.getRecentFile('space')
    with open(fname, 'r') as fp:
        result = yaml.safe_load(fp)
    return {'time': fname.replace('logs/space_', '').replace('.yaml', ''), 'data': result}

@app.get("/memory")
def read_memory():
    fname = utils.getRecentFile('memory')
    with open(fname, 'r') as fp:
        result = yaml.safe_load(fp)
    return {'time': fname.replace('logs/memory_', '').replace('.yaml', ''), 'data': result}

@app.get("/gpu")
def read_gpu():
    fname = utils.getRecentFile('gpu')
    with open(fname, 'r') as fp:
        result = yaml.safe_load(fp)
    return {'time': fname.replace('logs/gpu_', '').replace('.yaml', ''), 'data': result}

@app.get("/space/detail")
def ssh_space_detailed(host: str):
    matched = [server_id for server_id in server_ids if server_id.split()[0] == host]
    if len(matched) != 1:
        raise HTTPException(status_code=400, detail=f"There is not only 1 matched server id: {len(matched)} found.")
    result = ssh.get_space_detailed(matched[0])
    return result
    
@app.get("/gpu/detail")
def ssh_gpu_detailed(host: str):
    matched = [server_id for server_id in server_ids if server_id.split()[0] == host]
    if len(matched) != 1:
        raise HTTPException(status_code=400, detail=f"There is not only 1 matched server id: {len(matched)} found.")
    result = ssh.get_gpu_detailed(matched[0])
    return result
    
@app.get("/gpu/processes")
def ssh_gpu_processes(host: str):
    matched = [server_id for server_id in server_ids if server_id.split()[0] == host]
    if len(matched) != 1:
        raise HTTPException(status_code=400, detail=f"There is not only 1 matched server id: {len(matched)} found.")
    result = ssh.get_gpu_processes(matched[0])
    return result

@app.get("/container")
def read_container():
    fname = utils.getRecentFile('container')
    with open(fname, 'r') as fp:
        result = yaml.safe_load(fp)
    return {'time': fname.replace('logs/container_', '').replace('.yaml', ''), 'data': result}

@app.get("/container/detail")
def ssh_container_detailed(host: str):
    matched = [server_id for server_id in server_ids if server_id.split()[0] == host]
    if len(matched) != 1:
        raise HTTPException(status_code=400, detail=f"There is not only 1 matched server id: {len(matched)} found.")
    result = ssh.get_container_detailed(matched[0])
    return result
    
