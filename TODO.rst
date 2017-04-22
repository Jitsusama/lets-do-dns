TODO
====

*  Add --help/-h/help parameter. This should detail what parameters are
   required and how they effect the program's state. It should also give
   a short blurb about what the program does.

*  Add environment variable verification before running. Check that all
   required parameters are present in the passed environment variables,
   or trigger an error with text explaining which variables are missing
   or have incorrect values.

*  Think about renaming the modules and maybe the project.

*  Make a README.rst file to go along with the project.

*  Develop a script/program to be triggered by this program to handle
   updating Docker container processes when new keys they rely on are
   released.

   The basic steps it should perform being:

   #. Map CERTBOT_HOSTNAME to a running Docker container(s).

      .. note:: Possibly using an image tag that contains the hostname.

   #. Trigger kill -HUP of appropriate Docker container(s).


.. code:: python

    description = '''\
    Perform ACME DNS01 authentication for the EFF's certbot program.

    The DNS01 authentication record will be created via DigitalOcean's
    REST API.'''

    epilog = '''\
    This program requires the presence of the CERBOT_DOMAIN and
    CERTBOT_VALIDATION environment variables. These should be supplied by
    the certbot program when this program is called via its
    --manual-auth-hook or --manual-cleanup-hook arguments.

    This program also requires the presence of the DO_API_KEY and
    DO_DOMAIN environment variables. These have to be provided via the
    environment that certbot is executed from.

    DO_API_KEY refers to a DigitalOcean API key generated through its API
    control panel. This key should have read and write access to your
    DigitalOcean account.

    DO_DOMAIN refers to which domain under your DigitalOcean account will
    function as the root of the certbot SSL certificate authentication
    request.'''

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog=epilog)
    arguments = parser.parse_args(['--help'])
