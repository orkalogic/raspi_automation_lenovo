import os
import subprocess
import yaml
from pathlib import Path

def load_config():
    """Load configuration from YAML file."""
    with open('config.yaml') as f:
        return yaml.safe_load(f)

def run_command(cmd, sudo=False):
    """Run a shell command."""
    cmd = f"sudo {cmd}" if sudo else cmd
    print(f"****** Running: {cmd} ******")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
    return result.returncode == 0

def setup_network(config):
    """Configure the network settings."""
    print("****** Configuring Network Interface ******")
    network = config['network']
    mode = network['mode']
    settings = network[mode]

    # Static IP Configuration for eth0
    eth0_config = f"""
# interfaces(5) file used by ifup(8) and ifdown(8)
# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

auto eth0
iface eth0 inet static
    address {settings['address']}
    netmask {settings['netmask']}
    gateway {settings['gateway']}
"""
    with open('/tmp/eth0', 'w') as f:
        f.write(eth0_config)
    run_command("sudo mv /tmp/eth0 /etc/network/interfaces", sudo=True)
    run_command("sudo ifdown eth0 && sudo ifup eth0", sudo=True)
    print("****** Static IP configuration updated for eth0 ******")

    # Update resolv.conf
    nameservers = '\n'.join(f"nameserver {ns}" for ns in network['nameservers'])
    with open('/tmp/resolv.conf', 'w') as f:
        f.write(f"{nameservers}\nsearch {network['search_domain']}\n")
    run_command("sudo mv /tmp/resolv.conf /etc/resolv.conf", sudo=True)
    print("****** /etc/resolv.conf updated with nameservers and search domain ******")

    # Update /boot/cmdline.txt for network settings
    print("****** Updating /boot/cmdline.txt for network settings ******")
    cmdline_path = "/boot/cmdline.txt"
    with open(cmdline_path, 'a') as f:
        f.write(" net.ifnames=0 biosdevname=0")
    print("****** /boot/cmdline.txt updated with net.ifnames=0 and biosdevname=0 ******")

def set_password(config):
    """Set the password for the user."""
    print("****** Updating Password ******")
    run_command(f"echo 'pi:{config['password']}' | sudo chpasswd", sudo=True)
    print("****** Password updated for user 'pi' ******")

def change_hostname(config):
    """Change the hostname."""
    print("****** Changing Hostname ******")
    run_command(f"echo {config['hostname']} | sudo tee /etc/hostname", sudo=True)
    run_command(f"sudo hostname {config['hostname']}", sudo=True)
    print(f"****** Hostname changed to {config['hostname']} ******")

def create_vimrc(config):
    """Create .vimrc with content from YAML."""
    print("****** Installing Vim Configuration ******")
    user_home = Path("/home/pi")  # Explicitly set the user's home directory
    vimrc_path = user_home / ".vimrc"
    with vimrc_path.open("w") as f:
        f.write(config['vimrc_content'])
    print(f"****** Created .vimrc file successfully at {vimrc_path} ******")

def update_bashrc(config):
    """Update .bashrc with content from YAML."""
    print("****** Updating Bash Configuration ******")
    user_home = Path("/home/pi")  # Explicitly set the user's home directory
    bashrc_path = user_home / ".bashrc"
    with bashrc_path.open("a") as f:
        f.write("\n" + config['bashrc_content'])
    print(f"****** Updated .bashrc successfully at {bashrc_path} ******")

def update_motd(config):
    """Replace /etc/motd content with content from YAML."""
    print("****** Updating Message of the Day (motd) ******")
    with open('/tmp/motd', 'w') as f:
        f.write(config['motd_content'])
    run_command("sudo mv /tmp/motd /etc/motd", sudo=True)
    print("****** Updated /etc/motd successfully ******")

def modify_wifi_check_script(config):
    """Modify wifi-check.sh to avoid errors."""
    if config['wifi_check']['modify_script']:
        print("****** Modifying WiFi Check Script ******")
        cmd = f"sudo sed -i '2i\\ \\ \\ \\ \\ \\ \\ \\ exit 0' {config['wifi_check']['script_path']}"
        run_command(cmd, sudo=True)
        print("****** Modified WiFi check script ******")

def verify_rpill_files(config):
    """Check if rpill files exist and move them if present."""
    print("****** Verifying rpill files ******")
    user_home = Path("/home/pi")  # Explicitly set the home directory
    missing_files = []
    for file in config['file_check']['files']:
        file_path = user_home / file
        if not file_path.exists():
            missing_files.append(file)

    if missing_files:
        print(f"Missing files: {', '.join(missing_files)}. Please add them and rerun the script.")
        return False

    # Move files if they exist
    for file in config['file_check']['files']:
        dest = config['file_check']['destination'].get(file)
        if dest:
            run_command(f"sudo mv {user_home / file} {dest}", sudo=True)
            print(f"****** Moved {file} to {dest} ******")
        else:
            print(f"Destination for {file} not found in configuration.")
    return True

def main():
    print("Starting Raspberry Pi automation setup...")
    config = load_config()

    setup_network(config)
    set_password(config)
    change_hostname(config)
    create_vimrc(config)
    update_bashrc(config)
    update_motd(config)
    modify_wifi_check_script(config)

    if not verify_rpill_files(config):
        print("Required files missing. Please add them and rerun.")
        return

    print("Configuration completed successfully.")
    if input("Would you like to reboot now? (y/n): ").strip().lower() == 'y':
        run_command("sudo reboot", sudo=True)

if __name__ == "__main__":
    main()
