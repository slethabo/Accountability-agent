class AccountabilityAI:

    def __init__(self):
        pass

    def analyze(self, goals):

        if not goals:

            return (
                "You currently have no active goals. "
                "Add a goal to get started."
            )

        return (
            "I have reviewed your current goals. "
            "There are active goals that need attention."
        )