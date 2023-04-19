import vim

from gpt import default as gpt, GptError
from gpt import get_text_for_completion


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
    gpt.print_status()

def complete(args):
    if len(args) != 0:
        error('complete command has no args')

    buf = vim.current.buffer[:]
    l, c = vim.current.window.cursor

    text = get_text_for_completion(buf, l)
    insertion = gpt.complete_text(text)
    insertion.append('<' * 42)
    vim.current.buffer[l:l] = insertion

def ask(args):
    if len(args) == 0:
        error('Please, type a question after ask')

    text = ' '.join(args)
    for line in gpt.complete_text(text, max_tokens=2048):
        print(line)

commands = {
    'complete' : complete,
    'ask' :      ask,
    'status'   : status,
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
    except (MyException, GptError) as e:
        set_error(e)
