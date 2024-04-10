from ..model import SESSION_LOCAL, Log

session = SESSION_LOCAL()


def log_action(action, data):
    log_entry = Log(action=action, data=str(data))
    session.add(log_entry)
    session.commit()
