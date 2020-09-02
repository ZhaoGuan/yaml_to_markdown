#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import json
import requests
from bs4 import BeautifulSoup


def student_page(the_student_id):
    base_url = "https://test121.meishubao.com/admin/u_userinfo_home.html?id={student_id}".format(
        student_id=the_student_id)
    login_url = "https://test121.meishubao.com/admin/login.php"
    rep = requests.post(login_url, data={"username": "392", "password": "123456"})
    response = requests.get(base_url, headers={"cookie": rep.headers["Set-Cookie"]})
    print(response.text)
    soup = BeautifulSoup(response.text, features="html.parser")
    student_data = {}
    student = soup.find_all(attrs={"class": "form-control-static w-100"})
    # student information
    student_id = student[0].get_text().replace(" ", "").replace("\n", "")
    student_data["学员ID"] = student_id.split("ID:")[1]
    student_name = student[1].get_text().replace(" ", "").replace("\n", "")
    student_data["学员姓名"] = student_name.split("-")[0]
    student_data["学员性别"] = student_name.split("-")[1]
    student_data["学员头像"] = soup.find(attrs={"class": 'form-group w-100'}).find("img").get("src")
    # student_data["学员头像"] = soup.select(
    #     "body > div.page.pageadmin.pageuser.pagebackend.pagebackenduser > div:nth-child(7) > div > div > div > div.col-2.border-right > div > div.form-group.w-100 > img")[
    #     0].get("src")
    student_info = soup.find_all(attrs={"class": "row w-100 flex-wrap m-0"})
    student_info_age = student_info[0].find_all(attrs={"class": "form-control-static col-12"})
    student_age = student_info_age[0].get_text().replace(" ", "").replace("\n", "").replace("\xa0\xa0", "").split(
        "岁生日：")
    student_data["年龄"] = student_age[0].replace("年龄：", "")
    student_data["生日"] = student_age[1]
    student_info_list = student_info[0].find_all(attrs={"class": "form-control-static col-12 mt-2"})
    # student_info_list_data = [i.get_text().replace(" ", "").replace("\n", "") for i in student_info_list]
    for data in student_info_list:
        data_temp = data.get_text().replace(" ", "").replace("\n", "")
        if "往期作品：" in data_temp:
            link = [i.get("src") for i in data.find_all("img")]
            student_data["往期作品"] = link
        else:
            data_temp = data_temp.split("：")
            student_data[data_temp[0]] = data_temp[1]
    # student_class_info = soup.select(
    #     "body > div.page.pageadmin.pageuser.pagebackend.pagebackenduser > div:nth-child(7) > div > div > div > div.col-10 > div.col-4.border-right > div.form-control-static.col-12.mt-2")
    student_class_info = soup.find(attrs={"class": "form-control-static col-12 mt-2", "style": "font-weight: 500;"})
    student_class_info = student_class_info.get_text().replace(" ", "").split("\n")
    student_data["课时获得量"] = student_class_info[2].split("课时获得量")[1].replace("，", "")
    student_data["已消耗量"] = student_class_info[3].split("已消耗量")[1].replace("，", "")
    student_data["剩余量"] = student_class_info[4].split("剩余量")[1].replace("，", "")
    student_data["请假剩余"] = student_class_info[6].split("次，")[0].split("请假次数：剩余")[1].replace("，", "")
    student_data["请假已消耗"] = student_class_info[6].split("次，")[1].split("已消耗")[1].replace("次(查看详情)", "")
    # parent information
    parent = soup.find("div", attrs={"class": "col-5 border-right"})
    parent_data = parent.find_all(
        attrs={"class": "form-control-static col-12 mt-2"})
    parent_data = [i.get_text().replace(" ", "").replace("\n", "") for i in parent_data]
    for data in parent_data[1:]:
        if "：" in data:
            data = data.split("：")
        else:
            data = data.split(":")
        try:
            student_data[data[0]] = data[1]
        except:
            student_data[data[0]] = None
    parent_mail = parent.find(attrs={"class": "newScroll"}).get_text().replace("\n", ",").split(",,")
    parent_mail_result = []
    for mail_data in parent_mail:
        if mail_data != "":
            parent_mail_result.append(mail_data.replace("编辑", "").replace("删除", ""))
    student_data["邮寄地址"] = parent_mail_result
    # 业务信息
    # work_data = soup.select(
    #     "body > div.page.pageadmin.pageuser.pagebackend.pagebackenduser > div:nth-child(7) > div > div > div > div.col-10 > div.col-3")
    work_data = soup.find(attrs={"class": "col-3", "style": "float:left;"})
    work_data = work_data.find_all(attrs={"class": "form-control-static col-12 mt-2"})
    # work_data = [
    #     data.get_text().replace(" ", "").replace("\n", "").replace("\xa0", "").replace("编辑", "") for data in work_data]
    for data in work_data:
        data_temp = data.get_text().replace(" ", "").replace("\n", "").replace("\xa0", "").replace("编辑", "")
        if "分配班主任记录" in data_temp or "分配教管记录" in data_temp:
            continue
        if "推荐记录" in data_temp:
            result = []
            for data in data.find_all("a"):
                t = data.get_text().replace(" ", "").replace("\n", "").replace("\xa0", "").replace("编辑", "")
                l = data.get("href").split("id=")[1]
                result.append(t + " " + l)
            student_data["推荐记录"] = result
        else:
            if ":" in data_temp:
                data_temp = data_temp.split(":")
            else:
                data_temp = data_temp.split("：")
            try:
                student_data[data_temp[0]] = data_temp[1]
            except:
                student_data[data_temp[0]] = None
    # 学习极端
    # learning_phase = soup.select(
    #     "* > div.page.pageadmin.pageuser.pagebackend.pagebackenduser > div:nth-child(11) > div:nth-child(1) > table > tbody > tr > td:nth-child(2)")
    learning_phase = soup.find("table", attrs={"class": "table table-hover row mx-0 mb-0 text-center"}).find_all(
        attrs={"class": "w-100 border-bottom"})[0].find_all("td")
    student_data["学习阶段"] = learning_phase[1].get_text()
    # # 渠道
    # channel = soup.select(
    #     "body > div.page.pageadmin.pageuser.pagebackend.pagebackenduser > div:nth-child(11) > div:nth-child(1) > table > tbody > tr > td:nth-child(4)")
    # student_data["渠道名称"] = channel[0].get_text()
    student_data["渠道名称"] = learning_phase[3].get_text()
    # with open("./json/" + the_student_id + ".json", "w")as f:
    #     f.write(json.dumps(student_data, sort_keys=True, indent=4, ensure_ascii=False))
    print(json.dumps(student_data, sort_keys=True, indent=4, ensure_ascii=False))
    return student_data


if __name__ == "__main__":
    student_page("1790019")
