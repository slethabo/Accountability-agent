from datetime import datetime


class AccountabilityAI:

    def __init__(self):
        pass

    # ==============================
    # GET RECOMMENDATIONS
    # ==============================

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

            tasks = goal["tasks"]

            unfinished_tasks = [
                task
                for task in tasks
                if task[2] == 0
            ]

            # ------------------------------
            # Calculate urgency score
            # ------------------------------

            score = goal["priority"]

            if days_remaining is not None:

                if days_remaining < 0:
                    score -= 10

                elif days_remaining == 0:
                    score -= 9

                elif days_remaining <= 3:
                    score -= 7

                elif days_remaining <= 7:
                    score -= 5

                elif days_remaining <= 14:
                    score -= 2

            if unfinished_tasks:
                score -= 1

            recommendations.append(
                {
                    "goal": goal["goal"],
                    "priority": goal["priority"],
                    "due_date": goal["due_date"],
                    "days_remaining": days_remaining,
                    "tasks": tasks,
                    "unfinished_tasks": unfinished_tasks,
                    "score": score
                }
            )

        recommendations.sort(
            key=lambda item: item["score"]
        )

        return recommendations

    # ==============================
    # ANALYZE
    # ==============================

    def analyze(self, goals):

        if not goals:

            return (
                "ACCOUNTABILITY CHECK\n"
                "====================\n\n"
                "You currently have no active goals.\n"
                "Add a goal to get started."
            )

        recommendations = self.get_recommendations(
            goals
        )

        if not recommendations:

            return (
                "ACCOUNTABILITY CHECK\n"
                "====================\n\n"
                "You currently have no active goals."
            )

        total_tasks = 0
        completed_tasks = 0

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

        response = []

        response.append(
            "ACCOUNTABILITY CHECK"
        )

        response.append(
            "===================="
        )

        response.append(
            f"\nActive goals: "
            f"{len(recommendations)}"
        )

        response.append(
            f"Tasks completed: "
            f"{completed_tasks}/"
            f"{total_tasks}"
        )

        # ==============================
        # PRIORITY CHECK
        # ==============================

        response.append(
            "\nPRIORITY CHECK"
        )

        response.append(
            "--------------"
        )

        for index, item in enumerate(
            recommendations[:3],
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
                    f"{next_task[1]}"
                )

            else:

                response.append(
                    "   Action: Break this "
                    "goal into tasks."
                )

        # ==============================
        # MAIN RECOMMENDATION
        # ==============================

        top = recommendations[0]

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

        if top["unfinished_tasks"]:

            next_task = (
                top["unfinished_tasks"][0]
            )

            response.append(
                f"Start with: "
                f"{next_task[1]}"
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
        # ==============================
    # NATURAL LANGUAGE QUERY
    # ==============================

    def respond_to_query(self, query, goals):

        query = query.lower().strip()

        recommendations = self.get_recommendations(
            goals
        )

        if not recommendations:

            return (
                "You currently have no active goals."
            )

        # ------------------------------
        # What should I work on?
        # ------------------------------

        if (
            "what should i work on" in query
            or "what should i do" in query
            or "what do i work on" in query
        ):

            top = recommendations[0]

            response = (
                f"Focus on: {top['goal']}\n"
            )

            days = top["days_remaining"]

            if days is not None:

                if days < 0:

                    response += (
                        "This goal is overdue.\n"
                    )

                elif days == 0:

                    response += (
                        "This goal is due today.\n"
                    )

                elif days <= 7:

                    response += (
                        f"This goal is due "
                        f"in {days} days.\n"
                    )

            if top["unfinished_tasks"]:

                next_task = (
                    top["unfinished_tasks"][0]
                )

                response += (
                    f"Start with: "
                    f"{next_task[1]}"
                )

            else:

                response += (
                    "Start by breaking this "
                    "goal into smaller tasks."
                )

            return response

        # ------------------------------
        # What's overdue?
        # ------------------------------

        if (
            "what is overdue" in query
            or "what's overdue" in query
            or "overdue" in query
        ):

            overdue = []

            for item in recommendations:

                days = item["days_remaining"]

                if days is not None and days < 0:

                    overdue.append(item)

            if not overdue:

                return "You currently have no overdue goals."

            response = "OVERDUE GOALS\n\n"

            for item in overdue:

                response += (
                    f"- {item['goal']}\n"
                )

            return response.rstrip()

        # ------------------------------
        # How am I doing?
        # ------------------------------

        if (
            "how am i doing" in query
            or "my progress" in query
            or "how am i progressing" in query
        ):

            total_tasks = 0
            completed_tasks = 0

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

            if total_tasks == 0:

                progress = 0

            else:

                progress = int(
                    (
                        completed_tasks
                        / total_tasks
                    ) * 100
                )

            return (
                f"You have "
                f"{completed_tasks}/"
                f"{total_tasks} tasks complete "
                f"({progress}%)."
            )

        # ------------------------------
        # Unknown query
        # ------------------------------

        return (
            "I don't understand that yet.\n"
            "Try asking:\n"
            "- What should I work on?\n"
            "- What's overdue?\n"
            "- How am I doing?"
        )