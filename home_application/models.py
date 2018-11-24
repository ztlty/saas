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

from django.db import models


class Scripts(models.Model):
    """业务信息"""

    script_name = models.CharField(u'脚本名称', max_length=64)
    script_desc = models.CharField(u'脚本说明', max_length=64)
    script_content = models.CharField(u'脚本内容', max_length=1024)
    script_param = models.CharField(u'默认参数', max_length=64)

    def __unicode__(self):
        return '{}.{}.{}.{}'.format(self.script_name,
                                    self.script_desc,
                                    self.script_content,
                                    self.script_param)
