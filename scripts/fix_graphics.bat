@echo off
cd "%~dp0"
copy config.txt config_backup.txt
powershell -Command "(Get-Content config.txt) -replace 'Renderer=OpenGL', 'Renderer=Direct3D' | Set-Content config.txt"
echo Graphics fixed. Use Alt+Enter for fullscreen toggle if needed.
pause
