import os
import sqlite3

from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox

from db_connection import path, initialize, hash_password


def test_import_browse_and_delete_synthetic_csv(tmp_path, monkeypatch):
    import main

    app = QApplication.instance() or QApplication([])
    monkeypatch.setenv('APP_USER_ID', '1')
    with sqlite3.connect(path) as conn:
        initialize(conn)
        conn.execute('INSERT INTO Users VALUES (1, ?, ?)', ('demo', hash_password('example-only')))
    source = tmp_path / 'expenses.csv'
    source.write_text('category,amount\ntravel,120\nfood,45\n', encoding='utf-8')
    monkeypatch.setattr(QFileDialog, 'getOpenFileName', lambda *a, **k: (str(source), ''))
    monkeypatch.setattr(QMessageBox, 'warning', lambda *a, **k: None)
    window = main.MainApplication()
    try:
        window.table_view.get_all_items()
        window.stats_view.refresh_boxes()
        window.stats_view.update_graph()
        window.csv_view.add_csv()
        window.table_view.combo_box()
        window.table_view.get_all_items()
        assert window.table_view.table.rowCount() == 2
        assert window.table_view.table.horizontalHeaderItem(1).text() == 'category'
        window.table_view.table.selectRow(0)
        window.table_view.delete()
        assert window.table_view.table.rowCount() == 1
        window.csv_view.display_all_files()
        window.csv_view.table.selectRow(0)
        window.csv_view.delete()
        assert window.csv_view.table.item(0, 0).text() == 'no'
    finally:
        window.close()
