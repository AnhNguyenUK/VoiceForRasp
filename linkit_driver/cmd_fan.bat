curl -d data=SOCKET -d data=%1 root@mysmartfanserver.local:1337
timeout /t 1
curl root@mysmartfanserver.local:1337