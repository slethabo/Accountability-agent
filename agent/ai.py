class AccountabilityAI:

    def __init__(self):
        pass

    def analyze(self, goals):

        if not goals:
            return (
                "ACCOUNTABILITY CHECK\n"
                "====================\n\n"
                "You currently have no active goals.\n"
                "Add a goal to get started."
            )

        response = []

        response.append(
            "ACCOUNTABILITY CHECK"
        )
        response.append(
            "===================="
        )

        active_goals = 0
        incomplete_tasks = 0
        completed_tasks = 0

        for goal in goals:

            if goal["completed"]:
                continue

            active_goals += 1

            tasks = goal["tasks"]

            for task in tasks:

                if task[2] == 0:
                    incomplete_tasks += 1
                else:
                    completed_tasks += 1

        response.append(
            f"\nYou currently have "
            f"{active_goals} active goals."
        )

        response.append(
            f"Tasks: {completed_tasks} completed, "
            f"{incomplete_tasks} incomplete."
        )

        response.append(
            "\nWHAT NEEDS ATTENTION"
        )
        response.append(
            "---------------------"
        )

        recommendation_number = 1

        for goal in goals:

            if goal["completed"]:
                continue

            goal_name = goal["goal"]
            due_date = goal["due_date"]
            tasks = goal["tasks"]

            unfinished_tasks = [
                task
                for task in tasks
                if task[2] == 0
            ]

            # Goal has no tasks
            if not tasks:

                response.append(
                    f"\n{recommendation_number}. "
                    f"{goal_name}"
                )

                response.append(
                    "   This goal has no tasks."
                )

                if due_date:

                    response.append(
                        f"   Deadline: {due_date}"
                    )

                    response.append(
                        "   Action: Break this goal "
                        "into smaller tasks."
                    )

                else:

                    response.append(
                        "   Action: Create a "
                        "specific first task."
                    )

                recommendation_number += 1

            # Goal has unfinished tasks
            elif unfinished_tasks:

                next_task = unfinished_tasks[0]

                response.append(
                    f"\n{recommendation_number}. "
                    f"{goal_name}"
                )

                response.append(
                    f"   Next action: "
                    f"{next_task[1]}"
                )

                recommendation_number += 1

        if recommendation_number == 1:

            response.append(
                "\nEverything currently has "
                "an actionable task."
            )

        response.append(
            "\nMAIN RECOMMENDATION"
        )
        response.append(
            "-------------------"
        )

        # Find the first goal with unfinished work
        for goal in goals:

            if goal["completed"]:
                continue

            tasks = goal["tasks"]

            unfinished_tasks = [
                task
                for task in tasks
                if task[2] == 0
            ]

            if unfinished_tasks:

                response.append(
                    f"\nFocus on: {goal['goal']}"
                )

                response.append(
                    f"Start with: "
                    f"{unfinished_tasks[0][1]}"
                )

                break

        else:

            for goal in goals:

                if not goal["completed"]:

                    response.append(
                        f"\nFocus on: "
                        f"{goal['goal']}"
                    )

                    response.append(
                        "Start by breaking this "
                        "goal into tasks."
                    )

                    break

        return "\n".join(response)