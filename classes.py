import json

class Transcript:
    def __init__(self, id, status, summary = None):
        self.id = id
        self.status = status
        self.summary = summary

    def __str__(self) -> str:
        return json.dumps(self.__dict__, indent=4)
        