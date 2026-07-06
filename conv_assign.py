import heapq
from dataclasses import dataclass, field


@dataclass
class AgentContainer:
    name: str
    last_assigned_at: int = 0
    limit: int = 2
    conversations: set[int] = field(default_factory=set)

    @property
    def open_count(self) -> int:
        return len(self.conversations)

    def has_capacity(self) -> bool:
        return self.open_count < self.limit


class AssignmentSystem:
    def __init__(self, agents: list[str]):
        self._agents = {name: AgentContainer(name=name) for name in agents}
        self._assigned_conversations: dict[int, str] = {}

        # Heap entry
        # open count, last_assigned_at, name
        self._pq = []
        self._clock = 0
        for name in agents:
            self._push(name)

    def _push(self, agent_name: str):
        agent = self._agents[agent_name]
        heapq.heappush(self._pq, (agent.open_count, agent.last_assigned_at, agent.name))

    def _valid(self, entry: tuple[int, int, str]):
        # entries that were older and pushed to heap might go stale, as we modify limit and assign conversations
        open_count, last_at, name = entry
        agent = self._agents[name]
        return (
            open_count == agent.open_count
            and last_at == agent.last_assigned_at
            and agent.has_capacity()
        )

    def set_limit(self, agent_name: str, limit: int) -> None:
        if limit < 0:
            raise ValueError("Limit cannot be negative")
        agent = self._agents.get(agent_name)
        if agent is None:
            raise LookupError("Agent not found")
        agent.limit = limit

        if agent.has_capacity():
            self._push(agent_name)

    def assign(self, conversation_id: int) -> str | None:
        if conversation_id in self._assigned_conversations:
            raise ValueError("Conversation already assigned")

        while self._pq:
            entry = heapq.heappop(self._pq)
            if not self._valid(entry):
                continue
            _, _, agent_name = entry
            agent = self._agents[agent_name]

            self._assigned_conversations[conversation_id] = agent.name
            agent.conversations.add(conversation_id)
            self._clock += 1
            agent.last_assigned_at = self._clock
            if agent.has_capacity():
                self._push(agent_name)
            return agent.name
        return None

    def close(self, conversation_id: int) -> None:
        if conversation_id not in self._assigned_conversations:
            raise LookupError("Conversation not found in assigment")

        agent_name = self._assigned_conversations[conversation_id]
        agent = self._agents[agent_name]

        del self._assigned_conversations[conversation_id]
        agent.conversations.remove(conversation_id)
        if agent.has_capacity():
            self._push(agent_name)
