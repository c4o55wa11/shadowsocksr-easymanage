# /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import subprocess


def log_except(func):
    def w(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print e.message

    return w


@log_except
def check_active(pid_path='/var/run/shadowsocksr.pid'):
    is_exist = False
    if os.path.isfile(pid_path):
        with open(pid_path, 'r+b') as file_handler:
            ssr_pid = file_handler.readline().strip(os.linesep)
            if ssr_pid.isdigit() and os.path.isdir(''.join([os.path.sep, 'proc', os.path.sep, ssr_pid])):
                is_exist = True
    return is_exist


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
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())
            while True:
                ret = check_active()
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
