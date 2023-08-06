import ctypes
import inspect
import threading
from functools import partial
from typing import Any, Callable

from tortfunc.exceptions import FunctionTimeOut


def threaded_timeout(function: Callable[..., Any], timeout: float) -> Callable[..., Any]:
    def thread_kill_func(*args, **kwargs):
        # First param is gibberish to prevent it conflicting with main function's kwargs
        def returnable_func(asfasfvzc: list, *targs, **tkwargs):
            asfasfvzc.append(function(*targs, **tkwargs))

        ret = []
        target_func = partial(returnable_func, ret)

        kill_thread = KillableThread(target=target_func, args=args, kwargs=kwargs)
        kill_thread.start()
        kill_thread.join(timeout=timeout)

        if kill_thread.is_alive():

            kill_thread.terminate()
            raise FunctionTimeOut()
        
        if ret:
            return ret[0]

    return thread_kill_func


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class KillableThread(threading.Thread):
    """A thread that can be manually killed by raising an exception.

    Based on code from: http://tomerfiliba.com/recipes/Thread2/
    """

    def _get_my_tid(self):
        """determines this (self's) thread id"""
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        raise AssertionError("could not determine the thread's id")

    def raise_exc(self, exctype):
        """raises the given exception type in the context of this thread"""
        _async_raise(self.ident, exctype)

    def terminate(self):
        """raises SystemExit in the context of the given thread, which should
        cause the thread to exit silently (unless caught)"""
        self.raise_exc(SystemExit)
