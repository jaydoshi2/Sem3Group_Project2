class EnrollmentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PasswordError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)



