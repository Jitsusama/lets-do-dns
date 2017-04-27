TODO
====

*  Perform a DNS lookup during the authentication hook stage, after the
   record has been created, instead of putting in an arbitrary timeout.
   Retry every 500ms, up to 4 seconds, before giving up with an exception.

   Use dnspython library for the lookups.

*  Add error handling for ``requests.get`` and ``requests.put`` related
   library exceptions and throw our own custom exceptions based on them.

*  Add error handling for ``subprocess.check_call`` exceptions and throw
   our own custom exceptions base on them.

*  Add failure timeout for ``requests.get`` and ``requests.put`` actions.

*  Tidy up py.test fixtures and add comments to test modules when
   conftest.py is being used for fixtures within that test module.

*  Create a Jenkins CI build script (Jenkinsfile).

*  Push project to PyPi.

*  Develop a script/program that can be triggered by this program to handle
   updating Docker container processes when new keys they rely on are
   released.

   The basic steps it should perform being:

   #. Map ``CERTBOT_HOSTNAME`` to a running Docker container(s).

      .. note:: Possibly using an image tag that contains the hostname.

   #. Trigger ``kill -HUP`` of appropriate Docker container(s).
