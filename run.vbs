set shell=wscript.createObject("wscript.shell")  
run=shell.Run("exec\run_django.bat", 0)
run=shell.Run("exec\open_index.bat", 0)