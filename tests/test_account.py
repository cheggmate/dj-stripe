"""
.. module:: dj-stripe.tests.test_account
   :synopsis: dj-stripe Account Tests.

.. moduleauthor:: Alex Kavanaugh (@kavdev)

"""

from django.conf import settings
from django.test.testcases import TestCase

from mock import patch

from djstripe.models import Account

from . import FAKE_ACCOUNT


class TestAccount(TestCase):

    @patch("stripe.Account.retrieve")
    def test_get_connected_account_from_token(self, account_retrieve_mock):
        account_retrieve_mock.return_value = FAKE_ACCOUNT

        Account.get_connected_account_from_token("fake_token")

        account_retrieve_mock.assert_called_once_with(api_key="fake_token")

    @patch("stripe.Account.retrieve")
    def test_get_default_account(self, account_retrieve_mock):
        account_retrieve_mock.return_value = FAKE_ACCOUNT

        Account.get_default_account()

        account_retrieve_mock.assert_called_once_with(api_key=settings.STRIPE_SECRET_KEY)

    @patch("stripe.Account.retrieve")
    def test_account_delete_raises_unexpected_exception(self, account_retrieve_mock):
        account_retrieve_mock.side_effect = stripe.InvalidRequestError("Unexpected Exception", "blah")

        with self.assertRaisesMessage(stripe.InvalidRequestError, "Unexpected Exception"):
            self.account.purge()

        account_retrieve_mock.assert_called_once_with(self.account.stripe_id)

    def test_transfer(self):
        self.assertTrue(self.account.can_transfer())

    @patch("stripe.Account.retrieve")
    def test_cannot_transfer(self, acccount_retrieve_fake):
        self.account.delete()
        self.assertFalse(self.account.can_transfer())

    def test_transfer_accepts_only_decimals(self):
        with self.assertRaises(ValueError):
            self.account.transfer(10)