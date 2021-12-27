from pinata.session import PinataAPISession


class PinataClient:
    def __init__(self, session: PinataAPISession):
        self.session = session


__all__ = ["PinataClient"]
