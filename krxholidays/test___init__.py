from datetime import datetime
from unittest import TestCase

from krxholidays import add_business_days


class Test(TestCase):
    def test_add_business_days(self):
        print(add_business_days(datetime(2023, 9, 26), 1))
        print(add_business_days(datetime(2023, 9, 27), 1))
        print(add_business_days(datetime(2023, 9, 24), 1))
        print(add_business_days(datetime(2023, 9, 25), 1))
        print(add_business_days(datetime(2023, 9, 22), 1))
        print(add_business_days(datetime(2023, 10, 1), 1))

        print(add_business_days(datetime(2023, 9, 26), 2))
