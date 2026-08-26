from agent.database import initialize_database
from agent.core import AccountabilityAgent
from agent.ai import AccountabilityAI


initialize_database()

agent = AccountabilityAgent()
ai = AccountabilityAI()


while True:
    print("\n================================")
    print("     ACCOUNTABILITY AGENT")
    print("================================")

    print("1. Add goal")
    print("2. View goals")
    print("3. Complete goal")
    print("4. Delete goal")
    print("5. Add task")
    print("6. View tasks")
    print("7. Complete task")
    print("8. Delete task")
    print("9. Move task")
    print("10. Today's plan")
    print("11. Actionable recommendations")
    print("12. Accountability report")
    print("13. Exit")


    

    choice = input("\nChoose an option: ")

    # ==============================
    # ADD GOAL
    # ==============================

    if choice == "1":

        goal = input(
            "Enter your goal: "
        )

        due_date = input(
            "Enter due date (YYYY-MM-DD), "
            "or press Enter to skip: "
        )

        if not due_date.strip():
            due_date = None

        print(
            "\nPriority:"
        )

        print(
            "1. Critical"
        )

        print(
            "2. High"
        )

        print(
            "3. Normal"
        )

        print(
            "4. Low"
        )

        priority = input(
            "Choose priority (1-4): "
        )

        if not priority.isdigit():

            priority = 3

        else:

            priority = int(priority)

            if priority not in [1, 2, 3, 4]:

                priority = 3

        agent.add_goal(
            goal,
            due_date,
            priority
        )

        print(
            "Goal added successfully."
        )

    # ==============================
    # VIEW GOALS
    # ==============================

    elif choice == "2":

        agent.show_goals()

    # ==============================
    # COMPLETE GOAL
    # ==============================

    elif choice == "3":

        agent.show_goals()

        goal_id = input(
            "\nEnter the ID of the goal "
            "you completed: "
        )

        if goal_id.isdigit():

            agent.complete_goal(
                int(goal_id)
            )

            print(
                "Goal marked as complete."
            )

        else:

            print(
                "Please enter a valid "
                "goal ID."
            )

    # ==============================
    # DELETE GOAL
    # ==============================

    elif choice == "4":

        agent.show_goals()

        goal_id = input(
            "\nEnter the ID of the goal "
            "you want to delete: "
        )

        if goal_id.isdigit():

            agent.delete_goal(
                int(goal_id)
            )

            print(
                "Goal deleted successfully."
            )

        else:

            print(
                "Please enter a valid "
                "goal ID."
            )

    # ==============================
    # ADD TASK
    # ==============================

    elif choice == "5":

        agent.show_goals()

        goal_id = input(
            "\nEnter the ID of the goal "
            "this task belongs to: "
        )

        if not goal_id.isdigit():

            print(
                "Please enter a valid "
                "goal ID."
            )

            continue

        task = input(
            "Enter your task: "
        )

        due_date = input(
            "Enter task due date "
            "(YYYY-MM-DD), "
            "or press Enter to skip: "
        )

        if not due_date.strip():

            due_date = None

        success = agent.add_task(
            int(goal_id),
            task,
            due_date
        )

        if success:

            print(
                "Task added successfully."
            )

        else:

            print(
                "Goal not found. "
                "Task was not added."
            )

    # ==============================
    # VIEW TASKS
    # ==============================

    elif choice == "6":

        agent.show_tasks()

    # ==============================
    # COMPLETE TASK
    # ==============================

    elif choice == "7":

        agent.show_tasks()

        task_id = input(
            "\nEnter the ID of the task "
            "you completed: "
        )

        if task_id.isdigit():

            agent.complete_task(
                int(task_id)
            )

            print(
                "Task marked as complete."
            )

        else:

            print(
                "Please enter a valid "
                "task ID."
            )

    # ==============================
    # DELETE TASK
    # ==============================

    # ==============================
    # DELETE TASK
    # ==============================

    elif choice == "8":

        agent.show_tasks()

        task_id = input(
            "\nEnter the ID of the task "
            "you want to delete: "
        )

        if task_id.isdigit():

            agent.delete_task(
                int(task_id)
            )

            print(
                "Task deleted successfully."
            )

        else:

            print(
                "Please enter a valid task ID."
            )

    # ==============================
    # MOVE TASK
    # ==============================

    elif choice == "9":

        agent.show_tasks()

        task_id = input(
            "\nEnter the ID of the task "
            "you want to move: "
        )

        if not task_id.isdigit():

            print(
                "Please enter a valid task ID."
            )

            continue

        agent.show_goals()

        new_goal_id = input(
            "\nEnter the ID of the goal "
            "you want to move the task to: "
        )

        if not new_goal_id.isdigit():

            print(
                "Please enter a valid goal ID."
            )

            continue

        success = agent.move_task(
            int(task_id),
            int(new_goal_id)
        )

        if success:

            print(
                "Task moved successfully."
            )

        else:

            print(
                "Task or goal not found."
            )

    # ==============================
    # ACCOUNTABILITY REPORT
    # ==============================

    elif choice == "10":

        agent.accountability_report()

    # ==============================
    # TODAY'S PLAN
    # ==============================

    elif choice == "11":

        agent.daily_plan()

    # ==============================
    # ACTIONABLE RECOMMENDATIONS
    # ==============================

    elif choice == "12":

        agent.get_actionable_recommendations()

    # ==============================
    # EXIT
    # ==============================

    elif choice == "13":

        print(
            "Goodbye, Lee."
        )

        break

    # ==============================
    # INVALID OPTION
    # ==============================

    else:

        print(
            "Invalid option. "
            "Please choose 1-13."
        )