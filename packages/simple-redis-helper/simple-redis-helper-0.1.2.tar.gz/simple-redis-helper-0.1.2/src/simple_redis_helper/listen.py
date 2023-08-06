import argparse
import os
import redis
import traceback
from datetime import datetime

DATETIME_FORMAT_URL = "https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes"


def main(args=None):
    """
    The main method for parsing command-line arguments and running the application.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser(
        prog="simple_redis_helper-listen",
        description="Listens to the specified channel for messages to come through and outputs them on stdout if no output directory provided.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-H', '--host', metavar='HOST', required=False, default="localhost", help='The redis server to connect to')
    parser.add_argument('-p', '--port', metavar='PORT', required=False, default=6379, type=int, help='The port the redis server is listening on')
    parser.add_argument('-d', '--database', metavar='DB', required=False, default=0, type=int, help='The redis database to use')
    parser.add_argument('-c', '--channel', metavar='CHANNEL', required=True, default=None, help='The channel to broadcast the content on')
    parser.add_argument('-D', '--data_only', action='store_true', help='Whether to output only the message data')
    parser.add_argument('-s', '--convert_to_string', action='store_true', help='Whether to convert the message data to string (requires --data_only)')
    parser.add_argument('-o', '--output_dir', metavar='DIR', required=False, default=None, help='The directory to store the received messages/data in')
    parser.add_argument("-f", "--file_format", metavar="FORMAT", help="the format to use for the output files (when using '--output_dir'), see: %s" % DATETIME_FORMAT_URL, required=False, default="%Y%m%d_%H%M%S.%f.dat")
    parsed = parser.parse_args(args=args)

    # check output dir
    if parsed.output_dir is not None:
        if not os.path.exists(parsed.output_dir):
            raise Exception("Output directory does not exist: %s" % parsed.output_dir)
        if not os.path.isdir(parsed.output_dir):
            raise Exception("Output does not point to a directory: %s" % parsed.output_dir)
    # check output format
    try:
        datetime.now().strftime(parsed.file_format)
    except Exception as e:
        raise Exception("Invalid timestamp format: %s\nSee: %s" % (parsed.file_format, DATETIME_FORMAT_URL)) from e

    # connect
    r = redis.Redis(host=parsed.host, port=parsed.port, db=parsed.database)

    # handler for listening/outputting
    def anon_handler(message):
        data = message
        if parsed.data_only:
            data = message['data']
            if parsed.convert_to_string:
                data = data.decode()
        if parsed.output_dir is None:
            print(data)
        else:
            fname = datetime.now().strftime(parsed.file_format)
            fname = os.path.join(parsed.output_dir, fname)
            if parsed.convert_to_string:
                with open(fname, "w") as f:
                    f.write(data)
            else:
                with open(fname, "wb") as f:
                    f.write(data)

    # subscribe and start listening
    p = r.pubsub()
    p.psubscribe(**{parsed.channel: anon_handler})
    p.run_in_thread(sleep_time=0.001)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.
    :return: 0 for success, 1 for failure.
    :rtype: int
    """
    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == '__main__':
    main()

