import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict


load_dotenv()


class HelloAgentLLM:
    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        base_url: str = None,
        timeout: int = None,
    ):
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.model = model or os.getenv("LLM_MODEL_ID")
        self.base_url = base_url or os.getenv("LLM_BASE_URL")
        self.timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))
        if not all([self.api_key, self.model, self.base_url]):
            raise ValueError(
                "API key, model ID, and base URL must be provided or set in environment variables."
            )
        self.client = OpenAI(
            api_key=self.api_key, base_url=self.base_url, timeout=self.timeout
        )

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        print(f"正在调用LLM接口,模型:{self.model}，消息：{messages}")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            print("LLM接口调用成功，正在处理响应...")

            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)  # 实时输出内容
                collected_content.append(content)
            print("\nLLM响应处理完成。")
            return "".join(collected_content)

        except Exception as e:
            print(f"调用LLM接口失败: {e}")
            return None


if __name__ == "__main__":
    try:
        llmclient = HelloAgentLLM()
        test_messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that writes Python code.",
            },
            {"role": "user", "content": "写一个快速排序算法"},
        ]

        print("正在测试LLM接口...")
        result = llmclient.think(test_messages)
        print("LLM接口测试完成。")
        if result:
            print("LLM测试成功，结果如下：")
            print(result)

    except Exception as e:
        print(f"LLM测试失败: {e}")
