import re
from utils.utils import (
    image_to_text,
    fomat_currency,
    is_abbreviated_date,
    format_date
)

TOTAL_INVOICES_PATTERN = re.compile(r'Total\s*[:]*\s*\$?([\d,]+\.\d{2})')
INVOICE_NUMBER_PATTERN = re.compile(r'#\s*(\d+)')
INVOICE_DATE_PATTERN = re.compile(r"\b(\d{4}-\d{2}-\d{2}|[A-Z][a-z]{2} \d{1,2}, \d{4})\b") # noqa E501


def get_info_invoice(invoice_path: str):
    text_image = image_to_text(invoice_path)

    list_info = text_image.split('\n')

    invoice_date_match = INVOICE_DATE_PATTERN.search(text_image)
    invoice_number_match = INVOICE_NUMBER_PATTERN.search(text_image)
    total_invoice_match = TOTAL_INVOICES_PATTERN.search(text_image)

    invoice_date = invoice_date_match.group(1) if invoice_date_match else None
    abbreviated_date = is_abbreviated_date(invoice_date)

    invoice_number = invoice_number_match.group(1) if invoice_number_match else None # noqa E501
    total_invoice = total_invoice_match.group(1) if total_invoice_match else None # noqa E501

    if abbreviated_date:
        company_name = list_info[4]
    else:
        company_name = str(list_info[0]).split(" ")
        company_name = " ".join(company_name[0:2])

    if abbreviated_date:
        invoice_date = format_date(invoice_date, '%b %d, %Y', '%d/%m/%Y')
    else:
        invoice_date = format_date(invoice_date, '%Y-%m-%d', '%d/%m/%Y')

    total_invoice = fomat_currency(total_invoice)

    current_data = {
        "company_name": company_name,
        "invoice_date": invoice_date,
        "invoice_number": invoice_number,
        "total_invoice": total_invoice,
    }

    return None if None in current_data.values() else current_data
