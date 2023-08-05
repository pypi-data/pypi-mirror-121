class Time:
    def get_hour(self):
        import datetime as datetime
        dt = datetime.datetime.now()
        return dt.strftime("%H")
    def get_minute(self):
        import datetime as datetime
        dt = datetime.datetime.now()    
        return dt.strftime("%M")

    def get_second(self):
        import datetime as datetime
        dt = datetime.datetime.now()    
        return dt.strftime("%S")

    def get_meridian(self):
        import datetime as datetime
        dt = datetime.datetime.now()    
        return dt.strftime("%p")