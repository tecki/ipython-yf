ipython-yf
==========

An ipython extension to make it asyncio compatible
--------------------------------------------------

The asyncio package is the *next big thing* in python. It will
allow anyone to write asynchronous code that looks like synchronous
code, so getting the benefits from both worlds.

It is mostly based on the new `yield from` statement introduced in
Python 3.3. With it, you can do some kind of cooperative multitasking,
where you can explicitly tell when the other tasks are allowed to step
in, this is what the `yield from` keyword is for.

This IPython extension allows to use the `yield from` keyword on the
command line. To give a simple example:

```python
    >>> %load_ext yf
    >>> from asyncio import sleep, async
    >>> def f():
    ...     yield from sleep(3)
    ...     print("done")
    >>> yield from f()
     #[wait three seconds]
    done
    >>> async(f())
    >>> #[wait three seconds, or type other commands] done
```

This way you will be able to test or otherwise run your asyncio code
on the command line. Note that the event loop continues running while
you are typing commands, and while they are running.

This is of especial advantage when running a GUI as it is often done
on IPython. Until now, this extension supports the asyncio event loop
and the Qt event loop, using [quamash](https://github.com/harvimt/quamash).

This means, you can run `ipython3 --pylab`, plot some graphs, and
while your asyncio coroutines are running, the plots still stay responsive.
Try it! For example with the above code: during the waits mentioned
there you can still move the plots around in your plotting window.

Installation
------------

I didn't write an installation script yet, just copy the file `yf.py`
somewhere it can be imported, and everything should work.

Well, certainly only if the dependencies have been met. It certainly
needs Python 3.4, I tested it with IPython 1.2.1. Quamash 0.3 is needed
if you want to run it with Qt, but it should happily work without
Qt at all, using the asyncio event loop.

How does it work?
-----------------

Better don't ask. And don't look at the code, it is full of dirty tricks
you should *never* do. This includes usage of undocumented, accidental
features of the python compiler, setting private variables, calling
internal functions and those things mummy didn't tell you about.

But if you're still reading: the input you type in gets compiled into
an AST, which is then modified to call a function instead of doing a
`yield from`. This function then secretly makes the event loop run
again. (In Qt they call that a local event loop, in asyncio they call
it a *don't do that*).

The future
----------

In a bright, great future, all event loops will happily cooperate with
asyncio, which will ease the development of IPython tremendously.
Some people are already working on the asyncio capabilities of both
Qt and zmq, which are already two of the event loops used by IPython.
Maybe at some later point even CPython will step in and make its event
loops (`builtin.input` and the commands that run on the command line)
asyncio compatible.

Further reading
---------------

There has been some discussion on
[python-ideas](https://mail.python.org/pipermail/python-ideas/2014-September/029293.html)
and on the [Python issue tracker](http://bugs.python.org/issue22412).
