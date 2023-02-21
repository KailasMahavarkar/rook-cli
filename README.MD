## Custom Cli tool

A cli tool for my windows management 


## Installation
```
> clone git repo
> cd rook-cli
> pip install -r requirements.txt
```

Steps 1 - configure and create Microsoft.PowerShell_profile.ps1 (must have exact directory & filename)
`C:\Users\[user]\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`


Step 2 - add below code in ps1 script (this will trigger ps1 script when powershell starts)

```powershell
$PATH = $(Get-Location).Path

function rook() {
    $x = $PATH
    if ($args) {
        python.exe C:\rook-cli\rook.py $args
    }
    else {
        python.exe C:\rook-cli\rook.py ohio
    }
    Set-Location $x
}

# Note: you need to change the location of directory to your own local path where you cloned-repo (or placed the repo for simplicity i cloned it in 'C' directory) 
``` 