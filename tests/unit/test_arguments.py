"""Tests the lets_do_dns.arguments.py module."""

from mock import ANY, call

from lets_do_dns.arguments import Arguments


def test_calls_argument_parser(mocker):
    mock_argument_parser = mocker.patch(
        'lets_do_dns.arguments.argparse.ArgumentParser')

    Arguments('')

    mock_argument_parser.assert_called_once()


def test_passes_descriptive_texts_to_argument_parser(mocker):
    mock_argument_parser = mocker.patch(
        'lets_do_dns.arguments.argparse.ArgumentParser')

    Arguments('')

    mock_argument_parser.assert_called_once_with(
        description=ANY, epilog=ANY)


def test_passes_arguments_and_not_progname_to_parse_args(mocker):
    mock_argument_parser = mocker.patch(
        'lets_do_dns.arguments.argparse.ArgumentParser')

    Arguments(['lets-do-dns', '--help'])

    mock_argument_parser.assert_has_calls([
        call().parse_args(['--help'])])
