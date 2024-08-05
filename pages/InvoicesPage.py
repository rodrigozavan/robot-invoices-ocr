from urllib.request import urlretrieve
from utils.utils import format_date
from urllib.parse import urlsplit
from settings import INVOICES_DIR
from locators import Locators
from typing import List, Dict
import os
from playwright.sync_api import (
    Page,
    expect
)


class InvoicesPage:
    """
    Represents a page for managing invoices.

    Args:
        page (Page): The page object used for interacting with the web page.

    Attributes:
        page (Page): The page object used for interacting with the web page.
        url (str): The URL of the invoices page.

    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.__url = "https://rpachallengeocr.azurewebsites.net"
        self.locators = Locators.Invoices()

    @property
    def url(self):
        """
        Get the URL of the invoices page.

        Returns:
            str: The URL of the invoices page.

        """
        return self.__url

    @url.setter
    def url(self, value):
        """
        Set the URL of the invoices page.

        Args:
            value (str): The URL of the invoices page.

        """
        self.__url = value

    def open(self):
        """
        Open the invoices page in the browser.

        """
        self.page.goto(self.url)

    def start_challange(self, timeout: int = 10000):
        """
        Open the invoices page in the browser.

        """
        try:
            start_challange = self.page.locator(self.locators.btn_start_challange) # noqa E501
            expect(start_challange).to_be_visible(timeout=timeout)
            start_challange.click()
        except Exception as e:
            return {
                "error": True,
                "message": f"Erro ao iniciar desafio: {e}",
                "data": None,
            }

        return {
            "error": False,
            "message": "",
            "data": None,
        }

    def get_invoices_links(self, timeout: int = 5000) -> Dict[str, List]:
        """
        Retrieves the links to the invoices on the page.

        Args:
            timeout (int): The maximum time to wait for the
            links to be visible (in milliseconds). Default is 5000.

        Returns:
            dict: A dictionary containing the result of the operation.
                - If the links are visible, the dictionary will
                have the following structure:
                    {
                        "error": False,
                        "message": "",
                        "data": [list of links]
                    }
                - If the links are not visible, the dictionary will have
                the following structure:
                    {
                        "error": True,
                        "message": "The invoices links are not visible.",
                        "data": None
                    }
        """
        try:
            btn_paginate = self.page.locator(self.locators.btn_paginate)
            expect(btn_paginate.first).to_be_visible(timeout=timeout)

            links = []
            buttons = btn_paginate.all()

            for button in buttons:
                button.click()

                rows_invoices = self.page.locator(self.locators.rows_invoices)
                expect(rows_invoices.first).to_be_visible(timeout=timeout)
                rows_invoices = rows_invoices.all()

                for row in rows_invoices:
                    id_invoice = row.locator("td:nth-child(2)").text_content()

                    due_date = row.locator("td:nth-child(3)").text_content()
                    due_date = format_date(due_date, '%d-%m-%Y', '%d/%m/%Y')

                    link = row.locator("td:nth-child(4) a").get_attribute("href") # noqa E501
                    link = f"{self.url}{link}"

                    current_data = {
                        "id_invoice": id_invoice,
                        "due_date": due_date,
                        "link": link
                    }

                    links.append(current_data)

        except Exception as e:
            return {
                "error": True,
                "message": f"Erro ao coletar faturas: {e}",
                "data": None,
            }

        return {
                "error": False,
                "message": "",
                "data": links,
            }

    def download_invoices(self, invoices: list):
        """
        Downloads the given list of invoices from their URLs
        and saves them to the local filesystem.

        Args:
            invoices (list): A list of URLs pointing to the
            invoices to be downloaded.

        Returns:
            dict: A dictionary containing the result of the download operation. # noqa E501
            The dictionary has the following keys:
                - "error" (bool): Indicates whether an error occurred during
                the download process.
                - "message" (str): An error message if an error occurred, or
                an empty string if the download was successful.
                - "data" (list): A list of file paths where the downloaded
                invoices are saved. Empty if an error occurred.
        """
        try:

            for item in invoices:
                path_invoice = urlsplit(item["link"]).path
                filename = path_invoice.split("/")[-1]

                fullpath = os.path.join(INVOICES_DIR, filename)
                urlretrieve(item["link"], fullpath)

                item["fullpath"] = fullpath

        except Exception as e:
            return {
                "error": True,
                "message": f"Erro ao baixar faturas: {e}.",
                "data": None,
            }

        return {
            "error": False,
            "message": "",
            "data": invoices,
        }

    def submit_report(self, path: str, timeout: int = 10000):
        """
        Open the invoices page in the browser.

        """
        try:

            submit_reports = self.page.locator(self.locators.input_submit_reports) # noqa E501
            expect(submit_reports).to_be_visible(timeout=timeout)
            submit_reports.set_input_files(path)
        except Exception as e:
            return {
                "error": True,
                "message": f"Erro ao enviar relatório: {e}",
                "data": None,
            }

        return {
            "error": False,
            "message": "",
            "data": None,
        }
