from io import StringIO
import sys

def sandbox(code: str, block_globals: bool=False, 
            block_locals: bool=False) -> tuple:
    """Runs the code-string and captures any errors

    Args:
     code: executable string
     block_globals: if True don't use global namespace
     block_ locals: if True don't use local namespace
    Returns:
     output, stderr, and any exception code
    """
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()

    namespace_globals = {} if block_globals else globals()
    namespace_locals = {} if block_locals else locals()
    output, error, exception = None, None, None

    try:
        exec(code, namespace_globals, namespace_locals)
    except:
        import traceback
        exception = traceback.format_exc()

    output = redirected_output.getvalue()
    error = redirected_error.getvalue()

    # reset outputs to the original values
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    return output, error, exception
