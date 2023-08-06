try:
    from trytond.modules.hb_bank_statement_machine_learning.tests.test_hb_bank_statement_machine_learning import suite  # noqa: E501
except ImportError:
    from .test_hb_bank_statement_machine_learning import suite

__all__ = ['suite']
