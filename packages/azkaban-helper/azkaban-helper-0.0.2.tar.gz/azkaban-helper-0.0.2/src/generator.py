#!/usr/bin/python
# -*- coding: UTF-8 -*-
import collections
import os
import shutil
import sys
import zipfile
from collections import OrderedDict

import requests
import xlrd
import yaml


def ordered_yaml_load(yaml_path, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    with open(yaml_path) as stream:
        return yaml.load(stream, OrderedLoader)


def ordered_yaml_dump(data, stream=None, Dumper=yaml.SafeDumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


'''
 check dependency jobs whether exits in above jobs or not
'''


def check_job(flow, depend_jobs):
    exists_jobs = []
    for job in flow['nodes']:
        exists_jobs.append(job.get('name'))
    return set(depend_jobs).issubset(exists_jobs)


'''
check some cell value whether is null or not
'''


def null(var, desc):
    if len(var.strip()) == 0:
        raise Exception('The value ' + desc + 'is required')


'''
parse jobs and flows from excel 
'''


def parse_flows(excel, sheet_name):
    flow_list = collections.OrderedDict()
    sheet1 = excel.sheet_by_name(sheet_name)
    for i in range(1, sheet1.nrows):
        line = sheet1.row_values(i)
        if len(line) == 0:
            pass
        # get a flow from flow_list
        flow = flow_list.get(line[1], collections.OrderedDict())
        config = parse_flow_config(flow, i, line)
        if config is not None:
            flow['config'] = config

        nodes = flow.get('nodes')
        if nodes is None:
            nodes = []

        job = parse_job(flow, line)
        nodes.append(job)
        flow['nodes'] = nodes

        flow_list[line[1]] = flow
    return flow_list


'''
parse flow config from excel column
'''


def parse_flow_config(flow, i, line):
    config = flow.get('config', collections.OrderedDict())
    if len(config) != 0:
        return config
    if line[3] is not None:
        for conf in line[3].strip().split('|'):
            cp = conf.strip().split('=')
            if cp == '':
                pass
            try:
                config[cp[0]] = cp[1]
            except IndexError:
                print("flow configs error:", i, line[3], cp)
    else:
        print('location the ' + str(i) + 'th row: flow_configs is null ')
    return config


'''
parse jobs config from excel column
'''


def parse_job(flow, line):
    job_name, job_type = check_null(line)
    job = collections.OrderedDict()
    job['name'] = job_name
    job['type'] = job_type
    depend_jobs = []
    if line[8] is not None and line[8].strip() != '':
        depend_jobs = line[8].strip().split('|')
    if len(depend_jobs) != 0:
        job['dependsOn'] = depend_jobs
        if not check_job(flow, depend_jobs):
            raise Exception(
                'job ' + line[1] + '\'s depends: ' + line[8] + ' On not exist in above jobs')
    job_config = {'command': line[7]}
    job['config'] = job_config
    return job


'''
check null parameter from excel column
'''


def check_null(line):
    job_name = line[4].strip()
    null(job_name, 'job_name')
    job_type = line[6].strip()
    null(job_type, 'job_type')
    return job_name, job_type


def handle_dir(base_dir, sheet_name):
    try:
        shutil.rmtree(base_dir)
    except FileNotFoundError:
        pass
    os.mkdir(base_dir)
    # generate azkaban version describe file
    with open(base_dir + os.sep + sheet_name + '.project', 'w', encoding='utf-8') as version_file:
        version_file.write('azkaban-flow-version: 2.0')
        version_file.close()


def make_zip(source_dir, output_filename):
    zips = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zips.write(pathfile, arcname)
    zips.close()


def generator(excel, flow_sheets, save_dir):
    for project in flow_sheets:
        # the sheets of list didn't to handle
        exclude_sheets = ['info', 'projects', 'config', 'scheduler']
        if {project.strip()}.issubset(exclude_sheets):
            continue
        flows = parse_flows(excel, project)
        project_dir = save_dir + os.sep + project
        handle_dir(project_dir, project)
        for f in flows:
            flow_file = project_dir + os.sep + f + '.flow'
            with open(flow_file, 'w', encoding='utf-8') as output:
                ordered_yaml_dump(flows[f], output)
                output.close()
        make_zip(project_dir, project_dir + '.zip')
        print(project_dir + '.zip is generated')


HEADERS = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest'}


def login(excel):
    config_sheet = excel.sheet_by_name('config')
    url = config_sheet.cell_value(1, 0).strip()
    if not url.endswith('/'):
        url = url + '/'
    username = config_sheet.cell_value(1, 1).strip()
    password = config_sheet.cell_value(1, 2).strip()
    base_dir = config_sheet.cell_value(1, 3).strip()
    if base_dir == '':
        base_dir = os.getcwd()
    print('Read Azkaban Connection Info From "config" sheet: url="%s", username=%s,password=%s' % (
        url, username, password))
    session = requests.Session()
    data = {
        'action': 'login',
        'username': username,
        'password': password
    }
    response = session.post(url, data=data, verify=False, headers=HEADERS)
    if response.raise_for_status():
        raise Exception("login azkaban failed,please check the config sheet's content")
    else:
        return url, session, base_dir


def create_project(excel, url, session):
    ps = excel.sheet_by_name('projects')
    p_ids = {}
    for r in range(1, ps.nrows):
        p_name = ps.cell_value(r, 0)
        if p_name == '':
            continue
        p_desc = ps.cell_value(r, 1)
        if p_desc == '':
            p_desc = p_name
        params = (
            ('action', 'create'),
        )
        data = {
            'name': p_name,
            'description': p_desc
        }
        response = session.post(url + 'manager', data=data, params=params, verify=False, headers=HEADERS)
        if response.raise_for_status():
            raise Exception("request failed")
        else:
            print("create project %s %s response: %s" % (p_name, p_desc, response.json()))
            status = response.json().get('status')
            if status is None:
                raise Exception(response.json().get('error'))
        p_ids[p_name] = fetch_projects_id(url, session, p_name)
    return p_ids


def schedule_flow(url, session, p_name, f_name, cron):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'project': p_name,
        'ajax': 'scheduleCronFlow',
        'flow': f_name,
        'disabled': '[]',
        'failureEmailsOverride': 'false',
        'successEmailsOverride': 'false',
        'failureAction': 'finishCurrent',
        'failureEmails': '',
        'successEmails': '',
        'notifyFailureFirst': 'false',
        'notifyFailureLast': 'false',
        'concurrentOption': 'skip',
        'projectName': p_name,
        'cronExpression': cron
    }

    response = session.post(url + 'schedule', headers=headers, data=data, verify=False)
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        print(response.json())
        return response.json()['scheduleId']


def remove_schedule(url, session, schedule_id):
    data = {
        'action': 'removeSched',
        'scheduleId': schedule_id
    }
    response = session.post(url + 'schedule', headers=HEADERS, data=data, verify=False)
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        print(response.json())


def upload_project(url, session, base_dir, project):
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    zip_file_name = project + '.zip'
    zip_path = base_dir + os.sep + zip_file_name

    upload_data = MultipartEncoder(
        fields={
            'ajax': 'upload',
            'project': project,
            'file': (zip_file_name, open(zip_path, 'rb'), 'application/zip')
        }
    )

    response = session.post(url + 'manager', data=upload_data, headers={'Content-Type': upload_data.content_type})
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        print('upload project: %s successfully! success info: %s' % (project, response.json()))


def fetch_projects_id(url, session, project_name):
    params = {
        'project': project_name,
        'ajax': 'fetchprojectflows'
    }
    response = session.get(url + 'manager', headers=HEADERS, params=params, verify=False)
    project_id = response.json().get('projectId')
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        if project_id:
            print('project %s id is: %s' % (project_name, project_id))
            return project_id


def fetch_schedule_id(url, session, project_id, flow_name):
    params = {
        'ajax': 'fetchSchedule',
        'projectId': project_id,
        'flowId': flow_name
    }

    response = session.get(url + 'schedule', headers=HEADERS, params=params, verify=False)
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        if response.json():
            return response.json()['schedule']['scheduleId']
    return None


def schedule(excel, url, session):
    maps = create_project(excel, url, session)
    schedule_sheet = excel.sheet_by_name('scheduler')
    for row in range(1, schedule_sheet.nrows):
        project_name = schedule_sheet.cell_value(row, 0).strip()
        global project_ids
        flow_name = schedule_sheet.cell_value(row, 1).strip()
        cron = schedule_sheet.cell_value(row, 2).strip()
        enable = schedule_sheet.cell_value(row, 3)
        if project_name == '' or flow_name == '':
            continue
        if project_name != '' and flow_name != '':
            if cron != '' and enable:
                schedule_flow(url, session, project_name, flow_name, cron)
            else:
                schedule_id = fetch_schedule_id(url, session, maps[project_name], flow_name)
                if schedule_id:
                    remove_schedule(url, session, schedule_id)


'''
the sheets that exits in projects list. 
In other words ,the project has configure at a single sheet
'''


def valid_project(xl):
    valid_projects = []
    for project in xl.sheet_names():
        # the sheets of list didn't to handle
        exclude_sheets = ['info', 'projects', 'config', 'scheduler']
        if not {project.strip()}.issubset(exclude_sheets):
            valid_projects.append(project.strip())
    return valid_projects


def run_upload(xl):
    requests.packages.urllib3.disable_warnings()
    azkaban_url, s, b_dir = login(xl)
    create_project(xl, azkaban_url, s)
    configured_projects = valid_project(xl)
    for p in configured_projects:
        upload_project(azkaban_url, s, b_dir, p)


def main():
    args = sys.argv
    if len(args) < 2:
        print('python generator.py excel_path')
        sys.exit(-1)
    excel_file = args[1]
    if os.path.exists(excel_file) is None:
        print(excel_file, 'is not exists')
        sys.exit(-2)
    requests.packages.urllib3.disable_warnings()
    xl = xlrd.open_workbook(excel_file)
    flow_sheets = xl.sheet_names()
    azkaban_url, s, save_dir = login(xl)
    if save_dir.endswith(os.sep):
        save_dir = save_dir[:-1]
    if os.path.isdir(save_dir) is None:
        print(save_dir, 'is not exists')
        os.mkdir(save_dir)
    generator(xl, flow_sheets, save_dir)
    run_upload(xl)
    schedule(xl, azkaban_url, s)
    s.close()


if __name__ == '__main__':
    main()
