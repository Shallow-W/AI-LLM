from typing import Dict, Any


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
    tool_executor = ToolExecutor()

    from builtin.search import search

    search_description = "这是一个搜索工具，用来搜索。"
    tool_executor.registerTool(
        "search",
        search_description,
        search,
    )

    print("可用工具列表：")
    print(tool_executor.getAvailableTools())

    search_tool = tool_executor.getTool("search")
