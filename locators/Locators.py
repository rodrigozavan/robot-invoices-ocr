class Invoices:
    def __init__(self) -> None:
        self.__rows_invoices = '#tableSandbox tbody tr[role="row"]'
        self.__btn_next_page = '#tableSandbox_next'
        self.__btn_paginate = 'div span .paginate_button'

    @property
    def rows_invoices(self):
        return self.__rows_invoices

    @property
    def btn_next_page(self):
        return self.__btn_next_page

    @property
    def btn_paginate(self):
        return self.__btn_paginate
