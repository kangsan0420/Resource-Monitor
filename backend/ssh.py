# python 3.10

import paramiko
import re
from tqdm.auto import tqdm
from . import utils
import itertools

# ssh.py
def bash(host_user_pw, command):
    host, user, pw = host_user_pw.split()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    try:
        cli.connect(host, port=22, username=user, password=pw, allow_agent=False)
        stdin, stdout, stderr = cli.exec_command(command)
        if command.startswith('sudo'):
            stdin.write(f'{pw}\n')
        response = stdout.read().decode('U8').strip('\n')
    except Exception as e:
        response = f'Error[{host}]: {e}'
    finally:
        print(f"SSH on [{host_user_pw.split()[0]}]$ {command} => \n{response}")
        cli.close()
    return response


def get_memories(server_ids):
    rtn = []
    for server_id in tqdm(server_ids):
        info = {'host':server_id.split()[0]}
        txt = bash(server_id, 'free -h')
        cols, vals, _ = txt.split('\n')
        for k, v in zip(cols.split(), vals.split()[1:]):
            info[k] = f"{utils.convert_to_gigabytes(v):.0f}GB"
        rtn.append(info)
    return rtn


def get_gpu_processes(server_id):
    exp = '^\|\s+(?P<gpu>\d+)\s+N/A\s+N/A\s+(?P<pid>\d+)\s+C\s+(?P<name>[\S]*)\s+(?P<used>\d+)MiB \|$'
    txt = bash(server_id, 'nvidia-smi')
    g = re.findall(exp, txt, flags=re.MULTILINE) or []
    g = [{'GPU': int(gpu), 'PID': int(pid), 'Name': name, 'Used': utils.megabytes_to_formatted(int(alloc))} for gpu, pid, name, alloc in g]
    return g

def get_gpu_detailed(server_id):
    txt = bash(server_id, 'nvidia-smi')
    rtn_2d = re.findall('\|\s+(\d+M)iB / (\d+M)iB\s+\|', txt, flags=re.MULTILINE)
    rtn = []
    for gid, (used, size) in enumerate(rtn_2d):
        rtn.append({
            'Num': gid,
            'Size': utils.gigabytes_to_formatted(utils.convert_to_gigabytes(size)),
            'Used': utils.gigabytes_to_formatted(utils.convert_to_gigabytes(used))
        })
    return rtn

def get_gpus(server_ids):
    rtn = []
    for server_id in tqdm(server_ids):
        info = {'host':server_id.split()[0], 'Size':0, 'Used':0}
        txt = bash(server_id, 'nvidia-smi')
        rtn_2d = re.findall('\|\s+(\d+M)iB / (\d+M)iB\s+\|', txt, flags=re.MULTILINE)
        for used, size in rtn_2d:
            info['Size'] += utils.convert_to_gigabytes(size)
            info['Used'] += utils.convert_to_gigabytes(used)
        info['Size'] = utils.gigabytes_to_formatted(info['Size'])
        info['Used'] = utils.gigabytes_to_formatted(info['Used'])
        rtn.append(info)
    return rtn


def get_space_detailed(server_id):
    txt = bash(server_id, 'df -h')
    rtn_2d = [line.split() for line in txt.replace('Mounted on', 'Mount').split('\n')]
    dicts = []
    for fs, size, used, avail, use, mount in rtn_2d[1:]:
        if 'tmpfs' not in fs:
            size, used, avail = map(lambda x: x+'B', (size, used, avail))
            dicts.append({k:v for k, v in zip(rtn_2d[0], (fs, size, used, avail, use, mount))})
    return dicts

def get_spaces(server_ids):
    rtn = []
    for server_id in tqdm(server_ids):
        info = {'host':server_id.split()[0], 'Size':0, 'Used':0, 'Avail':0}
        txt = bash(server_id, 'df -h')
        rtn_2d = [line.split() for line in txt.split('\n')[1:]]
        for fs, size, used, avail, use, mount in rtn_2d:
            if 'tmpfs' not in fs:
                info['Size'] += utils.convert_to_gigabytes(size)
                info['Used'] += utils.convert_to_gigabytes(used)
                info['Avail'] += utils.convert_to_gigabytes(avail)
        info['Size'] = utils.gigabytes_to_formatted(info['Size'])
        info['Used'] = utils.gigabytes_to_formatted(info['Used'])
        info['Avail'] = utils.gigabytes_to_formatted(info['Avail'])
        rtn.append(info)
    return rtn

def get_containers(server_ids):
    rtn = []
    for server_id in tqdm(server_ids):
        lines = bash(server_id, 'docker ps -a').split('\n')
        exited, total = len(list(filter(lambda x: ' Exited (' in x, lines))), len(lines)-1
        active = total - exited
        rtn.append({'Host': server_id.split()[0], 'Active': active, 'Exited': exited})
    return rtn

def get_container_detailed(server_id, sizes=True):
    items = ['CONTAINER ID', 'IMAGE', 'COMMAND', 'CREATED', 'STATUS', 'PORTS', 'NAMES', 'SIZE']
    lines = bash(server_id, 'docker ps --no-trunc' + ' -as' if sizes else '').split('\n')
    indices = [lines[0].find(item) for item in items] + [9999]
    struct = [[line[a:b].strip() for a, b in itertools.pairwise(indices)] for line in lines]
    cols, struct = struct[0], struct[1:]
    data = [{col: item for col, item in zip(cols, line)} for line in struct]
    return data
