#!/usr/bin/env python3

import datetime
import csv
import re
from decimal import Decimal

from beancount.ingest import importer
from beancount.core import data
from beancount.core.amount import Amount


VERSION = '0.1.2'


class CSVImporter(importer.ImporterProtocol):
    ENCODING = 'iso-8859-15'
    CURRENCY = 'EUR'
    ACCOUNTPATTERN = re.compile(r'^NL[0-9]{2}TRIO[0-9]+$')

    FIELDS = ['Boekdatum',
              'Rekeningnummer',
              'Bedrag',
              'Debet/Credit',
              'Naam tegenrekening'
              'Tegenrekening',
              'Code',
              'Omschrijving']

    def __init__(self, account, currency=None, encoding=None, *args, **kwargs):
        self.account = account
        self.currency = currency or CSVImporter.CURRENCY
        self.encoding = encoding or CSVImporter.ENCODING
        super().__init__(*args, **kwargs)

    def name(self):
        return "TriodosImporter.vonshednob.github.com"

    def file_account(self, file_):
        with open(file_.name, 'rt', encoding=self.encoding) as fd:
            reader = csv.reader(fd, delimiter=',', quotechar='"')
            for row in reader:
                return row[1]
            return None

    def identify(self, file_):
        with open(file_.name, 'rt', encoding=self.encoding) as fd:
            try:
                reader = csv.reader(fd, delimiter=',', quotechar='"')
                for row in reader:
                    return CSVImporter.ACCOUNTPATTERN.match(row[1]) is not None
            except:
                return False

        return False

    def extract(self, file_, previous=None):
        transactions = []
        with open(file_.name, 'rt', encoding=self.encoding) as fd:
            reader = csv.reader(fd, delimiter=',', quotechar='"')
            for lineno, row in enumerate(reader):
                meta = data.new_metadata(file_.name, lineno+1)
                date = datetime.datetime.strptime(row[0], "%d-%m-%Y").date()
                account = self.resolve_account(row[1])
                amount = Amount(-1*Decimal(row[2].replace('.', '').replace(',', '.')), self.currency)
                payee = None
                links = set()
                tags = set()
                narration = row[7].lower()
                postings = [
                    data.Posting(account,
                                 amount,
                                 None,  # cost
                                 None,  # price
                                 None,  # flag
                                 None,  # meta
                                 )
                ]
                transaction = data.Transaction(meta,
                                               date,
                                               '*',
                                               payee,
                                               narration.title(),
                                               tags,
                                               links,
                                               postings)
                transactions.append(transaction)
        return transactions

    def resolve_account(self, rawaccount):
        if isinstance(self.account, str):
            return self.account
        elif isinstance(self.account, dict):
            return self.account[rawaccount]
        raise TypeError(self.account)

CONFIG = [
    CSVImporter({'NL00TRIO1234567890': 'Assets:EUR:Account',
                 'NL00TRIO0987654321': 'Assets:EUR:Savings'})
]

