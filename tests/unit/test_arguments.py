from certbot_dns_auth.arguments import Arguments


def test_calls_argumentparser(mocker):
    stub_argumentparser = mocker.patch(
        'certbot_dns_auth.arguments.argparse.ArgumentParser')

    Arguments('')

    stub_argumentparser.assert_called_once()
