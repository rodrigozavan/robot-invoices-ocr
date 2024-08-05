from playwright.sync_api import Playwright, sync_playwright
from utils.extract_data_invoices import get_info_invoice
from pages.InvoicesPage import InvoicesPage
from utils.utils import validate_duedate
from utils.csv_heandler import write_csv
from datetime import datetime
import json
import os
from settings import (
    DATA_INVOICES_DIR,
    REPORTS_DIR,
    logging
)


def run(playwright: Playwright) -> None:
    try:

        logging.info("Iniciando navegador...")

        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        logging.info("Navegador iniciado, coletando links das faturas...")

        today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        invoices_page = InvoicesPage(page)

        invoices_page.open()

        start_challange = invoices_page.start_challange()
        if start_challange.get("error"):
            logging.error(start_challange.get("message"))
            return start_challange

        invoices_links = invoices_page.get_invoices_links()
        if invoices_links.get("error"):
            logging.error(invoices_links.get("message"))
            return invoices_links

        invoices_data = invoices_links.get("data")

        logging.info("Links coletados, iniciando download das faturas...")

        files_invoices = invoices_page.download_invoices(invoices_data)
        if files_invoices.get("error"):
            logging.error(files_invoices.get("message"))
            return files_invoices

        invoices_data = files_invoices.get("data")

        total_invoices = len(invoices_data)

        logging.info(f"Download concluido, total de {total_invoices} faturas coletadas...") # noqa E501
        logging.info(f"Iniciando extração dos dados das faturas...") # noqa E501

        for invoice in invoices_data:
            fullpath_invoice = invoice.get("fullpath")
            info_invoices = get_info_invoice(fullpath_invoice)

            if info_invoices is None:
                message = "Erro ao coletar dados da fatura."
                logging.error(message)
                return {
                    "error": True,
                    "message": message,
                    "data": None,
                }

            for key, value in info_invoices.items():
                invoice[key] = value

            logging.info(f"Dados da fatura extraidos {fullpath_invoice}...")

        logging.info("Escrevendo json com os dados das faturas...")

        fullpath_json = f"{DATA_INVOICES_DIR}/invoices-data-{today}.json"

        with open(file=fullpath_json, mode="w", encoding="utf8") as f:
            json.dump(invoices_data, f, indent=4, ensure_ascii=False)

        logging.info(f"Json salvo em: {fullpath_json}...")

        date_to_write = []

        for data_item in invoices_data:

            is_overdue = validate_duedate(
                data_item["due_date"]
            )

            invoice_no = data_item["invoice_number"]

            if is_overdue:

                logging.info(f"Fatura {invoice_no} adicionada no relatório...") # noqa E501

                date_to_write.append({
                    "ID": data_item["id_invoice"],
                    "DueDate": data_item["due_date"],
                    "InvoiceNo": data_item["invoice_number"],
                    "InvoiceDate": data_item["invoice_date"],
                    "CompanyName": data_item["company_name"],
                    "TotalDue": data_item["total_invoice"]
                })

        filename = f"overdue-invoices-{today}.csv"
        filename = os.path.join(REPORTS_DIR, filename)
        write_csv(filename, date_to_write)

        submit_report = invoices_page.submit_report(filename)
        if submit_report.get("error"):
            logging.error(submit_report.get("message"))
            return submit_report

        message = f"Operação realizada com sucesso: Relatório salvo em: {filename}" # noqa E501

        logging.info(message)

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


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
