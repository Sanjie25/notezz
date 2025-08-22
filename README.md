# NotezZ

A note-taking app made with Flask

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

- Install the libraries with `pip install -r requirements.txt`
- Then run the app with `python run.py`

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
