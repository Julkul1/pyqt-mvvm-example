@echo off
REM Windows batch file for running pyqt-mvvm-example management scripts
REM Usage: run.bat [script] [command] [args...]

if "%1"=="" (
    echo Usage: run.bat [script] [command] [args...]
    echo.
    echo Available scripts:
    echo   dev     - Development utilities
    echo   build   - Build utilities  
    echo   setup   - Setup utilities
    echo   deploy  - Deployment utilities
    echo   clean   - Cleanup utilities
    echo   check   - Health check utilities
    echo.
    echo Examples:
    echo   run.bat dev check-all
    echo   run.bat setup all --dev
    echo   run.bat build exe
    echo   run.bat clean all
    echo   run.bat check all
    exit /b 1
)

python scripts/run.py %* 