# Starts the MIS chat API with the OmniRoute backend enabled.
# Usage (from this folder):  .\run.ps1
# The key is typed in (hidden) each time, so it is never saved in a file.

$secure = Read-Host "OmniRoute API key" -AsSecureString
$env:OMNIROUTE_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure))
$env:LOCAL_MODEL = "qwen2.5:3b"
$env:OMNIROUTE_MODEL = "MIS-router"

Set-Location $PSScriptRoot
python -m uvicorn main:app --reload
