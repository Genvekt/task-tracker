from task_admin.auth.models import User
from task_admin.db.repository import TaskRepository
from task_admin.tasks.models import Task, TaskStatus


def insert_user(db_session) -> User:
    db_session.execute(
        "INSERT INTO users (id, name, public_id, email) VALUES "
        "(1, 'lupa', 2, 'lupa@mail.com')"
    )
    return db_session.query(User).filter_by(name='lupa').first()

def insert_task(db_session, user) -> Task:
    db_session.execute(
        "INSERT INTO tasks (id, title, description, status, user_id) VALUES "
        f"(1, 'lupa_task', 'lupa special task','Done', {user.id})"
    )
    return db_session.query(Task).filter_by(id=1).first()


def test_repository_can_save_a_task(db_session):
    user = insert_user(db_session)
    task = Task(
        title="super_task",
        description="super puper task",
        assignee=user
    )

    repo = TaskRepository(session=db_session)
    repo.add(task)
    db_session.commit()

    rows = db_session.execute(
        "SELECT title, description, status, user_id FROM tasks"
    )
    assert list(rows) == [("super_task", "super puper task", "In Progress", 1)]


def test_repository_can_retrieve_a_task_with_user(db_session):
    user = insert_user(db_session)
    insert_task(db_session, user)

    repo = TaskRepository(session=db_session)
    retrieved_task = repo.get(id=1)

    expected = Task(
        title='lupa_task',
        description='lupa special task',
        status=TaskStatus.done,
        assignee=user
    )

    assert retrieved_task == expected
