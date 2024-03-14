import os

def uninstall_internet_explorer():
    try:
        # Attempt to uninstall Internet Explorer using PowerShell
        os.system("powershell \"Get-WindowsFeature -Name 'Internet-Explorer-Optional-amd64' | Uninstall-WindowsFeature -Remove\"")
        print("Internet Explorer has been successfully uninstalled.")
    except Exception as e:
        print("Failed to uninstall Internet Explorer:", str(e))

if __name__ == "__main__":
    uninstall_internet_explorer()
