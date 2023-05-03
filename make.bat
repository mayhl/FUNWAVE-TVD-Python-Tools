

@echo off

set arg=%1


set py=py
set pip=pip
set venv=.venv
set pkgname=funwavetvdtools
set poetry_path=%APPDATA%\Python\Scripts
set poetry=%poetry_path%\poetry




call:Switch switch %arg% || (

:switch-install_poetry
   curl -sSL https://install.python-poetry.org | %py% -
   set poetry_path=%APPDATA%\Python\Scripts
::   path|find /i "%poetry_path%" > nul || set path=%poetry_path%;%path%
   goto:EOF
  
:switch-venv
   if not exist %venv% %py% -m venv %venv% 
   echo Use 'call %venv%/Scripts/activate.bat' to activate virtual environment'
   goto:EOF

:switch-poetry_setup
   %poetry% lock --no-update
   %poetry% install
   goto:EOF
   
:switch-install
   call make.bat poetry_setup
   %pip% install .
   goto:EOF
   
:switch-develop
   call make.bat poetry_setup
   %pip% install -e .
   goto:EOF

:switch-uninstall
   %pip% uninstall %pkgname%
   goto:EOF
   
:switch-
   @echo ERROR: Invalid option '%ARG%'
   goto:EOF
)

:Switch
goto:%1-%2 2>nul || (
    type nul>nul
    goto:%1-
)
exit /b


