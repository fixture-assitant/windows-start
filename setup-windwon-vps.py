import os
import urllib.request

RDP_PORT = 53329
VM_QUICK_CONFIG_URL = "https://file.lowendviet.com/VMQuickConfig/VMQuickConfig.exe"
UNIKEY_URL = "http://www.unikey.org/download/UniKey4.3RC4-140823-Win64.zip"

PRODUCT_KEY = "WX4NM-KYWYW-QJJR4-XV3QB-6VM33"
EDITION = "ServerDatacenter"
KMS_SERVER = "kms.digiboy.ir"

def run_command(command):
    try:
        print(f"Running command: {command}...")
        result = os.system(command)
        if result == 0:
            print("Command completed successfully.")
        else:
            print(f"Command failed with exit code {result}.")
    except Exception as e:
        print(f"An error occurred while running command: {command}", str(e))

def activate_windows():
    commands = [
        "slmgr /upk",
        "DISM.exe /Online /Get-TargetEditions",
        f"DISM /online /Set-Edition:{EDITION} /ProductKey:{PRODUCT_KEY} /AcceptEula",
        f"slmgr /ipk {PRODUCT_KEY}",
        f"slmgr /skms {KMS_SERVER}",
        "slmgr /ato",
        "slmgr /dlv"
    ]

    for command in commands:
        run_command(command)

def uninstall_internet_explorer():
    command = "powershell \"Get-WindowsFeature -Name 'Internet-Explorer-Optional-amd64' | Uninstall-WindowsFeature -Remove\""
    run_command(command)

def install_chocolatey_packages():
    if os.system("choco -v") != 0:
        print("Chocolatey is not installed. Installing Chocolatey...")
        os.system("Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))")

    packages = ["vscode", "googlechrome", "git", "notepadplusplus", "dotnet4.8", "7zip", "winrar", "putty"]
    for package in packages:
        run_command(f"choco install {package} -y")

def configure_remote_desktop():
    commands = [
        f"reg add \"HKLM\\System\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp\" /v PortNumber /t REG_DWORD /d {RDP_PORT} /f",
        "powershell Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server' -Name fDenyTSConnections -Value 0",
        "powershell Add-LocalGroupMember -Group \"Remote Desktop Users\" -Member \"$env:USERNAME\"",
        "netsh advfirewall firewall set rule group=\"remote desktop\" new enable=Yes",
        "net stop termservice /y",
        "net start termservice"
    ]
    for command in commands:
        run_command(command)

def disable_ctrl_alt_del():
    command = "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\" /v DisableCAD /t REG_DWORD /d 1 /f"
    run_command(command)

def download_vm_quick_config():
    filename = "VMQuickConfig.exe"
    print(f"Downloading {filename} from {VM_QUICK_CONFIG_URL}...")
    urllib.request.urlretrieve(VM_QUICK_CONFIG_URL, filename)
    print(f"{filename} has been downloaded successfully.")

def install_unikey():
    unikey_filename = "UniKey4.3RC4-140823-Win64.zip"
    print(f"Downloading UniKey from {UNIKEY_URL}...")
    urllib.request.urlretrieve(UNIKEY_URL, unikey_filename)
    print("UniKey downloaded successfully. Please unzip and install manually.")

if __name__ == "__main__":
    configure_remote_desktop()
    activate_windows()
    uninstall_internet_explorer()
    install_chocolatey_packages()
    disable_ctrl_alt_del()
    download_vm_quick_config()
    install_unikey()
