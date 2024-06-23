import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVOICES_DIR = os.path.join(BASE_DIR, 'src', 'invoices')
REPORTS_DIR = os.path.join(BASE_DIR, 'src', 'reports')
DATA_INVOICES_DIR = os.path.join(BASE_DIR, 'src', 'data')

if not os.path.exists(INVOICES_DIR):
    os.makedirs(INVOICES_DIR)

if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

if not os.path.exists(DATA_INVOICES_DIR):
    os.makedirs(DATA_INVOICES_DIR)

logging.basicConfig(
    format='%(asctime)s [%(module)s] %(levelname)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.INFO
)
