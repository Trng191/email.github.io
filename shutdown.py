import os
from platform import system


def shutdown():
    os.system("shutdown -s -t 0")


if __name__ == "__main__":
    shutdown()
