from agent.database import get_connection
from datetime import datetime


class AccountabilityAgent:

    # ==============================
    # GOALS
    # ==============================

    def add_goal(self, goal, due_date=None, priority=3):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO goals
            (goal, due_date, priority)
            VALUES (?, ?, ?)
            """,
            (goal, due_date, priority)
        )

        connection.commit()
        connection.close()

    def show_goals(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                goal,
                completed,
                due_date,
                priority
            FROM goals
            ORDER BY id
            """
        )

        goals = cursor.fetchall()

        if not goals:
            print("\nNo goals added yet.")
            connection.close()
            return

        print("\nYour Goals:")

        for (
            goal_id,
            goal,
            completed,
            due_date,
            priority
        ) in goals:

            status = "✓" if completed else "○"

            print(
                f"{goal_id}. {status} {goal}"
            )

            print(
                f"   Priority: "
                f"{self._priority_name(priority)}"
            )

            if due_date:
                print(
                    f"   Due: {due_date}"
                )

                if not completed:
                    self._show_deadline_status(
                        due_date
                    )

            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    SUM(
                        CASE
                            WHEN completed = 1
                            THEN 1
                            ELSE 0
                        END
                    )
                FROM tasks
                WHERE goal_id = ?
                """,
                (goal_id,)
            )

            total_tasks, completed_tasks = cursor.fetchone()

            completed_tasks = completed_tasks or 0

            if total_tasks == 0:

                print(
                    "   No tasks yet."
                )

            else:

                progress = int(
                    (
                        completed_tasks
                        / total_tasks
                    ) * 100
                )

                print(
                    f"   Progress: "
                    f"{completed_tasks}/"
                    f"{total_tasks} "
                    f"tasks complete "
                    f"({progress}%)"
                )

                if completed_tasks == total_tasks:

                    print(
                        "   Status: "
                        "READY TO COMPLETE"
                    )

                else:

                    print(
                        "   Status: IN PROGRESS"
                    )

        connection.close()

    def complete_goal(self, goal_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE goals
            SET completed = 1
            WHERE id = ?
            """,
            (goal_id,)
        )

        connection.commit()
        connection.close()

    def delete_goal(self, goal_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM tasks
            WHERE goal_id = ?
            """,
            (goal_id,)
        )

        cursor.execute(
            """
            DELETE FROM goals
            WHERE id = ?
            """,
            (goal_id,)
        )

        connection.commit()
        connection.close()

    # ==============================
    # TASKS
    # ==============================

    def add_task(
        self,
        goal_id,
        task,
        due_date=None
    ):
        connection = get_connection()
        cursor = connection.cursor()

        # Make sure the goal exists
        cursor.execute(
            """
            SELECT id
            FROM goals
            WHERE id = ?
            """,
            (goal_id,)
        )

        goal = cursor.fetchone()

        if not goal:
            connection.close()
            return False

        cursor.execute(
            """
            INSERT INTO tasks
            (goal_id, task, due_date)
            VALUES (?, ?, ?)
            """,
            (
                goal_id,
                task,
                due_date
            )
        )

        connection.commit()
        connection.close()

        return True

    def show_tasks(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                tasks.id,
                tasks.task,
                tasks.completed,
                tasks.due_date,
                goals.goal
            FROM tasks
            JOIN goals
                ON tasks.goal_id = goals.id
            ORDER BY tasks.id
            """
        )

        tasks = cursor.fetchall()

        connection.close()

        if not tasks:

            print(
                "\nNo tasks added yet."
            )

            return

        print("\nYour Tasks:")

        for (
            task_id,
            task,
            completed,
            due_date,
            goal
        ) in tasks:

            status = "✓" if completed else "○"

            print(
                f"{task_id}. "
                f"{status} {task} "
                f"[Goal: {goal}]"
            )

            if due_date:

                print(
                    f"   Due: {due_date}"
                )

                if not completed:

                    self._show_deadline_status(
                        due_date
                    )

    def complete_task(self, task_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE tasks
            SET completed = 1
            WHERE id = ?
            """,
            (task_id,)
        )

        connection.commit()
        connection.close()

    def delete_task(self, task_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = ?
            """,
            (task_id,)
        )

        connection.commit()
        connection.close()

    def move_task(self, task_id, new_goal_id):

        connection = get_connection()
        cursor = connection.cursor()

        # Check that the task exists
        cursor.execute(
            """
            SELECT id
            FROM tasks
            WHERE id = ?
            """,
            (task_id,)
        )

        task = cursor.fetchone()

        if not task:
            connection.close()
            return False

        # Check that the new goal exists
        cursor.execute(
            """
            SELECT id
            FROM goals
            WHERE id = ?
            """,
            (new_goal_id,)
        )

        goal = cursor.fetchone()

        if not goal:
            connection.close()
            return False

        # Move the task
        cursor.execute(
            """
            UPDATE tasks
            SET goal_id = ?
            WHERE id = ?
            """,
            (
                new_goal_id,
                task_id
            )
        )

        connection.commit()
        connection.close()

        return True

    # ==============================
    # ACCOUNTABILITY REPORT
    # ==============================

    def accountability_report(self):

        connection = get_connection()
        cursor = connection.cursor()

        today = datetime.now().date()

        print("\n================================")
        print("     ACCOUNTABILITY REPORT")
        print("================================")

        cursor.execute(
            """
            SELECT
                id,
                goal,
                completed,
                due_date,
                priority
            FROM goals
            ORDER BY id
            """
        )

        goals = cursor.fetchall()

        if not goals:

            print(
                "\nNo goals found."
            )

            connection.close()
            return

        overdue = []
        due_today = []
        upcoming = []
        incomplete = []
        ready = []

        total_tasks = 0
        completed_tasks = 0

        for (
            goal_id,
            goal,
            completed,
            due_date,
            priority
        ) in goals:

            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    SUM(
                        CASE
                            WHEN completed = 1
                            THEN 1
                            ELSE 0
                        END
                    )
                FROM tasks
                WHERE goal_id = ?
                """,
                (goal_id,)
            )

            task_count, completed_count = cursor.fetchone()

            completed_count = completed_count or 0

            total_tasks += task_count
            completed_tasks += completed_count

            if due_date and not completed:

                try:

                    due = datetime.strptime(
                        due_date,
                        "%Y-%m-%d"
                    ).date()

                    days_remaining = (
                        due - today
                    ).days

                    if days_remaining < 0:

                        overdue.append(
                            (goal, due_date)
                        )

                    elif days_remaining == 0:

                        due_today.append(
                            (goal, due_date)
                        )

                    elif days_remaining <= 7:

                        upcoming.append(
                            (
                                goal,
                                due_date,
                                days_remaining
                            )
                        )

                except ValueError:
                    pass

            if not completed:

                if (
                    task_count > 0
                    and completed_count
                    == task_count
                ):

                    ready.append(
                        (
                            goal,
                            completed_count,
                            task_count
                        )
                    )

                elif task_count > 0:

                    incomplete.append(
                        (
                            goal,
                            completed_count,
                            task_count
                        )
                    )

        print("\nOVERDUE")

        if overdue:

            for goal, due_date in overdue:

                print(
                    f"   {goal} "
                    f"(Due: {due_date})"
                )

        else:

            print("   None")

        print("\nDUE TODAY")

        if due_today:

            for goal, due_date in due_today:

                print(
                    f"   {goal} "
                    f"(Due: {due_date})"
                )

        else:

            print("   None")

        print("\nUPCOMING")

        if upcoming:

            for (
                goal,
                due_date,
                days_remaining
            ) in upcoming:

                print(
                    f"   {goal} "
                    f"(Due: {due_date}, "
                    f"{days_remaining} days)"
                )

        else:

            print("   None")

        print("\nNEEDS ATTENTION")

        if incomplete:

            for (
                goal,
                completed_count,
                task_count
            ) in incomplete:

                progress = int(
                    (
                        completed_count
                        / task_count
                    ) * 100
                )

                print(
                    f"   {goal}: "
                    f"{completed_count}/"
                    f"{task_count} "
                    f"tasks complete "
                    f"({progress}%)"
                )

        else:

            print("   None")

        print("\nREADY TO COMPLETE")

        if ready:

            for (
                goal,
                completed_count,
                task_count
            ) in ready:

                print(
                    f"   {goal}: "
                    f"{completed_count}/"
                    f"{task_count} "
                    f"tasks complete "
                    f"(100%)"
                )

        else:

            print("   None")

        print("\nOVERALL PROGRESS")

        if total_tasks > 0:

            progress = int(
                (
                    completed_tasks
                    / total_tasks
                ) * 100
            )

            print(
                f"   {completed_tasks}/"
                f"{total_tasks} "
                f"tasks complete "
                f"({progress}%)"
            )

        else:

            print(
                "   No tasks recorded."
            )

        print(
            "\n================================"
        )

        connection.close()
    def get_accountability_data(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                goal,
                completed,
                due_date,
                priority
            FROM goals
            WHERE completed = 0
            ORDER BY id
            """
        )

        goals = cursor.fetchall()

        data = []

        for (
            goal_id,
            goal,
            completed,
            due_date,
            priority
        ) in goals:

            cursor.execute(
                """
                SELECT
                    id,
                    task,
                    completed,
                    due_date
                FROM tasks
                WHERE goal_id = ?
                ORDER BY id
                """,
                (goal_id,)
            )

            tasks = cursor.fetchall()

            data.append(
                {
                    "id": goal_id,
                    "goal": goal,
                    "completed": completed,
                    "due_date": due_date,
                    "priority": priority,
                    "tasks": tasks
                }
            )

        connection.close()

        return data
    # ==============================
    # TODAY'S PLAN
    # ==============================

    def daily_plan(self):

        connection = get_connection()
        cursor = connection.cursor()

        today = datetime.now().date()

        print("\n================================")
        print("          TODAY'S PLAN")
        print("================================")

        cursor.execute(
            """
            SELECT
                id,
                goal,
                due_date,
                priority
            FROM goals
            WHERE completed = 0
            """
        )

        goals = cursor.fetchall()

        priorities = []

        for (
            goal_id,
            goal,
            due_date,
            priority
        ) in goals:

            cursor.execute(
                """
                SELECT
                    id,
                    task,
                    due_date
                FROM tasks
                WHERE goal_id = ?
                AND completed = 0
                ORDER BY id
                """,
                (goal_id,)
            )

            tasks = cursor.fetchall()

            days_remaining = None

            if due_date:

                try:

                    goal_due = datetime.strptime(
                        due_date,
                        "%Y-%m-%d"
                    ).date()

                    days_remaining = (
                        goal_due - today
                    ).days

                except ValueError:

                    days_remaining = None

            # Calculate score.
            #
            # Lower score = higher priority.
            #
            # User priority:
            # Critical = 1
            # High = 2
            # Normal = 3
            # Low = 4

            score = priority

            # Deadline adjustment
            if days_remaining is not None:

                if days_remaining < 0:

                    score -= 4

                elif days_remaining == 0:

                    score -= 4

                elif days_remaining <= 3:

                    score -= 3

                elif days_remaining <= 7:

                    score -= 2

                elif days_remaining <= 14:

                    score -= 1

            # Goals with unfinished tasks
            # are more actionable.
            if tasks:

                score -= 1

            if score < 1:

                score = 1

            priorities.append(
                (
                    score,
                    priority,
                    goal,
                    due_date,
                    days_remaining,
                    tasks
                )
            )

        priorities.sort(
            key=lambda item: (
                item[0],
                item[5] == []
            )
        )

        if not priorities:

            print(
                "\nNo incomplete goals."
            )

            print(
                "Everything is currently complete."
            )

            connection.close()
            return

        print("\nPRIORITIES")

        position = 1

        for (
            score,
            priority,
            goal,
            due_date,
            days_remaining,
            tasks
        ) in priorities:

            print(
                f"\n{position}. {goal}"
            )

            print(
                f"   Priority: "
                f"{self._priority_name(priority)}"
            )

            if due_date:

                if days_remaining < 0:

                    print(
                        "   STATUS: OVERDUE"
                    )

                elif days_remaining == 0:

                    print(
                        "   STATUS: DUE TODAY"
                    )

                else:

                    print(
                        f"   Due: {due_date}"
                    )

                    print(
                        f"   {days_remaining} "
                        f"days remaining"
                    )

            else:

                print(
                    "   No deadline set"
                )

            if tasks:

                print(
                    "   NEXT TASK:"
                )

                task_id, task, task_due = tasks[0]

                print(
                    f"   - {task}"
                )

                if task_due:

                    print(
                        f"     Task due: "
                        f"{task_due}"
                    )

            else:

                print(
                    "   No incomplete tasks"
                )

            position += 1

        # ------------------------------
        # Recommendation
        # ------------------------------

        top = priorities[0]

        (
            score,
            priority,
            goal,
            due_date,
            days_remaining,
            tasks
        ) = top

        print("\n================================")
        print("RECOMMENDATION")
        print("================================")

        print(
            f"Focus on: {goal}"
        )

        print(
            f"Priority: "
            f"{self._priority_name(priority)}"
        )

        if days_remaining is not None:

            if days_remaining < 0:

                print(
                    "This goal is overdue."
                )

            elif days_remaining == 0:

                print(
                    "This goal is due today."
                )

            elif days_remaining <= 7:

                print(
                    f"This goal is due in "
                    f"{days_remaining} days."
                )

        if tasks:

            print(
                f"Start with: "
                f"{tasks[0][1]}"
            )

        else:

            print(
                "Create a task for this goal."
            )

        print(
            "================================"
        )

        connection.close()

    # ==============================
    # HELPERS
    # ==============================

    def _priority_name(self, priority):

        names = {
            1: "CRITICAL",
            2: "HIGH",
            3: "NORMAL",
            4: "LOW"
        }

        return names.get(
            priority,
            "NORMAL"
        )

    def _show_deadline_status(self, due_date):

        try:

            due = datetime.strptime(
                due_date,
                "%Y-%m-%d"
            ).date()

            today = datetime.now().date()

            if due < today:

                print(
                    "   STATUS: OVERDUE"
                )

            elif due == today:

                print(
                    "   STATUS: DUE TODAY"
                )

            else:

                days_remaining = (
                    due - today
                ).days

                print(
                    f"   Days remaining: "
                    f"{days_remaining}"
                )

        except ValueError:

            print(
                "   STATUS: INVALID DATE"
            )
        # ==============================
    # ACTIONABLE RECOMMENDATIONS
    # ==============================

    def get_actionable_recommendations(self):

        connection = get_connection()
        cursor = connection.cursor()

        today = datetime.now().date()

        print("\n================================")
        print("     ACTIONABLE RECOMMENDATIONS")
        print("================================")

        cursor.execute(
            """
            SELECT
                id,
                goal,
                completed,
                due_date,
                priority
            FROM goals
            WHERE completed = 0
            """
        )

        goals = cursor.fetchall()

        recommendations = []

        for (
            goal_id,
            goal,
            completed,
            due_date,
            priority
        ) in goals:

            cursor.execute(
                """
                SELECT
                    id,
                    task,
                    completed,
                    due_date
                FROM tasks
                WHERE goal_id = ?
                AND completed = 0
                ORDER BY id
                """,
                (goal_id,)
            )

            tasks = cursor.fetchall()

            days_remaining = None

            if due_date:

                try:

                    due = datetime.strptime(
                        due_date,
                        "%Y-%m-%d"
                    ).date()

                    days_remaining = (
                        due - today
                    ).days

                except ValueError:

                    days_remaining = None

            # --------------------------------
            # CASE 1: Goal has no tasks
            # --------------------------------

            if not tasks:

                if (
                    priority <= 2
                    or (
                        days_remaining is not None
                        and days_remaining <= 7
                    )
                ):

                    recommendations.append(
                        {
                            "type": "BREAKDOWN",
                            "goal": goal,
                            "due_date": due_date,
                            "priority": priority,
                            "days_remaining": days_remaining
                        }
                    )

            # --------------------------------
            # CASE 2: Goal has unfinished tasks
            # --------------------------------

            else:

                first_task = tasks[0]

                recommendations.append(
                    {
                        "type": "NEXT_TASK",
                        "goal": goal,
                        "task": first_task[1],
                        "task_due": first_task[3],
                        "due_date": due_date,
                        "priority": priority,
                        "days_remaining": days_remaining
                    }
                )

        # --------------------------------
        # Display recommendations
        # --------------------------------

        if not recommendations:

            print(
                "\nNo immediate recommendations."
            )

            connection.close()
            return

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            print(
                f"\n{index}. "
                f"{recommendation['goal']}"
            )
            print(
    f"   Priority: "
    f"{self._priority_name(recommendation['priority'])}"
)


            if recommendation["due_date"]:

                print(
                    f"   Due: "
                    f"{recommendation['due_date']}"
                )

            if recommendation["type"] == "BREAKDOWN":

                print(
                    "   ACTION: "
                    "Break this goal into tasks."
                )

                if (
                    recommendation["days_remaining"]
                    is not None
                ):

                    if (
                        recommendation["days_remaining"]
                        < 0
                    ):

                        print(
                            "   REASON: "
                            "Goal is overdue."
                        )

                    elif (
                        recommendation["days_remaining"]
                        == 0
                    ):

                        print(
                            "   REASON: "
                            "Goal is due today."
                        )

                    else:

                        print(
                            "   REASON: "
                            f"Due in "
                            f"{recommendation['days_remaining']} "
                            f"days."
                        )

            elif recommendation["type"] == "NEXT_TASK":

                print(
                    f"   NEXT ACTION: "
                    f"{recommendation['task']}"
                )

                if recommendation["task_due"]:

                    print(
                        f"   Task due: "
                        f"{recommendation['task_due']}"
                    )

        print(
            "\n================================"
        )

        connection.close()
