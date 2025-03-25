
def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def sanitize_input(input_string):
    # Remove or replace potentially dangerous characters
    sanitized_string = input_string.replace("'", "").replace('"', '')
    return sanitized_string
