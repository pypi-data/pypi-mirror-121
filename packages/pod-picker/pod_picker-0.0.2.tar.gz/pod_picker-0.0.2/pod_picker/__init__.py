import argparse
import sys

import pod_picker


def demo_print():
    print('demo print')


def pick_pod_version():
    pod_picker.pick_pod_version()


if __name__ == '__main__':
    pod_picker.pick_pod_version()
