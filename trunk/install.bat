ECHO "Installing packages for Auditron..."

SET PANDAPYTHON=C:\Panda3D-1.4.2\python\ppython.exe

ECHO "Installing cytpes"
CD packages\ctypes
CALL %PANDAPYTHON% setup.py install
CD ..

ECHO "Installing pywiiuse"
CD pywiiuse
CALL %PANDAPYTHON% setup.py install"
CD ..

ECHO "Copying the Wiiuse DLL"
COPY wiiuse.dll "C:\Panda3D-1.4.2\bin\wiiuse.dll"

ECHO "Done"
