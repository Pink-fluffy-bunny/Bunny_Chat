# AI角色对话系统 - 可可

一个基于Python的AI对话互动程序，让你与动漫角色"可可"进行情感交流。

## 功能特点

- 🎭 **角色扮演**: AI完全融入动漫角色"可可"的身份，提供沉浸式对话体验
- 💖 **情感分析**: 注重分析用户情感，提供温暖的情绪价值
- 🖼️ **可视化界面**: 简洁美观的GUI界面，角色形象展示
- 🗣️ **语音同步**: 支持文字和语音双输出，回应更加生动
- ⚡ **实时流式**: 流式响应显示，对话体验更自然
- 📦 **模块化设计**: 代码结构清晰，易于修改和扩展

## 系统要求

- Python 3.8+
- Windows 10/11 (推荐)
- 网络连接 (用于调用AI模型API)

## 安装部署

### 1. 创建虚拟环境
```bash
conda create -n AI_Chat python=3.10
conda activate AI_Chat
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
编辑 `.env` 文件，填入你的API密钥和模型信息：
```env
OPENAI_API_KEY = "your_api_key_here"
OPENAI_BASE_URL = "https://api.siliconflow.cn/v1"
OPENAI_MODEL = "Qwen/Qwen3-8B"
```

### 4. 运行程序
```bash
python main.py
```

## 项目结构

```
AI_Chat/
├── .env                    # 环境变量配置
├── main.py                 # 程序入口
├── readme.md               # 项目说明
├── requirements.txt        # 依赖包列表
├── assets/                 # 角色形象图片
│   └── character.png       # 角色图片
├── config/
│   └── character.yaml      # 角色设定文件
├── core/                   # 核心模块
│   ├── ai_processor.py     # AI处理核心
│   ├── async_worker.py     # 异步工作线程
│   └── chat.py             # 聊天代理
└── gui/                    # 图形界面
    └── main_window.py      # 主窗口界面
```

## 角色定制

### 修改角色设定
编辑 `config/character.yaml` 文件可以自定义角色：
- `name`: 角色名称
- `universe`: 角色所在世界
- `personality`: 性格特点列表
- `response_rules`: 回应规则列表

### 更换角色形象
替换 `assets/character.png` 文件即可更换角色图片。

## 使用说明

1. 启动程序后会看到角色形象和欢迎消息
2. 在底部输入框输入你想说的话
3. 点击"发送"按钮或按回车键发送消息
4. 可可会实时回复并伴有语音输出
5. 对话历史会显示在左侧聊天区域

## 开发说明

### 模块化设计
- **core/ai_processor.py**: 处理AI对话逻辑和API调用
- **core/async_worker.py**: 异步处理AI请求，避免界面卡顿
- **core/chat.py**: 聊天代理，管理对话历史
- **gui/main_window.py**: PyQt5图形界面实现

### 扩展开发
1. 添加新的角色：修改config/character.yaml
2. 添加新的回应规则：在character.yaml中扩展response_rules
3. 自定义界面：修改gui/main_window.py
4. 添加新功能：在core模块中扩展相应功能

## 注意事项

- 请确保网络连接正常以调用AI API
- 语音输出需要系统支持TTS功能
- 建议使用耳机获得更好的语音体验
- 对话内容会根据角色设定进行个性化回应

## 更新日志

### v1.0.2
- 实现多轮对话功能
- 对话历史记录维护
- 上下文感知的AI回复

### v1.0.1
- 修复AI回复逐个token输出的问题
- 改为一次性完整输出AI回复
- 优化对话体验

### v1.0.0
- 基础功能实现
- 角色对话系统
- GUI界面
- 语音文字同步输出
- 角色设定配置
