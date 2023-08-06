from pydantic.dataclasses import dataclass


@dataclass(frozen=True, init=False)
class IncludeTypeEnum:
    CUSTOM_FIELDS = "custom_fields"
    DOCUMENTS = "documents"
    ATTACHMENTS = "attachments"
    EXTENSIONS = "extensions"
    FOLDERS = "folders"
    RECIPIENTS = "recipients"
    POWERFORM = "powerform"
    TABS = "tabs"
    PAYMENT_TABS = "payment_tabs"
