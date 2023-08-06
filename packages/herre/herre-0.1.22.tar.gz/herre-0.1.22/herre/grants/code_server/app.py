from herre.graphical import GraphicalBackend, has_webview_error
from herre.console.context import console, get_current_console
from herre.grants.base import BaseGrant
from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib.oauth2_session import OAuth2Session
from aiohttp import ClientSession
import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer






class RedirectHandler(BaseHTTPRequestHandler):
    backend = None
    stop_server = False
    token = False



    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print(self.path)
        RedirectHandler.token = self.backend.session.fetch_token(self.backend.token_url, client_secret=self.backend.config.client_secret, authorization_response=self.path)
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes('<body>', "utf-8"))
        self.wfile.write(bytes('''<script>
                                setTimeout(window.close(), 5000);
                                </script>''', "utf-8"))
        self.wfile.write(bytes("<p>You can close this website now!</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        RedirectHandler.stop_server = True
     
        




class AuthorizationCodeServerGrant(BaseGrant):
    refreshable = True

    def fetchToken(self, **kwargs):

        self.web_app_client = WebApplicationClient(self.config.client_id, scope=self.scope)

        # Create an OAuth2 session for the OSF
        self.session = OAuth2Session(
            self.config.client_id, 
            self.web_app_client,
            scope=self.scope, 
            redirect_uri=self.config.redirect_uri,
            
        )

        auth_url, state = self.session.authorization_url(self.auth_url)
        webbrowser.open(auth_url)

        RedirectHandler.backend = self

        httpd = HTTPServer(("localhost", 6767), RedirectHandler)
        print("Server started http://%s:%s" % ("localhost", 6767))

        while not RedirectHandler.stop_server:
            httpd.handle_request()
        
        self.token = RedirectHandler.token
        return RedirectHandler.token
