from task_admin.auth.models import User
from task_admin.tasks.models import Task


def test_users_mapper_can_load_users(db_session):
    """Check correct mapping from User domain to database."""
    db_session.execute(
        "INSERT INTO users (name, public_id, email) VALUES "
        "('pupa', 1, 'pupa@mail.com'),"
        "('lupa', 2, 'lupa@mail.com')"
    )
    expected = [
        User(name="lupa", email="lupa@mail.com", public_id=2),
        User(name="pupa", email="pupa@mail.com", public_id=1),
    ]
    result = db_session.query(User).order_by(User.name).all()
    assert result == expected


def test_tasks_mapper_can_load_tasks(db_session):
    """Check correct mapping from Task domain to database."""
    db_session.execute(
        "INSERT INTO users (id, name, public_id, email) VALUES "
        "(1, 'pupa', 1, 'pupa@mail.com'),"
        "(2, 'lupa', 2, 'lupa@mail.com')"
    )
    db_session.execute(
        "INSERT INTO tasks (title, description, status, user_id) VALUES "
        "('pupa_task', 'pupa special task','In Progress', 1),"
        "('lupa_task', 'lupa special task','In Progress', 2)"
    )
    expected = [
        Task(title="lupa_task", description="lupa special task", assignee=User(name="lupa", email="lupa@mail.com", public_id=2)),
        Task(title="pupa_task", description="pupa special task", assignee=User(name="pupa", email="pupa@mail.com", public_id=1)),
    ]
    result = db_session.query(Task).join(User).order_by(User.name).all()

    assert result == expected
