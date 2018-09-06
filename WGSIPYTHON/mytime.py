import time


def application(env, start_response):
    status = '200 Ok'
    heardes = [('Myserver', 'WSGISever'), ('Accept', 'text/plain')]
    start_response(status, heardes)
    return time.ctime()
