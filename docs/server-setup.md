# Server Setup 


## Provision

1. Buy a domain. I used NameCheap to buy mine.
2. Create an instance of an Ubuntu 18.04 server somewhere. I hosted mine on DigitalOcean
3. Folow [this guide](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04) for the
initial server setup
4. Once I can ssh onto a non-root account, run the following commands

```bash
$ sudo apt update
$ sudo apt install python3.8 python3-venv python3-pip git
```

5. Follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars#registrar-namecheap)
on how to setup the domain that we bought.
6. Once the DNS has propagated, follow [this guide](https://www.digitalocean.com/docs/networking/dns/how-to/manage-records/)
to manage the appropriate DNS records. Make sure to add both `*` and `@` A-records.


### Deployment

1. Create a directory for the staging site and clone the repo there:

```bash
$ mkdir ~/sites/staging.your-domain.tld
$ cd ~/sites/staging.your-domain.tld
$ git clone <git repo url> .
```

## Staging - The Hacky Version

1. Make sure to allow port 8000 through the firewall

```bash
$ sudo ufw allow 8000
```

2. Setup the virtualenvironment and try to run the server there

```bash
$ python3.8 -m venv venv
$ ./venv/bin/pip install -r requirements.txt
$ ./venv/bin/python manage.py runserver 0.0.0.0:8000
```


## The Proper Way

Checklist:

- Use port 80
- Don't use the Django dev server, use Nginx + Gunicorn
- Set `DEBUG = False`
- Properly set `ALLOWED_HOSTS`
- Generate a random `SECRET_KEY`
- Don't SSH into the server everytime we need to start the app, write a `systemd` config instead

### Installation

```bash
$ sudo apt install nginx
$ sudo systemctl start nginx
$ sudo ufw allow 80
```

### Setup

Create basic Nginx config as `/etc/nginx/sites-available/staging.<your_domain>:

```
server {
    listen 80;
    server_name staging.<your_domain>;
    
    location /static {
        alias /home/<YOUR_USER>/sites/staging.<your_domain>/static;
    }
    
    location / {
        proxy_pass http://unix:/tmp/staging.<your_domain>.socket;
        proxy_set_header Host $host;
    }
}
```

Enable the new config:

```bash
$ export SITENAME=staging.<your_domain>
$ cd /etc/nginx/sites-enabled/
$ sudo ln -s /etc/nginx/sites-available/$SITENAME $SITENAME
$ sudo rm /etc/nginx/sites-enabled/default
$ sudo systemctl reload nginx
```

Systemd config on `/etc/systemd/system/gunicorn-staging.<your_domain>.service`:

```
[Unit]
Description=Gunicorn server for staging.<your_domain>

[Service]
Restart=on-failure  
User=alchermd  
WorkingDirectory=/home/<your_user>/sites/staging.<your_domain>  
EnvironmentFile=/home/<your_user>/sites/staging.<your_domain>/.env  

ExecStart=/home/<your_user>/sites/staging.<your_domain>/venv/bin/gunicorn \
    --bind unix:/tmp/staging.<your_domain>.socket \
    goat.wsgi:application  

[Install]
WantedBy=multi-user.target
```

...then load the new systemd config file

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl enable gunicorn-staging.<your_domain>.service
$ sudo systemctl start gunicorn-staging.<your_domain>.service
```

Setup static files

```bash
$ ./venv/bin/python manage.py collectstatic
```

Run gunicorn:

```bash
$ ./venv/bin/pip install gunicorn
$ ./venv/bin/gunicorn superlists.wsgi:application
```