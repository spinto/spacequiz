@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

echo.
echo ============================================================
echo   Space Quiz - Windows Runner
echo ============================================================
echo.

rem ------------------------------------------------------------
rem Check PowerShell
rem ------------------------------------------------------------

where powershell.exe >nul 2>&1
if errorlevel 1 (
echo ERROR: PowerShell was not found.
exit /b 1
)

rem ------------------------------------------------------------
rem Look for an already installed WinPython.
rem WinPython extracts into WPy* rather than using the ZIP name.
rem ------------------------------------------------------------

set "PYTHON_EXE="

for /d %%D in ("%CD%\WPy*") do (
if exist "%%~fD\python\python.exe" (
set "PYTHON_EXE=%%~fD\python\python.exe"
set "WINPY_DIR=%%~fD"
)
)

if defined PYTHON_EXE (
echo Existing WinPython found:
echo   !WINPY_DIR!
echo.

goto CHECK_TKINTER

)

rem ------------------------------------------------------------
rem Find latest stable WinPython64 "dot" release.
rem ------------------------------------------------------------

echo Checking latest stable WinPython release...
echo.

set "DOWNLOAD_URL="

for /f "usebackq delims=" %%U in (`powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; $headers=@{'User-Agent'='WinPython-BAT-Installer'}; $releases=Invoke-RestMethod -Uri 'https://api.github.com/repos/winpython/winpython/releases?per_page=30' -Headers $headers; foreach($r in $releases) { if(-not $r.draft -and -not $r.prerelease) { $a=$r.assets | Where-Object { $_.name -match '^WinPython64-[0-9.]+dot\.zip$' } | Select-Object -First 1; if($a) { $a.browser_download_url; break } } }"`) do (
set "DOWNLOAD_URL=%%U"
)

if not defined DOWNLOAD_URL (
echo ERROR: Could not find a stable WinPython dot release.
exit /b 1
)

echo Download URL:
echo   %DOWNLOAD_URL%
echo.

rem ------------------------------------------------------------
rem Get archive filename
rem ------------------------------------------------------------

for %%F in ("%DOWNLOAD_URL%") do set "ARCHIVE_NAME=%%~nxF"

echo Archive:
echo   %ARCHIVE_NAME%
echo.

set "TEMP_ZIP=%TEMP%%ARCHIVE_NAME%"

rem ------------------------------------------------------------
rem Download
rem ------------------------------------------------------------

if exist "%TEMP_ZIP%" (
echo Found existing download:
echo   %TEMP_ZIP%
echo.
) else (
echo Downloading WinPython...
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%TEMP_ZIP%'"

if errorlevel 1 (
    echo.
    echo ERROR: Download failed.
    del "%TEMP_ZIP%" >nul 2>&1
    exit /b 1
)

)

if not exist "%TEMP_ZIP%" (
echo ERROR: Downloaded archive was not found.
exit /b 1
)

rem ------------------------------------------------------------
rem Remember which WPy directories exist before extraction.
rem ------------------------------------------------------------

set "BEFORE_FILE=%TEMP%\winpython-before-%RANDOM%.txt"

dir /b /ad "%CD%\WPy*" 2>nul > "%BEFORE_FILE%"

rem ------------------------------------------------------------
rem Extract
rem ------------------------------------------------------------

echo.
echo Extracting WinPython...
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; Expand-Archive -LiteralPath '%TEMP_ZIP%' -DestinationPath '%CD%' -Force"

if errorlevel 1 (
echo.
echo ERROR: Extraction failed.
del "%BEFORE_FILE%" >nul 2>&1
exit /b 1
)

del "%TEMP_ZIP%" >nul 2>&1

rem ------------------------------------------------------------
rem Find the actual extracted WPy directory.
rem ------------------------------------------------------------

set "PYTHON_EXE="

for /d %%D in ("%CD%\WPy*") do (
if exist "%%~fD\python\python.exe" (
set "PYTHON_EXE=%%~fD\python\python.exe"
set "WINPY_DIR=%%~fD"
)
)

del "%BEFORE_FILE%" >nul 2>&1

if not defined PYTHON_EXE (
echo.
echo ERROR: Python was not found after extraction.
echo.
echo Expected a directory such as:
echo   %CD%\WPy64-313150\python\python.exe
echo.
exit /b 1
)

echo.
echo WinPython installed successfully:
echo   %WINPY_DIR%
echo.

:CHECK_TKINTER

rem ------------------------------------------------------------
rem Check tkinter.
rem ------------------------------------------------------------

echo Checking tkinter...

"%PYTHON_EXE%" -c "import tkinter; print('tkinter is available - Tk version:', tkinter.TkVersion)" >nul 2>&1

if not errorlevel 1 (
echo tkinter is already available.
echo.
goto DONE
)

echo tkinter is not available.
echo.
echo Attempting to install the PyPI tk package...
echo.

"%PYTHON_EXE%" -m pip install tk

if errorlevel 1 (
echo.
echo ERROR: Could not install the tk package.
exit /b 1
)

echo.
echo Verifying tkinter...

"%PYTHON_EXE%" -c "import tkinter; print('Tk version:', tkinter.TkVersion)"

if errorlevel 1 (
echo.
echo ERROR: tkinter is still unavailable after installing tk.
exit /b 1
)

:DONE

echo.
echo Compiling Quiz application...
start /B "Space Quiz" "%PYTHON_EXE%" "spacequiz_build.py"

endlocal
exit /b 0
