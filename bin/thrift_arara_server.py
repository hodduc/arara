#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import sys
# XXX(serialx): ugly hack for the unicode
reload(sys)
sys.setdefaultencoding('utf-8')

import optparse
import traceback
import time
import logging
import logging.handlers

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
THRIFT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../gen-py"))
sys.path.append(THRIFT_PATH)
sys.path.append(PROJECT_PATH)

from arara_thrift.ttypes import *
from thrift.protocol import TBinaryProtocol
from thrift.transport.TTransport import TTransportException
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.server import TServer

# import arara
import arara.model
from etc import arara_settings

from arara import CLASSES
from middleware import MANAGER_LIST, DEPENDENCY, HANDLER_PORT
from middleware.thrift_middleware import MAPPING, connect_thrift_server

handler_for_info = logging.handlers.RotatingFileHandler('arara_server.log', 'a', 2**20*50, 10)
formatter = logging.Formatter('%(asctime)s [%(process)d:%(thread)X] <%(name)s> ** %(levelname)s ** %(message)s')
handler_for_info.setFormatter(formatter)
handler_for_info.setLevel(logging.INFO)

logging.getLogger('').setLevel(logging.NOTSET)
logging.getLogger('').addHandler(handler_for_info)

if arara_settings.ARARA_DEBUG_HANDLER_ON:
    handler_for_debug = logging.handlers.RotatingFileHandler('arara_server_debug.log', 'a', 2**20*50, 10)
    handler_for_debug.setFormatter(formatter)
    handler_for_debug.setLevel(logging.DEBUG)

    logging.getLogger('').addHandler(handler_for_debug)

    
def open_thrift_server(server_name, processor, handler, port):
    handler_instance = handler()
    processor_ = processor.Processor(handler_instance)
    transport = TSocket.TServerSocket(port)
    tfactory = TTransport.TBufferedTransportFactory()
    #tfactory = TTransport.TFramedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolAcceleratedFactory()

    # 서버를 어떻게 띄울 것인가?
    # 1. TThreadedServer   : Thread per Connection
    # 2. TForkingServer    : Process per Connection
    # 3. TThreadPoolServer : Preloaded Thread with Pool

    if server_name in ['LoginManager', 'MemberManager']:
        server = TServer.TThreadPoolServer(processor_, transport, tfactory, pfactory)
        server.setNumThreads(10)
    else:
        server = TServer.TThreadedServer(processor_, transport, tfactory, pfactory)

    #if server_name in ['BlacklistManager']:
    #    logging.getLogger('open_server').info("%s running in TForkingServer", server_name)
    #    server = TServer.TForkingServer(processor_, transport, tfactory, pfactory)
    #else:
    #    logging.getLogger('open_server').info("%s running in TThreadedServer", server_name)
    #    server = TServer.TThreadedServer(processor_, transport, tfactory, pfactory)
    #server = TServer.TThreadPoolServer(processor_, transport, tfactory, pfactory)
    #server.setNumThreads(15)
    return server, handler_instance

def open_server(server_name, base_port):
    assert server_name in MANAGER_LIST
    base_class = CLASSES[server_name]
    thrift_class = dict(MAPPING)[server_name]
    port = base_port + HANDLER_PORT[server_name]
    logger.info("Opening ARAra Thrift middleware on port starting from %s...", port)
    import thread
    server, instance = open_thrift_server(server_name, thrift_class, base_class, port)
    thread.start_new_thread(resolve_dependencies, (server_name, instance, base_port))
    return server

def resolve_dependencies(base_server, instance, base_port):
    dependencies = DEPENDENCY[base_server]
    for dependency_server in dependencies:
        dependency_port = base_port + HANDLER_PORT[dependency_server]
        print 'Connecting to %s in localhost:%d' % (
                dependency_server, dependency_port)
        while True:
            try:
                client = connect_thrift_server('localhost',
                        base_port, dependency_server)
                break
            except TTransportException:
                print '%s cannot be connected. Retrying...' % dependency_server
                time.sleep(1)
                continue

if __name__ == '__main__':
    logger = logging.getLogger('main')
    parser = optparse.OptionParser()
    parser.add_option("-p", "--port=", dest="port", default=arara_settings.ARARA_SERVER_BASE_PORT, type="int",
                      help="The port to bind")
    options, args = parser.parse_args()
    
    arara.model.init_database()

    def exception_handler(type_, value, traceback_):
        error_msg = ''.join(traceback.format_exception(type_, value, traceback_))
        print >> sys.stderr, error_msg
        print >> sys.stdout, error_msg

    sys.excepthook = exception_handler

    print args[0]
    server = open_server(args[0], options.port)

    logger.info('Starting the server...')
    server.serve()
    print 'done.'
    

# vim: set et ts=8 sw=4 sts=4
