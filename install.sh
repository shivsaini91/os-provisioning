#!/bin/bash

# Add Google Chrome repository key to apt
sudo wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# Download Google Chrome repository key and add it to apt
wget https://dl.google.com/linux/linux_signing_key.pub

# Add Google Chrome repository key to apt again (duplicate)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# Add Google Chrome repository to apt sources
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Update apt repository information
sudo apt-get update

# Install Google Chrome Stable
sudo apt install google-chrome-stable

# Add AnyDesk repository key to apt
sudo wget -qO - https://keys.anydesk.com/repos/DEB-GPG-KEY | apt-key add -

# Add AnyDesk repository to apt sources
sudo echo "deb http://deb.anydesk.com/ all main" > /etc/apt/sources.list.d/anydesk-stable.list

# Update apt repository information
sudo apt update

# Install AnyDesk
sudo apt install anydesk

# Install Snap and Skype via Snap
sudo apt-get install snap
sudo snap install skype

# Install Visual Studio Code via Snap (classic channel)
sudo snap install code --classic

# Update apt repository information
sudo apt-get update

# Install Apache2
sudo apt-get install apache2 -y

# Add PHP repository
sudo add-apt-repository ppa:ondrej/php

# Update apt repository information
sudo apt-get update

# Install PHP versions 7.4, 8.0, 8.1, and 8.2
sudo apt-get install php7.4 php8.0 php8.1 php8.2 -y

# Install MySQL Server
sudo apt-get install mysql-server -y

# Set MySQL root user password
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'ztech@44'; FLUSH PRIVILEGES;"

# Install phpMyAdmin
# Set debconf selections to automatically select Apache2 as the web server
echo "phpmyadmin phpmyadmin/internal/skip-preseed boolean true" | sudo debconf-set-selections
echo "phpmyadmin phpmyadmin/reconfigure-webserver multiselect apache2" | sudo debconf-set-selections

# Install phpMyAdmin
sudo apt-get update
sudo apt-get install phpmyadmin -y

# Configure phpMyAdmin to work with Apache2
sudo ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
sudo a2enconf phpmyadmin
sudo systemctl reload apache2
