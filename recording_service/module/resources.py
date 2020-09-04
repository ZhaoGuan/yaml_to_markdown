#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import pymysql
import os
import yaml

PATH = os.path.dirname(os.path.abspath(__file__))


class Resources:

    def __init__(self):
        with open(PATH + "/../config/db_config.yml") as f:
            self.db_config = yaml.safe_load(f)
        self.db = pymysql.connect(self.db_config["host"], self.db_config["user"], self.db_config["password"],
                                  self.db_config["db"])
        self.cursor = self.db.cursor()

    def check_attribute(self, info):
        sql = 'SELECT id,info FROM attributes WHERE info="%s"' % str(info)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results) > 0:
            return False
        else:
            return True

    def insert_attribute(self, info):
        if self.check_attribute(info):
            sql = 'INSERT INTO attributes (info) VALUES ("%s")' % str(info)
            try:
                # 执行sql语句
                self.cursor.execute(sql)
                # 提交到数据库执行
                self.db.commit()
                return True, None
            except Exception as E:
                print(E)
                # 如果发生错误则回滚
                self.db.rollback()

                return False, E
        else:

            return False, "已经存在属性:" + str(info)

    def get_attributes(self):
        sql = "SELECT id,info FROM attributes"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        data_list = []
        for result in results:
            data = {
                "id": result[0],
                "info": result[1]
            }
            data_list.append(data)
        return data_list

    def get_attribute(self, the_id):
        sql = 'SELECT info FROM attributes WHERE `id`="%s"' % the_id
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result[0]

    def del_attribute(self, info):
        sql = 'DELETE FROM attributes WHERE `info` = "%s"' % str(info)
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return True, None
        except Exception as E:
            print(E)
            # 如果发生错误则回滚
            self.db.rollback()
            return False, E

    # element
    def check_element(self, name):
        sql = 'SELECT id,name FROM elements WHERE name ="%s"' % str(name)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results) > 0:
            return False
        else:
            return True

    def insert_element(self, name):
        if self.check_element(name):
            sql = 'INSERT INTO elements (name) VALUES ("%s")' % str(name)
            try:
                # 执行sql语句
                self.cursor.execute(sql)
                # 提交到数据库执行
                the_id = self.cursor.lastrowid
                self.db.commit()
                return True, the_id
            except Exception as E:
                # 如果发生错误则回滚
                self.db.rollback()
                return False, E
        else:
            return False, "已经存在元素:" + str(name)

    def get_element_attributes(self, element_id):
        sql = 'SELECT attribute_id FROM type_attribute WHERE `element_id`="%s"' % str(element_id)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        result_list = []
        for result in results:
            result_list.append({"info": self.get_attribute(result[0])})
        return result_list

    def get_element(self):
        sql = "SELECT id,name FROM elements"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        data_list = []
        for result in results:
            data = {
                "id": result[0],
                "info": result[1]
            }
            data_list.append(data)
        return data_list

    def add_attribute_to_element(self, element_id, attribute_ids):
        for the_id in attribute_ids:
            sql = 'INSERT INTO type_attribute (element_id,attribute_id) VALUES ("%s","%s")' % (
                str(element_id), str(the_id))
            try:
                # 执行sql语句
                self.cursor.execute(sql)
                # 提交到数据库执行
                self.db.commit()
            except Exception as E:
                # 如果发生错误则回滚
                self.db.rollback()
                return False, E
        return True, None

    def get_all_element_data(self):
        sql = 'SELECT id,name FROM elements'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        result_data = []
        for result in results:
            the_id = result[0]
            the_name = result[1]
            attribute_list = self.get_element_attributes(the_id)
            result_data.append({"id": the_id, "name": the_name, "attribute_list": attribute_list})
        return result_data

    def del_element(self, the_id):
        sql_one = 'DELETE FROM elements WHERE `id`="%s"' % str(the_id)
        sql_two = 'DELETE FROM type_attribute WHERE `element_id`="%s"' % str(the_id)
        try:
            # 执行sql语句
            self.cursor.execute(sql_one)
            self.cursor.execute(sql_two)
            # 提交到数据库执行
            self.db.commit()
        except Exception as E:
            # 如果发生错误则回滚
            self.db.rollback()
            return False, E

        return True, None

    def insert_recording(self, test_case, executor, result, message):
        sql = 'INSERT INTO recording (test_case,executor,result,message) VALUES ("%s","%s","%s","%s")' % (
            str(test_case), str(executor), str(result), str(message))
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except Exception as E:
            print(E)
            # 如果发生错误则回滚
            self.db.rollback()
            return False, E
        return True, None

    def close(self):
        self.db.close()


if __name__ == "__main__":
    r = Resources()
    a = r.get_all_element_data()
    print(a)
