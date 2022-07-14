from datetime import datetime
import numpy as np
import os

def getTime():
    return datetime.now().isoformat()

def getRecentFile(category):
    files = sorted(['logs/'+f for f in os.listdir('logs') if f.startswith(category)], reverse=True)
    return files[0] if len(files) > 0 else None

def flatten(json):
    return [{'host': key} | data for key, data in json.items()]

def read_server_ids(fname):
    with open(fname, 'r') as fp: # host user pw (multiline)
        info = fp.read().strip().split('\n')
    return info

def convert_to_gigabytes(digits_unit):
    factors = {'G':1, 'T':1e3, 'M':1e-3, 'K':1e-6, '0':1}
    unit = digits_unit[-1]
    if unit not in 'TGMK' and unit != '0':
        raise ValueError("\"digits_unit\" must end with 'T'|'G'|'M'|'K' or must be '0'. Not '%s'" % digits_unit)
    digits = digits_unit[:-1] or '0'
    size_in_gb = float(digits) * factors[unit]
    return size_in_gb

def gigabytes_to_formatted(float_number):
    if float_number == 0: return '0B'
    maps = {-3:'B', -2:'KB', -1:'MB', 0:'GB', 1:'TB'}
    factor = int(np.log10(float_number))//3
    formatted = f"{float_number * 10**(-factor*3):.1f}{maps[factor]}".replace('.0', '')
    return formatted

def megabytes_to_formatted(float_number):
    maps = {-2:'B', -1:'KB', 0:'MB', 1:'GB', 2:'TB'}
    factor = int(np.log10(float_number))//3
    formatted = f"{float_number * 10**(-factor*3):.1f}{maps[factor]}".replace('.0', '')
    return formatted
    
