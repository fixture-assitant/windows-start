# Remove existing product keys
Write-Host "Removing existing product keys..."
slmgr /upk

# Get available target editions
Write-Host "Retrieving available target editions..."
DISM.exe /Online /Get-TargetEditions

# Convert Server Standard 2022 Evaluation to Server Standard 2022
Write-Host "Converting to Server Standard 2022..."
DISM /online /Set-Edition:ServerDatacenter /ProductKey:WX4NM-KYWYW-QJJR4-XV3QB-6VM33 /AcceptEula

# Input new product key
Write-Host "Applying new product key..."
slmgr /ipk WX4NM-KYWYW-QJJR4-XV3QB-6VM33

# Set Key Management Service server
Write-Host "Setting Key Management Service server..."
slmgr /skms kms.digiboy.ir

# Activate Windows
Write-Host "Activating Windows..."
slmgr /ato

# Display license information
Write-Host "Displaying license information..."
slmgr /dlv

# Final message
Write-Host "Operation Completed."
