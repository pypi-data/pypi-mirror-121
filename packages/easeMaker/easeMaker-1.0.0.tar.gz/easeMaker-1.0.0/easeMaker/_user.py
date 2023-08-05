class User:
    def __init__(self):
        pass
    def isAdmin(self):
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
       