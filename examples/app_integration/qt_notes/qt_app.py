from __future__ import annotations

import os
import sys
from threading import Thread

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from examples.app_integration.qt_notes.api import build_server
from examples.app_integration.qt_notes.domain import NoteStore


class UiBridge(QObject):
    changed = Signal()
    focus_requested = Signal(int)


class NoteWindow(QWidget):
    def __init__(self, store: NoteStore) -> None:
        super().__init__()
        self.store = store
        self.setWindowTitle("Course Qt Notes")
        self.resize(680, 420)

        self.notes = QListWidget()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Note title")
        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Note body")
        add_button = QPushButton("Add note")
        add_button.clicked.connect(self.add_note)

        form = QVBoxLayout()
        form.addWidget(QLabel("Create a note locally"))
        form.addWidget(self.title_input)
        form.addWidget(self.body_input)
        form.addWidget(add_button)

        layout = QHBoxLayout(self)
        layout.addWidget(self.notes, 1)
        layout.addLayout(form, 2)
        self.refresh()

    def add_note(self) -> None:
        try:
            self.store.create(self.title_input.text(), self.body_input.toPlainText())
        except ValueError as exc:
            self.setWindowTitle(f"Course Qt Notes — {exc}")
            return
        self.title_input.clear()
        self.body_input.clear()
        self.refresh()

    def refresh(self) -> None:
        self.notes.clear()
        for note in self.store.list():
            self.notes.addItem(f"{note['id']}: {note['title']}")
            self.notes.item(self.notes.count() - 1).setData(
                Qt.ItemDataRole.UserRole, note["id"]
            )

    def focus_note(self, note_id: int) -> None:
        for index in range(self.notes.count()):
            item = self.notes.item(index)
            if item.data(Qt.ItemDataRole.UserRole) == note_id:
                self.notes.setCurrentItem(item)
                break
        self.showNormal()
        self.raise_()
        self.activateWindow()


def main() -> int:
    token = os.environ.get("COURSE_APP_TOKEN", "")
    if not token:
        raise SystemExit("Set COURSE_APP_TOKEN before starting the Qt application.")
    host = "127.0.0.1"
    port = int(os.environ.get("COURSE_QT_PORT", "8767"))

    app = QApplication(sys.argv)
    store = NoteStore()
    bridge = UiBridge()
    window = NoteWindow(store)
    bridge.changed.connect(window.refresh)
    bridge.focus_requested.connect(window.focus_note)

    server = build_server(
        host,
        port,
        token,
        store,
        on_changed=bridge.changed.emit,
        on_focus=bridge.focus_requested.emit,
    )
    server_thread = Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    def stop_server() -> None:
        server.shutdown()
        server.server_close()

    app.aboutToQuit.connect(stop_server)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
