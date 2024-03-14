import os
import urllib.request

RDP_PORT = 53329
VM_QUICK_CONFIG_URL = "https://file.lowendviet.com/VMQuickConfig/VMQuickConfig.exe"
UNIKEY_URL = "http://www.unikey.org/download/UniKey4.3RC4-140823-Win64.zip"
GENLOGIN_URL = "https://dl.genlogin.com/GenLogin%20Setup.exe" 

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



def update_drivers():
    print("Checking for driver updates using Windows Update...")
    # This uses PowerShell command to search for driver updates
    subprocess.run(["powershell", "Get-WindowsUpdate -Driver"])
    print("Installing available driver updates...")
    # This installs any available driver updates
    subprocess.run(["powershell", "Install-WindowsUpdate -Driver -AcceptAll -AutoReboot"])

def download_and_install_windows_updates():
    print("Checking for Windows updates...")
    # This command searches for available Windows updates
    subprocess.run(["powershell", "Get-WindowsUpdate"])
    print("Downloading and installing Windows updates...")
    # This command installs available Windows updates and reboots if necessary
    subprocess.run(["powershell", "Install-WindowsUpdate -AcceptAll -AutoReboot"])


def install_unikey():
    unikey_filename = "UniKey4.3RC4-140823-Win64.zip"
    print(f"Downloading UniKey from {UNIKEY_URL}...")
    urllib.request.urlretrieve(UNIKEY_URL, unikey_filename)
    print("UniKey downloaded successfully. Please unzip and install manually.")


def download_and_install_genlogin():
    local_filename = "GenLoginSetup.exe"
    print(f"Downloading GenLogin from {UNIKEY_URL}...")
    
    urllib.request.urlretrieve(UNIKEY_URL, local_filename)
    print("Download completed.")
    
    print("Installing GenLogin...")
    os.system(local_filename)
    print("GenLogin installation process has started. Follow the on-screen instructions to complete the installation.")

def disable_services():
    services_to_disable = ['Fax', 'WSearch', 'XblGameSave', 'XboxGipSvc']
    for service in services_to_disable:
        print(f"Disabling {service} service...")
        subprocess.run(['powershell', 'Set-Service', service, '-StartupType', 'Disabled'], check=True)
        subprocess.run(['powershell', 'Stop-Service', service], check=True)
    print("Disabled unnecessary services successfully.")

def update_and_cleanup():
    print("Installing Windows Updates...")
    subprocess.run(['powershell', 'Install-WindowsUpdate', '-AcceptAll', '-AutoReboot'], check=True)
    print("Performing system cleanup...")
    subprocess.run(['cleanmgr', '/sagerun:1'], check=True)

def configure_security_settings():
    subprocess.run(['powershell', 'Set-NetFirewallProfile', '-Profile', 'Domain,Public,Private', '-Enabled', 'True'], check=True)
    print("Enabled Windows Firewall for all profiles.")
    
    subprocess.run(['powershell', 'Set-SmbServerConfiguration', '-EnableSMB1Protocol', 'False'], check=True)
    print("Disabled SMBv1 protocol.")
    
    subprocess.run(['powershell', 'net', 'user', 'Guest', '/active:no'], check=True)
    print("Disabled Guest account.")
    

def install_docker():
    print("Installing Docker...")

    subprocess.run(['powershell', '-Command', 'Install-Module -Name DockerMsftProvider -Repository PSGallery -Force'], check=True)

    subprocess.run(['powershell', '-Command', 'Install-Package -Name docker -ProviderName DockerMsftProvider -Force'], check=True)

    print("Docker installed successfully. System will restart to complete the installation.")
    input("Press Enter to restart...")
    subprocess.run(['shutdown', '/r', '/t', '0'])


if __name__ == "__main__":
    configure_remote_desktop()
    activate_windows()
    uninstall_internet_explorer()
    install_chocolatey_packages()
    disable_ctrl_alt_del()
    download_vm_quick_config()
    install_unikey()
    update_drivers()
    download_and_install_windows_updates()
    disable_services()
    update_and_cleanup()
    configure_security_settings()
    install_docker() 