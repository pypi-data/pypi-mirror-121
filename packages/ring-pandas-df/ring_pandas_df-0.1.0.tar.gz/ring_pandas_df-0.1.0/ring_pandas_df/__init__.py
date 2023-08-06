"""ring_pandas_df - Add ring key support for pandas DataFrame."""

__version__ = '0.1.0'
__author__ = 'fx-kirin <fx.kirin@gmail.com>'
__all__: list = []

import pandas as pd

from pandas.util import hash_pandas_object


def __ring_key(self):
    return hash_pandas_object(self).sum()


setattr(pd.DataFrame, "__ring_key__", __ring_key)
