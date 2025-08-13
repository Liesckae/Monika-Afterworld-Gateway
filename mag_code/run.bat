@echo off

REM ================================
REM Run a Python script with pythonw
REM Usage: run.bat <path_to_python_script>
REM Returns: 0 on success, 1 on failure
REM ================================

REM Ensure the script path is provided
if "%1"=="" (
    echo Error: No file path provided.
    echo Usage: run.bat ^<path_to_python_script^>
    exit /b 1
)

REM Resolve the full path of the script
for %%I in ("%1") do set "SCRIPT_PATH=%%~fI"

REM Check if the file exists
if not exist "%SCRIPT_PATH%" (
    echo Error: File "%SCRIPT_PATH%" not found.
    exit /b 1
)

REM Try to find pythonw.exe
where pythonw.exe >nul 2>&1
if %ERRORLEVEL%==0 (
    set "PYTHON_EXE=pythonw.exe"
) else (
    echo Error: pythonw.exe not found in PATH.
    exit /b 1
)

REM Run the Python script
echo Running "%SCRIPT_PATH%" with %PYTHON_EXE%...
"%PYTHON_EXE%" "%SCRIPT_PATH%"
set "PY_EXIT=%ERRORLEVEL%"

REM Check the exit code
if "%PY_EXIT%"=="0" (
    echo Script executed successfully.
    exit /b 0
) else (
    echo Script failed with exit code %PY_EXIT%.
    exit /b 1
)