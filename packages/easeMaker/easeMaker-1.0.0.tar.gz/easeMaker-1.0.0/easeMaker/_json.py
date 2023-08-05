class Json:
    def get_json_value(self,json_data,key):
        import json
        list = json.loads(json_data)
        return list.get(key)    
