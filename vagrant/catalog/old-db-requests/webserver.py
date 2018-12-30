from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from request_db_items import get_Restaurants
from add_db_items import add_Restaurants, update_Restaurants
from delete_db_items import delete_Restaurants
import cgi


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!" # this line is what is show to the browser
                output += "<form method='POST' enctype='multipart/form-data' action='hello'>" \
                          "<h2>What would you like me to say?</h2><input name='message' type='text'>" \
                          "<input type='submit' value='Submit'> </form>"
                output += "</html></body>"

                self.wfile.write(output)
                print("pagina inicial")
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                restaurants = get_Restaurants()
                output = ""
                output += "<html><body>"
                output += "<h2><a href = '/restaurants/new'>create a new restaurant</a><h2>"
                output += "<ul>"
                for restaurant in restaurants:
                    output += "<li><h3>" + restaurant.name + "</h3>"
                    output += "<h4><a href = 'restaurants/%s/edit'>edit</a></h4>" % restaurant.id
                    output += "<h4><a href = 'restaurants/%s/delete'>delete</a></h4></li>" % restaurant.id
                output += "</ul>"
                output += "Hello!  <a href = '/hello'>back to hello</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='hello'>" \
                          "<h2>What would you like me to say?</h2><input name='message' type='text'>" \
                          "<input type='submit' value='Submit'> </form>"
                output += "</html></body>"
                self.wfile.write(output)
                print("pagina inicial")
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantIdPath = self.path.split("/")[2]
                myRestaurant = get_Restaurants(restaurantIdPath)
                if myRestaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += myRestaurant.name
                    output += "<h1>"
                    output += "</h1>"
                    output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/edit'>" % restaurantIdPath
                    output += "<input name = 'newRestaurantName' type = 'text' placeholder = '%s' > " % myRestaurant.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
                    return

            if self.path.endswith("/delete"):
                restaurantIdPath = self.path.split("/")[2]
                myRestaurant = get_Restaurants(restaurantIdPath)
                if myRestaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>"
                    output += myRestaurant.name
                    output += "</h1>"
                    output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIdPath
                    output += "<h2>Are you sure to delete this?</h2>"
                    output += "<input type='submit' value='Delete'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
                    return

        except IOError:
            self.send_error(404, "file not found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    restaurantIDPath = self.path.split("/")[2]
                    myRestaurantQuery = get_Restaurants(restaurantIDPath)
                    if myRestaurantQuery != []:
                        delete_Restaurants(myRestaurantQuery)
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = get_Restaurants(restaurantIDPath)
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        update_Restaurants(myRestaurantQuery)
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    add_Restaurants(messagecontent)

                    self.send_response(303)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^c used, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
