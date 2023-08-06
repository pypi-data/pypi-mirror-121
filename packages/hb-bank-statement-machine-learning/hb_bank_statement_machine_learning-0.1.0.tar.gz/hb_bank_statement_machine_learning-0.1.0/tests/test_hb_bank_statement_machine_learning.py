import unittest
from random import choices

from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.modules.company.tests import (
    create_company, set_company, PartyCompanyCheckEraseMixin, CompanyTestMixin)
from trytond.modules.account.tests.tools import create_chart, get_accounts


def create_parties(self):
    pool = Pool()
    Party = pool.get('party.party')
    parties = []
    for x in range(10):
        parties.append(Party.create(name='Party %d' % x))

    return parties


def create_bank(self, company):
    pool = Pool()

    Party = pool.get('party.party')
    Bank = pool.get('bank')
    BankAccount = pool.get('bank.account')
    Sequence = pool.get('ir.sequence')
    SequenceType = pool.get('ir.sequence.type')
    AccountJournal = pool.get('account.journal')
    StatementJournal = pool.get('account.statement.journal')

    accounts = get_accounts(company)
    cash = accounts['cash']

    bank_party = Party.create(name='Bank')
    bank = Bank()
    bank.party = bank_party

    bank_account = BankAccount()
    bank_account.bank = bank
    bank_account.owners.append(Party(company.party.id))
    bank_account.currency = company.currency
    bank_account_number = bank_account.numbers.new()
    bank_account_number.type = 'iban'
    bank_account_number.number = 'ES0600815398730001414452'

    sequence_type, = SequenceType.find([('name', '=', "Account Journal")])
    sequence = Sequence(name='Satement',
        sequence_type=sequence_type,
        company=company,
    )
    account_journal = AccountJournal(name='Statement',
        type='statement',
        sequence=sequence,
    )

    journal = StatementJournal(name='Number',
        journal=account_journal,
        validation='number_of_lines',
        account=cash,
        bank_account=bank_account,
    )
    return journal


def create_base_statement(company, parties, journal):
    pool = Pool()
    Statement = pool.get('account.statement')
    Line = pool.get('account.statement.line')
    accounts = get_accounts().values()

    all_lines = []

    for x in range(10):
        statement = Statement()
        statement.name = 'Test %d' % x
        statement.company = company
        statement.journal = journal
        statement.end_balance = '100.'
        statement.start_balance = '0.'
        statement.number_of_lines = 10
        statement.total_amount = 100
        bank_stmt_lines = []
        for y in range(10):
            line = Line()
            line.number = 'Test %d %d' % (x, y)
            line.amount = '10.'
            line.account = choices(accounts)
            line.party = choices(parties)
            bank_stmt_lines.append(line)

        statement.lines = bank_stmt_lines
        all_lines.extend(bank_stmt_lines)

    return all_lines


class HbBankStatementMachineLearningTestCase(
    PartyCompanyCheckEraseMixin,
    CompanyTestMixin,
    ModuleTestCase
):
    'Test Hb Bank Statement Machine Learning module'
    module = 'hb_bank_statement_machine_learning'

    @with_transaction
    def test_on_change_number(self):
        pool = Pool()
        company = create_company()
        with set_company(company):
            create_chart(company, tax=True)
            parties = create_parties(company)
            journal = create_bank(company)
            all_lines = create_base_statement(company, parties, journal)

            expected_line = choices(all_lines)
            Line = pool.get('account.statement.line')
            line = Line()
            line.number = expected_line.number
            line.set_account_and_party_from_ml()
            self.assertEqual(expected_line.account.id, line.account.id)
            self.assertEqual(expected_line.party.id, line.party.id)


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            HbBankStatementMachineLearningTestCase))
    return suite
