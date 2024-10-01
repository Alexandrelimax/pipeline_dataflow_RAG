from abc import ABC, abstractmethod
from fastapi import APIRouter

class BaseController(ABC):
    router: APIRouter

    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)
        self.register_routes()

    @abstractmethod
    def register_routes(self):
        pass
