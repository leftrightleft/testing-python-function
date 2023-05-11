import sqlite3
import os
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

def connect_to_db(request):
    # Parse the query parameters
    query_components = parse_qs(urlparse(request.path).query)
    name = query_components["parameter"][0] if "parameter" in query_components else None

    # Open a connection to the database
    database_uri = os.environ.get('SQLITE_URI', ':memory:')
    database = sqlite3.connect(database_uri, check_same_thread=False)

    # Execute a SQL query
    cursor = database.cursor()
    cursor.execute(
        "SELECT * FROM books WHERE name LIKE '%" + name + "%'"
    )

    # Iterate over the rows and print the results
    for x in cursor:
        print(x)

def run_server():
    # Start the web server
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, connect_to_db)
    print("Server running on port 8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
