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
    :rtype: NoneType
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
    :rtype: extensions.cursor
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
    :rtype: NoneType
    """
    global pgsql_pool
    if not pgsql_pool.closed:
        pgsql_pool.closeall()
    pgsql_pool = None

    logger.log.info("postgresql connection closed")


def get_pos():
    """
    读取position信息
    :rtype: __generator
    """
    for row in _get_pos("company_position_new"):
        yield row
    for row in _get_pos("company_position", 50000):
        yield row
    # for row in _get_pos("company_position_old"):
    #     yield row
    pass


def _get_pos(table_name, limit=None):
    """
    读取单个表的position信息
    :type table_name: str or unicode
    :type limit: int or NoneType
    :rtype: __generator
    """
    if limit:
        sql_pos = "SELECT name, category, description FROM %s ORDER BY publish_date DESC LIMIT %s;" % (
            table_name, limit)
    else:
        sql_pos = "SELECT name, category, description FROM %s;" % (table_name,)

    pgsql_cursor = get_cursor()
    pgsql_cursor.execute(sql_pos)
    for row in pgsql_cursor:
        yield row

    logger.log.info("[%s] has been read, count: %s." % (table_name, pgsql_cursor.rowcount,))
