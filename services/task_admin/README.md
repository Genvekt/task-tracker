### Roles in the system
- Admin: Superuser, has access everywhere
- Manager: Has access to accounting and tasks. Can reassign tasks.
- Accountant: Has access to accounting and tasks.
- Worker: Has access to tasks.

### Task-admin API endpoints

| Endpoint               | Method | URL Params                            | Roles             | Description                      | Ready |
|------------------------|--------|---------------------------------------|-------------------|----------------------------------|-------|
| `/api/tasks`           | GET    | filter<br/>sort<br/>page<br/>per_page | *                 | Read task list                   | 👌    |
| `/api/tasks`           | POST   |                                       | *                 | Create task                      | ✅     |
| `/api/tasks/reassign`  | POST   |                                       | admin<br/>manager | Reassign all open tasks randomly | ✅     |
| `/api/tasks/<task_id>` | GET    |                                       | *                 | Read task                        | ✅     |
| `/api/tasks/<task_id>` | PUT    |                                       | *                 | Update task                      | ✅     |
| `/api/tasks/<task_id>` | DELETE |                                       | *                 | Delete task                      | ❌     |

### Analytics API endpoints

| Endpoint                     | Method | URL Params | Roles | Description         | Ready |
|------------------------------|--------|------------|-------|---------------------|-------|
| `/api/dashboard`             | GET    |            | admin | Read dashboard data | ❌     |