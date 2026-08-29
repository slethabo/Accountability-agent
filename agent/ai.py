from datetime import datetime


class AccountabilityAI:

    def __init__(self):
        pass

    # =================================
    # MAIN ANALYSIS
    # =================================

    def analyze(self, goals):

        if not goals:
            return (
                "ACCOUNTABILITY CHECK\n"
                "====================\n\n"
                "You currently have no active goals.\n"
                "Add a goal to get started."
            )

        today = datetime.now().date()

        active_goals = []
        total_tasks = 0
        completed_tasks = 0

        # =================================
        # COLLECT GOAL INFORMATION
        # =================================

        for goal in goals:

            if goal["completed"]:
                continue

            tasks = goal["tasks"]

            total_tasks += len(tasks)

            completed_tasks += sum(
                1
                for task in tasks
                if task[2] == 1
            )

            due_date = None

            if goal["due_date"]:

                try:
                    due_date = datetime.strptime(
                        goal["due_date"],
                        "%Y-%m-%d"
                    ).date()

                except ValueError:
                    due_date = None

            days_remaining = None

            if due_date:

                days_remaining = (
                    due_date - today
                ).days

            unfinished_tasks = [
                task
                for task in tasks
                if task[2] == 0
            ]

            active_goals.append(
                {
                    "id": goal["id"],
                    "goal": goal["goal"],
                    "priority": goal["priority"],
                    "due_date": goal["due_date"],
                    "days_remaining": days_remaining,
                    "tasks": tasks,
                    "unfinished_tasks": unfinished_tasks
                }
            )

        # =================================
        # CALCULATE URGENCY
        # =================================

        for item in active_goals:

            days = item["days_remaining"]

            # Lower score = higher urgency.

            if days is not None:

                if days < 0:
                    score = 1

                elif days == 0:
                    score = 2

                elif days <= 3:
                    score = 3

                elif days <= 7:
                    score = 4

                elif days <= 14:
                    score = 5

                else:
                    score = 6

            else:

                score = 7

            # Priority acts as a secondary factor.

            score += (
                item["priority"] * 0.1
            )

            # Goals with unfinished tasks
            # are slightly more actionable.

            if item["unfinished_tasks"]:
                score -= 0.05

            item["score"] = score

        # =================================
        # SORT GOALS
        # =================================

        active_goals.sort(
            key=lambda item: item["score"]
        )

        # =================================
        # BUILD ACCOUNTABILITY CHECK
        # =================================

        response = []

        response.append(
            "ACCOUNTABILITY CHECK"
        )

        response.append(
            "===================="
        )

        response.append(
            f"\nActive goals: "
            f"{len(active_goals)}"
        )

        response.append(
            f"Tasks completed: "
            f"{completed_tasks}/"
            f"{total_tasks}"
        )

        # =================================
        # PRIORITY CHECK
        # =================================

        response.append(
            "\nPRIORITY CHECK"
        )

        response.append(
            "--------------"
        )

        for index, item in enumerate(
            active_goals[:3],
            start=1
        ):

            response.append(
                f"\n{index}. "
                f"{item['goal']}"
            )

            days = item["days_remaining"]

            if days is not None:

                if days < 0:

                    response.append(
                        "   Status: OVERDUE"
                    )

                elif days == 0:

                    response.append(
                        "   Status: DUE TODAY"
                    )

                else:

                    response.append(
                        f"   Due in "
                        f"{days} days"
                    )

            else:

                response.append(
                    "   No deadline set"
                )

            if item["unfinished_tasks"]:

                next_task = (
                    item["unfinished_tasks"][0]
                )

                response.append(
                    f"   Next action: "
                    f"{next_task[1].strip()}"
                )

            else:

                response.append(
                    "   Action: Break this "
                    "goal into tasks."
                )

        # =================================
        # MAIN RECOMMENDATION
        # =================================

        top = active_goals[0]

        response.append(
            "\nMAIN RECOMMENDATION"
        )

        response.append(
            "-------------------"
        )

        response.append(
            f"\nFocus on: "
            f"{top['goal']}"
        )

        days = top["days_remaining"]

        if days is not None:

            if days < 0:

                response.append(
                    "Reason: This goal is overdue."
                )

            elif days == 0:

                response.append(
                    "Reason: This goal is due today."
                )

            elif days <= 7:

                response.append(
                    f"Reason: This goal is due "
                    f"in {days} days."
                )

            else:

                response.append(
                    f"Reason: This goal is due "
                    f"in {days} days."
                )

        else:

            response.append(
                "Reason: This goal has no "
                "deadline but requires attention."
            )

        if top["unfinished_tasks"]:

            next_task = (
                top["unfinished_tasks"][0]
            )

            response.append(
                f"Start with: "
                f"{next_task[1].strip()}"
            )

        else:

            response.append(
                "Start by breaking this "
                "goal into smaller tasks."
            )

        response.append(
            "\n===================="
        )

        return "\n".join(response)

    # =================================
    # STRUCTURED RECOMMENDATIONS
    # =================================

    def get_recommendations(self, goals):

        if not goals:
            return []

        today = datetime.now().date()

        recommendations = []

        for goal in goals:

            if goal["completed"]:
                continue

            due_date = None

            if goal["due_date"]:

                try:
                    due_date = datetime.strptime(
                        goal["due_date"],
                        "%Y-%m-%d"
                    ).date()

                except ValueError:
                    due_date = None

            days_remaining = None

            if due_date:

                days_remaining = (
                    due_date - today
                ).days

            unfinished_tasks = [
                task
                for task in goal["tasks"]
                if task[2] == 0
            ]

            # =================================
            # DETERMINE URGENCY
            # =================================

            if days_remaining is not None:

                if days_remaining < 0:

                    urgency = "HIGH"
                    reason = "OVERDUE"

                elif days_remaining == 0:

                    urgency = "HIGH"
                    reason = "DUE TODAY"

                elif days_remaining <= 3:

                    urgency = "HIGH"
                    reason = (
                        f"DUE IN "
                        f"{days_remaining} DAYS"
                    )

                elif days_remaining <= 7:

                    urgency = "MEDIUM"
                    reason = (
                        f"DUE IN "
                        f"{days_remaining} DAYS"
                    )

                else:

                    urgency = "LOW"
                    reason = "UPCOMING"

            else:

                urgency = "MEDIUM"
                reason = "NO DEADLINE"

            # =================================
            # DETERMINE ACTION
            # =================================

            if unfinished_tasks:

                action = (
                    unfinished_tasks[0][1].strip()
                )

            else:

                action = (
                    "Break this goal into "
                    "smaller tasks."
                )

            recommendations.append(
                {
                    "goal_id": goal["id"],
                    "goal": goal["goal"],
                    "priority": goal["priority"],
                    "due_date": goal["due_date"],
                    "days_remaining": days_remaining,
                    "urgency": urgency,
                    "reason": reason,
                    "action": action
                }
            )

        # =================================
        # SORT RECOMMENDATIONS
        # =================================

        urgency_order = {
            "HIGH": 1,
            "MEDIUM": 2,
            "LOW": 3
        }

        recommendations.sort(
            key=lambda item: (
                urgency_order[
                    item["urgency"]
                ],
                item["priority"],
                item["days_remaining"]
                if item["days_remaining"] is not None
                else 9999
            )
        )

        return recommendations