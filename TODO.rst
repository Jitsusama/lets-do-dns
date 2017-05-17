TODO
====

*  Add error handling for ``requests.get`` and ``requests.put`` related
   library exceptions and throw our own custom exceptions based on them.

   *  requests.exceptions.RequestException seems to be the common ancestor
      for all exceptions from the requests library.

*  Add error handling for ``subprocess.check_call`` exceptions and throw
   our own custom exceptions based on them.

*  Add failure timeout for ``requests.get`` and ``requests.put`` actions.

*  Create a Jenkins CI build script (Jenkinsfile).

*  Push project to PyPi.

*  Develop a script/program that can be triggered by this program to handle
   updating Docker container processes when new keys they rely on are
   released.

   The basic steps it should perform being:

   #. Map ``CERTBOT_HOSTNAME`` to a running Docker container(s).

      .. note:: Possibly using an image tag that contains the hostname.

   #. Trigger ``kill -HUP`` of appropriate Docker container(s).
