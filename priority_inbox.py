import heapq
from dataclasses import dataclass, field
from collections import defaultdict


PRIORITY = {
    "URGENT": 0,
    "HIGH": 1,
    "NORMAL": 2,
    "LOW": 3,
}


@dataclass
class Conversation:
    conversation_id: str
    priority: str
    created_at: int
    required_skill: str


@dataclass
class Agent:
    agent_id: str
    skills: set[str]
    limit: int
    status: str = "active"
    last_assigned_at: int = 0
    conversations: set[str] = field(default_factory=set)

    @property
    def open_count(self) -> int:
        return len(self.conversations)

    def has_capacity(self) -> bool:
        return self.open_count < self.limit


class PriorityInbox:
    def __init__(self):
        self._agents: dict[str, Agent] = {}
        self._conversations: dict[str, Conversation] = {}

        # Heap entry:
        # (priority_num, created_at, conversation_id)
        self._conversation_pq: list[tuple[int, int, str]] = []

        # skill -> heap of agents
        # Heap entry:
        # (open_count, last_assigned_at, agent_id)
        self._agents_by_skill: dict[str, list[tuple[int, int, str]]] = defaultdict(list)

        self._clock = 0

    def add_agent(self, agent_id: str, skills: set[str], limit: int) -> None:
        if agent_id in self._agents:
            raise ValueError("Agent already exists")

        if limit < 0:
            raise ValueError("Limit cannot be negative")

        agent = Agent(
            agent_id=agent_id,
            skills=skills,
            limit=limit,
        )

        self._agents[agent_id] = agent

        for skill in skills:
            self._push_agent_for_skill(agent_id, skill)

    def _push_agent_for_skill(self, agent_id: str, skill: str) -> None:
        agent = self._agents[agent_id]

        heapq.heappush(
            self._agents_by_skill[skill],
            (agent.open_count, agent.last_assigned_at, agent.agent_id)
        )

    def _valid_agent_entry(
        self,
        entry: tuple[int, int, str],
        skill: str
    ) -> bool:
        open_count, last_assigned_at, agent_id = entry
        agent = self._agents[agent_id]

        return (
            open_count == agent.open_count
            and last_assigned_at == agent.last_assigned_at
            and agent.status == "active"
            and agent.has_capacity()
            and skill in agent.skills
        )

    def _get_best_agent_for_skill(self, skill: str) -> str | None:
        heap = self._agents_by_skill[skill]

        while heap:
            entry = heapq.heappop(heap)

            if not self._valid_agent_entry(entry, skill):
                continue

            _, _, agent_id = entry
            return agent_id

        return None

    def set_agent_status(self, agent_id: str, status: str) -> None:
        if status not in {"active", "away", "offline"}:
            raise ValueError("Invalid status")

        if agent_id not in self._agents:
            raise LookupError("Agent not found")

        agent = self._agents[agent_id]
        agent.status = status

        if status == "active" and agent.has_capacity():
            for skill in agent.skills:
                self._push_agent_for_skill(agent_id, skill)

    def add_conversation(
        self,
        conversation_id: str,
        priority: str,
        created_at: int,
        required_skill: str
    ) -> None:
        if conversation_id in self._conversations:
            raise ValueError("Conversation already exists")

        if priority not in PRIORITY:
            raise ValueError("Invalid priority")

        conv = Conversation(
            conversation_id=conversation_id,
            priority=priority,
            created_at=created_at,
            required_skill=required_skill,
        )

        self._conversations[conversation_id] = conv

        heapq.heappush(
            self._conversation_pq,
            (PRIORITY[priority], created_at, conversation_id)
        )

    def assign_next(self) -> tuple[str, str] | None:
        skipped = []

        while self._conversation_pq:
            priority_num, created_at, conversation_id = heapq.heappop(
                self._conversation_pq
            )

            conv = self._conversations[conversation_id]

            agent_id = self._get_best_agent_for_skill(conv.required_skill)

            if agent_id is None:
                # This conversation cannot be assigned right now.
                # Keep it aside and try the next one.
                skipped.append((priority_num, created_at, conversation_id))
                continue

            agent = self._agents[agent_id]

            agent.conversations.add(conversation_id)

            self._clock += 1
            agent.last_assigned_at = self._clock

            # Agent state changed, so push fresh entries into all skill heaps.
            if agent.has_capacity():
                for skill in agent.skills:
                    self._push_agent_for_skill(agent_id, skill)

            del self._conversations[conversation_id]

            # Restore skipped conversations.
            for item in skipped:
                heapq.heappush(self._conversation_pq, item)

            return conversation_id, agent_id

        # Nothing assignable right now. Restore skipped conversations.
        for item in skipped:
            heapq.heappush(self._conversation_pq, item)

        return None
