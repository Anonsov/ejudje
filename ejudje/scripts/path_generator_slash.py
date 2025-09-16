def path_generator_slash(*args):
    """Functions that returns the path with slashes

    Returns:
        path: put the args parameters and get the path as in OSes
    """
    path_output = ""
    for i in args:
        path_output += i + "/"
    return path_output
