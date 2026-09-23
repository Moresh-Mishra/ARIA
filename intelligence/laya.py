import laya


class LayaEngine:

    def __init__(self):
        self.router = laya.Router(preload=False)

    def decide(self, intent):

        state = {
            "intent": intent.intent,
            "task": intent.task,
            "parameters": intent.parameters.model_dump(),
        }

        questions = {
            "confirmation": {
                "type": "choice",
                "instructions": (
                    "Does this action require explicit user "
                    "confirmation before execution?"
                ),
                "criteria": {
                    "yes": (
                        "The action has meaningful consequences, "
                        "affects an external system, or could be "
                        "difficult to reverse."
                    ),
                    "no": (
                        "The action is safe, reversible, or a "
                        "normal low-risk personal assistant action."
                    ),
                },
            }
        }

        return self.router.predict(state, questions)