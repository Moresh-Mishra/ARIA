import laya


class LayaEngine:

    def __init__(self):
        self.router = laya.Router(preload=False)

    def should_confirm(self, intent):

        state = {
            "intent": intent.intent,
            "task": intent.task,
            "parameters": intent.parameters.model_dump(),
        }

        questions = {
            "confirmation": {
                "type": "choice",
                "instructions": (
                    "Should this action require explicit user confirmation "
                    "before execution?"
                ),
                "criteria": {
                    "yes": "The action can have meaningful consequences, "
                           "affect external systems, or should not happen "
                           "without user approval.",
                    "no": "The action is safe, reversible, or low-risk."
                }
            }
        }

        return self.router.predict(
            state,
            questions
        )