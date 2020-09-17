Provisioning a new site
===================================

## Prerequisites

1. Buy a domain. I used NameCheap to buy mine.
2. Create an instance of an Ubuntu 18.04 server somewhere. I hosted mine on DigitalOcean
3. Folow [this guide](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04) for the
initial server setup
4. Follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars#registrar-namecheap)
on how to setup the domain that we bought.
5. Once the DNS has propagated, follow [this guide](https://www.digitalocean.com/docs/networking/dns/how-to/manage-records/)
to manage the appropriate DNS records. Make sure to add both `*` and `@` A-records.

## Required Packages

* python3.8 
* python3-venv 
* python3-pip 
* git

## Nginx Virtual Host Config

* see `nginx.template.conf`
* replace `DOMAIN` with, e.g, `staging.my-domain.com`

## Systemd Service

* see `gunicorn-systemd.template.service`
* replace `DOMAIN` with, e.g, `staging.my-domain.com`

## Folder Structure

Assume we have a user account at `/home/username`

```
/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── virtualenv
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc
```