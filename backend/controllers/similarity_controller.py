from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from backend.interfaces.similarity_interface import ISimilarity
from base_controller import BaseController

class SimilaritySearchController(BaseController):
    def __init__(self, similarity_service: ISimilarity):
        self.similarity_service = similarity_service
        super().__init__(prefix="/similarity")  # Chama o construtor da classe Base

    def register_routes(self):
        self.router.add_api_route("/document", self.search_document_with_document, methods=["POST"])
        self.router.add_api_route("/text", self.search_document_with_text, methods=["POST"])

    async def search_document_with_document(self, file: UploadFile = File(...)) -> JSONResponse:
        try:
            document_data = await file.read()
            response = await self.similarity_service.process_document(document_data, file.filename)
            return JSONResponse(content={"response": response})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def search_document_with_text(self, text: str) -> JSONResponse:
        try:
            response = await self.similarity_service.process_text(text)
            return JSONResponse(content={"response": response})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
