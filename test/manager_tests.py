import sqlite3
from datetime import datetime, timedelta
from typing import Generator

import pytest

from app.core.manager.manager_report import ReporterInteractor, XReportCommand
from app.core.manager.report_type import ReportType
from app.core.terminal.terminal import TerminalInteractor
from app.infra.persistence.repository import SqlLiteRepository
from app.runner.settings import TEST_DB_LOCATION

test_sqlite_repository = SqlLiteRepository(TEST_DB_LOCATION)
terminal = TerminalInteractor(test_sqlite_repository)
reporter = ReporterInteractor(x_report=XReportCommand(test_sqlite_repository))


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


def test_x_report_with_no_receipts() -> None:
    report = reporter.make_report(datetime.date(datetime.today()), ReportType.X_REPORT)
    assert len(report["items_sold"]) == 0
    assert report["total_receipts"] == 0
    assert report["total_cost"] == 0.0


def test_x_report_with_open_receipt() -> None:
    receipt_id = terminal.open_receipt()
    terminal.add_item_to_receipt(receipt_id, 0, 1)
    report = reporter.make_report(datetime.date(datetime.today()), ReportType.X_REPORT)
    assert len(report["items_sold"]) == 0
    assert report["total_receipts"] == 0
    assert report["total_cost"] == 0.0


def test_x_report_with_closed_receipt() -> None:
    receipt_id = terminal.open_receipt()
    terminal.add_item_to_receipt(receipt_id, 0, 1)
    terminal.close_receipt(receipt_id)
    report = reporter.make_report(datetime.date(datetime.today()), ReportType.X_REPORT)
    assert len(report["items_sold"]) == report["items_sold"][0]["units"] == 1
    assert report["total_receipts"] == 1
    assert report["total_cost"] == 3.99


def test_x_report_with_other_date() -> None:
    receipt_id = terminal.open_receipt()
    terminal.add_item_to_receipt(receipt_id, 0, 1)
    terminal.close_receipt(receipt_id)
    report = reporter.make_report(
        datetime.date(datetime.today() - timedelta(days=1)), ReportType.X_REPORT
    )
    assert len(report["items_sold"]) == 0
    assert report["total_receipts"] == 0
    assert report["total_cost"] == 0.0


def test_x_report_with_multiple_items_receipt() -> None:
    receipt_id = terminal.open_receipt()
    terminal.add_item_to_receipt(receipt_id, 0, 2)
    terminal.add_item_to_receipt(receipt_id, 3, 1)
    terminal.close_receipt(receipt_id)
    report = reporter.make_report(datetime.date(datetime.today()), ReportType.X_REPORT)
    assert len(report["items_sold"]) == 2
    assert sum([item["units"] for item in report["items_sold"].values()]) == 3
    assert report["total_receipts"] == 1
    assert report["total_cost"] == 3.99 * 2 + 1.45


def test_x_report_with_multiple_receipts() -> None:
    first_receipt_id = terminal.open_receipt()
    terminal.add_item_to_receipt(first_receipt_id, 0, 1)
    terminal.add_item_to_receipt(first_receipt_id, 2, 2)
    terminal.close_receipt(first_receipt_id)

    second_receipt_id = terminal.open_receipt()
    terminal.add_item_to_receipt(second_receipt_id, 0, 1)
    terminal.close_receipt(second_receipt_id)

    report = reporter.make_report(datetime.date(datetime.today()), ReportType.X_REPORT)
    assert len(report["items_sold"]) == 2
    assert sum([item["units"] for item in report["items_sold"].values()]) == 4
    assert report["total_receipts"] == 2
    assert report["items_sold"][0]["name"] == "Beer"
    assert report["items_sold"][2]["name"] == "Cheese"
    assert report["total_cost"] == 3.99 * 2 + 2.99 * 2
