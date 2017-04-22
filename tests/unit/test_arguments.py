from certbot_dns_auth.arguments import Arguments
from mock import ANY


def test_calls_argumentparser(mocker):
    stub_argumentparser = mocker.patch(
        'certbot_dns_auth.arguments.argparse.ArgumentParser')

    Arguments('')

    stub_argumentparser.assert_called_once()


def test_passes_output_texts_to_argumentparser(mocker):
    stub_argumentparser = mocker.patch(
        'certbot_dns_auth.arguments.argparse.ArgumentParser')

    Arguments('')

    stub_argumentparser.assert_called_once_with(description=ANY, epilog=ANY)
