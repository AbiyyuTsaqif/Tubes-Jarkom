import socket
import os


# fungsi untuk membaca isi file dalam bentuk binary
def read_file(filepath):
    file = open(filepath, 'rb')
    content = file.read()
    return content

# http response


def http_response(file):
    response = ''  # inisisasi response

    # mengambil filename dari request dengan metode split
    filename = file.split()[1][1:]

    # menentukan filepath dengan menggabungkan base directory dengan filename menggunakan metode join
    filepath = os.path.join(DIRECTORY, filename)

    if os.path.isfile(filepath):  # pengkondisian jika file ditemukan
        content = read_file(filepath)
        # buat HTTP header
        http_header = "HTTP/1.1 200 OK\r\n"
        http_header += f"Content-Length: {len(content)}\r\n"
        http_header += "Content-Type: text/html\r\n"
        http_header += "\r\n"
        # gabungkan header dengan konten file
        response = http_header.encode('utf-8') + content
    else:  
        # jika file tidak ada, buat HTTP header dengan status code 404 Not Found
        http_header = "HTTP/1.1 404 Not Found\r\n"
        http_header += "Content-Length: 0\r\n"
        http_header += "\r\n"
        # kirimkan response dengan header saja (tanpa konten)
        response = http_header.encode('utf-8')
    return response


# Alamat Server
HOST = '127.0.0.1'

# Port Server
PORT = 8241

# base directory folder
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Buat TCP Scoket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind alamat dan port tertentu
s.bind((HOST, PORT))

# Tunggu Koneksi masuk
s.listen()

# Pesan konfirmasi bahwa server telah berjalan
print(f"Server berjalan di {HOST} port {PORT} (http://{HOST}:{PORT})......")

while True:
    # Menerima koneksi server
    connnectionSocket, addr = s.accept()

    # Membaca data yang dikirimkan client
    file = connnectionSocket.recv(1024).decode()

    # memanggil fungsi http response untuk menampilkan http respons
    http_respons = http_response(file)

    # print method path dan protocol yang terdapat pada variabel request
    method, path, protocol = file.split('\n')[0].split()
    print("file telah berhasil terbuka")
    print('Method :', method)
    filepath = os.path.join(DIRECTORY, file.split()[1][1:])
    print("Directory File .py : ", DIRECTORY)
    print('Path :', filepath)
    print('Protocol: ', protocol)

    connnectionSocket.sendall(http_respons)  # kirim response ke client
    connnectionSocket.close()  # Menutup koneksi