import socket
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

conn = psycopg2.connect("dbname=sampledb user=userEYQ password=ch6YJjwttWXGbk1S host=172.30.171.226 port=5432")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
cur.execute("SELECT * FROM test;")
stuff = cur.fetchall()
conn.commit()
cur.close()
conn.close()
	
class RH(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		message = ['myapp test1' + 'Client: ' + self.address_string() + '<br>',
					'Server: ' + IP + ' aka ' + hostname + '<br>',
					'Date: ' + self.date_time_string() + '<br>']
		for i in stuff:
			message.append(str(i) + '<br>')
		for i in message:
			print(i)
			self.wfile.write(bytes(i, "utf8"))
		return

def run():
	server_address = (IP, 8080)
	httpd = HTTPServer(server_address, RH)
	httpd.serve_forever()
run()
