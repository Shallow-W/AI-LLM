from typing import Dict, Any
from dotenv import load_dotenv


class ToolExecutor:
    def __init__(self):
        self.tools = {}

    def registerTool(self, name: str, description: str, func: callable):

        if name in self.tools:
            print(f"工具 '{name}' 已经注册，覆盖原有工具。")

        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 注册成功。")

    def getTool(self, name: str) -> callable:
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        return "\n".join(
            [f"{name}: {info['description']}" for name, info in self.tools.items()]
        )


if __name__ == "__main__":
    load_dotenv()
    tool_executor = ToolExecutor()

    from builtin.search import search

    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool(
        "search",
        search_description,
        search,
    )

    print("可用工具列表：")
    print(tool_executor.getAvailableTools())

    search_tool = tool_executor.getTool("search")
    if search_tool:
        result = search_tool("美国总统特朗普的生日是什么时候？")
        print("搜索结果：")
        print(result)
    else:
        print("未找到 'search' 工具。")
