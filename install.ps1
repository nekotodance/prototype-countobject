Write-Host "========================================"
Write-Host "prototype-countobject"
Write-Host "install start."
Write-Host "========================================"

$folder = Split-Path -Parent $MyInvocation.MyCommand.Definition
$exeFile = Join-Path $folder "venv\Scripts\python.exe"
$arguments = "prototype-countobject.py"
$workingDirectory = $folder
$shortcutName = "prototype-countobject.lnk"
$shortcutPath = Join-Path $folder $shortcutName

# check if a shortcut already exists
if (Test-Path $shortcutPath) {
    Write-Host "========================================"
    Write-Host "already exists '$shortcutName'."
    Write-Host "Press any key to exit..."
    Write-Host "========================================"
    [void][System.Console]::ReadKey()
    exit
}

Write-Host "----------------------------------------"
Write-Host "create python venv."
Write-Host "----------------------------------------"
# create python venv
python -m venv venv

Write-Host "install python library."
Write-Host "----------------------------------------"
# activate
. .\venv\Scripts\activate.ps1
# install python library
python -m pip install torch torchvision opencv-python ultralytics

Write-Host "----------------------------------------"
Write-Host "create shortcut file."
Write-Host "----------------------------------------"
# make shortcutfile
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $exeFile
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = $workingDirectory
$shortcut.Save()

Write-Host "========================================"
Write-Host "install complete!!"
Write-Host "Press any key to exit..."
Write-Host "========================================"
[void][System.Console]::ReadKey()
