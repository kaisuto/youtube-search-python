import copy

import httpx

from youtubesearchpython.__future__.handlers.componenthandler import ComponentHandler
from youtubesearchpython.__future__.internal.constants import *


class RequestHandler(ComponentHandler):
    async def _makeRequest(self, requestBody=None, timeout=None) -> None:
        if requestBody is None:
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
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://www.youtube.com/youtubei/v1/search",
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

    async def _parseSource(self) -> None:
        try:
            if not self.continuationKey:
                responseContent = await self._getValue(self.response, contentPath)
            else:
                responseContent = await self._getValue(
                    self.response, continuationContentPath
                )
            if responseContent:
                for element in responseContent:
                    if itemSectionKey in element.keys():
                        self.responseSource = await self._getValue(
                            element, [itemSectionKey, "contents"]
                        )
                    if continuationItemKey in element.keys():
                        self.continuationKey = await self._getValue(
                            element, continuationKeyPath
                        )
            else:
                self.responseSource = await self._getValue(
                    self.response, fallbackContentPath
                )
                self.continuationKey = await self._getValue(
                    self.responseSource[-1], continuationKeyPath
                )
        except:
            raise Exception("ERROR: Could not parse YouTube response.")

    async def _makeBrowseRequest(self, requestBody=None, timeout=None) -> None:
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
            async with httpx.AsyncClient() as client:
                response = await client.post(
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

    async def _parseBrowseSearchSource(self) -> None:
        try:
            if self.continuationKey:
                elements = await self._getValue(
                    self.response, browseContinuationContentPath
                )
            else:
                elements = await self._getValue(self.response, browseContentPath)

            responseSource = []
            for element in elements:
                if itemSectionKey in element.keys():
                    videoElements = await self._getValue(
                        element, [itemSectionKey, "contents"]
                    )
                    responseSource.extend(videoElements)

                if continuationItemKey in element.keys():
                    self.continuationKey = await self._getValue(
                        element, continuationKeyPath
                    )
            self.responseSource = responseSource
        except KeyError as e:
            raise Exception("ERROR: Could not parse YouTube response.")

    async def _parseBrowseListSource(self) -> None:
        try:
            if self.continuationKey:
                self.responseSource = await self._getValue(
                    self.response, browseContinuationGridContentPath
                )
                return

            responseSource = []
            elements = await self._getValue(self.response, browseGridContentPath)
            for element in elements:
                if itemSectionKey in element.keys():
                    gridRendererElements = await self._getValue(
                        element, [itemSectionKey, "contents"]
                    )
                    for gridRendererElement in gridRendererElements:
                        gridVideoRendererElements = await self._getValue(
                            gridRendererElement, gridVideoRendererPath
                        )
                        for gridVideoRendererElement in gridVideoRendererElements:
                            if gridVideoElementKey in gridVideoRendererElement.keys():
                                responseSource.append(gridVideoRendererElement)

                            if continuationItemKey in gridVideoRendererElement.keys():
                                self.continuationKey = await self._getValue(
                                    gridVideoRendererElement, continuationKeyPath
                                )

            self.responseSource = responseSource
        except KeyError as e:
            raise Exception("ERROR: Could not parse YouTube response.")
