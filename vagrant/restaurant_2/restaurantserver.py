## import webserver libraries
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
## import CRUD operations
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

## Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                change_id = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=change_id).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += f"<h1>Are you sure?</h1>"
                    output += f"<form method='POST' enctype='multipart/form-data' action='/restaurants/{change_id}/delete'>"
                    output += f"<input type='submit' value='Confirm'></form>"
                    output += "</body></html>"
                    self.wfile.write(output.encode())
                    print(output)
            if self.path.endswith("/edit"):
                change_id = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=change_id).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += f"<h2>Edit Restaurant {myRestaurantQuery.name}</h2>"
                    output += f"<form method='POST' enctype='multipart/form-data' action='/restaurants/{change_id}/edit'>"
                    output += f"<input name='message' type='text' placeholder={myRestaurantQuery.name}><input type='submit' value='Rename'></form>"

                    output += "</body></html>"
                    self.wfile.write(output.encode())
                    print(output)
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurant_names = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Create a new Restaurant</a><br>"
                for restaurant in restaurant_names:
                    output += restaurant.name + "<br>"
                    output += f"<a href='/restaurants/{restaurant.id}/edit'>Edit</a><br>"
                    output += f"<a href='/restaurants/{restaurant.id}/delete'>Delete</a><br><br>"

                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>Make a new Restaurant.</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='message' type='text'><input type='submit' value='Create'></form>"


                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
        except IOError:
            self.send_error(404, f"File not found {self.path}")

        
    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                change_id = self.path.split('/')[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id=change_id).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                return
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = pdict['boundary'].encode('utf-8')
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    restaurantName = messagecontent[0].decode('utf-8')
                    change_id = self.path.split('/')[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=change_id).one()
                    if myRestaurantQuery:
                        myRestaurantQuery.name = restaurantName
                        session.add(myRestaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

                return
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = pdict['boundary'].encode('utf-8')
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    restaurantName = messagecontent[0].decode('utf-8')
                    newRestaurant = Restaurant(name = restaurantName)
                    session.add(newRestaurant)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return
        except:
            pass




## Call the webserver
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print(f"Web server is running on port {port}.")
        server.serve_forever()

    except KeyboardInterrupt:
        print(f"Keyboard interrupt, stopping web server...")
        server.socket.close()




if __name__=='__main__':
    main()
