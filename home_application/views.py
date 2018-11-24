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

from common.mymako import render_mako_context
from common.log import logger
from common.mymako import render_mako_context, render_json, render_mako_tostring
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from home_application.models import Scripts

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
