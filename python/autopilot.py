import platform
from . import chain


if __name__ == '__main__':
    if platform.system() == 'Windows':
        chain.CVChainWindows().run()
