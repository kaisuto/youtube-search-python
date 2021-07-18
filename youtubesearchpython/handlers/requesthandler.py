import copy

import httpx

from youtubesearchpython.handlers.componenthandler import ComponentHandler
from youtubesearchpython.internal.constants import *


class RequestHandler(ComponentHandler):
    def _makeRequest(self) -> None:
        """Fixes #47"""
        requestBody = copy.deepcopy(requestPayload)
        requestBody["query"] = self.query
        requestBody["client"] = {
            "hl": self.language,
            "gl": self.region,
        }
        if self.searchPreferences:
            requestBody["params"] = self.searchPreferences
        if self.continuationKey:
            requestBody["continuation"] = self.continuationKey

        try:
            with httpx.Client() as client:
                response = client.post(
                    "https://www.youtube.com/youtubei/v1/search",
                    params={
                        "key": searchKey,
                    },
                    headers={
                        "User-Agent": userAgent,
                    },
                    json=requestBody,
                )
                self.response = response.json()
        except:
            raise Exception("ERROR: Could not make request.")

    def _parseSource(self) -> None:
        try:
            if not self.continuationKey:
                responseContent = self._getValue(self.response, contentPath)
            else:
                responseContent = self._getValue(self.response, continuationContentPath)
            if responseContent:
                for element in responseContent:
                    if itemSectionKey in element.keys():
                        self.responseSource = self._getValue(
                            element, [itemSectionKey, "contents"]
                        )
                    if continuationItemKey in element.keys():
                        self.continuationKey = self._getValue(
                            element, continuationKeyPath
                        )
            else:
                self.responseSource = self._getValue(self.response, fallbackContentPath)
                self.continuationKey = self._getValue(
                    self.responseSource[-1], continuationKeyPath
                )
        except Exception as e:
            raise Exception("ERROR: Could not parse YouTube response.")

    def _makeBrowseRequest(self, requestBody=None, timeout=None) -> None:
        if requestBody is None:
            requestBody = copy.deepcopy(requestPayload)

        if self.query:
            requestBody["query"] = self.query

        requestBody["browseId"] = self.browseId
        requestBody["client"] = {
            "hl": self.language,
            "gl": self.region,
        }
        if self.searchPreferences:
            requestBody["params"] = self.searchPreferences
        if self.continuationKey:
            requestBody["continuation"] = self.continuationKey

        try:
            with httpx.Client() as client:
                response = client.post(
                    "https://www.youtube.com/youtubei/v1/browse",
                    params={
                        "key": searchKey,
                    },
                    headers={
                        "User-Agent": userAgent,
                    },
                    json=requestBody,
                    timeout=timeout,
                )
                self.response = response.json()
        except:
            raise Exception("ERROR: Could not make request.")

    def _parseBrowseSearchSource(self) -> None:
        try:
            if self.continuationKey:
                elements = self._getValue(self.response, browseContinuationContentPath)
            else:
                elements = self._getValue(self.response, browseContentPath)

            responseSource = []
            for element in elements:
                if itemSectionKey in element.keys():
                    videoElements = self._getValue(
                        element, [itemSectionKey, "contents"]
                    )
                    responseSource.extend(videoElements)

                if continuationItemKey in element.keys():
                    self.continuationKey = self._getValue(element, continuationKeyPath)
            self.responseSource = responseSource
        except KeyError as e:
            raise Exception("ERROR: Could not parse YouTube response.")

    def _parseBrowseListSource(self) -> None:
        try:
            if self.continuationKey:
                self.responseSource = self._getValue(
                    self.response, browseContinuationGridContentPath
                )
                return

            responseSource = []
            elements = self._getValue(self.response, browseGridContentPath)
            for element in elements:
                if itemSectionKey in element.keys():
                    gridRendererElements = self._getValue(
                        element, [itemSectionKey, "contents"]
                    )
                    for gridRendererElement in gridRendererElements:
                        gridVideoRendererElements = self._getValue(
                            gridRendererElement, gridVideoRendererPath
                        )
                        for gridVideoRendererElement in gridVideoRendererElements:
                            if gridVideoElementKey in gridVideoRendererElement.keys():
                                responseSource.append(gridVideoRendererElement)

                            if continuationItemKey in gridVideoRendererElement.keys():
                                self.continuationKey = self._getValue(
                                    gridVideoRendererElement, continuationKeyPath
                                )

            self.responseSource = responseSource
        except KeyError as e:
            raise Exception("ERROR: Could not parse YouTube response.")
