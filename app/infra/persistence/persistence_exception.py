class PersistenceException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class RecordNotFoundException(PersistenceException):
    def __init__(self) -> None:
        super().__init__("Requested resource not found with passed query parameters")
