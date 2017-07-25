# /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import subprocess


def params_check(func):
    def w(*args, **kwargs):
        if kwargs.get('port', None):
            if isinstance(kwargs['port'], int) and 0 < kwargs['port'] < 65536:
                return func(*args, **kwargs)
            else:
                return None
        else:
            return None

    return w


def log_except(func):
    def w(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print e.message

    return w


@log_except
@params_check
def check_active(port=8080):
    command = "netstat -ano|grep tcp|grep :%d|grep -v grep|wc -l" % port
    pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output = pipe.stdout.read(1024)
    return int(output) > 0


@log_except
def run_ssr(path='.' + os.path.sep, file_name='server.py'):
    py_path = ''.join([path, file_name])
    command = "python %s -d start" % py_path
    output = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
    return output.stdout.read(1024)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '[-] port miss'
        sys.exit(0)
    port = int(sys.argv[1])

    server_path = sys.argv[2] if len(sys.argv) > 2 else os.path.sep
    if not server_path.endswith(os.path.sep):
        server_path += os.path.sep
    server_file_name = sys.argv[3] if len(sys.argv) > 3 else 'server.py'
    pid = os.fork()
    if pid == 0:
        # os.chdir("/")
        os.umask(0)
        os.setsid()
        cid = os.fork()
        if cid == 0:
            stdin, stdout, stderr = '/dev/null', '/dev/null', '/dev/null'
            for f in sys.stdout, sys.stderr:
                f.flush()
            si = file(stdin, 'r')
            so = file(stdout, 'a+')
            se = file(stderr, 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            # os.dup2(so.fileno(), sys.stdout.fileno())
            # os.dup2(se.fileno(), sys.stderr.fileno())
            while True:
                ret = check_active(port=port)
                if ret is not None:
                    pass
                    if ret:
                        time.sleep(30)
                    else:
                        print '[-] not find ssr'
                        run_ssr(server_path, server_file_name)
                else:
                    print '[-] check_active method params check error'
        else:
            sys.exit(0)
    else:
        sys.exit(0)
