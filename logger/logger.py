# -*- coding:utf-8 -*-
import logging
import os


def get_cwd(loggers):
    """
    获取当前路径，不存在就创建
    :param logger_name: 文件的名字
    :return:
    """
    # log_path是存放日志的路径
    cur_path = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(os.path.dirname(cur_path), loggers)
    # 如果不存在这个logs文件夹，就自动创建一个
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    return log_path


class Logger:
    def __init__(self, logger_name):
        # 创建一个logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        log_path = get_cwd(logger_name)
        file_path = '/log.out'
        fh = logging.FileHandler(log_path + file_path, mode='a', encoding='utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        fh.setLevel(logging.DEBUG)

        # 创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        """
        定义一个函数，回调logger实例
        """
        return self.logger


if __name__ == '__main__':
    logger = Logger("logs").get_log()
    logger.debug("User %s is loging" % 'jeck')
    logger.info("logger test: {}".format('liusilin'))
