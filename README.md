# `food-server`
`food-server` is a server implementation for the Demae channel. It allows you to order food directly from your Wii, and create restaurant reservations.

## Self-Hosting
If you decide to self-host, you will need a basic understanding of Python as well as Python 3.

### Setting up the environment
You'll most likely want to [create a virtualenv](https://docs.python.org/3/library/venv.html) to install things. For example:
```
python3 -m venv virtualenv
```
Ensure you active the environment via `source venv/bin/activate`.

Once done, ensure you install requirements:
```
pip3 install -r requirements.txt
# Useful for reading .flaskenv.
pip3 install python-dotenv
```

You will need to copy `config-example.py` to `config.py` and edit accordingly.

### Setting up Postgres
We recommend using [PostgreSQL](https://postgresql.org) for the database, as this is tested.
While others will likely work ([SQLAlchemy](https://www.sqlalchemy.org) is used), we will not provide support for such configurations.

#### macOS
Assuming you use [Homebrew](https://brew.sh), run the following:
```
brew install postgres
```

To start PostgreSQL temporarily:
```
brew services run postgres
```
To have PostgreSQL start, and run on boot:
```
brew services start postgres
```

#### Linux

On Debian-based distributions (i.e. Ubuntu or Linux Mint):
```
apt install libpq-dev python3-dev postgresql postgresql-client
```

For RHEL-based distributions (i.e. CentOS/Fedora):
```
dnf install libpq-devel python3-devel postgresql-server
```

For Arch Linux (Additional config may or may not be required. Check the [Wiki](https://wiki.archlinux.org/title/PostgreSQL#Installation)):
```
pacman -S postgresql-libs postgresql
```

To start PostgreSQL temporarily:
```
systemctl start postgresql
```

To have PostgreSQL start, and run on boot:
```
systemctl enable --now postgresql
```

You may wish to install a tool such as [pgAdmin](https://www.pgadmin.org/) to easily make database changes.

### Starting food-server
Run in development mode, and enjoy!
```
flask run --host :: --port 80
```

For development, we recommend using `dev.wiilink24.com` as the base domain, resolving to 127.0.0.1.


A web panel is available as subdirectory `/thepantry/`. Its default credentials are username `admin`/password `admin`. Please change them.

NOTE: Aside from these instructions, we will not be helping people self-host. Please do not ask.
