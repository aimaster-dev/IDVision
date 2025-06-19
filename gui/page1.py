# gui/page1_idcard.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QLineEdit, QFormLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from idanalyzer_api import IDAnalyzerClient

class IDCardPhoto(QWidget):
    def __init__(self, main_window, api_key):
        super().__init__()
        self.main_window = main_window
        self.api_client = IDAnalyzerClient(api_key)
        self.front_img_path = None
        self.back_img_path = None
        self.fields = {}

        self.layout = QVBoxLayout()

        # --- Image preview section ---
        img_layout = QHBoxLayout()
        self.front_image_label = QLabel("No front image")
        self.front_image_label.setFixedSize(300, 200)
        img_layout.addWidget(self.front_image_label)

        self.back_image_label = QLabel("No back image")
        self.back_image_label.setFixedSize(300, 200)
        img_layout.addWidget(self.back_image_label)

        self.layout.addLayout(img_layout)

        # --- Image selection buttons ---
        btn_layout = QHBoxLayout()
        self.select_front_button = QPushButton("Select ID Front")
        self.select_front_button.clicked.connect(self.select_front_image)
        btn_layout.addWidget(self.select_front_button)

        self.select_back_button = QPushButton("Select ID Back")
        self.select_back_button.clicked.connect(self.select_back_image)
        btn_layout.addWidget(self.select_back_button)
        self.layout.addLayout(btn_layout)

        # --- "Verify" and "Next" buttons ---
        verify_next_layout = QHBoxLayout()
        self.verify_button = QPushButton("Verify ID")
        self.verify_button.clicked.connect(self.on_verify)
        self.verify_button.setEnabled(False)
        verify_next_layout.addWidget(self.verify_button)

        self.next_button = QPushButton("Next (Face Verification)")
        self.next_button.clicked.connect(self.on_next)
        self.next_button.setEnabled(False)
        verify_next_layout.addWidget(self.next_button)

        self.layout.addLayout(verify_next_layout)

        # --- Display extracted fields ---
        self.fields_form = QFormLayout()
        self.name_field = QLineEdit(); self.name_field.setReadOnly(True)
        self.dob_field = QLineEdit(); self.dob_field.setReadOnly(True)
        self.idnum_field = QLineEdit(); self.idnum_field.setReadOnly(True)
        self.expiry_field = QLineEdit(); self.expiry_field.setReadOnly(True)
        self.address_field = QLineEdit(); self.address_field.setReadOnly(True)
        self.fields_form.addRow("Name:", self.name_field)
        self.fields_form.addRow("DOB:", self.dob_field)
        self.fields_form.addRow("ID Number:", self.idnum_field)
        self.fields_form.addRow("Expiry:", self.expiry_field)
        self.fields_form.addRow("Address:", self.address_field)
        self.layout.addLayout(self.fields_form)

        # --- Status labels ---
        self.match_status_label = QLabel("")
        self.verification_status_label = QLabel("")
        self.layout.addWidget(self.match_status_label)
        self.layout.addWidget(self.verification_status_label)

        self.setLayout(self.layout)

    def select_front_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Select ID Front Image", "", "Images (*.jpg *.jpeg *.png)")
        if not fname:
            return
        self.front_img_path = fname
        self.front_image_label.setPixmap(QPixmap(fname).scaled(300, 200))
        self.front_image_label.setText("")
        self.update_verify_button_status()

    def select_back_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Select ID Back Image", "", "Images (*.jpg *.jpeg *.png)")
        if not fname:
            return
        self.back_img_path = fname
        self.back_image_label.setPixmap(QPixmap(fname).scaled(300, 200))
        self.back_image_label.setText("")
        self.update_verify_button_status()

    def update_verify_button_status(self):
        self.verify_button.setEnabled(bool(self.front_img_path and self.back_img_path))

    def on_verify(self):
        self.extract_fields()

    def extract_fields(self):
        try:
            fields = self.api_client.scan_id(self.front_img_path, self.back_img_path)
            self.fields = fields
            print("DEBUG IDAnalyzer response:", fields)
            self.name_field.setText(fields.get("name", ""))
            self.dob_field.setText(fields.get("dob", ""))
            self.idnum_field.setText(fields.get("id_number", ""))
            self.expiry_field.setText(fields.get("expiry", ""))
            self.address_field.setText(fields.get("address", ""))
            # Statuses: front/back match and verification
            raw = fields.get("raw", {})
            verification = raw.get("verification", {})
            dualside_match = verification.get("dualside", None)
            passed = verification.get("passed", False)
            # Set front/back match status
            if dualside_match is not None:
                if dualside_match is True:
                    self.match_status_label.setText("Front/Back Match: ✅")
                else:
                    self.match_status_label.setText("Front/Back Match: ❌")
            else:
                self.match_status_label.setText("Front/Back Match: N/A")
            # Set verification status
            if passed:
                self.verification_status_label.setText("ID Verification: ✅")
                self.next_button.setEnabled(True)
            else:
                self.verification_status_label.setText("ID Verification: ❌")
                self.next_button.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "ID Extraction Failed", str(e))
            self.next_button.setEnabled(False)
            self.match_status_label.setText("")
            self.verification_status_label.setText("")

    def on_next(self):
        self.main_window.switch_page(1)

    def clear_window(self):
        self.front_image_label.setText("No front image")
        self.front_image_label.setPixmap(QPixmap())
        self.back_image_label.setText("No back image")
        self.back_image_label.setPixmap(QPixmap())
        self.name_field.clear()
        self.dob_field.clear()
        self.idnum_field.clear()
        self.expiry_field.clear()
        self.address_field.clear()
        self.verify_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.front_img_path = None
        self.back_img_path = None
        self.fields = {}
        self.match_status_label.setText("")
        self.verification_status_label.setText("")
