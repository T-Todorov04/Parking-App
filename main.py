# main.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QLabel, QDialog, QSpinBox, QDialogButtonBox
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
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Рег. номер", "Дата на плащане", "Край на плащане"])

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
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(row_data["id"])))
            self.table.setItem(row_position, 1, QTableWidgetItem(row_data["plate"]))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(row_data["date_of_payment"])))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(row_data["end_of_payment"])))

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
            print(f"Обработка на кола: {car['plate']}")

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())