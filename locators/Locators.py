class Invoices:
    def __init__(self) -> None:
        self.__rows_invoices = '#tableSandbox tbody tr[role="row"]'

    @property
    def rows_invoices(self):
        return self.__rows_invoices
