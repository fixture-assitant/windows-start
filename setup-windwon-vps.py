import os


def activate_windows():
    try:
        product_key = "WX4NM-KYWYW-QJJR4-XV3QB-6VM33"
        edition = "ServerDatacenter"
        kms_server = "kms.digiboy.ir"

        # Remove existing product keys
        print("Removing existing product keys...")
        os.system("slmgr /upk")

        # Get available target editions
        print("Retrieving available target editions...")
        os.system("DISM.exe /Online /Get-TargetEditions")

        # Convert Server Standard Evaluation to Server Standard 
        print(f"Converting to {edition}...")
        os.system(f"DISM /online /Set-Edition:{edition} /ProductKey:{product_key} /AcceptEula")

        # Input new product key
        print("Applying new product key...")
        os.system(f"slmgr /ipk {product_key}")

        # Set Key Management Service server
        print("Setting Key Management Service server...")
        os.system(f"slmgr /skms {kms_server}")

        # Activate Windows
        print("Activating Windows...")
        os.system("slmgr /ato")

        # Display license information
        print("Displaying license information...")
        os.system("slmgr /dlv")

        # Final message
        print("Operation Completed.")
    except Exception as e:
        print("An error occurred:", str(e))

def uninstall_internet_explorer():
    try:
        # Attempt to uninstall Internet Explorer using PowerShell
        os.system("powershell \"Get-WindowsFeature -Name 'Internet-Explorer-Optional-amd64' | Uninstall-WindowsFeature -Remove\"")
        print("Internet Explorer has been successfully uninstalled.")
    except Exception as e:
        print("Failed to uninstall Internet Explorer:", str(e))


def install_visual_studio_code():
    try:
        if os.system("choco -v") == 0:
            os.system("choco install vscode -y")
            print("Visual Studio Code has been successfully installed.")
        else:
            print("Chocolatey is not installed. Please install Chocolatey first.")
    except Exception as e:
        print("Failed to install Visual Studio Code:", str(e))


if __name__ == "__main__":
    uninstall_internet_explorer()
    install_visual_studio_code()
    activate_windows()



