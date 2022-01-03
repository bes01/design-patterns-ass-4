import datetime
import sqlite3
from typing import Protocol

from app.core.persistence.models import Receipt, Item


class IPOSRepository(Protocol):

    def create_receipt(self) -> int:
        pass

    def add_item(self, receipt_id: int, item_id: int) -> None:
        pass

    def close_receipt(self, receipt_id: int) -> None:
        pass

    def get_receipt(self, receipt_id: int) -> Receipt:
        pass


class POSRepository:

    def __init__(self, db_file_location: str) -> None:
        self._datasource = sqlite3.connect(db_file_location, check_same_thread=False)

    def create_receipt(self) -> int:
        cursor = self._datasource.cursor()
        cursor.execute("insert into Receipts(open_date) values (?)", [datetime.date.today()])
        self._datasource.commit()
        receipt_id = cursor.lastrowid
        cursor.close()
        return receipt_id

    def add_item(self, receipt_id: int, item_id: int) -> None:
        cursor = self._datasource.cursor()

        if self._receipt_item_exists(receipt_id, item_id):
            cursor.execute("update Receipts_Items set quantity = quantity + 1 "
                           "where receipt_id = ? and item_id = ?", [receipt_id, item_id])
        else:
            cursor.execute("insert into Receipts_Items(receipt_id, item_id) values (?, ?)", [receipt_id, item_id])

        self._datasource.commit()
        cursor.close()

    def _receipt_item_exists(self, receipt_id: int, item_id: int):
        cursor = self._datasource.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM Receipt_Items WHERE receipt_id= ? and item_id = ?);",
                       [receipt_id, item_id])
        receipt_exists = cursor.fetchone()
        cursor.close()
        return receipt_exists

    def close_receipt(self, receipt_id: int) -> None:
        if self._receipt_exists(receipt_id, 0):
            cursor = self._datasource.cursor()
            cursor.execute("update Receipt_Items set closed = 1"
                           "where receipt_id = ?", [receipt_id])
            self._datasource.commit()
            cursor.close()
        else:
            raise Exception("Couldn't find receipt with passed id!")

    def _receipt_exists(self, receipt_id: int, closed: int) -> bool:
        cursor = self._datasource.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM Receipt WHERE _id= ? and closed = ?);", [receipt_id, closed])
        receipt_exists = cursor.fetchone()
        cursor.close()
        return receipt_exists

    def get_receipt(self, receipt_id: int) -> Receipt:
        cursor = self._datasource.cursor()
        cursor.execute("select * from Receipts where _id = ?", [receipt_id])
        receipt_row = cursor.fetchone()
        if receipt_row is None:
            raise Exception("Couldn't find receipt with passed id!")
        cursor.execute(
            "select * from Items where _id in (select ri.item_id from Receipt_Items ri where ri.receipt_id = ?)",
            [receipt_id])
        item_rows = cursor.fetchall()
        items = []
        for item in item_rows:
            items.append(Item(item[0], item[1], item[2], item[3], item[4], item[5]))
        return Receipt(receipt_row[0], bool(receipt_row[1]), receipt_row[2], items)
