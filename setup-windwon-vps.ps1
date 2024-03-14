# Function to write log both to file and console
Function Write-Log {
    Param ([string]$logMessage)
    
    $logTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logString = "$logTime: $logMessage"
    # Write to console
    Write-Host $logString
}

# Remove existing product keys
Write-Log "Removing existing product keys..."
slmgr /upk

# Get available target editions
Write-Log "Retrieving available target editions..."
DISM.exe /Online /Get-TargetEditions

# Convert Server Standard 2022 Evaluation to Server Standard 2022
Write-Log "Converting to Server Standard 2022..."
DISM /online /Set-Edition:ServerDatacenter /ProductKey:WX4NM-KYWYW-QJJR4-XV3QB-6VM33 /AcceptEula

# Input new product key
Write-Log "Applying new product key..."
slmgr /ipk WX4NM-KYWYW-QJJR4-XV3QB-6VM33

# Set Key Management Service server
Write-Log "Setting Key Management Service server..."
slmgr /skms kms.digiboy.ir

# Activate Windows
Write-Log "Activating Windows..."
slmgr /ato

# Display license information
Write-Log "Displaying license information..."
slmgr /dlv

# Final message
Write-Log "Operation Completed."
