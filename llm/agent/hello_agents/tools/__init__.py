from .registry import ToolExecutor
from dotenv import load_dotenv


def init() -> ToolExecutor:
    load_dotenv()
    tool_executor = ToolExecutor()

    from .builtin import search

    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool(
        "search",
        search_description,
        search,
    )

    print("可用工具列表：")
    print(tool_executor.getAvailableTools())
    return tool_executor


tool_executor = init()
