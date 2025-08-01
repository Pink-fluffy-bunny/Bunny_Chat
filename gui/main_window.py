import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QLabel, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QTextCursor
import pyttsx3
import os

from core.ai_processor import AICore
from core.async_worker import AsyncWorker

class ChatMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI角色对话系统 - 可可")
        self.setGeometry(100, 100, 800, 600)
        
        # 初始化语音引擎
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 200)  # 语速
        self.tts_engine.setProperty('volume', 0.9)  # 音量
        
        # 初始化AI核心和工作线程
        self.ai_core = AICore()
        self.worker = AsyncWorker(self.ai_core)
        
        # 连接信号
        self.worker.response_ready.connect(self.on_response_complete)
        self.worker.error_occurred.connect(self.on_error)
        
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧角色区域
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        # 角色图片
        self.character_label = QLabel()
        self.character_label.setAlignment(Qt.AlignCenter)
        self.character_label.setMinimumSize(300, 400)
        
        # 设置默认角色图片
        if os.path.exists("assets/character.png"):
            pixmap = QPixmap("assets/character.png")
        else:
            # 创建空白图片作为占位符
            pixmap = QPixmap(300, 400)
            pixmap.fill(Qt.gray)
            
        self.character_label.setPixmap(pixmap.scaled(300, 400, Qt.KeepAspectRatio))
        
        left_layout.addWidget(self.character_label)
        
        # 右侧聊天区域
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        # 聊天显示区域
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(400)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        
        # 输入区域
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入你想对可可说的话...")
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 15px;
                font-size: 14px;
            }
        """)
        
        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        # 添加组件到布局
        right_layout.addWidget(self.chat_display)
        right_layout.addLayout(input_layout)
        
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        
        # 显示欢迎消息
        self.append_welcome_message()
        
    def append_welcome_message(self):
        """添加欢迎消息"""
        welcome_msg = "你好呀~我是可可，很高兴认识你！有什么想和我聊的吗？"
        self.chat_display.append(f"<b>可可:</b> {welcome_msg}")
        self.speak_text(welcome_msg)
        
    def send_message(self):
        """发送消息"""
        user_message = self.input_field.text().strip()
        if not user_message:
            return
            
        # 显示用户消息
        self.chat_display.append(f"<b>你:</b> {user_message}")
        self.input_field.clear()
        
        # 滚动到底部
        self.chat_display.moveCursor(QTextCursor.End)
        
        # 启动AI处理
        self.send_button.setEnabled(False)
        self.input_field.setEnabled(False)
        
        self.worker.set_query(user_message)
        self.worker.start()
        
    def append_to_chat(self, text):
        """追加文本到聊天显示"""
        # 获取当前光标位置
        cursor = self.chat_display.textCursor()
        
        # 如果是新消息，先添加换行
        if not self.chat_display.toPlainText().endswith("可可: "):
            self.chat_display.append("<b>可可:</b> ")
            
        # 插入文本
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        
        # 滚动到底部
        self.chat_display.moveCursor(QTextCursor.End)
        
    def on_response_complete(self, response):
        """响应完成处理"""
        # 显示AI的完整回复
        if response.strip():
            self.chat_display.append(f"<b>可可:</b> {response}")
        
        # 滚动到底部
        self.chat_display.moveCursor(QTextCursor.End)
        
        # 启用输入
        self.send_button.setEnabled(True)
        self.input_field.setEnabled(True)
        self.input_field.setFocus()
        
        # 语音输出
        if response.strip():
            self.speak_text(response)
        
    def on_error(self, error_msg):
        """错误处理"""
        self.chat_display.append(f"<b style='color: red;'>错误:</b> {error_msg}")
        self.send_button.setEnabled(True)
        self.input_field.setEnabled(True)
        self.input_field.setFocus()
        
    def speak_text(self, text):
        """语音输出"""
        try:
            # 在新线程中执行语音输出，避免阻塞GUI
            def run_tts():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            tts_thread = QThread()
            # 使用lambda创建简单的线程任务
            from PyQt5.QtCore import QTimer
            timer = QTimer()
            timer.timeout.connect(lambda: [run_tts(), timer.stop()])
            timer.setSingleShot(True)
            timer.start(100)
            
        except Exception as e:
            print(f"语音输出错误: {e}")

def main():
    app = QApplication(sys.argv)
    window = ChatMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
