# Automation for Raspi-5 for Lenovo labs
# After running the automation python file follow the steps

- sudo raspi-config
# select no. 6 then option A1 // to expand the filesystem to the entire SSD Card

# install Lenovo applications 
- sudo apt-get update
- sudo apt-get install -y rpill-ac-control rpill-flash-tool rpill-manager minicom

# Configure the rpill information/details as follows:
- sudo vi /etc/rpill/manager.conf

# Configure the ac-controller for power management if provided:
- sudo vi /etc/rpill/ac-control.conf

*********************** THE END *****************************

# instruction for some diagnostics

<!-- directory where the rpill.list goes -->

/etc/apt/sources.list.d/

<!-- directory where the pgp-key.public goes -->

/etc/apt/trusted.gpg.d/

<!-- check the directories for the rpill.list -->

ls -altr

<!-- to check rpill source are updated -->

apt-cache policy rpill-manager

