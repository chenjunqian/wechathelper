import os
import errno


if __name__ == '__main__':
    FIFO_SERVE = 'server_wechat_pipe'
    FIFO_CLIENT = 'client_wechat_pipe'

    try:
        os.mkfifo(FIFO_CLIENT)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise

    with open(FIFO_SERVE, 'w') as fifo:
        fifo.write('Hello, this is client')
        fifo.flush()


    while True:
        with open(FIFO_CLIENT) as fifo:
            while True:
                data = fifo.read()
                if len(data)==0:
                    break
                print('From Server: "{0}"'.format(data))


