from PyQt5.QtCore import QThread, pyqtSignal
import asyncio 

class AsyncWorker(QThread):
    """异步工作线程，用于处理AI请求"""
    
    response_ready = pyqtSignal(str)  # 响应准备信号
    error_occurred = pyqtSignal(str)   # 错误信号
    
    def __init__(self, ai_core):
        super().__init__()
        self.ai_core = ai_core
        self.query = ""
        self.is_running = False
        
        # 连接AI核心的信号
        self.ai_core.error_occurred.connect(self.error_occurred.emit)
    
    def set_query(self, query: str):
        """设置要处理的查询"""
        self.query = query
    
    def run(self):
        """线程主函数"""
        if not self.query:
            return
            
        try:
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 运行异步任务
            response = loop.run_until_complete(
                self.ai_core.generate_response(self.query)
            )
            
            # 发送最终响应
            self.response_ready.emit(response)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            loop.close()
