import sqlite3
from typing import Generator

import pytest
from fastapi import HTTPException

from app.core.terminal.terminal import TerminalInteractor
from app.infra.persistence.repository import SqlLiteRepository
from app.runner.settings import TEST_DB_LOCATION

test_sqlite_repository = SqlLiteRepository(TEST_DB_LOCATION)
terminal = TerminalInteractor(test_sqlite_repository)


def clean_up_test_db() -> None:
    con = sqlite3.connect(TEST_DB_LOCATION)
    cursor = con.cursor()
    cursor.execute("delete from Receipts")
    cursor.execute("delete from main.Receipt_items")
    con.commit()
    con.close()


@pytest.fixture(autouse=True)
def clean_up() -> Generator[None, None, None]:
    clean_up_test_db()
    yield


#  cashier can't have two open receipts
def test_two_open_receipt() -> None:
    try:
        terminal.open_receipt()
        terminal.open_receipt()
        pytest.fail()
    except HTTPException:
        pass


# all receipt ids must be unique
def test_close_receipt() -> None:
    first_receipt_id = terminal.open_receipt()
    terminal.close_receipt(first_receipt_id)
    second_receipt_id = terminal.open_receipt()
    assert first_receipt_id != second_receipt_id


def test_add_item_to_closed_receipt() -> None:
    try:
        receipt_id = terminal.open_receipt()
        terminal.close_receipt(receipt_id)
        terminal.add_item_to_receipt(receipt_id, 0, 1)
        pytest.fail()
    except HTTPException:
        pass


def test_add_item_with_zero_quantity() -> None:
    try:
        receipt_id = terminal.open_receipt()
        terminal.close_receipt(receipt_id)
        terminal.add_item_to_receipt(receipt_id, 0, 0)
        pytest.fail()
    except HTTPException:
        pass


def test_add_item_with_negative_quantity() -> None:
    try:
        receipt_id = terminal.open_receipt()
        terminal.close_receipt(receipt_id)
        terminal.add_item_to_receipt(receipt_id, 0, -1)
        pytest.fail()
    except HTTPException:
        pass


def test_add_item_with_unknown_id() -> None:
    try:
        receipt_id = terminal.open_receipt()
        terminal.add_item_to_receipt(receipt_id, -1, 1)
        pytest.fail()
    except HTTPException:
        pass


def test_single_add_item_and_get_receipt() -> None:
    receipt_id = terminal.open_receipt()
    terminal.add_item_to_receipt(receipt_id, 0, 1)
    receipt, total_cost = terminal.get_receipt(receipt_id)
    assert receipt.id == receipt_id
    assert len(receipt.items) == 1 == receipt.items[0].count
    assert (
        total_cost
        == 3.99
        == receipt.items[0].sum_price
        == receipt.items[0].item.get_price()
    )
    assert receipt.items[0].item.get_name() == "Beer"


def test_triple_quantity_add_item_and_get_receipt() -> None:
    receipt_id = terminal.open_receipt()
    terminal.add_item_to_receipt(receipt_id, 0, 3)
    receipt, total_cost = terminal.get_receipt(receipt_id)
    assert receipt.id == receipt_id
    assert 3 == receipt.items[0].count
    assert (
        total_cost
        == 3.99 * 3
        == receipt.items[0].sum_price
        == receipt.items[0].item.get_price() * 3
    )
    assert receipt.items[0].item.get_name() == "Beer"


def test_add_same_item_twice_item_and_get_receipt() -> None:
    receipt_id = terminal.open_receipt()
    terminal.add_item_to_receipt(receipt_id, 0, 1)
    terminal.add_item_to_receipt(receipt_id, 0, 1)
    receipt, total_cost = terminal.get_receipt(receipt_id)
    assert receipt.id == receipt_id
    assert 2 == receipt.items[0].count
    assert (
        total_cost
        == 3.99 * 2
        == receipt.items[0].sum_price
        == receipt.items[0].item.get_price() * 2
    )
    assert receipt.items[0].item.get_name() == "Beer"


def test_add_different_items_and_get_receipt() -> None:
    receipt_id = terminal.open_receipt()
    terminal.add_item_to_receipt(receipt_id, 0, 1)
    terminal.add_item_to_receipt(receipt_id, 2, 2)
    receipt, total_cost = terminal.get_receipt(receipt_id)
    assert receipt.id == receipt_id
    assert 2 == len(receipt.items)
    assert 3 == sum([item.count for item in receipt.items])
    assert (
        total_cost == 3.99 + 2 * 2.99 == sum([item.sum_price for item in receipt.items])
    )
