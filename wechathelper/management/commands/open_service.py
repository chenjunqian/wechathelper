import os
import errno
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    '''
        开启开放服务使用的命令脚本
    '''

    def handle(self, *args, **options):
        FIFO = 'wechat_pipe'

        try:
            os.mkfifo(FIFO)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise
        while True:
            with open(FIFO) as fifo:
                while True:
                    data = fifo.read()
                    if len(data)==0:
                        break
                    print('Read: "{0}"'.format(data))