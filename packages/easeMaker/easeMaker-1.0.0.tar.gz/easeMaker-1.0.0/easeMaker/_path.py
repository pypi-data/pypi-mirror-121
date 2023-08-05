class Path: 
    def get_parent_directory(self,path):
        from pathlib import Path
        import os
        path = os.path.abspath(path)
        return Path(path).resolve().parents[1]
    def getcwd(self):
        import os
        return os.getcwd()
    def exists(self,path):
        import os
        return os.path.exists(self,path)