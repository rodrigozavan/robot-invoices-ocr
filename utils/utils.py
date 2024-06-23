from datetime import datetime
import pytesseract
import locale
import os

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def image_to_text(image, lang: str = 'eng') -> str:
    """
    Converts an image to text using OCR (Optical Character Recognition).

    Parameters:
        image (PIL.Image.Image): The input image to be converted.

    Returns:
        str: The extracted text from the image.
    """
    return pytesseract.image_to_string(image, lang=lang)


def clear_directory(directory: str) -> None:
    """
    Clears the invoices directory.

    """
    for root, _, files in os.walk(directory):
        for file in files:
            os.remove(os.path.join(root, file))


def is_abbreviated_date(date: str) -> bool:
    """
    Checks if a date string is in the abbreviated format 'MMM DD, YYYY'.

    Args:
        date (str): The date string to be checked.

    Returns:
        bool: True if the date string is in the
        abbreviated format, False otherwise.

    Raises:
        None

    Examples:
        >>> is_abbreviated_date('Jan 01, 2022')
        True

        >>> is_abbreviated_date('2022-01-01')
        False
    """
    try:
        datetime.strptime(date, '%b %d, %Y')
        return True
    except ValueError:
        return False


def format_date(date: str, current_format: str, target_format: str) -> str: # noqa E501
    """
    Formats an abbreviated date string into the 'YYYY-MM-DD' format.

    Args:
        date (str): The abbreviated date string in the format 'MMM DD, YYYY'.

    Returns:
        str: The formatted date string in the 'YYYY-MM-DD' format.

    Raises:
        None

    Examples:
        >>> format_abbreviated_date('Jan 01, 2022')
        '2022-01-01'

        >>> format_abbreviated_date('Invalid Date')
        'Invalid Date'
    """
    try:
        return datetime.strptime(date, current_format).strftime(target_format)
    except ValueError:
        return date


def fomat_currency(value: str) -> str:
    """
    Formats a currency string from the format '$1,000.00' to '1000.00'.

    Args:
        value (str): The currency string to be formatted.

    Returns:
        str: The formatted currency string in the format '1000.00'.

    Raises:
        None

    Examples:
        >>> format_currency('$1,000.00')
        '1000.00'
        >>> format_currency('1,000.00')
        '1,000.00'
    """
    return str(value).replace(',', '')


def validate_duedate(due_date: str, date_invoice: str):
    """
    Validates if the invoice is overdue.

    Args:
        due_date (str): The due date of the invoice.
        date_invoice (str): The date of the invoice.

    Returns:
        bool: True if the invoice is overdue, False otherwise.
    """
    due_date = datetime.strptime(due_date, '%d/%m/%Y')
    date_invoice = datetime.strptime(date_invoice, '%d/%m/%Y')

    return date_invoice <= due_date
