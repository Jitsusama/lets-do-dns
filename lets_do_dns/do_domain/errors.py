"""Interprets exceptions returned by the DigitalOcean API."""


def exception_message(exception):
    """For requests exceptions, return a reinterpretation of the error."""
    request = exception.request
    response = exception.response

    appended_string = (
        'the following error while performing a {} operation against the '
        '{} URI: {}'.format(request.method, request.url, exception))

    if response:
        final_string = 'Received a {} response with {}'.format(
            response.status_code, appended_string)
    else:
        final_string = 'Encountered {}'.format(appended_string)

    return final_string
