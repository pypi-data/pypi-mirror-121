from typing import Any, Dict, List, Optional, Union

from docusign_integration.models.envelope import (
    IncludeTypeEnum,
)
from docusign_integration.api import BaseApi
from urllib.parse import urlencode, urljoin
import fitz
from pydantic import validate_arguments
import pydash


class EnvelopeApi(BaseApi):
    @validate_arguments
    def list_envelope_documents(
        self,
        account_id: str,
        envelope_id: str,
        only_content: bool = True,
        **query_params,
    ) -> Dict[str, Any]:
        """Retrieves a list of documents associated with the specified envelope.

        reference: https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopedocuments/list/

        Args:
            account_id (str)
            envelope_id (str)
            only_content (bool, optional): Defaults to True.

        Returns:
            Dict[str, Any]
        """

        url = urljoin(
            self.base_url,
            f"{self.api_version}/accounts/{account_id}/envelopes/{envelope_id}/documents?{urlencode(query_params)}",
        )
        response = self.get(url, stream=True)
        response.raise_for_status()
        response_data = response.json()

        if only_content:
            response_data["envelopeDocuments"] = pydash.filter_(
                response_data.get("envelopeDocuments", []), {"type": "content"}
            )

        return response_data

    @validate_arguments
    def download_envelope_document(
        self, account_id: str, envelope_id: str, document_id: int
    ) -> fitz.Document:
        """Download envelope document into a fitz document (PDF)

        reference: https://developers.docusign.com/docs/esign-rest-api/how-to/download-envelope-documents/

        Args:
            account_id (str)
            envelope_id (str)
            document_id (int)

        Returns:
            fitz.Document
        """

        url = urljoin(
            self.base_url,
            f"{self.api_version}/accounts/{account_id}/envelopes/{envelope_id}/documents/{document_id}",
        )
        response = self.get(url)
        response.raise_for_status()

        return fitz.open("pdf", response.content)

    @validate_arguments
    def get_envelope_data(
        self,
        account_id: str,
        envelope_id: str,
        *,
        advanced_update: Optional[bool] = None,
        include: Optional[List[Union[str, IncludeTypeEnum]]] = None,
    ) -> Dict[str, Any]:
        """Retrieves the overall status for the specified envelope.

        reference: https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopes/get/

        Args:
            account_id (str)
            envelope_id (str)
            advanced_update (Optional[bool], optional): Defaults to None.
            include (Optional[List[Union[str, IncludeTypeEnum]]], optional): Defaults to None.

        Returns:
            Dict[str, Any]
        """

        url = urljoin(
            self.base_url,
            f"{self.api_version}/accounts/{account_id}/envelopes/{envelope_id}",
        )

        query_params = pydash.omit_by(
            {
                "advanced_update": advanced_update,
                "include": ",".join(include) if include is not None else None,
            },
            lambda v: v is None,
        )

        response = self.get(url, params=query_params)
        response.raise_for_status()

        return response.json()

    @validate_arguments
    def list_document_recipients(
        self,
        account_id: str,
        envelope_id: str,
        *,
        include_anchor_tab_locations: Optional[bool] = None,
        include_extended: Optional[bool] = None,
        include_metadata: Optional[bool] = None,
        include_tabs: Optional[bool] = None,
    ):
        """Gets the status of recipients for an envelope.

        Args:
            account_id (str)
            envelope_id (str)
            include_anchor_tab_locations (Optional[bool], optional): Defaults to None.
            include_extended (Optional[bool], optional): Defaults to None.
            include_metadata (Optional[bool], optional): Defaults to None.
            include_tabs (Optional[bool], optional): Defaults to None.

        Returns:
            [type]: [description]
        """

        url = urljoin(
            self.base_url,
            f"{self.api_version}/accounts/{account_id}/envelopes/{envelope_id}/recipients",
        )

        query_params = pydash.omit_by(
            {
                "include_anchor_tab_locations": include_anchor_tab_locations,
                "include_extended": include_extended,
                "include_metadata": include_metadata,
                "include_tabs": include_tabs,
            },
            lambda v: v is None,
        )

        response = self.get(url, params=query_params)
        response.raise_for_status()

        return response.json()
