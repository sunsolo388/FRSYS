set shell=wscript.createObject("wscript.shell")  
run=shell.Run("run_django.bat", 0)
run=shell.Run("open_index.bat", 0)