async def process(self, user_input: str):

    self.state.current_task = user_input

    intent = await self.llm.understand(
        user_input
    )

    decision = self.laya.should_confirm(
        intent
    )

    return {
        "intent": intent,
        "decision": decision
    }