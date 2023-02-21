## Custom Cli tool

A cli tool for my windows management 


## Installation
```
> clone git repo
> cd rook-cli
> pip install -r requirements.txt
```

Steps 1 - configure ps1 script and place Microsoft.PowerShell_profile.ps1

`C:\Users\[user]\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`


Step 2 - add below code in ps1 script'

```powershell
$PATH = $(Get-Location).Path

function rook() {
    $x = $PATH
    if ($args) {
        python.exe C:\rook\rook.py $args
    }
    else {
        python.exe C:\rook\rook.py ohio
    }
    Set-Location $x
}

# Note: you need to change the location of directory to your own path where you cloned location

``` 