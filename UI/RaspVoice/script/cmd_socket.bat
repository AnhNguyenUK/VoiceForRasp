curl -d data=SOCKET -d data=%1 root@mysmartsocketserver.local:1337 -v
timeout /t 1
curl root@mysmartsocketserver.local:1337 