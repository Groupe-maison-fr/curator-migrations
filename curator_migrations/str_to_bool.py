import argparse


def str_to_bool(value):
    if isinstance(value, bool):
        return value

    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True

    if value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False

    raise argparse.ArgumentTypeError('Boolean value expected.')
