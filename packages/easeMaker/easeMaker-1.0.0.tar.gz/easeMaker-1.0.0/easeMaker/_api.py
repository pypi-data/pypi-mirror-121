import requests


class API:
    def __init__(self,host="localhost",port=5000,app_name=__file__):
        self.host = host
        self.port = port    
        from flask import Flask
        self.app = Flask(app_name)    
        
    def createAPI(self,api_return=""):   
        self.vtr = api_return        
        app = self.app
        @app.route("/")
        def api():
            return self.vtr
        
    def start(self):
        self.app.run(self.host,self.port,False)    
    def get_url(self):
        return f"http://{self.host}:{self.port}/"
api = API(app_name="API")        

api.createAPI(api_return="HellcxasxaSXaso!")
rq = requests.get(api.get_url())
print(rq.text)    
api.start() 
  