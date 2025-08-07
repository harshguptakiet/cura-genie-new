@echo off
echo Starting CuraGenie Backend and Frontend...
echo.

echo Starting Backend...
cd curagenie-backend
start "CuraGenie Backend" cmd /k "python main.py"

echo Waiting for backend to start...
timeout /t 10 /nobreak > nul

echo Starting Frontend...
cd ..
start "CuraGenie Frontend" cmd /k "npm run dev"

echo Both services are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul
