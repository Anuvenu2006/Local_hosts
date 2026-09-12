import sys

from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


app = QApplication(sys.argv)

window = QLabel("🐿️ CHIP")
window.setFont(QFont("Arial", 40))
window.setAlignment(Qt.AlignCenter)

window.resize(300, 150)
window.setWindowTitle("Squirrel File Thief")

window.show()

sys.exit(app.exec())