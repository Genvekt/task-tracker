### Roles in the system
- Admin: Superuser, has access everywhere
- Manager: Has access to accounting and tasks. Can reassign tasks.
- Accountant: Has access to accounting and tasks.
- Worker: Has access to tasks.

### Task-admin API endpoints

| Endpoint               | Method | URL Params                            | Roles             | Description                      |
|------------------------|--------|---------------------------------------|-------------------|----------------------------------|
| `/api/tasks`           | GET    | filter<br/>sort<br/>page<br/>per_page | *                 | Read task list                   |
| `/api/tasks`           | POST   |                                       | *                 | Create task                      |
| `/api/tasks/reassign`  | POST   |                                       | admin<br/>manager | Reassign all open tasks randomly |
| `/api/tasks/<task_id>` | GET    |                                       | *                 | Read task                        |
| `/api/tasks/<task_id>` | PUT    |                                       | *                 | Update task                      |
| `/api/tasks/<task_id>` | DELETE |                                       | *                 | Delete task                      |


### Accounting API endpoints

| Endpoint                     | Method | URL Params                            | Roles                            | Description                   |
|------------------------------|--------|---------------------------------------|----------------------------------|-------------------------------|
| `/api/journal`               | GET    | filter<br/>sort<br/>page<br/>per_page | admin<br/>manager<br/>accountant | Read journal entries          |
| `/api/accounts`              | GET    | filter<br/>sort<br/>page<br/>per_page | admin<br/>manager<br/>accountant | Read the list of all accounts |
| `/api/accounts/<account_id>` | GET    |                                       | admin<br/>manager<br/>accountant | Read account                  |

### Analytics API endpoints

| Endpoint                     | Method | URL Params | Roles | Description         |
|------------------------------|--------|------------|-------|---------------------|
| `/api/dashboard`             | GET    |            | admin | Read dashboard data |