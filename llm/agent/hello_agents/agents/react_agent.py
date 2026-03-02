import sys
import os

# 将父目录添加到 sys.path 以便导入 sibling 模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import HelloAgentLLM, llmclient
from tools import ToolExecutor, tool_executor
import re

# ReAct 提示词模板
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 Finish[最终答案] 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}
"""


class ReactAgent:
    def __init__(
        self, llm_client: HelloAgentLLM, tool_executor: ToolExecutor, max_steps: int = 5
    ):
        self.llm = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def run(self, question: str):
        self.history = []
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"\n🔄 === Step {current_step} ===")
            # 生成 Agent 的回答
            tools_desc = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_desc, question=question, history=history_str
            )
            # 调用大模型
            message = [{"role": "user", "content": prompt}]
            response = self.llm.think(messages=message)

            if not response:
                print("⚠️ LLM 没有返回任何内容，结束对话。")
                break
            # 下面进行解析
            thought, action = self._parse_response(response)
            if thought:
                print(f"🤔 Thought: {thought}")
            if not action:
                print("❌ 没有解析到 Action，结束对话。")
                break

            if action.startswith("Finish"):
                final_answer = re.match(r"Finish\[(.*)\]", action).group(1)
                print(f"🎉 Final Answer: {final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                continue
            print(f"🛠️ Action: 调用工具 '{tool_name}'，输入: {tool_input}")

            tool_func = self.tool_executor.getTool(tool_name)
            if not tool_func:
                observation = f"未找到'{tool_name}'工具。"
            else:
                observation = tool_func(tool_input)
            print(f"👀 Observation: {observation}")

            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")
        print("🛑 达到最大步骤数，结束对话。")
        return None

    def _parse_response(self, text: str):
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)

        thought = thought_match.group(1).strip() if thought_match else ""
        action = action_match.group(1).strip() if action_match else ""

        return thought, action

    def _parse_action(self, action_text: str):
        """解析Action字符串，提取工具名称和输入。"""
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None


print("🚀 正在测试ReactAgent...")
react_agent = ReactAgent(llmclient, tool_executor)
question = "2026年小米的最新手机是什么？"
react_agent.run(question)
