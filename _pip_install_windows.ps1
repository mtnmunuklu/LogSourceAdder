# To run this file you will need to install python3 and then open Powershell as administrator and first run:
# Set-ExecutionPolicy Unrestricted
# Then run this script:
# .\_pip_install_windows.ps1

$VIRTUAL_ENV = $PWD.Path + '\venv'
Write-Host("Virtual Envirement File")
py -3 -m venv venv
.\venv\Scripts\Activate.ps1

# Check you have an activated venv and you're in the right directory for it
if($VIRTUAL_ENV -eq ($PWD.Path+'\venv') ) {
    Write-Host("Upgrading pip in present virtual environment")
    python -m pip install --upgrade pip
    Write-Host("Installing requirements in present virtual environment")
    pip install python-dotenv
    pip install pylint
    pip install mysql-connector-python
}else {
    Write-Host("
    ---------------------------------------------------------------------------------
        You need to have THIS directory's venv activated to install requirements!
        You are now in:    $($PWD.Path)
    ---------------------------------------------------------------------------------
    ")
}