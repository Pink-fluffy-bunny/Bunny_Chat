from openai import AsyncOpenAI
from dotenv import load_dotenv
import json, os, yaml, sys
from PyQt5.QtCore import QObject, pyqtSignal

def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        # PyInstaller创建的临时文件夹
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def load_env_file():
    """加载环境变量文件"""
    env_path = get_resource_path('.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()

class AICore(QObject):
    stream_response = pyqtSignal(str)   # 流式响应信号
    response_complete = pyqtSignal()    # 完成信号
    error_occurred = pyqtSignal(str)    # 错误信号
    
    def __init__(self):
        super().__init__()
        load_env_file()
        base_url = os.getenv("OPENAI_BASE_URL")
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        
        self.model = os.getenv("OPENAI_MODEL")
    
        # 获取角色配置文件路径
        character_profile = os.getenv("CHARACTER_PROFILE", "config/character.yaml")
        # 处理打包后的路径
        character_profile_path = get_resource_path(character_profile)
        
        with open(character_profile_path, "r", encoding="utf-8") as f:
            self.character = yaml.safe_load(f)
            
        # 构建更详细的角色提示词
        personality_traits = '，'.join(self.character['personality'])
        response_rules = '\n'.join([f"- {rule}" for rule in self.character['response_rules'][:5]])  # 取前5条规则作为示例
        
        self.base_prompt = f"""
你是一个名为{self.character['name']}的动漫角色，来自{self.character['universe']}。
你的性格特点包括：{personality_traits}。

请严格按照以下规则与用户对话：
1. 回答必须简短、口语化，符合角色性格
2. 根据不同情境使用相应的回应方式
3. 注重分析用户的情感，提供情绪价值
4. 回答长度控制在1-2句话内

示例回应规则：
{response_rules}

请始终以{self.character['name']}的身份和语气与用户对话，不要暴露你是AI助手。
""".strip()
    
    async def generate_response(self, query: str) -> str:
        try:
            # 使用非流式输出，一次性获取完整响应
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.base_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                stream=False  # 改为非流式输出
            )
            
            # 获取完整响应内容
            full_response = response.choices[0].message.content
            
            # 发送完整响应
            self.response_complete.emit()
            return full_response if full_response else ""
        except Exception as e:
            self.error_occurred.emit(str(e))
            return f"对话出错: {str(e)}"

if __name__ == "__main__":
    import asyncio
    async def test():
        query = "你好，你是谁？"
        core = AICore()
        response = await core.generate_response(query=query)
        print(response)
    
    asyncio.run(test())
