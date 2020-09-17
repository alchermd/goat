Deploying a New Release
===================================

## Prerequisites

1. Make sure your local virtual environment is active
2. Push the latest changes

## Using Fabric

```bash
$ cd ./deploy_tools
$ fab deploy:host=<your_user>@<domain>
```

## Provision the New Site

If the deploy is for a new site, e.g., a new subdomain, you need to configure a new Nginx and Systemd config

```bash
$ sudo cp ./deploy_tools/nginx.template.conf /etc/nginx/sites-available/<domain>
$ sudo vim /etc/nginx/sites-available/<domain> # <- edit the DOMAIN and <your_user> parts
$ sudo ln -s /etc/nginx/sites-available/<domain> /etc/nginx/sites-enabled/<domain>
$ sudo cp ./deploy_tools/gunicorn-systemd.template.service /etc/systemd/system/gunicorn-<domain>.service
$ sudo vim /etc/systemd/system/gunicorn-<domain>.service # <- edit the DOMAIN and <your_user> parts as well
$ sudo systemctl daemon-reload
$ sudo systemctl reload nginx
$ sudo systemctl enable gunicorn-<domain>.service
$ sudo systemctl start gunicorn-<domain>.service
```