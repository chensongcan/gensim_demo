# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import data
import logger
import processing

if __name__ == "__main__":
    logger.log.info("Model Training start running...")

    data.pg.init()

    processing.init()

    processing.text_process()

    data.pg.close()

    logger.log.info("Model Training finished.")
