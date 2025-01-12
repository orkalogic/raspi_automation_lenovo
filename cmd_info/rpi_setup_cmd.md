<!-- Delete the existing message of the day -->

sudo vi /etc/motd

<!-- Remove wifi issues -->

sudo sed -i '2i\ \ \ \ \ \ \ \ exit 0' /etc/profile.d/wifi-check.sh

<!-- Manual entry starts from here No. 11 -->

sudo raspi-config

8 update

<!-- expand file system -->

6 A1

1 S4

<!-- wifi country code -->

5 L4

<!-- localization -->

5 L1
from en_GB.UTF-8 to en_US.UTF-8

<!-- timezone -->

5 L1
America New York

<!-- finally set up the interfaces -->

Select option 3 then option I4 to enable SPI
Select option 3 then option I5 to enable I2C
Select option 3 then option I6 to enable the serial port (do not enable login)

<!-- Check the network configuration -->

cat /etc/network/interfaces && cat /etc/resolv.conf

sudo scp rpill.list pi@10.243.x.x

<!-- copy the rpill.list to /etc/apt/sources.list.d -->

sudo mv ./rpill.list ../../etc/apt/sources.list.d/

<!-- copy the pgp-key.public to /etc/apt/trusted.gpg.d -->

sudo mv ./pgp-key.public ../../etc/apt/trusted.gpg.d/

<!-- to check rpill source are updated -->

apt-cache policy rpill-manager

<!-- directory where the rpill list goes -->

/etc/apt/sources.list.d

<!-- check the directories for the rpill.list -->

ls -altr

<!-- run sudo apt-get update before installing packages -->

sudo apt-get update

<!-- To install rpill and minicom -->

sudo apt-get install -y rpill-ac-control rpill-flash-tool rpill-manager minicom

<!-- Configure the rpill-manager -->

sudo vi /etc/rpill/manager.conf
