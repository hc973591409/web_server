import time
HTML_DIR = './html'


class MyFrameWeb(object):
    def __init__(self, urls):
        # 初始化路由
        self.urls = urls
        self.status = ''
        self.headers = ''

    def __call__(self, env, start_response):
        path = env.get("PATH_INFO")
        # 静态文件的时候
        if path.startswith('/static'):
            try:
                print("------------")
                print(HTML_DIR + '/index.html')
                f = open(HTML_DIR + '/index.html', 'rb')
            except IOError:
                self.status = '404 NOT FIND'
                self.headers = [("Content/Type", "html/plain")]
                start_response(self.status, self.headers)
                return "<h1>22NOT FIND DONT EXIST</h1>"
            else:
                self.status = '200 OK'
                self.headers = [("Content/Type", "html/plain")]
                start_response(self.status, self.headers)
                return f.read().decode('utf-8')

        for file_name, handler in self.urls:
            if file_name == env.get("PATH_INFO", '/'):
                return handler(env, start_response)

        else:
            self.status = '404 NOT FIND'
            self.headers = [("Content/Type", "html/plain")]
            start_response(self.status, self.headers)
            return "<h1>37NOT FIND DONT EXIST</h1>"


def show_time(env, start_response):
    status = '200 OK'
    headers = [("Content/Type", "html/plain")]
    start_response(status, headers)
    return '<h1>' + time.ctime() + '</h1>'


def say_hello(env, start_response):
    status = '200 OK'
    headers = [("Content/Type", "html/plain")]
    start_response(status, headers)
    return '<h1>hello world</h1>'


urls = [
    ('/', show_time),
    ('/time', show_time),
    ('/sayhello', say_hello)
]

app = MyFrameWeb(urls)
