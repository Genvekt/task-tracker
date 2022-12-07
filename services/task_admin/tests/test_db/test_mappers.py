from task_admin.auth.models import User
from task_admin.tasks.models import Task


def test_users_mapper_can_load_users(db_session):
    """Check correct mapping from User domain to database."""
    db_session.execute(
        "INSERT INTO users (name) VALUES "
        "('pupa'),"
        "('lupa')"
    )
    expected = [
        User("lupa"),
        User("pupa"),
    ]
    result = db_session.query(User).order_by(User.name).all()
    assert result == expected


def test_tasks_mapper_can_load_tasks(db_session):
    """Check correct mapping from Task domain to database."""
    db_session.execute(
        "INSERT INTO users (id, name) VALUES "
        "(1, 'pupa'),"
        "(2, 'lupa')"
    )
    db_session.execute(
        "INSERT INTO tasks (title, description, status, user_id) VALUES "
        "('pupa_task', 'pupa special task','In Progress', 1),"
        "('lupa_task', 'lupa special task','In Progress', 2)"
    )
    expected = [
        Task(title="pupa_task", description="pupa special task", assignee=User("pupa")),
        Task(title="lupa_task", description="lupa special task", assignee=User("lupa")),
    ]
    result = db_session.query(Task).join(User).order_by(User.name).all()
    assert result == expected
