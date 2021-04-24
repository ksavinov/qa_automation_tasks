#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Тестовая система представляет собой иерархию классов, описывающую тест-кейсы.
У каждого тест-кейса есть:
Номер (tc_id) и название (name)
Методы для подготовки (prep), выполнения (run) и завершения (clean_up) тестов.
Метод execute, который задаёт общий порядок выполнения тест-кейса и обрабатывает исключительные ситуации.
Все этапы выполнения тест-кейса, а также исключительные ситуации должны быть задокументированы в лог-файле или в стандартном выводе.

Тест-кейс 1: Список файлов
[prep] Если текущее системное время, заданное как целое количество секунд от начала эпохи Unix, не кратно двум, то необходимо прервать выполнение тест-кейса.
[run] Вывести список файлов из домашней директории текущего пользователя.
[clean_up] Действий не требуется.
Тест-кейс 2: Случайный файл
[prep] Если объем оперативной памяти машины, на которой исполняется тест, меньше одного гигабайта, то необходимо прервать выполнение тест-кейса.
[run] Создать файл test размером 1024 КБ со случайным содержимым.
[clean_up] Удалить файл test.
"""
import os
import time
import random
import string
import psutil
import logging

logger = logging.getLogger(__name__)


class OddUnixTimeException(Exception):
    pass


class NotEnoughRAMException(Exception):
    pass


class NoSuchTestCaseID(Exception):
    pass


class NoSuchTestCase(Exception):
    pass


class TestPrepFuncs:
    def check_unix_time_odd(self):
        logger.info("TestPrepFuncs.check_unix_time_odd called")
        unix_time = int(time.time())
        if unix_time % 2 != 0:
            raise OddUnixTimeException(unix_time)

    def check_ram(self):
        logger.info("TestPrepFuncs.check_ram called")
        ram_gb = int(psutil.virtual_memory().total / 1024 / 1024 / 1024)
        if ram_gb < 1:
            raise NotEnoughRAMException(ram_gb)


class TestCases:
    def __init__(self):
        self.tc_ids = {
            1: "files_list",
            2: "random_file"}
        self.tc_names = {"Список файлов": "files_list",
                         "Случайный файл": "random_file"}

    def files_list(self):
        logger.info("Run Test Case: get_user_files")
        user_home_dir = os.path.expanduser("~")
        home_dir_files = os.listdir(user_home_dir)
        print(home_dir_files)

    def random_file(self):
        logger.info("Run Test Case: create_file_test")
        filename = "test"
        required_size = 1024 * 1024
        with open(filename, 'w') as temp_file:
            while True:
                file_size = os.stat(filename).st_size
                if file_size >= required_size:
                    break
                random_symbol = "".join(
                    random.choice(string.ascii_letters + string.digits))
                temp_file.write(random_symbol)


class TestCleanUpFuncs:
    def delete_file_test(self):
        logger.info("TestCleanUpFuncs.delete_file_test called")
        filename = "test"
        os.remove(filename)


class TestClass(TestPrepFuncs, TestCases, TestCleanUpFuncs):
    def prep(self, prep_func=None):
        logger.info("TestClass.prep called with params: prep_func=%s", prep_func)
        if prep_func is not None:
            getattr(TestPrepFuncs, prep_func)(self)

    def run(self, name, tc_id):
        logger.info("TestClass.run called with params: name=%s, tc_id=%s", name, tc_id)
        tc = TestCases()
        if name is not None:
            try:
                case_name = tc.tc_names[name]
                getattr(TestCases, case_name)(self)
            except KeyError:
                raise NoSuchTestCase(name)
        if tc_id is not None:
            try:
                case_func = tc.tc_ids[tc_id]
                getattr(TestCases, case_func)(self)
            except KeyError:
                raise NoSuchTestCaseID(tc_id)

    def clean_up(self, clean_up_func=None):
        logger.info("TestClass.clean_up called with params: clean_up_func=%s", clean_up_func)
        if clean_up_func is not None:
            getattr(TestCleanUpFuncs, clean_up_func)(self)

    def execute(self, tc_id=None, name=None, prep=None, clean_up=None):
        logger.info("TestClass.execute called with params: tc_id=%s, name=%s,"
                    " prep=%s, clean_up=%s", tc_id, name, prep, clean_up)
        try:
            self.prep(prep)
            self.run(name, tc_id)
            self.clean_up(clean_up)
            logger.info("PASSED")
        except BaseException as e:
            logger.exception(e)
            logger.error("FAIL")


if __name__ == "__main__":
    t = TestClass()
    # run test by test case ID
    # t.execute(tc_id=1, prep="check_unix_time_odd")
    # t.execute(tc_id=2, prep="check_ram", clean_up="delete_file_test")

    # run test by test case name
    t.execute(name="Список файлов", prep="check_unix_time_odd")
    t.execute(name="Случайный файл", prep="check_ram",
              clean_up="delete_file_test")
