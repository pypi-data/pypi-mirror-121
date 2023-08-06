from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.transaction import Transaction

from tlru_cache import tlru_cache

from .bank_ml import BankML


class Line(metaclass=PoolMeta):
    __name__ = 'account.statement.line'

    @tlru_cache(lifetime=3600)
    def _get_machine_learning(self, database_name, user,
                              from_date='2019-08-01'):
        """Method cached with the time LRU to return the machine learning"""
        pool = Pool()
        ml = BankML()
        try:
            ml.learn(pool, from_date=from_date)
        except ValueError:
            pass  # no enough data
        finally:
            return ml

    def get_machine_learning(self, **kwargs):
        pool = Pool()
        user = Transaction().user
        return self._get_machine_learning(pool.database_name, user, **kwargs)

    def set_account_and_party_from_ml(self):
        """Fill the party and account from the machine learning prediction"""
        if not self.number:
            return

        pool = Pool()
        ml = self.get_machine_learning()
        account, party = ml.predict(self.number)
        if account:
            self.account = pool.get('account.account')(account)

        if party:
            self.party = pool.get('party.party')(party)

    @fields.depends('number')
    def on_change_number(self):
        self.set_account_and_party_from_ml()
