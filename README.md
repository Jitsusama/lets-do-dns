lets-do-dns
-----------
This program's purpose is to function as a manual authentication and
cleanup hook for the Let's Encrypt [EFF's][1] [certbot][2] client program
when you wish to use [ACME-DNS][3] authentication during the certificate
authentication process, while also using [DigitalOcean's][4] DNS
infrastructure for the creation and removal of the ACME-DNS required DNS
TXT records. This program also supports being passed a command string that
will be called during the cleanup hook stage of the authentication process.

Installation
============
Installation of this program is quite easy, as it only has one external
dependency, and this program includes this dependency in its setup.py
file.

That said, there are 4 ways that you can install this program;

*  The first is via the normal means, that is, PyPI via PIP as so:

   `pip install lets-do-dns`

*  You can also install this program from a clone of the source
   repository, as so (remember, if you want to modify the source code
   without re-installing, pass the `-e` flag to PIP):

   `pip install .`

*  You can also use Docker to install/run this program. You can do this
   like so when grabbing from the Docker Hub:

   `docker pull jitsusama/lets-do-dns`

*  Finally, you can build the image from a clone of the source
   repository like so:

   `docker build -t jitsusama/lets-do-dns .`

Usage
=====
Make sure you pass the `DO_APIKEY` and `DO_DOMAIN` environment
variables to certbot when it is called. Tell certbot to load this program
by passing its name to certbot via the `--manual-auth-hook` and the
`--manual-cleanup-hook` CLI arguments.

If you would also like for this program to call your own program during
the cleanup hook stage, make sure you pass the `LETS_DO_POSTCMD`
environment variable to certbot as well, specifying the invocation string
of your program.

Here's an example of how you can use this program from the CLI when
you installed the program via PIP:

```bash
DO_APIKEY=super-secret-key \
DO_DOMAIN=mydomain.com \
LETS_DO_POSTCMD='echo ${CERTBOT_DOMAIN} > command_output.txt' \
certbot certonly --manual -d myhostname.mydomain.com \
    --preferred-challenges dns \
    --manual-auth-hook lets-do-dns \
    --manual-cleanup-hook lets-do-dns
```

Here's an example of how you can use this program from Docker when
you pulled the image from the Docker Hub:

```bash
docker run -v "$(pwd)/my-cert-dir:/etc/letsencrypt" \
    -e "DO_APIKEY=super-secret-key" \
    -e "DO_DOMAIN=mydomain.com" \
    -e 'LETS_DO_POSTCMD="echo ${CERTBOT_DOMAIN} > /etc/letsencrypt/command_output.txt"' \
    jitsusama/lets-do-dns \
    certonly --manual -d myhostname.mydomain.com \
        --preferred-challenges dns \
        --manual-auth-hook lets-do-dns \
        --manual-cleanup-hook lets-do-dns
```

[1]: https://eff.org
[2]: https://certbot.eff.org
[3]: https://tools.ietf.org/html/draft-ietf-acme-acme-06#section-8.4
[4]: https://digitalocean.com
