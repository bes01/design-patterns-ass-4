import datetime
import sqlite3
from typing import List

from app.core.models import CountedItem, ItemGroup, Receipt, SingleItem
from app.infra.persistence.persistence_exception import RecordNotFoundException


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
        cursor.execute("SELECT EXISTS(SELECT 1 FROM Receipts WHERE closed = FALSE);")
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
        if self.receipt_exists(receipt_id, False):
            cursor = self._datasource.cursor()
            cursor.execute(
                "update Receipts set closed = TRUE " "where _id = ?", [receipt_id]
            )
            self._datasource.commit()
            cursor.close()
        else:
            raise RecordNotFoundException()

    def receipt_exists(self, receipt_id: int, closed: bool) -> bool:
        cursor = self._datasource.cursor()
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM Receipts WHERE _id= ? and closed = ?);",
            [receipt_id, closed],
        )
        receipt_exists = cursor.fetchone()
        cursor.close()
        return bool(receipt_exists[0])

    def item_exists(self, item_id: int) -> bool:
        cursor = self._datasource.cursor()
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM main.Items WHERE id= ? );",
            [item_id],
        )
        item_exists = cursor.fetchone()
        cursor.close()
        return bool(item_exists[0])

    def get_receipt(self, receipt_id: int) -> Receipt:
        cursor = self._datasource.cursor()
        cursor.execute("select * from Receipts where _id = ?", [receipt_id])
        receipt_row = cursor.fetchone()
        if receipt_row is None:
            raise RecordNotFoundException()
        cursor.execute(
            "select i.name, i.price, ri.quantity, i.id from Items i "
            "join Receipt_items ri on i.id = ri.item_id "
            "where ri.receipt_id = ? and i.type = 'SINGLE'",
            [receipt_id],
        )
        item_rows = cursor.fetchall()
        items = []
        for item in item_rows:
            items.append(
                CountedItem(
                    SingleItem(item[3], item[0], item[1]), item[2], item[1] * item[2]
                )
            )

        cursor.execute(
            "select i.name, i.pack_size, it.name, it.price, ri.quantity, i.id, i.pack_item_id "
            "from Items i "
            "join Receipt_items ri on i.id = ri.item_id "
            "join Items it on it.id = i.pack_item_id "
            "where ri.receipt_id = ? "
            "and i.type = 'PACK'",
            [receipt_id],
        )
        pack_rows = cursor.fetchall()
        for pack in pack_rows:
            items.append(
                CountedItem(
                    ItemGroup(
                        pack[5],
                        pack[0],
                        [SingleItem(pack[6], pack[2], pack[3])] * pack[1],
                    ),
                    pack[4],
                    pack[1] * pack[4] * pack[3],
                )
            )

        return Receipt(receipt_row[0], bool(receipt_row[1]), receipt_row[2], items)

    def get_current_day_receipts(self) -> List[Receipt]:
        cursor = self._datasource.cursor()
        cursor.execute(
            "select _id from Receipts where open_date = ? and closed = TRUE",
            [datetime.date.today()],
        )
        receipt_ids = cursor.fetchall()
        receipts = []
        for receipt_id in receipt_ids:
            receipts.append(self.get_receipt(receipt_id[0]))
        cursor.close()
        return receipts
