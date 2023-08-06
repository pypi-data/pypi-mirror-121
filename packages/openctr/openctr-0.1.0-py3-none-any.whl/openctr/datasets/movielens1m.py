import pandas as pd
import numpy as np
import os
from ..features import FeatureEncoder as BaseFeatureEncoder

class FeatureEncoder(BaseFeatureEncoder):
    def bucketize_zipcode(self, df, col_name):
        # divide by 1000 to get large buckets
        return df['zipcode'].map(lambda x: int(float(x.split("-")[0]) / 1000))


