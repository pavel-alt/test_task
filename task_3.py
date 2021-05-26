import logging
from sys import exit
from abc import ABC, abstractmethod
from os import listdir, urandom, remove
from os.path import expanduser
from time import time
from psutil import virtual_memory


class TestCase(ABC):

    def __init__(self, tc_id, name):
        self.tc_id = tc_id
        self.name = name

    @abstractmethod
    def prep(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def clean_up(self):
        pass

    def execute(self):
        """
        Метод задаёт общий порядок выполнения тест-кейса
        и обрабатывает исключительные ситуации.
        """
        log.info(f"Started test-case id:{self.tc_id}, name:{self.name}")
        try:
            self.prep()
            self.run()
            self.clean_up()
        except Exception as err:
            log.error(err)
            exit()
        log.info(f"Finished test-case id:{self.tc_id}, name:{self.name}")


class TestCase1(TestCase):
    """ Тест-кейс 1: Список файлов
    · [prep] Если текущее системное время, заданное как целое количество секунд от начала эпохи Unix, не кратно двум,
    то необходимо прервать выполнение тест-кейса.
    · [run] Вывести список файлов из домашней директории текущего пользователя.
    · [clean_up] Действий не требуется."""

    def prep(self):
        log.debug("Start: preparation")
        if round(time()) % 2 != 0:
            log.warning("Appropriate time. Test case completed.")
            exit(0)
        log.debug("Finish: preparation")

    def run(self):
        log.debug("Start: run")
        home_dir = expanduser("~")
        print(listdir(path=home_dir))
        log.debug("Finish: run")

    def clean_up(self):
        pass


class TestCase2(TestCase):
    """ Тест-кейс 2: Случайный файл
    · [prep] Если объем оперативной памяти машины, на которой исполняется тест, меньше одного гигабайта, то необходимо
    прервать выполнение тест-кейса.
    · [run] Создать файл test размером 1024 КБ со случайным содержимым.
    · [clean_up] Удалить файл test."""

    def prep(self):
        log.debug("Start: preparation")
        if virtual_memory()[0] / 1073741824 < 1:
            log.warning("Appropriate RAM. Test case completed.")
            exit(0)
        log.debug("Finish: preparation")

    def run(self):
        log.debug("Start: run")
        with open(f"{expanduser('~')}/test", "wb") as file:
            file.write(urandom(1024*1024))
        log.debug("Finish: run")

    def clean_up(self):
        log.debug("Start: clean up")
        remove(f"{expanduser('~')}/test")
        log.debug("Finish: clean up")


def get_logger(name=__file__, file='log.txt', encoding='utf-8'):
    """
    Функция осуществляет логирование в файл.
    """
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')
    fh = logging.FileHandler(file, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log


log = get_logger()

if __name__ == "__main__":
    obj_1 = TestCase1(1, 'One test')
    obj_1.execute()

    obj_2 = TestCase2(2, 'Two test')
    obj_2.execute()
