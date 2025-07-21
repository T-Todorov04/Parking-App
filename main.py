# main.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QLabel, QDialog, QSpinBox, QDialogButtonBox, QMessageBox
)
from datetime import datetime, timedelta
from utils.dbConnection import get_connection


class PaymentDialog(QDialog):
    def __init__(self, car_id):
        super().__init__()
        self.setWindowTitle(f"Плащане за кола ID {car_id}")
        self.setMinimumWidth(300)
        self.layout = QVBoxLayout()

        self.days_input = QSpinBox()
        self.days_input.setMinimum(1)
        self.days_input.setMaximum(365)
        self.layout.addWidget(QLabel("Брой дни за плащане:"))
        self.layout.addWidget(self.days_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)


class EditCarDialog(QDialog):
    def __init__(self, car_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Редакция на кола ID {car_data['id']}")
        self.setMinimumWidth(300)
        self.layout = QVBoxLayout()

        self.plate_input = QLineEdit(car_data["plate"])
        self.date_input = QLineEdit(str(car_data["date_of_payment"]) if car_data["date_of_payment"] else "")
        self.end_input = QLineEdit(str(car_data["end_of_payment"]) if car_data["end_of_payment"] else "")

        self.layout.addWidget(QLabel("Рег. номер:"))
        self.layout.addWidget(self.plate_input)

        self.layout.addWidget(QLabel("Дата на плащане (YYYY-MM-DD):"))
        self.layout.addWidget(self.date_input)

        self.layout.addWidget(QLabel("Край на плащане (YYYY-MM-DD):"))
        self.layout.addWidget(self.end_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)

    def get_data(self):
        return {
            "plate": self.plate_input.text().strip(),
            "date_of_payment": self.date_input.text().strip() or None,
            "end_of_payment": self.end_input.text().strip() or None
        }


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Паркинг Система")
        self.resize(1000, 600)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Лява страна
        self.left_layout = QVBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Търси по регистрационен номер...")
        self.search_bar.textChanged.connect(self.filter_table)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Рег. номер", "Дата на плащане", "Край на плащане", "Статус"])
        self.table.setSortingEnabled(True)

        self.left_layout.addWidget(self.search_bar)
        self.left_layout.addWidget(self.table)

        # Дясна страна
        self.right_layout = QVBoxLayout()
        self.edit_button = QPushButton("Обработка")
        self.pay_button = QPushButton("Плащане")

        self.edit_button.clicked.connect(self.edit_car)
        self.pay_button.clicked.connect(self.pay_car)

        self.right_layout.addWidget(QLabel("Действия:"))
        self.right_layout.addWidget(self.edit_button)
        self.right_layout.addWidget(self.pay_button)

        self.add_button = QPushButton("Добави кола")
        self.add_button.clicked.connect(self.add_car)
        self.right_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Изтрий кола")
        self.delete_button.clicked.connect(self.delete_car)
        self.right_layout.addWidget(self.delete_button)

        self.right_layout.addStretch()

        self.layout.addLayout(self.left_layout, 3)
        self.layout.addLayout(self.right_layout, 1)

        self.load_data()

    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                id,
                license_plate AS plate,
                time_of_payment AS date_of_payment,
                end_of_payment
            FROM cars
        """)
        self.data = cursor.fetchall()
        cursor.close()
        conn.close()
        self.refresh_table(self.data)

    def refresh_table(self, data):
        self.table.setRowCount(0)
        for row_data in data:
            status = "Платено" if row_data["date_of_payment"] else "Не са платили"
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(row_data["id"])))
            self.table.setItem(row_position, 1, QTableWidgetItem(row_data["plate"]))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(row_data["date_of_payment"])))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(row_data["end_of_payment"])))
            self.table.setItem(row_position, 4, QTableWidgetItem(status))

    def filter_table(self):
        text = self.search_bar.text().lower()
        filtered = [car for car in self.data if text in car["plate"].lower()]
        self.refresh_table(filtered)

    def get_selected_car(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        car_id = int(self.table.item(row, 0).text())
        for car in self.data:
            if car["id"] == car_id:
                return car
        return None

    def edit_car(self):
        car = self.get_selected_car()
        if car:
            dialog = EditCarDialog(car, self)
            if dialog.exec():
                updated = dialog.get_data()
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE cars SET license_plate = %s, time_of_payment = %s, end_of_payment = %s WHERE id = %s",
                    (updated["plate"], updated["date_of_payment"], updated["end_of_payment"], car["id"])
                )
                conn.commit()
                cursor.close()
                conn.close()
                self.load_data()

    def pay_car(self):
        car = self.get_selected_car()
        if car:
            dialog = PaymentDialog(car["id"])
            if dialog.exec():
                days = dialog.days_input.value()
                conn = get_connection()
                cursor = conn.cursor()
                now = datetime.now().strftime("%Y-%m-%d")
                end = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                cursor.execute(
                    "UPDATE cars SET time_of_payment = %s, end_of_payment = %s WHERE id = %s",
                    (now, end, car["id"])
                )
                conn.commit()
                cursor.close()
                conn.close()
                self.load_data()

    def add_car(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавяне на нова кола")
        dialog.setMinimumWidth(300)
        layout = QVBoxLayout()

        license_input = QLineEdit()
        layout.addWidget(QLabel("Регистрационен номер:"))
        layout.addWidget(license_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)
        dialog.setLayout(layout)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec():
            plate = license_input.text().strip()
            if plate:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO cars (license_plate, time_of_payment, end_of_payment) VALUES (%s, NULL, NULL)",
                    (plate,)
                )
                conn.commit()
                cursor.close()
                conn.close()
                self.load_data()

    def delete_car(self):
        car = self.get_selected_car()
        if car:
            reply = QMessageBox.question(
                self,
                "Потвърждение за изтриване",
                f"Сигурен ли си, че искаш да изтриеш кола с номер {car['plate']}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cars WHERE id = %s", (car["id"],))
                conn.commit()
                cursor.close()
                conn.close()
                self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())