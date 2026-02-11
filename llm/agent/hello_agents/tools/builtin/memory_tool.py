from base import Tool


class MemoryTool(Tool):
    def __init__(
        self,
        user_id: str = "default_user",
        memory_config: MemoryConfig = None,
        memory_types: list[str] = None,
        # 对象初始化不能携带[]{}等可变对象，避免多个对象间共享同一引用
    ):
        super().__init__(name="memory", description="A tool for managing memories.")

        self.memory_config = memory_config or MemoryConfig()
        self.memory_types = memory_types or ["working", "episodic", "semantic"]

        self.memory_manager = MemoryManager(
            config=self.memory_config,
            user_id=user_id,
            enable_working="working" in self.memory_types,
            enable_short_term="episodic" in self.memory_types,
            enable_long_term="semantic" in self.memory_types,
            enable_perceptual="perceptual" in self.memory_types,
        )
        # 掩码使能信号
        pass

    def execute(self, action: str, **kwargs) -> str:
        # 使用kwargs实现连接性和功能性的解耦
        if action == "add":
            return self._add_momery(**kwargs)
        elif action == "search":
            return self._search_momery(**kwargs)
        elif action == "summary":
            return self._summary_momery(**kwargs)
        elif action == "status":
            pass
        elif action == "update":
            pass
        elif action == "remove":
            pass
        elif action == "forget":
            pass
        elif action == "consolidate":
            pass
        elif action == "clear_all":
            pass

    def _add_momery(
        self,
        content="",
        memory_type="working",
        importance=0.5,
        file_path: str = None,
        modality: str = None,
        **metadata,
    ) -> str:
        try:

            memory_id = self.memory_manager.add_memory(
                content=content,
                memory_type=memory_type,
                importance=importance,
                metadata=metadata,
                auto_classify=False,
            )
            return f"✅ 记忆已添加 ID: {memory_id[:8]}"
        except Exception as e:
            return f"❌ 添加记忆失败: {str(e)}"
