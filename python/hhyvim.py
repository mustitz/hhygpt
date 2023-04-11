import vim


class MyException(Exception):
    pass

def error(msg):
    raise MyException(msg)

def set_error(msg):
    msg = str(msg).replace("'", "''")
    vim.command(f"let s:error_msg = '{msg}'")


def empty():
    available = ' '.join(commands.keys())
    print(f"Available commands: {available}")

def status(args):
    if len(args) != 0:
        error('status command has no args')
    print('Hhy Gpt Plugin status:')

commands = {
    'status': status,
}

def execute(args):
    if len(args) == 0:
        return empty()

    cmd, *args = args
    func = commands.get(cmd)
    if func is None:
        error(f"Unknown command '{cmd}'")

    func(args)

def entry(cmd):
    vim.command('let s:error_msg = ""')
    try:
        args = str(cmd).split()
        execute(args)
    except MyException as e:
        set_error(e)
