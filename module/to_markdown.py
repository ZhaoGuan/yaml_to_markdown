#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import yaml
from jinja2 import Template
import yaml
import os

PATH = os.path.dirname(os.path.abspath(__file__))
case_template = '''
###测试用例
* 用例描述: {{ desc }} 
####前置条件
{%- for pre_condition in pre_condition_list %}
* {{ pre_condition.index }}. {{ pre_condition.info }}  
{%- endfor %}
***
####用例步骤
| 等级 | 测试点| 操作 | 预期   |
| :----: | :----: | :----: | :----: |
{%- for case in case_list %}
| {{ case.level }} | {{ case.desc }} | {{ case.action }} | {{case.assert}} |
{%- endfor %}
* * *  
####附加用例
####版本变更记录
{%- for change_log in change_log_list %}
* {{ change_log.version }}  
  <details>
    <p>{{- change_log.message }}</p>
  </details>
{%- endfor %}
####需求连接
{%- for doc in doc_list %}
* [ {{ doc.name }} ]( {{ doc.link }} )
{%- endfor %}
####关联模块
{%- for related_module in related_module_list %}
* {{ related_module }}
{%- endfor %}
'''


def yaml_to_md(yaml_case_path):
    with open(yaml_case_path) as f:
        yaml_case_data = yaml.safe_load(f)
    # 描述
    desc = yaml_case_data["Desc"]
    # 前置条件
    pre_condition_list = yaml_case_data["PreCondition"]
    pre_condition_list = [{"index": pre_condition_list.index(pre_condition), "info": pre_condition} for pre_condition in
                          pre_condition_list]
    # 测试计划
    test_plan = yaml_case_data["TestPlan"]
    # 需求连接
    doc_list = yaml_case_data["Story"]
    # 变更版本记录
    change_log_list = yaml_case_data["ChangeLog"]
    # 关联模块
    related_module_list = yaml_case_data["RelatedModule"]
    case_list = []
    for plan in test_plan:
        # 用例名称
        desc = plan["CheckPoint"]["desc"]
        # 用例等级没有为P0
        if "level" in plan["CheckPoint"].keys():
            level = plan["CheckPoint"]["level"]
            if level is None:
                level = "P0"
        else:
            level = "P0"
        # 操作步骤
        cases = plan["CheckPoint"]["cases"]
        for case in cases:
            if cases.index(case) == 0:
                case_list.append(
                    {"level": level, "desc": desc, "action": case["case"]["action"], "assert": case["case"]["assert"]})
            else:
                case_list.append(
                    {"level": level, "desc": "", "action": case["case"]["action"], "assert": case["case"]["assert"]})
    the_template = Template(case_template)
    md_result = the_template.render(desc=desc, pre_condition_list=pre_condition_list, case_list=case_list,
                                    doc_list=doc_list,
                                    change_log_list=change_log_list, related_module_list=related_module_list)
    with open(PATH + "/../md_cases/example.md", "w") as f:
        f.write(md_result)


if __name__ == "__main__":
    yaml_to_md("../cases/example.yml")
