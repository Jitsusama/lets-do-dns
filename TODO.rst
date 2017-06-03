TODO
====

*  Push project to PyPi.

*  Develop a script/program that can be triggered by this program to handle
   updating Docker container processes when new keys they rely on are
   released.

   The basic steps it should perform being:

   #. Map ``CERTBOT_HOSTNAME`` to a running Docker container(s).

      .. note:: Possibly using an image tag that contains the hostname.

   #. Trigger ``kill -HUP`` of appropriate Docker container(s).
