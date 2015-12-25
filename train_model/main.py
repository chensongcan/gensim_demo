# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import data
import logger
import test
import util

if __name__ == "__main__":
    logger.log.info("Model Training start running...")

    data.pg.init()

    util.text_process.init()

    util.text_process.run("tmp/pos_data.txt", data.pg.get_train_pos())

    raw_pos = data.pg.get_pos()

    util.text_process.run("tmp/pos_index.txt", raw_pos)

    data.pg.close()

    dictionary = util.topic_model.build_dictionary(source="tmp/pos_data.txt", path="tmp/pos_data.dict")

    model = util.topic_model.build_lda(dictionary, path="tmp/lda.model")

    index = util.topic_model.build_index(model, dictionary, path="tmp/pos.index")

    data.pg.init()

    test.run(index, model, dictionary, raw_pos)

    data.pg.close()

    logger.log.info("Model Training finished.")
