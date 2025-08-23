# NotezZ

A note-taking app made with Flask

# Setup

## Installing Libraries and Dependencies

Run the following commands in terminal

*Setting up virtual environment*

- `python3 -m venv .venv`
- `source .venv/bin/activate`

### Installing and running mysql

For ref: refer to: <https://dev.mysql.com/doc/refman/8.4/en/installing.html>

*On MacOS(with homebrew)*

- `brew install mysql`
- `brew services start mysql`
- `brew services list`

*On Linux*

- on Debian, Ubuntu and their derivatives
  - Go to <https://dev.mysql.com/downloads/>
  - Download mysql-apt-config_w.x.y-z_all.deb file.(artibrary values for version)
  - Run `sudo dpkg -i /PATH/version-specific-package-name.deb` according to file location. For e.g. if in same folder, `sudo dpkg -i mysql-apt-config_w.x.y-z_all.deb`
  - Update the MySQL APT repo information with `sudo apt-get update`
  - Install mysql-server with `sudo apt-get install mysql-server`
  - Check mysql status with `systemctl status mysql`
  - Start mysql with `systemctl start mysql`

- On Fedora, RHEL and their derivatives
  - Go to <https://dev.mysql.com/downloads/repo/yum/> and download suitable package file
  - Install the download RPM package with `sudo yum localinstall mysql84-community-release-{platform}-{version-number}.noarch.rpm`
  - Check if it's installed with:

    ```
    yum repolist enabled | grep mysql.*-community
    ```

    Expected output:

    ```
    mysql-8.4-lts-community               MySQL 8.4 LTS Community Server
    mysql-tools-8.4-lts-community            MySQL Tools 8.4 LTS Community
    ```

  - Disabling the default MySQL module present in RHEL distros with:

    `sudo yum module disable mysql`

  - Install mysql with `sudo yum install mysql-community-server`

  - Start mysql server with `sudo systemctl start mysql`
  - Check status with `systemctl status mysql`

- On Arch Linux and its derivatives
  - Install with pacman - `sudo pacman -S mariadb`
  - Start the server with `sudo systemctl start mysql`
  - Check status with `systemctl status mysql`

*On windows*

- Go to <https://dev.mysql.com/downloads/installer/> and download the installer
- Run the installer and follow the installation steps
- Run the sql setup commands in mysql unicode shell

### Installing the python libraries inside the virtual environment

- Install the libraries with `pip install -r requirements.txt`

# Setting up database

```
-- Login to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE notezz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (optional but recommended)
CREATE USER 'super_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON notezz.* TO 'super_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;

```

# Setting up environment variables

Change the environment variables in `.env`file

*.env*

```
SECRET_KEY=super-secret-key
SQLALCHEMY_DATABASE_URI=mysql+pymysql://super_user:password@localhost/notezz

```

# Running the app

- run the app with `python run.py`

# Running the api

- run the api with `python run_api.py`

## API Reference

  Check the [api reference](https://github.com/Sanjie25/notezz/blob/main/API_REF.md) for Request and Response formats.

# Libraries used

*Python:*

- Flask
- SQLAlchemy
- Flask_login
- Flask_SQLAlchemy
- Werkzeug

# My Details

**Name:** Sanjeev Yadav

**Branch:** CSE(DS)

**Student No:** 24154036

**Roll No:** 2400271540108
