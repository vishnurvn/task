import re

EMAIL_REGEX = re.compile(r'\w+@\w+.(com|org|edu|co.in)')


def email_validator(email: str) -> bool:
    """
    Email validator. Validates email with respect to a regular expression.

    Parameters
    ----------
    email : str
        Email of a user as string object.

    Returns
    -------
    boolean : bool
        Return True if the email is valid and False if the email is not valid

    """
    if re.match(EMAIL_REGEX, email):
        return True
    return False

