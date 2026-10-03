"""MySQL (XAMPP) layer - small on purpose.
business -> read only (rules & policy, edit it in phpMyAdmin)
products -> read / add / update
Works with ANY column names: it reads the table structure from MySQL itself."""
import os

import pymysql
from dotenv import load_dotenv

load_dotenv()


def _run(sql, args=()):
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"), port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"), password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "businessai"),
        cursorclass=pymysql.cursors.DictCursor, autocommit=True)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            return list(cur.fetchall())
    finally:
        conn.close()


def columns(table):
    return _run(f"DESCRIBE `{table}`")          # Field, Type, Key, Extra ...


def get_business():
    return _run("SELECT * FROM `business`")


def get_products():
    return _run("SELECT * FROM `products`")


def add_product(data: dict):
    valid = {c["Field"] for c in columns("products")}
    data = {k: v for k, v in data.items() if k in valid}
    cols = ", ".join(f"`{k}`" for k in data)
    marks = ", ".join(["%s"] * len(data))
    _run(f"INSERT INTO `products` ({cols}) VALUES ({marks})", tuple(data.values()))


def update_product(pk_col, pk_val, data: dict):
    valid = {c["Field"] for c in columns("products")} - {pk_col}
    data = {k: v for k, v in data.items() if k in valid}
    sets = ", ".join(f"`{k}`=%s" for k in data)
    _run(f"UPDATE `products` SET {sets} WHERE `{pk_col}`=%s", (*data.values(), pk_val))


def primary_key(table="products"):
    for c in columns(table):
        if c["Key"] == "PRI":
            return c["Field"]
    return columns(table)[0]["Field"]


def _rows_to_text(rows):
    return "\n".join("- " + " | ".join(f"{k}: {v}" for k, v in r.items() if v not in (None, ""))
                     for r in rows) or "(none)"


def llm_context():
    """Text snapshot (business rules/policy + all products) that is sent to the LLM."""
    return ("BUSINESS DETAILS, RULES AND POLICY:\n" + _rows_to_text(get_business())
            + "\n\nPRODUCTS:\n" + _rows_to_text(get_products()))