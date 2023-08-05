from _system import System
class SystemCleaner:
    def clearsSystemLogs(self):
        import os
        if System.isWindows():
            os.system("c:&&cd wind*&&del *.log /a /s /q /f") 
    def clearTempFiles(self):  
        import os
        os.system("del /s /f /q C:\Windows\Prefetch\*.*")
        os.system("del /s /f /q C:\Windows\Temp\*.*")
        os.system("del /s /f /q %USERPROFILE%\appdata\local\temp\*.*")
        os.system("del %temp%\*.* /s /q")
    def defragC(self):
        import os
        os.system("defrag c:")  
    def cleanC(self):
        import os
        os.system("cleanmgr /sagerun")  
    def deleteAllJunkFiles(self):
        import os
        os.system("cleanmgr /verylowdisk /d")                    