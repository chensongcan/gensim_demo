# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import conf
import data
import logger
import preprocess


if __name__ == "__main__":
    logger.log.info("Model Training is running...")

    conf.jieba.init()

    data.pg.init()

    raw_pos = data.pg.get_pos()

    data.pg.close()

    raw_pos = preprocess.pos_process(raw_pos)

    preprocess.text_process(raw_pos)

    logger.log.info("Model Training finished.")
