from certbot_dns_auth.arguments import Arguments
from mock import ANY, call


def test_calls_argumentparser(mocker):
    stub_argumentparser = mocker.patch(
        'certbot_dns_auth.arguments.argparse.ArgumentParser')

    Arguments('')

    stub_argumentparser.assert_called_once()


def test_passes_output_texts_to_argumentparser(mocker):
    stub_argumentparser = mocker.patch(
        'certbot_dns_auth.arguments.argparse.ArgumentParser')

    Arguments('')

    stub_argumentparser.assert_called_once_with(
        description=ANY, epilog=ANY)


def test_passes_arguments_and_not_progname_to_parseargs(mocker):
    stub_argumentparser = mocker.patch(
        'certbot_dns_auth.arguments.argparse.ArgumentParser')
    passed_arguments = ['lets-do-dns', '--help']

    Arguments(passed_arguments)

    stub_argumentparser.assert_has_calls([
        call().parse_args(passed_arguments[1:])])