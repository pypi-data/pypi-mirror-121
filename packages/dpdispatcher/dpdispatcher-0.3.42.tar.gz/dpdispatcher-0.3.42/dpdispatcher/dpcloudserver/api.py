
import os
import json
try:
    import oss2
    from oss2 import SizedFileAdapter, determine_part_size
    from oss2.models import PartInfo
except ImportError:
    pass
import requests
from urllib.parse import urljoin
from dpdispatcher import dlog

from .retcode import RETCODE
from .config import HTTP_TIME_OUT, API_HOST
token = ''

def get(url, params):
    global token
    headers = {'Authorization': "jwt " + token}
    ret = requests.get(
                urljoin(API_HOST, url),
                params=params,
                timeout=HTTP_TIME_OUT,
                headers=headers
                )
    # print(url,'>>>', params, '<<<', ret.text)
    ret = json.loads(ret.text)
    if ret['code'] != RETCODE.OK:
        raise ValueError(f"{url} Error: {ret['code']} {ret['message']}")

    return ret['data']

def post(url, params):
    global token
    headers = {'Authorization': "jwt " + token}
    ret = requests.post(
                urljoin(API_HOST, url),
                json=params,
                timeout=HTTP_TIME_OUT,
                headers=headers
                )
    # print(url,'>>>', params, '<<<', ret.text)
    ret = json.loads(ret.text)
    if ret['code'] != RETCODE.OK:
        raise ValueError(f"{url} Error: {ret['code']} {ret['message']}")

    return ret['data']


def login(password, email=None, username=None):
    global token
    post_data = {"password": password}
    if email is None and username is None:
        raise ValueError(f"Error: can not find username or email from remote_profile")
    if email is not None:
        post_data['email'] = email
    if username is not None:
        post_data['username'] = username
    ret = post(
            '/account/login',
            post_data
            )
    dlog.debug(f"debug: login ret:{ret}")
    token = ret['token']


def _get_oss_bucket(endpoint, bucket_name):
    #  res = get("/tools/sts_token", {})
    res = get("/data/get_sts_token", {})
    # print('debug>>>>>>>>>>>>>', res)
    dlog.debug(f"debug: _get_oss_bucket: res:{res}")
    auth = oss2.StsAuth(
                res['AccessKeyId'],
                res['AccessKeySecret'],
                res['SecurityToken']
                )
    return oss2.Bucket(auth, endpoint, bucket_name)


def download(oss_file, save_file, endpoint, bucket_name):
    bucket = _get_oss_bucket(endpoint, bucket_name)
    dlog.debug(f"debug: download: oss_file:{oss_file}; save_file:{save_file}")
    bucket.get_object_to_file(oss_file, save_file)
    return save_file


def upload(oss_task_zip, zip_task_file, endpoint, bucket_name):
    dlog.debug(f"debug: upload: oss_task_zip:{oss_task_zip}; zip_task_file:{zip_task_file}")
    bucket = _get_oss_bucket(endpoint, bucket_name)
    total_size = os.path.getsize(zip_task_file)
    part_size = determine_part_size(total_size, preferred_size=1000 * 1024)
    upload_id = bucket.init_multipart_upload(oss_task_zip).upload_id
    parts = []
    with open(zip_task_file, 'rb') as fileobj:
        part_number = 1
        offset = 0
        while offset < total_size:
            num_to_upload = min(part_size, total_size - offset)
            result = bucket.upload_part(oss_task_zip, upload_id, part_number, SizedFileAdapter(fileobj, num_to_upload))
            parts.append(PartInfo(part_number, result.etag))
            offset += num_to_upload
            part_number += 1
    # result = bucket.complete_multipart_upload(oss_task_zip, upload_id, parts)
    result = bucket.complete_multipart_upload(oss_task_zip, upload_id, parts)
    # print('debug:upload_result:', result, dir())
    return result


def job_create(job_type, oss_path, input_data, program_id=None):
    post_data = {
                'job_type': job_type,
                'oss_path': oss_path,
                'input_data': input_data,
            }
    if program_id is not None:
        post_data["program_id"] = program_id
    ret = post('/data/insert_job', post_data)
    return ret['job_id']


def job_create_v2(job_type, oss_path, input_data, program_id=None, group_id=None):
    post_data = {
                'job_type': job_type,
                'oss_path': oss_path,
            }
    if program_id is not None:
        post_data["program_id"] = program_id
    if group_id is not None:
        post_data["job_group_id"] = group_id
    if input_data.get('command') is not None:
        post_data["cmd"] = input_data.get('command')
    if input_data.get('backward_files') is not None:
        post_data["out_files"] = input_data.get('backward_files')
    input_keys = ['job_group_id', 'job_name', 'rerun', 'image_name', 'disk_size', 'scass_type',
                  'instance_group_id', 'log_file', 'platform', 'region', 'zone', 'on_demand']
    for key in input_keys:
        if key in input_data:
            post_data[key] = input_data[key]
    ret = post('/data/v2/insert_job', post_data)
    group_id = ret.get('job_group_id')
    return ret['job_id'], group_id

def get_jobs(page=1, per_page=10):
    ret = get(
        '/data/jobs',
        {
            'page': page,
            'per_page': per_page,
        }
    )
    return ret['items']


def get_tasks(job_id, page=1, per_page=10):
    ret = get(
        f'data/job/{job_id}/tasks',
        {
            'page': page,
            'per_page': per_page,
        }
    )
    return ret['items']


def get_tasks_v2(job_id, group_id, page=1, per_page=10):
    ret = get(
        f'data/job/{group_id}/tasks',
        {
            'page': page,
            'per_page': per_page,
        }
    )
    for each in ret['items']:
        if job_id == each["task_id"]:
            return [each]
    if len(ret['items']) != 0:
        return get_tasks_v2(job_id, group_id, page=page+1)
    return []

#%%

