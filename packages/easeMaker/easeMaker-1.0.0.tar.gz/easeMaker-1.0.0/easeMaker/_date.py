class Date:
    def get_year(self):
        import datetime as datetime
        dt = datetime.datetime.now()    
        return dt.strftime("%Y")
    def get_month(self):
        import datetime as datetime
        dt = datetime.datetime.now()    
        return dt.strftime("%m")
    def get_day(self):
        import datetime as datetime
        dt = datetime.datetime.now()    
        return dt.strftime("%d")