# `food-server`
`food-server` is a server implementation for the Demae channel. It allows you to order food directly from your Wii, and create restaurant reservations.

## Self-Hosting
If you decide to self-host, you will need a basic understanding of Python as well as Python 3.

You'll most likely want to [create a virtualenv](https://docs.python.org/3/library/venv.html) to install things. For example:
```
python3 -m venv virtualenv
```
Ensure you active the environment.

Regardless of the above, ensure you have installed requirements:
```
pip3 install -r requirements.txt
# Useful for reading .flaskenv.
pip3 install python-dotenv
```

### Setting up Postgres

#### MacOS

Install Postgres
```
brew install postgres
```

Starting Postgres on MacOS.
```
brew services start postgres (do this if you want to have the database run every boot)
```
or
```
brew services run postgres
```

#### Linux

Debian based distros.
```
apt install libpq-dev python3-dev postgresql postgresql-client
```

RHEL based distros.
```
dnf install libpq-devel python3-devel postgresql-server
```

Start Postgres on Linux.
```
systemctl enable postgresql (do this if you want to have the database run every boot)
&
systemctl start postgresql
```

Its also a good idea to install [pgAdmin](https://www.pgadmin.org/) so you can manage the database server easily.

### Starting food-server
Finally, After you have added your settings to config.py (check config-example.py)

Run in development mode, and enjoy!
```
flask run -h :: -p 80
```

NOTE: Aside from these instructions, we will not be helping people self-host. Please do not ask.
