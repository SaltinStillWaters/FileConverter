import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog
)
from PyQt5.QtGui import QFont
from converter import *


class FileConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Converter")
        self.setGeometry(200, 200, 600, 400)

        # Main layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        # Set font for labels and buttons
        label_font = QFont("Arial", 16)  # Change font size to 16
        button_font = QFont("Arial", 14)  # Change font size to 14

        # PDF/Image conversion section
        pdf_label = QLabel("PDF/Image Conversions", self)
        pdf_label.setFont(label_font)
        self.layout.addWidget(pdf_label)

        pdf_to_images_btn = QPushButton("PDF to Images", self)
        pdf_to_images_btn.setFont(button_font)
        pdf_to_images_btn.setMinimumHeight(40)  # Set button height
        pdf_to_images_btn.clicked.connect(self.handle_pdf_to_images)
        self.layout.addWidget(pdf_to_images_btn)

        images_to_pdf_btn = QPushButton("Images to PDF", self)
        images_to_pdf_btn.setFont(button_font)
        images_to_pdf_btn.setMinimumHeight(40)
        images_to_pdf_btn.clicked.connect(self.handle_images_to_pdf)
        self.layout.addWidget(images_to_pdf_btn)

        # YouTube Downloader section
        yt_label = QLabel("YouTube Downloader", self)
        yt_label.setFont(label_font)
        self.layout.addWidget(yt_label)

        yt_url_label = QLabel("YouTube URL:", self)
        yt_url_label.setFont(label_font)
        self.layout.addWidget(yt_url_label)

        self.yt_url_entry = QLineEdit(self)
        self.yt_url_entry.setFont(button_font)
        self.yt_url_entry.setMinimumHeight(30)
        self.layout.addWidget(self.yt_url_entry)

        download_mp4_btn = QPushButton("Download as MP4", self)
        download_mp4_btn.setFont(button_font)
        download_mp4_btn.setMinimumHeight(40)
        download_mp4_btn.clicked.connect(self.handle_download_mp4)
        self.layout.addWidget(download_mp4_btn)

        download_m4a_btn = QPushButton("Download as M4A", self)
        download_m4a_btn.setFont(button_font)
        download_m4a_btn.setMinimumHeight(40)
        download_m4a_btn.clicked.connect(self.handle_download_m4a)
        self.layout.addWidget(download_m4a_btn)

        self.setCentralWidget(self.central_widget)

    # Event handlers
    def handle_pdf_to_images(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_paths:
            convert_pdf_to_png(file_paths)

    def handle_images_to_pdf(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Image Files", "", "Image Files (*.jpg *.png)")
        if file_paths:
            convert_jpg_or_png_to_pdf(file_paths)

    def handle_download_mp4(self):
        yt_url = self.yt_url_entry.text()
        if yt_url:
            convert_yt_to_mp4([yt_url])

    def handle_download_m4a(self):
        yt_url = self.yt_url_entry.text()
        if yt_url:
            convert_yt_to_m4a([yt_url])


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileConverterApp()
    window.show()
    sys.exit(app.exec_())
