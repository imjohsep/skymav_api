import asyncio
import logging

import json
import time

log = logging.getLogger(__name__)

clients = {}

def accept_client(client_reader, client_writer):
    task = asyncio.Task(handle_client(client_reader, client_writer))
    clients[task] = (client_writer)

    def client_done(task):
        del clients[task]
        client_writer.close()
        log.info("End Connection")

    log.info("New Connection")
    task.add_done_callback(client_done)


@asyncio.coroutine
def handle_client(client_reader, client_writer):
    data = {'result':{'status':'Connection Ready'}}
    postmessage(data,client_writer)
    count = 0
    while True:
        data = (yield from asyncio.wait_for(client_reader.readline(),timeout=1.0))
        print(data)
        if not data: #client disconnected
            break

        data = yield from asyncio.wait_for(test1(),timeout=1.0)
        yield from postmessage(data,client_writer)

        data = yield from asyncio.wait_for(test2(),timeout=1.0)
        yield from postmessage(data,client_writer)

@asyncio.coroutine
def postmessage(data, client_writer):
        mimetype=('text/event-stream')
        response = ('data: {0}\n\n'.format(data).encode('utf-8'))
        client_writer.write(response)
        client_writer.drain()

@asyncio.coroutine
def test1():
        data = {'result':{
                        'test1':{ }
                    }
                }
        data = json.dumps(data)
        return data

@asyncio.coroutine
def test2():
        data = {'result':{
                    'test2':{ }
                    }
                }
        data = json.dumps(data)
        return data

def main():
    loop = asyncio.get_event_loop()
    f = asyncio.start_server(accept_client, host=None, port=2991)
    loop.run_until_complete(f)
    loop.run_forever()

if __name__ == '__main__':
    log = logging.getLogger("")
    formatter = logging.Formatter("%(asctime)s %(levelname)s " +
                                  "[%(module)s:%(lineno)d] %(message)s")
    # log the things
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(formatter)
    log.addHandler(ch)
    main()
