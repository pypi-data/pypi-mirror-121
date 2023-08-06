import argparse
import time

def countdown_sleep(second: int):
    # check second is natural number (contains 0)
    if not isinstance(second, int) or second < 0:
        raise ValueError("'second' should be a natural number (contains 0). second: %s" % second)

    # countdown
    for i in range(second, 0, -1):
        print(f"\b \b\r{i}", end="", flush=True)
        time.sleep(1)


def cli():
    parser = argparse.ArgumentParser(description='Sleep and print countdown.')
    parser.add_argument('second', type=int, help='sleep seconds')
    args = parser.parse_args()
    countdown_sleep(args.second)
