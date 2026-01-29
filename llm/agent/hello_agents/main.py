from tool.tools import *


if "__main__" == __name__:
    print("Hello Agents!")
    memory_tool = MemoryTool(user_id="user_123")
    result = memory_tool.execute(
        action="add",
        content="This is a test memory.",
        memory_type="working",
        importance=0.8,
    )
    print(result)
