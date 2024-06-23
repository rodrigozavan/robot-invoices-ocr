from playwright.sync_api import Playwright, sync_playwright
from utils.utils import validate_duedate, clear_directory
from utils.extract_data_invoices import get_info_invoice
from pages.InvoicesPage import InvoicesPage
from utils.csv_heandler import write_csv
from datetime import datetime
import json
import os
from settings import (
    INVOICES_DIR,
    DATA_INVOICES_DIR,
    REPORTS_DIR
)


def run(playwright: Playwright) -> None:
    try:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        invoices_page = InvoicesPage(page)

        invoices_page.open()

        invoices_links = invoices_page.get_invoices_links()
        if invoices_links.get("error"):
            return invoices_links

        invoices_data = invoices_links.get("data")

        files_invoices = invoices_page.download_invoices(invoices_data)
        if files_invoices.get("error"):
            return files_invoices

        invoices_data = files_invoices.get("data")

        for invoice in invoices_data:
            info_invoices = get_info_invoice(invoice.get("fullpath"))

            if info_invoices is None:
                return {
                    "error": True,
                    "message": f"Erro ao coletar dados da fatura.",
                    "data": None,
                }

            for key, value in info_invoices.items():
                invoice[key] = value

        with open(
            file=f"{DATA_INVOICES_DIR}/invoices-data-{today}.json",
            mode="w", encoding="utf8"
        ) as f:
            json.dump(invoices_data, f, indent=4, ensure_ascii=False)

        date_to_write = []

        for data_item in invoices_data:

            is_overdue = validate_duedate(
                data_item["due_date"], data_item["invoice_date"]
            )

            if is_overdue:

                date_to_write.append({
                    "ID": data_item["id_invoice"],
                    "DueDate": data_item["due_date"],
                    "InvoiceNo": data_item["invoice_number"],
                    "InvoiceDate": data_item["invoice_date"],
                    "CompanyName": data_item["company_name"],
                    "TotalDue": data_item["total_invoice"]
                })

        if date_to_write:
            filename = f"overdue-invoices-{today}.csv"
            filename = os.path.join(REPORTS_DIR, filename)
            write_csv(filename, date_to_write)
            message = f"Operação realizada com sucesso: Relatório salvo em: {filename}" # noqa E501
        else:
            message = "Operação realizada com sucesso: Sem faturas vencidas."

        return {
            "error": False,
            "message": message,
            "data": None,
        }

    except Exception as e:
        return {
            "error": True,
            "message": f"Erro inesperado: {e}.",
            "data": None,
        }

    finally:
        context.close()
        browser.close()
        clear_directory(INVOICES_DIR)


if __name__ == "__main__":

    with sync_playwright() as playwright:
        result = run(playwright)
        print(result)
