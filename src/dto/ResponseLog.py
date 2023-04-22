class ResponseLog:
    def __init__(self, log_id, remote_id, date, user_id, action, name, email):
        self.log_id = log_id
        self.remote_id = remote_id
        self.date = date
        self.user_id = user_id
        self.action = action

        self.name = name
        self.email = email

    def get_json(self) -> dict:
        return {'log_id': self.log_id,
                'remote_id': self.remote_id,
                'date': self.date,
                'user_id': self.user_id,
                'action': self.action,
                'name': self.name,
                'email': self.email}