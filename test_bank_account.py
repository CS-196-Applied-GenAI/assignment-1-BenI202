import contextlib
import io
import importlib.util
import runpy
import sys
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

BANK_FILE = PROJECT_DIR / "test-last.py"
spec = importlib.util.spec_from_file_location("test_last_bank", BANK_FILE)
test_last_bank = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = test_last_bank
spec.loader.exec_module(test_last_bank)

BankAccount = test_last_bank.BankAccount
InsufficientFundsError = test_last_bank.InsufficientFundsError


class TestBankAccount(unittest.TestCase):
    def test_constructor_stores_trimmed_owner_and_float_balance(self):
        account = BankAccount("  Alice  ", 25)

        self.assertEqual(account.owner, "Alice")
        self.assertEqual(account.balance, 25.0)
        self.assertEqual(account.get_transaction_count(), 0)
        self.assertEqual(account.get_history(), [])

    def test_constructor_rejects_blank_owner(self):
        for owner in ("", "   "):
            with self.subTest(owner=repr(owner)):
                with self.assertRaisesRegex(ValueError, "Owner name cannot be empty"):
                    BankAccount(owner)

    def test_constructor_rejects_negative_initial_balance(self):
        with self.assertRaisesRegex(ValueError, "Initial balance cannot be negative"):
            BankAccount("Alice", -0.01)

    def test_deposit_adds_money_and_records_transaction(self):
        account = BankAccount("Alice", 100)

        new_balance = account.deposit(50.25)

        self.assertEqual(new_balance, 150.25)
        self.assertEqual(account.balance, 150.25)
        self.assertEqual(account.get_transaction_count(), 1)
        self.assertEqual(account.get_history(), ["deposit  +50.25  -> 150.25"])

    def test_deposit_rejects_zero_and_negative_amounts(self):
        account = BankAccount("Alice", 100)

        for amount in (0, -10):
            with self.subTest(amount=amount):
                with self.assertRaisesRegex(ValueError, "Deposit amount must be positive"):
                    account.deposit(amount)

        self.assertEqual(account.balance, 100)
        self.assertEqual(account.get_history(), [])

    def test_withdraw_removes_money_and_records_transaction(self):
        account = BankAccount("Alice", 100)

        new_balance = account.withdraw(35.5)

        self.assertEqual(new_balance, 64.5)
        self.assertEqual(account.balance, 64.5)
        self.assertEqual(account.get_history(), ["withdraw -35.50  -> 64.50"])

    def test_withdraw_allows_balance_to_reach_zero(self):
        account = BankAccount("Alice", 100)

        self.assertEqual(account.withdraw(100), 0)
        self.assertEqual(account.balance, 0)
        self.assertEqual(account.get_history(), ["withdraw -100.00  -> 0.00"])

    def test_withdraw_rejects_zero_and_negative_amounts(self):
        account = BankAccount("Alice", 100)

        for amount in (0, -1):
            with self.subTest(amount=amount):
                with self.assertRaisesRegex(ValueError, "Withdrawal amount must be positive"):
                    account.withdraw(amount)

        self.assertEqual(account.balance, 100)
        self.assertEqual(account.get_history(), [])

    def test_withdraw_rejects_amounts_above_balance(self):
        account = BankAccount("Alice", 20)

        with self.assertRaisesRegex(InsufficientFundsError, "current balance is only 20.00"):
            account.withdraw(20.01)

        self.assertEqual(account.balance, 20)
        self.assertEqual(account.get_history(), [])

    def test_transfer_moves_money_between_different_accounts(self):
        alice = BankAccount("Alice", 500)
        bob = BankAccount("Bob", 25)

        result = alice.transfer(200, bob)

        self.assertIsNone(result)
        self.assertEqual(alice.balance, 300)
        self.assertEqual(bob.balance, 225)
        self.assertEqual(
            alice.get_history(),
            ["withdraw -200.00  -> 300.00", "transfer -200.00 to Bob"],
        )
        self.assertEqual(bob.get_history(), ["deposit  +200.00  -> 225.00"])

    def test_transfer_rejects_same_account(self):
        account = BankAccount("Alice", 100)

        with self.assertRaisesRegex(ValueError, "Cannot transfer money to the same account"):
            account.transfer(10, account)

        self.assertEqual(account.balance, 100)
        self.assertEqual(account.get_history(), [])

    def test_transfer_reuses_withdraw_validation_for_invalid_amounts(self):
        source = BankAccount("Alice", 100)
        target = BankAccount("Bob", 25)

        with self.assertRaisesRegex(ValueError, "Withdrawal amount must be positive"):
            source.transfer(0, target)

        self.assertEqual(source.balance, 100)
        self.assertEqual(target.balance, 25)
        self.assertEqual(source.get_history(), [])
        self.assertEqual(target.get_history(), [])

    def test_transfer_rejects_insufficient_funds_without_depositing_to_target(self):
        source = BankAccount("Alice", 10)
        target = BankAccount("Bob", 25)

        with self.assertRaisesRegex(InsufficientFundsError, "Cannot withdraw 10.01"):
            source.transfer(10.01, target)

        self.assertEqual(source.balance, 10)
        self.assertEqual(target.balance, 25)
        self.assertEqual(source.get_history(), [])
        self.assertEqual(target.get_history(), [])

    def test_get_history_returns_a_copy(self):
        account = BankAccount("Alice", 100)
        account.deposit(50)

        history = account.get_history()
        history.append("fake transaction")

        self.assertEqual(account.get_history(), ["deposit  +50.00  -> 150.00"])

    def test_repr_includes_owner_and_two_decimal_balance(self):
        account = BankAccount("Alice", 12.5)

        self.assertEqual(repr(account), "BankAccount(owner='Alice', balance=12.50)")

    def test_manual_smoke_test_runs_when_module_is_executed_directly(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            runpy.run_path(str(BANK_FILE), run_name="__main__")

        printed = output.getvalue()
        self.assertIn("BankAccount(owner='Alice', balance=450.00)", printed)
        self.assertIn("BankAccount(owner='Bob', balance=200.00)", printed)
        self.assertIn("Alice's history:", printed)
        self.assertIn("Bob's history:", printed)


if __name__ == "__main__":
    unittest.main()
