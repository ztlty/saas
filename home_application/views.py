# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
import base64
import datetime

from common.mymako import render_mako_context
from common.log import logger
from common.mymako import render_mako_context, render_json, render_mako_tostring
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from home_application.models import Scripts
import time

def home(request):
    """
    首页
    """
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')
    # 查询业务
    res = client.cc.search_business()

    if res.get('result', False):
        bk_biz_list = res.get('data').get('info')
    else:
        logger.error(u"请求业务列表失败：%s" % res.get('message'))
        bk_biz_list = []
    script_list = Scripts.objects.all()
    return render_mako_context(request, '/home_application/index.html',{
                                   'bk_biz_list': bk_biz_list,
                                   'script_list': script_list,
                               })


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')




def get_hosts(request):
        """
        获取主机
        """
        client = get_client_by_request(request)
        client.set_bk_api_ver('v2')
        bk_biz_id = request.GET["bk_biz_id"]
        res = client.cc.search_host({
            "page": {"start": 0, "limit": 5, "sort": "bk_host_id"},
            "ip": {
                "flag": "bk_host_innerip|bk_host_outerip",
                "exact": 1,
                "data": []
            },
            "condition": [
                {
                    "bk_obj_id": "host",
                    "fields": [
                        # "bk_cloud_id",
                        # "bk_host_id",
                        # "bk_host_name",
                        # "bk_os_name",
                        # "bk_os_type",
                        # "bk_host_innerip",
                    ],
                    "condition": []
                },
                {"bk_obj_id": "module", "fields": [], "condition": []},
                {"bk_obj_id": "set", "fields": [], "condition": []},
                {
                    "bk_obj_id": "biz",
                    "fields": [
                        "default",
                        "bk_biz_id",
                        "bk_biz_name",
                    ],
                    "condition": [
                        {
                            "field": "bk_biz_id",
                            "operator": "$eq",
                            "value": bk_biz_id
                        }
                    ]
                }
            ]
        })

        if res.get('result', False):
            bk_host_list = res.get('data').get('info')
        else:
            bk_host_list = []
            logger.error(u"请求主机列表失败：%s" % res.get('message'))

        # print bk_host_list

        bk_host_list = [
            {
                'bk_host_innerip': host['host']['bk_host_innerip'],
                'bk_host_name': host['host']['bk_host_name'],
                'bk_host_id': host['host']['bk_host_id'],
                'bk_os_type': host['host']['bk_os_type'],
                'bk_os_name': host['host']['bk_os_name'],
                'bk_cloud_id': host['host']['bk_cloud_id'][0]['bk_inst_id'],
                'bk_cloud_name': host['host']['bk_cloud_id'][0]['bk_inst_name'],
                'bk_set_name': ' '.join(map(lambda x: x['bk_set_name'], host['set'])[:1]),
                'bk_module_name': ' '.join(map(lambda x: x['bk_module_name'], host['module'])[:1]),
            }
            for host in bk_host_list
        ]
        return render_json({
            'result': True,
            'data': bk_host_list
        })

def fast_execute_script(request):
    """快速执行脚本"""

    bk_biz_id = int(request.POST.get('bk_biz_id'))
    bk_host_innerip = request.POST.get('bk_host_innerip')
    bk_cloud_id = request.POST.get('bk_cloud_id')
    script_content = request.POST.get('script_content')
    start = time.time()

    # 创建操作记录

    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')

    res = client.job.fast_execute_script({
        'bk_biz_id': bk_biz_id,
        'ip_list': [{
            "bk_cloud_id": bk_cloud_id,
            "ip": bk_host_innerip
        }],
        'account': 'root',
        'script_type': 1,
        'script_content': base64.b64encode(script_content),
        'script_param': '',
    })

    if not res.get('result'):
        return render_json(res)

    task_id = res.get('data').get('job_instance_id')
    while not client.job.get_job_instance_status({
        'bk_biz_id': bk_biz_id,
        'job_instance_id': task_id,
    }).get('data').get('is_finished'):
        print 'waiting job finished...'
        time.sleep(1.2)

    res = client.job.get_job_instance_log({
        'bk_biz_id': bk_biz_id,
        'job_instance_id': task_id
    })

    log_content = res['data'][0]['step_results'][0]['ip_logs'][0]['log_content']

    return render_json({
        'result': True,
        'data': {
            'time': datetime.datetime.now().strftime('%Y/%m/%d/%H:%M:%S'),
            'log': log_content
        },
        'message': '%s: elapsed %ss' % (res.get('message'), round(time.time() - start, 2))
    })

def test(request):
    return render_json({
        'result': True,
        'data': 'world',
        'message':'hello'})