def todo_manager(todo_list, tasks, actions):
    # Add tasks
    for task in tasks:
        todo_list.append([task, "pending"])
        print(f"➕ Added: {task}")

    # Remove tasks
    if actions.get('remove'):
        for task in actions['remove']:
            todo_list[:] = [t for t in todo_list if t[0] != task]
            print(f"❌ Removed: {task}")

    # Complete tasks
    if actions.get('complete'):
        for task in todo_list:
            if task[0] in actions['complete']:
                task[1] = "done"
                print(f"✅ Completed: {task[0]}")

    # Display tasks
    print("\n📋 Current Tasks:")
    for task, status in todo_list:
        print(f"{task} - {status}")

todo_list = []

tasks = ["Study", "Workout", "Read"]
actions = {
    "remove": ["Workout"],
    "complete": ["Study"]
}

todo_manager(todo_list, tasks, actions)