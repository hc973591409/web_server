from multiprocessing import Process
import socket
import re
import sys


class HTTPserver(object):
    def __init__(self, port, application):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口重用
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("", port))
        self.app = application
        self.response_body = ""
        self.headers = ""
        self.content = ""

    def start(self):
        self.server_socket.listen(129)
        print("服务器框架开启")

        while True:
            client_socket, client_addr = self.server_socket.accept()
            print("(%s, %s)已经连接" % (client_addr[0], client_addr[1]))
            client_process = Process(target=self.client_headle, args=(client_socket,))
            client_process.start()
            # 客户端已经作为实参传递，应该及时关闭，释放内存，防止内存泄漏
            client_socket.close()

    def client_headle(self, client_socket):
        request_data = client_socket.recv(2018)
        request_string = request_data.decode("utf-8")
        string_list = request_string.splitlines()
        string = string_list[0]
        file_name = re.match(r"\w+\s(/[^ ]*)", string).group(1)
        method = re.match(r"(\w+)\s/[^ ]*", string).group(1)
        # print(file_name)
        # print(method)
        # 构建一个字典传入app
        env = {"PATH_INFO": file_name, "METHOD": method}
        self.response_body = self.app(env, self.start_response)
        self.content = self.headers + '\r\n' + self.response_body
        client_socket.send(self.content.encode('utf-8'))

    def start_response(self, status, headers):
        self.headers = "HTTP /1.1 " + status + "\r\n"
        for header in headers:
            self.headers += '%s: %s\r\n' % (header[0], header[1])


def main():
    if len(sys.argv) < 2:
        exit("请输入正确的格式 ex: moudel:app")
    try:
        model_name, app_name = (sys.argv[1]).split(":")

    except Exception as e:
        print(e)
        print("格式不正确")
    finally:
        m = __import__(model_name)
        try:
            app = getattr(m, app_name)
        except Exception as e:
            print(e)
            print("属性不正确")

        http_server = HTTPserver(8899, app)
        http_server.start()


if __name__ == '__main__':
    main()

