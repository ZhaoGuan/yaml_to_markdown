#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import yaml
from jinja2 import Template
import yaml
import os
import copy
import shutil

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


class YamlToMd:
    def __init__(self):
        self.except_list = ["book.json", "SUMMARY.md", "README.md", "node_modules", "_book"]
        self.md_case_path = os.path.abspath(PATH + "/../md_cases")
        self.yaml_case_path = os.path.abspath(PATH + "/../cases")

    @classmethod
    def yaml_to_md(cls, yaml_case_path, md_case_path):
        with open(yaml_case_path) as f:
            yaml_case_data = yaml.safe_load(f)
        # 描述
        desc = yaml_case_data["Desc"]
        # 前置条件
        pre_condition_list = yaml_case_data["PreCondition"]
        pre_condition_list = [{"index": pre_condition_list.index(pre_condition), "info": pre_condition} for
                              pre_condition in
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
                        {"level": level, "desc": desc, "action": case["case"]["action"],
                         "assert": case["case"]["assert"]})
                else:
                    case_list.append(
                        {"level": level, "desc": "", "action": case["case"]["action"],
                         "assert": case["case"]["assert"]})
        the_template = Template(case_template)
        md_result = the_template.render(desc=desc, pre_condition_list=pre_condition_list, case_list=case_list,
                                        doc_list=doc_list,
                                        change_log_list=change_log_list, related_module_list=related_module_list)
        with open(md_case_path, "w") as f:
            f.write(md_result)

    def clean_md_cases(self):
        file_list = os.listdir(self.md_case_path)
        for file in file_list:
            file_path = self.md_case_path + "/" + file
            if file not in self.except_list:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)

    def all_yaml_to_md(self, path):
        file_list = os.listdir(path)
        dir_list = []
        for file in file_list:
            file_path = path + "/" + file
            if os.path.isdir(file_path):
                dir_list.append(file_path)
            else:
                if ".yml" in file_path:
                    md_file_path = copy.deepcopy(path).replace(self.yaml_case_path, self.md_case_path)
                    if not os.path.exists(md_file_path):
                        os.makedirs(md_file_path)
                    md_file_path += "/" + file
                    self.yaml_to_md(file_path, md_file_path.replace(".yml", ".md"))
        for dir_path in dir_list:
            self.all_yaml_to_md(dir_path)

    def get_md_path(self, path, data={"root": []}):
        file_list = os.listdir(path)
        dir_list = []
        md_list = []
        for file in file_list:
            if file in self.except_list:
                continue
            file_path = path + "/" + file
            if not os.path.isdir(file_path):
                file_path = file_path.replace(self.md_case_path, "")
                md_list.append(file_path)
            else:
                dir_list.append(file_path)
        save_md_list = copy.deepcopy(md_list)
        [save_md_list.remove(dir.replace(self.md_case_path, "") + ".md") for dir in dir_list]
        [list(data.values())[0].append(md) for md in save_md_list]
        for dir in dir_list:
            name_file_path = dir.replace(self.md_case_path, "")
            if name_file_path + ".md" not in md_list:
                assert False, "未发现文件夹对应的md文件" + dir
            temp = {name_file_path + ".md": []}
            list(data.values())[0].append(self.get_md_path(dir, temp))
        return data

    def summary_data(self, file_steam, base, data):
        for k, v in data.items():
            for v_data in v:
                if isinstance(v_data, str):
                    name = v_data.split("/")[-1].replace("/", "").replace(".md", "")
                    write_data = base + "* [" + name + "](" + v_data + ")" + "\n"
                    file_steam.write(write_data)
                if isinstance(v_data, dict):
                    name = list(v_data.keys())[0].split("/")[-1].replace("/", "").replace(".md", "")
                    write_data = base + "* [" + name + "](" + list(v_data.keys())[0] + ")" + "\n"
                    file_steam.write(write_data)
                    temp_base = copy.deepcopy(base)
                    temp_base += "  "
                    self.summary_data(file_steam, temp_base, v_data)

    def summary(self):
        self.clean_md_cases()
        self.all_yaml_to_md(self.yaml_case_path)
        path_result = self.get_md_path(self.md_case_path)
        with open(PATH + "/../md_cases/SUMMARY.md", "w") as f:
            self.summary_data(f, "", path_result)


if __name__ == "__main__":
    ytm = YamlToMd()
    ytm.summary()
