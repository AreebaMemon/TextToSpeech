import sys
import pyttsx3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel,
    QComboBox, QSlider, QCheckBox, QListWidget, QGroupBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class TextToSpeechApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.engine = pyttsx3.init()
        self.set_default_voice()

    def initUI(self):
        self.setWindowTitle("Advanced Text-to-Speech Converter")
        self.setGeometry(300, 100, 1000, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QGroupBox {
                background-color: #ffffff;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005BB5;
            }
            QTextEdit, QListWidget {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
            }
            QSlider::groove:horizontal {
                background-color: #ddd;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: #0078D7;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)

        # Main layout: Split into left and right sections
        main_layout = QHBoxLayout()

        # Left Side: Text Input
        left_layout = QVBoxLayout()
        input_group = QGroupBox("Text Input")
        input_layout = QVBoxLayout()
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Enter text here...")
        self.text_input.textChanged.connect(self.update_word_char_count)
        input_layout.addWidget(self.text_input)

        # Word & Character Counter
        self.counter_label = QLabel("Words: 0 | Characters: 0")
        input_layout.addWidget(self.counter_label)

        # Clear Button
        clear_btn = QPushButton("Clear Text", self)
        clear_btn.clicked.connect(self.clear_text)
        input_layout.addWidget(clear_btn)

        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)
        main_layout.addLayout(left_layout)

        # Right Side: Controls
        right_layout = QVBoxLayout()

        # Settings Section
        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()

        #Language Selection
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel("Language:")
        self.lang_combo = QComboBox(self)
        self.lang_combo.addItems(["English", "French", "Spanish", "Sindhi", "Urdu"])
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)
        settings_layout.addLayout(lang_layout)

        # Voice Selection
        voice_layout = QHBoxLayout()
        self.voice_label = QLabel("Voice:")
        self.voice_combo = QComboBox(self)
        self.voice_combo.addItems(["Male", "Female"])
        voice_layout.addWidget(self.voice_label)
        voice_layout.addWidget(self.voice_combo)
        settings_layout.addLayout(voice_layout)

        # Speed Control
        speed_layout = QHBoxLayout()
        self.speed_label = QLabel("Speed:")
        self.speed_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.speed_slider.setRange(50, 200)
        self.speed_slider.setValue(100)
        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_slider)
        settings_layout.addLayout(speed_layout)

        # Volume Control
        volume_layout = QHBoxLayout()
        self.volume_label = QLabel("Volume:")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        volume_layout.addWidget(self.volume_label)
        volume_layout.addWidget(self.volume_slider)
        settings_layout.addLayout(volume_layout)

        # Slow Mode Checkbox
        self.slow_mode = QCheckBox("Slow Mode", self)
        settings_layout.addWidget(self.slow_mode)

        settings_group.setLayout(settings_layout)
        right_layout.addWidget(settings_group)

        # History Section
        history_group = QGroupBox("History")
        history_layout = QVBoxLayout()
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)

        # Clear History Button
        clear_history_btn = QPushButton("Clear History", self)
        clear_history_btn.clicked.connect(self.clear_history)
        history_layout.addWidget(clear_history_btn)

        history_group.setLayout(history_layout)
        right_layout.addWidget(history_group)

        # Button Controls
        btn_layout = QHBoxLayout()
        self.speak_btn = QPushButton("🔊 Speak", self)
        self.speak_btn.clicked.connect(self.speak)
        btn_layout.addWidget(self.speak_btn)

        self.stop_btn = QPushButton("⏹ Stop", self)
        self.stop_btn.clicked.connect(self.stop_speaking)
        btn_layout.addWidget(self.stop_btn)

        self.save_btn = QPushButton("💾 Save MP3", self)
        self.save_btn.clicked.connect(self.save_audio)
        btn_layout.addWidget(self.save_btn)

        right_layout.addLayout(btn_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def set_default_voice(self):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

    def speak(self):
        text = self.text_input.toPlainText()
        if text:
            self.engine.setProperty('rate', self.speed_slider.value())
            self.engine.setProperty('volume', self.volume_slider.value() / 100)

            # Map language selection to voice
            language = self.lang_combo.currentText()
            if language == "French":
                self.engine.setProperty('voice', "fr")  # French voice
            elif language == "Spanish":
                self.engine.setProperty('voice', "es")  # Spanish voice
            elif language == "Sindhi":
                self.engine.setProperty('voice', "sd")  # Sindhi voice (if available)
            elif language == "Urdu":
                self.engine.setProperty('voice', "ur")  # Urdu voice (if available)
            else:
                self.engine.setProperty('voice', "en")  # Default to English

            if self.voice_combo.currentText() == "Female":
                voices = self.engine.getProperty('voices')
                self.engine.setProperty('voice', voices[1].id)

            if self.slow_mode.isChecked():
                self.engine.setProperty('rate', 75)

            self.engine.say(text)
            self.engine.runAndWait()
            self.history_list.addItem(text)

    def stop_speaking(self):
        self.engine.stop()

    def save_audio(self):
        text = self.text_input.toPlainText()
        if text:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Audio File", "", "MP3 Files (*.mp3)")
            if file_name:
                self.engine.save_to_file(text, file_name)
                self.engine.runAndWait()
                print(f"Audio saved as {file_name}")

    def update_word_char_count(self):
        text = self.text_input.toPlainText()
        words = len(text.split())
        chars = len(text)
        self.counter_label.setText(f"Words: {words} | Characters: {chars}")

    def clear_text(self):
        self.text_input.clear()

    def clear_history(self):
        self.history_list.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec())