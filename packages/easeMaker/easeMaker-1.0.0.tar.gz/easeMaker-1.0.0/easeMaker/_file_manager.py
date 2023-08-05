class File_Manager:   
    class File:
        def __init__(self,filename,mode='r', buffering=-1, encoding=None,errors=None, newline=None):
            self.filename  = filename
            self.mode      = mode
            self.buffering = buffering
            self.encoding  = encoding
            self.errors    = errors
            self.newline   = newline
        def open(self):
            import io
            filename  = self.filename             
            mode      = self.mode                  
            buffering = self.buffering           
            encoding  = self.encoding          
            errors    = self.errors          
            newline   = self.newline          
            return io.open(filename,mode, buffering, encoding, errors, newline)
        def write_str(self,text):
            with self.open(self.filename,"w") as f:
                f.write(text)   
        def read(self):
            with self.open(self.filename) as f:
                return f.read()            
        def create(self,text):
            with self.open(self.filename,"x") as f:
                f.write(text)  
        def write_bytes(self,text):
            with self.open(self.filename,"wb") as f:
                f.write(text)  
        def read_bytes(self):
            with self.open(self.filename,"rb") as f:
                return f.read()             
                  
                
    def write_str(self,text):
        with open(self.filename,"w") as f:
            f.write(text)   
    def read(self):
        with open(self.filename) as f:
            return f.read()            
    def create(self,text):
        with open(self.filename,"x") as f:
            f.write(text)  
    def write_bytes(self,text):
        with open(self.filename,"wb") as f:
            f.write(text)  
    def read_bytes(self):
        with open(self.filename,"rb") as f:
            return f.read()   
    def get_filename(self,path):
        import os
        base, extension = os.path.splitext(path)
        return os.path.basename(base)
    def get_absolute_filename(self,path):
        import os
        base, extension = os.path.splitext(path)
        return base   
    def get_file_extension(self,path):
        import pathlib
        path = pathlib.Path(path)
        return ''.join(path.suffixes)                                                                                