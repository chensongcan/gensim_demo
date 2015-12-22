# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import psycopg2.pool
import conf
import logger

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


def init():
    """
    创建PostgreSQL连接
    :return:
    """
    global pgsql_pool, pgsql_conn
    pgsql_pool = psycopg2.pool.SimpleConnectionPool(3, 5, database=conf.pg.settings["database"],
                                                    user=conf.pg.settings["user"],
                                                    password=conf.pg.settings["password"],
                                                    host=conf.pg.settings["host"],
                                                    port=conf.pg.settings["port"],
                                                    connection_factory=psycopg2.extras.RealDictConnection)
    pgsql_conn = pgsql_pool.getconn()
    pgsql_conn.set_client_encoding("UTF8")

    logger.log.info("postgresql is connecting...")


def get_cursor():
    """
    获取PostgreSQL游标
    :return:
    """
    global pgsql_conn
    if pgsql_conn.closed:
        pgsql_conn = pgsql_pool.getconn()
        pgsql_conn.set_client_encoding("UTF8")
    pgsql_cursor = pgsql_conn.cursor()
    return pgsql_cursor


def close():
    """
    释放PostgreSQL连接
    :return:
    """
    global pgsql_pool
    if not pgsql_pool.closed:
        pgsql_pool.closeall()
    pgsql_pool = None

    logger.log.info("postgresql connection closed")


def get_pos():
    """
    读取position信息
    :return:
    """
    pos_col = []
    pos_col.extend(_get_pos("company_position_new"))
    pos_col.extend(_get_pos("company_position"))
    pos_col.extend(_get_pos("company_position_old"))

    logger.log.info("all positions have been read, count: %s." % (len(pos_col),))
    return pos_col


def _get_pos(table_name):
    """
    读取单个表的position信息
    :param table_name:
    :return:
    """
    sql_pos = "SELECT name, category, description FROM %s;" % (table_name,)

    pgsql_cursor = get_cursor()
    pgsql_cursor.execute(sql_pos)
    raw_pos = pgsql_cursor.fetchall()

    logger.log.info("[%s] has been read, count: %s." % (table_name, len(raw_pos),))
    return raw_pos
