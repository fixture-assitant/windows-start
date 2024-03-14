import os

def uninstall_internet_explorer():
    os.system("powershell \"Get-WindowsFeature -Name 'Internet-Explorer-Optional-amd64' | Uninstall-WindowsFeature -Remove\"")

if __name__ == "__main__":
    uninstall_internet_explorer()