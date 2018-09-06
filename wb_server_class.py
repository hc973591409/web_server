from multiprocessing import Process
import socket
import re

HTML_DIR = 'html'


# noinspection PyUnresolvedReferences
class WebServer(object):
    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 新建套接字
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 这是端口可以一直占用，不会出现掉线了不能再用
        self.server.bind(("", port))

    def start(self):
        self.server.listen(128)
        print("web服务器已经开启")
        while True:
            client, client_address = self.server.accept()
            print("%s,%s 已经连接" % (client_address[0], client_address[1]))
            client_process = Process(target=self.handler_client, args=(client,))
            client_process.start()
            client.close()

    @staticmethod
    def handler_client(client):
        """
        :param client: 客户端套接字
        :return:
        """
        recv_data = client.recv(1024)
        recv_string = recv_data.decode('utf-8')
        print(recv_string)
        str_list = recv_string.splitlines()
        print(str_list)  # test
        string = str_list[0]
        m = re.match(r'\w+\s(/[^ ]*)', string)
        file_name = m.group(1)
        if '/' == file_name:
            # 显示主页
            # 构建头
            header_start = 'HTTP/1.1 200 OK \r\n'
            headers_1 = 'Content-Type: text/html \r\n'
            print("*" * 50)
            print("filename = ", HTML_DIR + file_name)
            try:
                file_name = './html' + '/index.html'
                with open(file_name, 'rb') as f:
                    response_body = f.read()
                    response_body = response_body.decode('utf-8')
            except Exception as e:
                print(e)

            response = header_start + headers_1 + '\r\n' + response_body

            client.send(bytes(response, 'utf-8'))
        elif '/index.html' == file_name:
            # 显示主页
            # 构建头
            print("*" * 50)
            print("filename = ", HTML_DIR + file_name)
            header_start = 'HTTP/1.1 200 OK \r\n'
            headers_1 = 'Content-Type: text/html \r\n'
            with open(HTML_DIR + file_name, 'rb') as f:
                response_body = f.read()
                response_body = response_body.decode('utf-8')
            response = header_start + headers_1 + '\r\n' + response_body
            client.send(bytes(response, 'utf-8'))
        else:
            header_start = 'HTTP/1.1 404 NOT FIND \r\n'
            headers_1 = 'Content-Type: text/html \r\n'
            response_body = '<h1>sorry not find</h1>'
            response = header_start + headers_1 + '\r\n' + response_body
            client.send(bytes(response, 'utf-8'))


def main():
    web_server = WebServer(8001)
    web_server.start()


if __name__ == '__main__':
    main()
