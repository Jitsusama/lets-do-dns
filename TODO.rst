TODO
====

*  http.response() should be wrapped into a class with its helper
   methods.

*  Add --help/-h/help parameter. This should detail what parameters are
   required and how they effect the program's state. It should also give
   a short blurb about what the program does.

*  Add environment variable verification before running. Check that all
   required parameters are present in the passed environment variables,
   or trigger an error with text explaining which variables are missing
   or have incorrect values.

*  Think about renaming the modules and maybe the project.

*  Develop a script/program to be triggered by this program to handle
   updating Docker container processes when new keys they rely on are
   released.

   The basic steps it should perform being:

   #. Map CERTBOT_HOSTNAME to a running Docker container(s).

      .. note:: Possibly using an image tag that contains the hostname.

   #. Trigger kill -HUP of appropriate Docker container(s).
