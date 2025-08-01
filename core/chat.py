from core.ai_processor import AICore
import asyncio

class ChatAgent:
    def __init__(self):
        self.ai_core = AICore()
        self.conversation_history = []
        
    def chat(self, user_message: str) -> str:
        """处理用户消息并返回AI回复"""
        # 添加用户消息到对话历史
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # 创建异步事件循环并运行AI生成
        try:
            response = asyncio.run(self.ai_core.generate_response(user_message))
            
            # 添加AI回复到对话历史
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
        except Exception as e:
            return f"对话出错: {str(e)}"
