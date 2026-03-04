from ..core.agent import Agent
from ..core.llm import HelloAgentLLM
from ..core.config import Config
from ..core.message import Message


class SimpleAgent(Agent):
    """
    一个简单的Agent实现
    """

    def __init__(
        self,
        name: str = "SimpleAgent",
        llm: HelloAgentLLM = None,
        system_prompt: str = None,
        config: Config = None,
        **kwargs,
    ):
        if llm is None:
            llm = HelloAgentLLM()

        super().__init__(name=name, llm=llm, system_prompt=system_prompt, config=config)

    def run(self, input_text: str, **kwargs) -> str:
        # 简单实现处理逻辑
        message = Message(role="user", content=input_text)
        self.add_message(message)
        return f"SimpleAgent received: {input_text}"
