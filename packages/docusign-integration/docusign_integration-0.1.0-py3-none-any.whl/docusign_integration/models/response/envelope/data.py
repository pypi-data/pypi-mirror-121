from typing import Optional
from pydantic import BaseModel


class EnvelopeDataSender(BaseModel):
    userName: str
    userId: str
    accountId: str
    email: str


class EnvelopeDataMetadata(BaseModel):
    allowAdvancedCorrect: bool
    enableSignWithNotary: bool
    allowCorrect: bool


class EnvelopeDataResponse(BaseModel):
    status: str
    documentsUri: str
    recipientsUri: str
    attachmentsUri: str
    envelopeUri: str
    emailSubject: str
    envelopeId: str
    signingLocation: str
    customFieldsUri: str
    notificationUri: str
    enableWetSign: bool
    allowMarkup: bool
    allowReassign: bool
    createdDateTime: str
    lastModifiedDateTime: str
    deliveredDateTime: str
    initialSentDateTime: str
    sentDateTime: str
    completedDateTime: str
    statusChangedDateTime: str
    documentsCombinedUri: str
    certificateUri: str
    templatesUri: str
    expireEnabled: bool
    expireDateTime: str
    expireAfter: int
    sender: EnvelopeDataSender
    purgeState: str
    envelopeIdStamping: bool
    is21CFRPart11: bool
    signerCanSignOnMobile: bool
    autoNavigation: bool
    isSignatureProviderEnvelope: bool
    hasFormDataChanged: bool
    allowComments: bool
    hasComments: bool
    allowViewHistory: bool
    envelopeMetadata: EnvelopeDataMetadata
    anySigner: Optional[str]
    envelopeLocation: str
    isDynamicEnvelope: bool
