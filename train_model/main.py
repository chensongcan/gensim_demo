# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import data
import logger
import util

if __name__ == "__main__":
    logger.log.info("Model Training start running...")

    data.pg.init()

    util.text_process.init()

    util.text_process.run("tmp/pos_data.txt", data.pg.get_train_pos())

    util.text_process.run("tmp/pos_index.txt", data.pg.get_pos())

    data.pg.close()

    dictionary = util.topic_model.build_dictionary(data="tmp/pos_data.txt", path="tmp/pos_data.dict")

    model = util.topic_model.build_lda(dictionary)

    index = util.topic_model.build_index(model, dictionary)

    logger.log.info("Model Training finished.")
