from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import mysql.connector

# Establish a connection to MySQL database
db = mysql.connector.connect(host='localhost', user='root', password='root', port=3306, database='phr_db')

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/records':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM phr_records")
            records = cursor.fetchall()
            records_json = json.dumps(records)
            self.wfile.write(records_json.encode())
        elif self.path == '/':
            self.send_response(200)
            message = 'Welcome to PHR'
            self.wfile.write(message.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        if self.path == '/records':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            # Extracting values from JSON data
            patient_id = data.get('patient_id')
            record_type = data.get('record_type')
            date_recorded = data.get('date_recorded')
            record_data = json.dumps(data.get('record_data'))

            cursor = db.cursor()
            sql = "INSERT INTO phr_records (patient_id, record_type, date_recorded, record_data) VALUES (%s, %s, %s, %s)"
            val = (patient_id, record_type, date_recorded, record_data)
            cursor.execute(sql, val)
            db.commit()

            self.send_response(201)
            self.end_headers()
            self.wfile.write(b'Record created successfully')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_PUT(self):
        if self.path.startswith('/records/'):
            record_id = int(self.path.split('/')[2])
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data.decode())

            record_data = json.dumps(data.get('record_data'))

            cursor = db.cursor()
            sql = "UPDATE phr_records SET record_data = %s WHERE id = %s"
            val = (record_data, record_id)
            cursor.execute(sql, val)
            db.commit()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Record updated successfully')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_DELETE(self):
        if self.path.startswith('/records/'):
            record_id = int(self.path.split('/')[2])

            cursor = db.cursor()
            sql = "DELETE FROM phr_records WHERE id = %s"
            val = (record_id,)
            cursor.execute(sql, val)
            db.commit()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Record deleted successfully')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8010):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port} ...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
