class GQLException(Exception):
    pass


import inspect


def gql(f):
    def wrapper(*args, **kwargs):
        print("hehehe", inspect.signature(f))
        print("args", args, "kwargs", kwargs)
        return f(*args, **kwargs)

    return wrapper
