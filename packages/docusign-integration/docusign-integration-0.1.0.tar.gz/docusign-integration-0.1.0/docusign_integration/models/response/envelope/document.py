from typing import List, Optional, Union
from pydantic import BaseModel


class EnvelopeDocumentAvailableType(BaseModel):
    class Config:
        allow_mutation = True

    type: str
    isDefault: bool


class EnvelopeDocumentPage(BaseModel):
    class Config:
        allow_mutation = True

    pageId: str
    sequence: int
    height: int
    width: int
    dpi: int


class EnvelopeDocument(BaseModel):
    class Config:
        allow_mutation = True

    documentId: Union[int, str]
    documentIdGuid: str
    name: str
    type: str
    uri: str
    order: Optional[int]
    pages: Optional[List[EnvelopeDocumentPage]]
    availableDocumentTypes: Optional[List[EnvelopeDocumentAvailableType]]
    display: Optional[str]
    includeInDownload: Optional[bool]
    signerMustAcknowledge: Optional[str]
    templateRequired: bool
    authoritativeCopy: bool


class EnvelopeListDocumentsResponse(BaseModel):
    class Config:
        allow_mutation = True

    envelopeId: str
    envelopeDocuments: List[EnvelopeDocument]

    @property
    def has_only_content(self) -> bool:
        for document in self.envelopeDocuments:
            if document.type != "content":
                return False
        return True
