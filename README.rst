lets-do-dns
===========

This program's purpose is to function as a manual authentication and
cleanup hook for the Let's Encrypt EFF_\'s certbot_ client program when you
wish to use ACME-DNS authentication during the certificate authentication
process, while also using DigitalOcean_\'s DNS infrastructure for the
creation and removal of the ACME-DNS required DNS TXT records. This program
also supports being passed a command string that will be called during the
cleanup hook stage of the authentication process.

Installation
------------

Installation of this program is quite easy, as it only has one external
dependency, and this program includes this dependency in its setup.py
file. So, you should be able to install the whole enchilada with the
following command:

.. code-block:: bash

   pip install lets-do-dns

Usage
-----

Make sure you pass the ``DO_APIKEY`` and ``DO_DOMAIN`` environment
variables to certbot when it is called. Tell certbot to load this program
by passing its name to certbot via the ``--manual-auth-hook`` and the
``--manual-cleanup-hook`` CLI arguments.

If you would also like for this program to call your own program during
the cleanup hook stage, make sure you pass the ``LETS_DO_POSTCMD``
environment variable to certbot as well, specifying the invocation string
of your program.

Here's an example of how you can use this program:

.. code-block:: bash

   DO_API_KEY=super-secret-key \
   DO_DOMAIN=mydomain.com \
   LETS_DO_POSTCMD='echo ${CERTBOT_DOMAIN} > command_output.txt' \
   certbot certonly --manual -d myhostname.mydomain.com \
       --preferred-challenges dns \
       --manual-auth-hook lets-do-dns \
       --manual-cleanup-hook lets-do-dns

.. _EFF: https://eff.org
.. _certbot: https://certbot.eff.org
.. _ACME-DNS: https://tools.ietf.org/html/draft-ietf-acme-acme-06#section-8.4
.. _DigitalOcean: https://digitalocean.com
