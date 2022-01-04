import datetime
import sqlite3
from typing import List, Protocol

from app.core.persistence.models import Item, Receipt


class IPOSRepository(Protocol):
    def create_receipt(self) -> int:
        pass

    def open_receipt_exists(self) -> bool:
        pass

    def add_item(self, receipt_id: int, item_id: int, quantity: int) -> None:
        pass

    def close_receipt(self, receipt_id: int) -> None:
        pass

    def get_receipt(self, receipt_id: int) -> Receipt:
        pass


class IReportRepository(Protocol):
    def get_current_day_receipts(self) -> List[Receipt]:
        pass


class SqlLiteRepository:
    def __init__(self, db_file_location: str) -> None:
        self._datasource = sqlite3.connect(db_file_location, check_same_thread=False)

    def create_receipt(self) -> int:
        cursor = self._datasource.cursor()
        cursor.execute(
            "insert into Receipts(open_date) values (?)", [datetime.date.today()]
        )
        self._datasource.commit()
        receipt_id = cursor.lastrowid
        cursor.close()
        return int(receipt_id)

    def open_receipt_exists(self) -> bool:
        cursor = self._datasource.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM Receipts WHERE closed = 0);")
        receipt_exists = cursor.fetchone()
        cursor.close()
        return bool(receipt_exists[0])

    def add_item(self, receipt_id: int, item_id: int, quantity: int) -> None:
        cursor = self._datasource.cursor()

        if self._receipt_item_exists(receipt_id, item_id):
            cursor.execute(
                "update Receipt_Items set quantity = quantity + ? "
                "where receipt_id = ? and item_id = ?",
                [quantity, receipt_id, item_id],
            )
        else:
            cursor.execute(
                "insert into Receipt_Items(receipt_id, item_id, quantity) values (?, ?, ?)",
                [receipt_id, item_id, quantity],
            )

        self._datasource.commit()
        cursor.close()

    def _receipt_item_exists(self, receipt_id: int, item_id: int) -> bool:
        cursor = self._datasource.cursor()
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM Receipt_Items WHERE receipt_id= ? and item_id = ?);",
            [receipt_id, item_id],
        )
        receipt_exists = cursor.fetchone()
        cursor.close()
        return bool(receipt_exists[0])

    def close_receipt(self, receipt_id: int) -> None:
        if self._receipt_exists(receipt_id, 0):
            cursor = self._datasource.cursor()
            cursor.execute(
                "update Receipts set closed = 1 " "where _id = ?", [receipt_id]
            )
            self._datasource.commit()
            cursor.close()
        else:
            raise Exception("Couldn't find receipt with passed id!")

    def _receipt_exists(self, receipt_id: int, closed: int) -> bool:
        cursor = self._datasource.cursor()
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM Receipts WHERE _id= ? and closed = ?);",
            [receipt_id, closed],
        )
        receipt_exists = cursor.fetchone()
        cursor.close()
        return bool(receipt_exists[0])

    def get_receipt(self, receipt_id: int) -> Receipt:
        cursor = self._datasource.cursor()
        cursor.execute("select * from Receipts where _id = ?", [receipt_id])
        receipt_row = cursor.fetchone()
        if receipt_row is None:
            raise Exception("Couldn't find receipt with passed id!")
        cursor.execute(
            "select i.*, ri.quantity from Items i join Receipt_items ri on i.id = ri.item_id where ri.receipt_id = ?",
            [receipt_id],
        )
        item_rows = cursor.fetchall()
        items = []
        for item in item_rows:
            items.append(Item(item[0], item[1], item[2], item[3], item[4]))
        return Receipt(receipt_row[0], bool(receipt_row[1]), receipt_row[2], items)

    def get_current_day_receipts(self) -> List[Receipt]:
        cursor = self._datasource.cursor()
        cursor.execute(
            "select _id from Receipts where open_date = ? and closed = 1",
            [datetime.date.today()],
        )
        receipt_ids = cursor.fetchall()
        receipts = []
        for receipt_id in receipt_ids:
            receipts.append(self.get_receipt(receipt_id[0]))
        cursor.close()
        return receipts
