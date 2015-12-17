# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
import logging
import sklearn.datasets

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

dataset = sklearn.datasets.fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
data = dataset.data

print data[0]
