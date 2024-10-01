import os
from backend.interfaces.file_handler_interface import FileHandlerInterface

class LocalFileHandler(FileHandlerInterface):
    def write(self, file_path: str, data: bytes) -> None:
        """Escreve os dados binários no arquivo especificado."""
        with open(file_path, "wb") as file:
            file.write(data)

    def read(self, file_path: str) -> bytes:
        """Lê os dados binários de um arquivo."""
        with open(file_path, "rb") as file:
            return file.read()

    def remove(self, file_path: str) -> None:
        """Remove o arquivo especificado."""
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"O arquivo '{file_path}' não foi encontrado.")
