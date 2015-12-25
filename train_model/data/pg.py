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


def get_train_pos():
    """
    读取训练用position信息
    :rtype: __generator
    """
    for row in _get_pos("company_position_new"):
        yield row
    for row in _get_pos("company_position", 200000):
        yield row


def get_pos():
    """
    读取company_position_new信息
    :rtype: list
    """
    sql_pos = """SELECT company_position_new.id AS id, company_position_new.name AS name,
                        city.name AS city, position_type.name AS category,
                        company_position_new.company_id AS company_id,
                        company_position_new.education_id AS education_id,
                        company_position_new.description AS description,
                        company_position_new.publish_date AS publish_date,
                        position_permission.school AS school, position_permission.major AS major,
                        position_permission.grade_max AS grade_max, position_permission.sex AS sex
                 FROM company_position_new
                      LEFT JOIN position_permission ON company_position_new.id = position_permission.position_id
                      LEFT JOIN city ON company_position_new.city_id = city.id
                      LEFT JOIN position_type ON company_position_new.category = position_type.id
                 WHERE company_position_new.deleted = 0
                       AND (company_position_new.expire_date > CURRENT_DATE
                       OR company_position_new.expire_date IS NULL);"""

    pgsql_cursor = get_cursor()
    pgsql_cursor.execute(sql_pos)
    raw_pos = pgsql_cursor.fetchall()

    logger.log.info("[info about position] has been read, count: %s." % (len(raw_pos),))
    return raw_pos


def get_school():
    """
    读取school_info表信息
    :rtype: list
    """
    sql = "SELECT name, is_985, is_211, city FROM school_info;"
    pgsql_cursor = get_cursor()
    pgsql_cursor.execute(sql)
    raw = pgsql_cursor.fetchall()

    logger.log.info("[school_info] has been read, count: %d." % (len(raw),))
    return raw
