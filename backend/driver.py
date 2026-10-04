"""
The Driver class manages a session's request state, instances of the VL, facilitates processing business logic etc.
"""


class Driver:
    def __init__(self,session_id: str):
        self.session_id = session_id
        self.vl = None  # Placeholder for the VL instance
        self.state = {}  # Placeholder for request state



