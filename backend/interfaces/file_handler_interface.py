from abc import ABC, abstractmethod

class FileHandlerInterface(ABC):
    @abstractmethod
    def write(self, file_path: str, data: bytes) -> None:
        """Escreve dados binários em um arquivo."""
        pass

    @abstractmethod
    def read(self, file_path: str) -> bytes:
        """Lê os dados binários de um arquivo."""
        pass

    @abstractmethod
    def remove(self, file_path: str) -> None:
        """Remove o arquivo do sistema."""
        pass
