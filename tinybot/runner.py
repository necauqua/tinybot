import os
import argparse


def run(bot_cls):
    """
    Runs a little CLI for the bot. Used to give the token to a bot and to
    choose between longpoll and webhook (and their config).

    Funny, but it can be used as a decorator on the bot class.
    """

    parser = argparse.ArgumentParser(description=bot_cls.description)
    subparsers = parser.add_subparsers(
        metavar='type{longpoll, webhook}', dest='type',
        help='Technique used for listening to updates.\n'
             'It is recommended to call the program with arguments \'TYPE -h\' for type-specific help.'
    )

    longpoll_parser = subparsers.add_parser(
        'longpoll',
        description='This mode uses the long polling technique to receive the updates. '
                    'It sends a requests to a Telegram server and waits for response for a given timeout. '
                    'Telegram server would respond if anything happens within this '
                    'time, or respond with empty request after timeout.'
    )
    longpoll_parser.add_argument('token', help='The token of given bot')

    def ranged_int(mn, mx):
        def checker(x):
            value = int(x)
            if value < mn:
                raise argparse.ArgumentTypeError('%s is less than %s!' % (value, mn))
            if value > mx:
                raise argparse.ArgumentTypeError('%s is more than %s!' % (value, mx))
            return value

        return checker

    longpoll_parser.add_argument('-t', '--timeout', type=ranged_int(0, 600), default=30,
                                 help='Long poll timeout in seconds. Integer in range [0, 600]. '
                                      'Defaults to 30')

    webhook_parser = subparsers.add_parser(
        'webhook',
        description='This mode uses the webhook technique to receive the updates. '
                    'It launches a small HTTP server which will react to '
                    'update requests from Telegram servers.'
    )

    webhook_parser.add_argument('token', help='The token of given bot')
    webhook_parser.add_argument('port', type=ranged_int(0, 65535), help='Local port to listen at')
    webhook_parser.add_argument('url', help='URL which will be set as the webhook link.')

    args = parser.parse_args()

    if args.type is None:
        parser.parse_args(['-h'])
        return

    bot_cls.token = getattr(args, 'token', os.getenv('TELEGRAM_BOT_TOKEN'))
    if args.type == 'longpoll':
        bot_cls.launch_longpoll(args.timeout)
    elif args.type == 'webhook':
        bot_cls.launch_webhook(args.url, args.port)
