from core.event_bus import EventBus
from core.state import SakhaState

from intelligence.llm import LLM
from intelligence.laya import LayaEngine

from agents.executor import AgentExecutor


class SakhaRuntime:

    def __init__(self):

        self.state = SakhaState()

        self.events = EventBus()

        self.llm = LLM()
        self.laya = LayaEngine()
        self.executor = AgentExecutor()

    async def process(self, user_input: str):

        self.state.current_task = user_input

        # Understand
        intent = await self.llm.understand(
            user_input
        )

        # Decide
        decision = self.laya.decide(
            intent
        )

        # Temporary execution rule
        confirmation = (
            decision.get("answers", {})
            .get("confirmation", {})
            .get("choice", "no")
            if isinstance(decision, dict)
            else "no"
        )

        if confirmation == "no":

            execution = await self.executor.execute(
                intent
            )

        else:

            execution = {
                "success": False,
                "requires_confirmation": True
            }

        return intent, decision, execution