class WorkingMemory:
    def __init__(self, config: MemoryConfig):
        self.max_capacity = config.working_memory_capacity or 50
        self.max_age_minutes = config.working_memory_ttl or 60
        self.memories = []

    def add(self, memory_item: MemoryItem) -> str:
        self._expire_old_memories()

        if len(self.memories) >= self.max_capacity:
            self.memories.pop(0)

        self.memories.append(memory_item)
        return memory_item.id
