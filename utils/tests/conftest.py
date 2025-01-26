import socket


def guard(*args, **kwargs):
    raise Exception("I told you not to use the Internet!")


socket.socket = guard
