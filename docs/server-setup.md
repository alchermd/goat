# Server Setup (Staging)

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

## Deployment

1. Create a directory for the staging site and clone the repo there:

```bash
$ mkdir ~/sites/staging.your-domain.tld
$ cd ~/sites/staging.your-domain.tld
$ git clone <git repo url> .
```

2. Make sure to allow port 8000 through the firewall

```bash
$ sudo ufw allow 8000
```

3. Setup the virtualenvironment and try to run the server there

```bash
$ python3.8 -m venv venv
$ ./venv/bin/pip install -r requirements.txt
$ ./venv/bin/python manage.py runserver 0.0.0.0:8000
```