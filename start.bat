@echo off

cd /d "C:\nginx"
start nginx.exe

cd /d "C:\Program Files\mosquitto"
start mosquitto -v -c broker.conf &