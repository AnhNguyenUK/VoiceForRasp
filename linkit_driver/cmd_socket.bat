curl -d data=SOCKET -d data=%1 root@mysmartsocketserver.local:1337
timeout /t 1
curl root@mysmartsocketserver.local:1337