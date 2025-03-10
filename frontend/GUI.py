from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QStackedWidget,
    QWidget,
    QLineEdit,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QLabel,
    QSizePolicy,
)
from PyQt5.QtGui import (
    QIcon,
    QPainter,
    QMovie,
    QColor,
    QTextCharFormat,
    QFont,
    QPixmap,
    QTextBlockFormat,
)
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"


def answer_modifier(answer):
    lines = answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer


def query_modifier(query):
    new_query = query.lower().strip()
    query_words = new_query.split()

    question_words = {
        "how",
        "what",
        "who",
        "when",
        "where",
        "why",
        "which",
        "whose",
        "whom",
        "can",
        "what's",
        "where's",
        "how's",
    }

    auxiliary_verbs = {
        "is",
        "are",
        "am",
        "was",
        "were",
        "do",
        "does",
        "did",
        "can",
        "could",
        "will",
        "would",
        "shall",
        "should",
        "may",
        "might",
        "must",
        "have",
        "has",
        "had",
    }

    # Check if the first word suggests a question
    is_question = query_words[0] in question_words or query_words[0] in auxiliary_verbs

    # Ensure proper punctuation at the end
    if new_query and new_query[-1] in [".", "?", "!"]:
        new_query = new_query[:-1]  # Remove existing punctuation

    new_query += "?" if is_question else "."

    return new_query.capitalize()


def set_microphone_status(command):
    with open(rf"{TempDirPath}/Mic.data", "w", encoding="utf-8") as file:
        file.write(command)


def get_microphone_status():
    with open(rf"{TempDirPath}/Mic.data", "r", encoding="utf-8") as file:
        return file.read()


def set_assistant_status(status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
        file.write(status)


def get_assistant_status():
    with open(rf"{TempDirPath}/Status.data", "r", encoding="utf-8") as file:
        return file.read()


def mic_button_initialized():
    set_microphone_status("False")


def mic_button_closed():
    set_microphone_status("True")


def graphics_dictionary_path(filename):
    path = rf"{GraphicsDirPath}\{filename}"
    return path


def temp_dictionary_path(filename):
    path = rf"{TempDirPath}\{filename}"
    return path


def show_text_to_screen(text):
    with open(rf"{TempDirPath}\Responses.data", "w", encoding="utf-8") as file:
        file.write(text)


class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        max_gif_size_W = int(screen_width / 4)
        max_gif_size_H = int(max_gif_size_W / 16 * 9)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(graphics_dictionary_path("Jarvis.gif"))
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)
        self.label = QLabel("")
        self.label.setStyleSheet(
            "color: white; font-size: 16px; margin-right: 195px; border: none; margin-top: -30px;"
        )
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_label)
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet(
            """
        QScrollBar:vertical {
            border: none;
            background: black;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: white;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical {
            background: black;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
            height: 10px;
        }
        QScrollBar::sub-line:vertical {
            background: black;
            subcontrol-position: top;
            subcontrol-origin: margin;
            height: 10px;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            border: none;
            background: none;
            color: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """
        )

    def loadMessages(self):
        global old_chat_message

        with open(
            temp_dictionary_path("Responses.data"), "r", encoding="utf-8"
        ) as file:
            messages = file.read()

            if None == messages:
                pass

            elif len(messages) < 1:
                pass

            elif str(old_chat_message) == str(messages):
                pass

            else:
                self.addMessage(message=messages, color="White")
                old_chat_message = messages

    def SpeechRecogText(self):
        with open(temp_dictionary_path("Status.data"), "r", encoding="utf-8") as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(graphics_dictionary_path("voice.png"), 60, 60)
            mic_button_initialized()
        else:
            self.load_icon(graphics_dictionary_path("mic.png"), 60, 60)
            mic_button_closed()

        self.toggled = not self.toggled

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)


class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        gif_label = QLabel()
        movie = QMovie(graphics_dictionary_path("Jarvis.gif"))
        gif_label.setMovie(movie)
        max_gif_size_H = int(screen_width / 16 * 9)
        max_gif_size_W = 2000
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.icon_label = QLabel()
        pixmap = QPixmap(graphics_dictionary_path("Mic_on.png"))
        new_pixmap = pixmap.scaled(60, 60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size: 16px; margin-bottom: 0;")
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        with open(temp_dictionary_path("Status.data"), "r", encoding="utf-8") as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(graphics_dictionary_path("Mic_on.png"), 60, 60)
            mic_button_initialized()
        else:
            self.load_icon(graphics_dictionary_path("Mic_off.png"), 60, 60)
            mic_button_closed()

        self.toggled = not self.toggled


class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)


class CustomTopBar(QWidget):
    def __init__(self, parent, stack_widget):
        super().__init__(parent)
        self.setMinimumHeight(60)
        self.initUI()
        self.current_screen = None
        self.stack_widget = stack_widget
        self.offset = 0

    def initUI(self):
        self.setFixedHeight(50)

        # Main layout for the top bar
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 0, 10, 0)

        # Left: Assistant name
        title_label = QLabel(f"{str(Assistantname).capitalize()}  AI")
        title_label.setStyleSheet(
            "color: black; font-size: 18px; background-color: white;"
        )
        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addStretch()  # Push everything to the left

        # Center: Home and Chat buttons
        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        home_button = QPushButton()
        home_icon = QIcon(graphics_dictionary_path("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText("  Home")
        home_button.setStyleSheet(
            "height: 40px; line-height: 40px; background-color: white; color: black; "
            "padding: 0 10px; margin: 5px; border: none"
        )
        home_button.setMinimumWidth(100)

        message_button = QPushButton()
        message_icon = QIcon(graphics_dictionary_path("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("  Chat")
        message_button.setStyleSheet(
            "height: 40px; line-height: 40px; background-color: white; color: black; "
            "padding: 0 10px; margin: 5px; border: none"
        )
        message_button.setMinimumWidth(100)

        center_layout.addWidget(home_button)
        center_layout.addWidget(message_button)

        # Right: Window control buttons
        minimize_button = QPushButton()
        minimize_icon = QIcon(graphics_dictionary_path("Minimize2.png"))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color: white;")
        minimize_button.clicked.connect(self.minimize_window)

        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(graphics_dictionary_path("Maximize.png"))
        self.restore_icon = QIcon(graphics_dictionary_path("Minimize.png"))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color: white;")
        self.maximize_button.clicked.connect(self.maximize_window)

        close_button = QPushButton()
        close_icon = QIcon(graphics_dictionary_path("Close.png"))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color: white;")
        close_button.clicked.connect(self.close_window)

        right_layout = QHBoxLayout()
        right_layout.addStretch()  # Push everything to the right
        right_layout.addWidget(minimize_button)
        right_layout.addWidget(self.maximize_button)
        right_layout.addWidget(close_button)

        # Add all sections to the main layout
        main_layout.addLayout(title_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(right_layout)

        # Set the main layout
        self.setLayout(main_layout)

        # Button functionality
        home_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimize_window(self):
        self.parent().showMinimized()

    def maximize_window(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def close_window(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        intial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(intial_screen)
        self.current_screen = intial_screen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        screeen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0, 0, screeen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)


def gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    gui()
