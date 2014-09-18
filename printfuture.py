import sys
from asyncio import Future
from functools import partial

def load_ipython_extension(ip):
    class Hook(ip.displayhook_class):
        def delayedprint(self, future):
            ec = self.shell.execution_count
            self.shell.execution_count = future.number
            try:
                sys.displayhook(future.result())
            finally:
                self.shell.execution_count = ec

        def __call__(self, result=None):
            super().__call__(result)
            if isinstance(result, Future):
                result.number = self.shell.execution_count
                result.add_done_callback(self.delayedprint)

    ip.displayhook_class = Hook
    ip.init_displayhook()
