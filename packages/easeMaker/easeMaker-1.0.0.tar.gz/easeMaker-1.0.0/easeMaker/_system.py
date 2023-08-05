
class System:
    class Clipboard:
        def __init__(self, encoding="utf-8"):
            import ctypes
            from ctypes import wintypes
            self.CF_UNICODETEXT = 13
            self.dg = encoding
            self.user32 = ctypes.windll.user32
            self.kernel32 = ctypes.windll.kernel32
            self.OpenClipboard = self.user32.OpenClipboard
            self.OpenClipboard.argtypes = wintypes.HWND,
            self.OpenClipboard.restype = wintypes.BOOL
            self.CloseClipboard = self.user32.CloseClipboard
            self.CloseClipboard.restype = wintypes.BOOL
            self.EmptyClipboard = self.user32.EmptyClipboard
            self.EmptyClipboard.restype = wintypes.BOOL
            self.GetClipboardData = self.user32.GetClipboardData
            self.GetClipboardData.argtypes = wintypes.UINT,
            self.GetClipboardData.restype = wintypes.HANDLE
            self.SetClipboardData = self.user32.SetClipboardData
            self.SetClipboardData.argtypes = (wintypes.UINT, wintypes.HANDLE)
            self.SetClipboardData.restype = wintypes.HANDLE
            self.GlobalLock = self.kernel32.GlobalLock
            self.GlobalLock.argtypes = wintypes.HGLOBAL,
            self.GlobalLock.restype = wintypes.LPVOID
            self.GlobalUnlock = self.kernel32.GlobalUnlock
            self.GlobalUnlock.argtypes = wintypes.HGLOBAL,
            self.GlobalUnlock.restype = wintypes.BOOL
            self.GlobalAlloc = self.kernel32.GlobalAlloc
            self.GlobalAlloc.argtypes = (wintypes.UINT, ctypes.c_size_t)
            self.GlobalAlloc.restype = wintypes.HGLOBAL
            self.GlobalSize = self.kernel32.GlobalSize
            self.GlobalSize.argtypes = wintypes.HGLOBAL,
            self.GlobalSize.restype = ctypes.c_size_t
            self.GMEM_MOVEABLE = 0x0002
            self.GMEM_ZEROINIT = 0x0040

        def get_text(self):
            import ctypes
            self.OpenClipboard(None)

            handle = self.GetClipboardData(self.CF_UNICODETEXT)
            pcontents = self.GlobalLock(handle)
            size = self.GlobalSize(handle)
            if pcontents and size:
                raw_data = ctypes.create_string_buffer(size)
                ctypes.memmove(raw_data, pcontents, size)
                text = raw_data.raw.decode(self.dg)
            else:
                text = None

            self.GlobalUnlock(handle)
            self.CloseClipboard()
            return text

        def send_text(self, text):
            import ctypes
            s = text
            if not isinstance(s, type(u"")):
                s = s.decode('mbcs')
            data = s.encode('utf-16le')
            self.OpenClipboard(None)
            self.EmptyClipboard()
            handle = self.GlobalAlloc(
                self.GMEM_MOVEABLE | self.GMEM_ZEROINIT, len(data) + 2)
            pcontents = self.GlobalLock(handle)
            ctypes.memmove(pcontents, data, len(data))
            self.GlobalUnlock(handle)
            self.SetClipboardData(self.CF_UNICODETEXT, handle)
            self.CloseClipboard()

    def get_clipboard_data(self, encoding="utf-8"):
        return self.Clipboard(encoding).get_text()

    def set_clipboard_data(self, text):
        self.Clipboard().send_text(text)

    def isWindows(self):
        import sys
        if "win" in sys.platform:
            return True
        else:
            return False

    def isMac(self):
        import sys
        if "mac" in sys.platform:
            return True
        else:
            return False

    def isLinux(self):
        import sys
        if "linux" in sys.platform:
            return True
        else:
            return False
    def get_current_user(self):
        import os
        return os.getlogin()        
    
    def getTempDir(self):
        import os

        if os.path.exists(f"C:/Users/{os.getlogin()}/AppData/Local/Temp"):
            return f"C:/Users/{os.getlogin()}/AppData/Local/Temp"
        else:
            try:
                import win32api
                return win32api.GetTempPath()
            except ImportError:
                import socket
                if socket.gethostbyname(socket.gethostname()) == "127.0.0.1":
                    raise Exception("Please install win32api")
                else:
                    os.system("pip install win32api")
                    import win32api
                    return win32api.GetTempPath()
    def run_ps1_command(self,cmd):
        if self.isWindows():
            import subprocess
            subprocess.run(["powershell", "-Command", cmd],shell=True)
        else:
            raise OSError("This Function only supports Windows OS. And does not support: {} OS".format(self.get_OS()))
    def get_ps1_command_output(self, cmd, decoding="utf-8"):
        if self.isWindows():
            import os
            try:
                import subprocess
                output = subprocess.run(
                    ["powershell", "-Command", cmd], stdout=subprocess.PIPE, shell=True)
                return output.stdout.decode(decoding)
            except ImportError:
                import socket
                if socket.gethostbyname(socket.gethostname()) == "127.0.0.1":
                    raise Exception("Please install subprocess")
                else:
                    os.system("pip install subprocess")
                    output = subprocess.run(
                        ["powershell", "-Command", cmd], stdout=subprocess.PIPE, shell=True)
                    return output.stdout.decode(decoding)
        else:
            raise OSError("This Function only supports Windows OS. And does not support: {} OS".format(self.get_OS()))        

    def get_shell_command_output(self,cmd, decoding="utf-8"):
        import os
        try:
            import subprocess
            output = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
            return output.stdout.decode(decoding)
        except ImportError:
            import socket
            if socket.gethostbyname(socket.gethostname()) == "127.0.0.1":
                raise Exception("Please install subprocess")
            else:
                os.system("pip install subprocess")
                output = subprocess.run(
                    cmd, stdout=subprocess.PIPE, shell=True)
                return output.stdout.decode(decoding)

    def get_ipaddress(self):
        import socket
        return socket.gethostbyname(socket.gethostname())

    def get_OS(self):
        import sys
        return sys.platform