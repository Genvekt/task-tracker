### Accounting API endpoints

| Endpoint                     | Method | URL Params                            | Roles                            | Description                   | Ready |
|------------------------------|--------|---------------------------------------|----------------------------------|-------------------------------|-------|
| `/api/journal`               | GET    | filter<br/>sort<br/>page<br/>per_page | admin<br/>manager<br/>accountant | Read journal entries          | 👌    |
| `/api/accounts`              | GET    | filter<br/>sort<br/>page<br/>per_page | admin<br/>manager<br/>accountant | Read the list of all accounts | ❌     |
| `/api/accounts/<account_id>` | GET    |                                       | admin<br/>manager<br/>accountant | Read account                  | ❌     |
