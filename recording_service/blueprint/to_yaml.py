#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from sanic.blueprints import Blueprint
from sanic.response import json
from module.resources import Resources
from module.service_method import request_params_check

to_yaml = Blueprint('to_yaml')

db = Resources()


@to_yaml.route("/add_attribute", methods=['POST', 'OPTIONS'])
async def add_attribute(request):
    post_json = request.json
    try:
        info = post_json["info"]
        result, err = db.insert_attribute(info)
        if result:
            return json({"code": 20000})
        else:
            return json({"code": 50008, "message": str(err)})
    except Exception as e:
        return json({"code": 50008, "message": e})


@to_yaml.route("/get_attributes", methods=['GET', 'OPTIONS'])
async def get_attribute(request):
    data = db.get_attributes()
    return json(
        {
            "code": 20000,
            "data": data

        }
    )


@to_yaml.route("/del_attributes", methods=['GET', 'OPTIONS'])
async def del_attribute(request):
    args_with_blank_values = request.get_args(keep_blank_values=True)
    info = args_with_blank_values["info"][0]
    data = db.del_attribute(info)
    return json(
        {
            "code": 20000,
            "data": data

        }
    )


@to_yaml.route("/create_element", methods=['POST', 'OPTIONS'])
async def create_element(request):
    post_json = request.json
    name = post_json["name"]
    attribute_list = post_json["attribute_list"]
    attribute_ids = [i["id"] for i in attribute_list]
    result, the_id = db.insert_element(name)
    if result:
        result, msg = db.add_attribute_to_element(the_id, attribute_ids)
        if result:
            return json({"code": 20000})
        else:
            return json({"code": 50008, "message": msg})
    else:
        return json({"code": 50008, "message": str(the_id)})


@to_yaml.route("/get_elements_info", methods=['GET', 'OPTIONS'])
async def get_elements_info(request):
    data = db.get_all_element_data()
    return json({"code": 20000, "data": data})


@to_yaml.route("/del_element", methods=['GET', 'OPTIONS'])
async def del_element(request):
    args_with_blank_values = request.get_args(keep_blank_values=True)
    the_id = args_with_blank_values["id"][0]
    result, msg = db.del_element(the_id)
    if result:
        return json(
            {
                "code": 20000,
                "data": msg
            }
        )
    else:
        return json({"code": 50008, "message": msg})


@to_yaml.route("/recording", methods=['POST', 'OPTIONS'])
async def recording(request):
    data = request.json
    check, message = request_params_check(["pathName", "executor", "message", "result"], list(data.keys()))
    if check is False:
        return json({"code": 50008, "msg": message})
    test_case = data["pathName"]
    executor = data["executor"]
    result = data["result"]
    message = data["message"]
    if executor == "":
        return json({"code": 50008, "msg": "未正确填写执行用户名称！"})
    result, message = db.insert_recording(test_case, executor, result, message)
    if result:
        return json({"code": 20000})
    else:
        return json({"code": 50008, "msg": message})
