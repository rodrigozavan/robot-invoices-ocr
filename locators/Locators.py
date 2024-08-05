class Invoices:
    def __init__(self) -> None:
        self.__rows_invoices = '#tableSandbox tbody tr[role="row"]'
        self.__btn_start_challange = '#start'
        self.__btn_paginate = 'div span .paginate_button'
        self.__input_submit_reports = 'input[name="csv"]'

    @property
    def rows_invoices(self):
        return self.__rows_invoices

    @property
    def btn_start_challange(self):
        return self.__btn_start_challange

    @property
    def btn_paginate(self):
        return self.__btn_paginate

    @property
    def input_submit_reports(self):
        return self.__input_submit_reports
