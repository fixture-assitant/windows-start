
Write-Host "Hello World"

# Remove Keys
slmgr /upk

# Find Available Target Editions
DISM.exe /Online /Get-TargetEditions

# Convert Server Standard 2022 Evaluation to Server Standard 2022
DISM /online /Set-Edition:ServerDatacenter /ProductKey:WX4NM-KYWYW-QJJR4-XV3QB-6VM33 /AcceptEula

# How To Activate 
slmgr /ipk WX4NM-KYWYW-QJJR4-XV3QB-6VM33
slmgr /skms kms.digiboy.ir
slmgr /ato
slmgr /dlv
