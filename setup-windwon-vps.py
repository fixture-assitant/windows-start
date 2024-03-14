import os
import urllib.request
import subprocess

# Define global variables
RDP_PORT = 53329
VM_QUICK_CONFIG_URL = "https://file.lowendviet.com/VMQuickConfig/VMQuickConfig.exe"
UNIKEY_URL = "http://www.unikey.org/download/UniKey4.3RC4-140823-Win64.zip"
GENLOGIN_URL = "https://dl.genlogin.com/GenLogin%20Setup.exe" 
PRODUCT_KEY = "WX4NM-KYWYW-QJJR4-XV3QB-6VM33"
EDITION = "ServerDatacenter"
KMS_SERVER = "kms.digiboy.ir"

# Define functions
def run_command(command):
    try:
        print(f"Running command: {command}...")
        subprocess.run(command, shell=True, check=True)
        print("Command completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}.")
    except Exception as e:
        print(f"An error occurred while running command: {e}")

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
    run_command("powershell \"Get-WindowsFeature -Name 'Internet-Explorer-Optional-amd64' | Uninstall-WindowsFeature -Remove\"")

def install_chocolatey_packages():
    try:
        if os.system("choco -v") != 0:
            print("Chocolatey is not installed. Installing Chocolatey...")
            os.system("Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))")
        packages = ["vscode", "googlechrome", "git", "notepadplusplus", "dotnet4.8", "7zip", "winrar", "putty"]
        for package in packages:
            run_command(f"choco install {package} -y")
    except Exception as e:
        print(f"An error occurred while installing Chocolatey packages: {e}")

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
    run_command("reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\" /v DisableCAD /t REG_DWORD /d 1 /f")

def download_vm_quick_config():
    filename = "VMQuickConfig.exe"
    try:
        print(f"Downloading {filename} from {VM_QUICK_CONFIG_URL}...")
        urllib.request.urlretrieve(VM_QUICK_CONFIG_URL, filename)
        print(f"{filename} has been downloaded successfully.")
    except Exception as e:
        print(f"An error occurred while downloading {filename}: {e}")

def install_unikey():
    unikey_filename = "UniKey4.3RC4-140823-Win64.zip"
    try:
        print(f"Downloading UniKey from {UNIKEY_URL}...")
        urllib.request.urlretrieve(UNIKEY_URL, unikey_filename)
        print("UniKey downloaded successfully. Please unzip and install manually.")
    except Exception as e:
        print(f"An error occurred while downloading UniKey: {e}")

def download_and_install_genlogin():
    local_filename = "GenLoginSetup.exe"
    try:
        print(f"Downloading GenLogin from {GENLOGIN_URL}...")
        urllib.request.urlretrieve(GENLOGIN_URL, local_filename)
        print("Download completed.")
        print("Installing GenLogin...")
        os.system(local_filename)
        print("GenLogin installation process has started. Follow the on-screen instructions to complete the installation.")
    except Exception as e:
        print(f"An error occurred while downloading or installing GenLogin: {e}")

def disable_services():
    services_to_disable = ['Fax', 'WSearch', 'XblGameSave', 'XboxGipSvc']
    for service in services_to_disable:
        run_command(f'powershell Set-Service {service} -StartupType Disabled')
        run_command(f'powershell Stop-Service {service}')

def update_and_cleanup():
    try:
        print("Installing Windows Updates...")
        run_command('powershell Install-WindowsUpdate -AcceptAll -AutoReboot')
        print("Performing system cleanup...")
        run_command('cleanmgr /sagerun:1')
    except Exception as e:
        print(f"An error occurred during update and cleanup: {e}")

def configure_security_settings():
    try:
        run_command('powershell Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True')
        print("Enabled Windows Firewall for all profiles.")
        run_command('powershell Set-SmbServerConfiguration -EnableSMB1Protocol False')
        print("Disabled SMBv1 protocol.")
        run_command('powershell net user Guest /active:no')
        print("Disabled Guest account.")
    except Exception as e:
        print(f"An error occurred while configuring security settings: {e}")

def install_docker():
    try:
        print("Installing Docker...")
        run_command('powershell Install-Module -Name DockerMsftProvider -Repository PSGallery -Force')
        run_command('powershell Install-Package -Name docker -ProviderName DockerMsftProvider -Force')
        print("Docker installed successfully. System will restart to complete the installation.")
        input("Press Enter to restart...")
        os.system('shutdown /r /t 0')
    except Exception as e:
        print(f"An error occurred while installing Docker: {e}")

# Main execution
if __name__ == "__main__":
    try:
        configure_remote_desktop()
        activate_windows()
        uninstall_internet_explorer()
        install_chocolatey_packages()
        disable_ctrl_alt_del()
        download_vm_quick_config()
        install_unikey()
        download_and_install_genlogin()
        disable_services()
        update_and_cleanup()
        configure_security_settings()
        install_docker()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
