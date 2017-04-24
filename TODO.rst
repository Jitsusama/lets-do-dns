TODO
====

*  Think about renaming the modules and maybe the project.

*  Make a README.rst file to go along with the project.

*  Develop a script/program to be triggered by this program to handle
   updating Docker container processes when new keys they rely on are
   released.

   The basic steps it should perform being:

   #. Map CERTBOT_HOSTNAME to a running Docker container(s).

      .. note:: Possibly using an image tag that contains the hostname.

   #. Trigger kill -HUP of appropriate Docker container(s).
