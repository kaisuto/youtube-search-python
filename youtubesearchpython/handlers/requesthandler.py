from urllib.request import Request, urlopen
from urllib.parse import urlencode

import json
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
        requestBodyBytes = json.dumps(requestBody).encode("utf_8")
        request = Request(
            "https://www.youtube.com/youtubei/v1/search"
            + "?"
            + urlencode(
                {
                    "key": searchKey,
                }
            ),
            data=requestBodyBytes,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Content-Length": len(requestBodyBytes),
                "User-Agent": userAgent,
            },
        )
        try:
            self.response = urlopen(request).read().decode("utf_8")
        except:
            raise Exception("ERROR: Could not make request.")

    def _parseSource(self) -> None:
        try:
            if not self.continuationKey:
                responseContent = self._getValue(json.loads(self.response), contentPath)
            else:
                responseContent = self._getValue(
                    json.loads(self.response), continuationContentPath
                )
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
                self.responseSource = self._getValue(
                    json.loads(self.response), fallbackContentPath
                )
                self.continuationKey = self._getValue(
                    self.responseSource[-1], continuationKeyPath
                )
        except:
            raise Exception("ERROR: Could not parse YouTube response.")

    def _makeChannelSearchRequest(self) -> None:
        """Fixes #47"""
        requestBody = copy.deepcopy(requestPayload)
        requestBody["query"] = self.query
        requestBody["client"] = {
            "hl": self.language,
            "gl": self.region,
        }
        requestBody["params"] = self.searchPreferences
        requestBody["browseId"] = self.browseId

        requestBodyBytes = json.dumps(requestBody).encode("utf_8")
        request = Request(
            "https://www.youtube.com/youtubei/v1/browse"
            + "?"
            + urlencode(
                {
                    "key": searchKey,
                }
            ),
            data=requestBodyBytes,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Content-Length": len(requestBodyBytes),
                "User-Agent": userAgent,
            },
        )
        try:
            self.response = json.loads(urlopen(request).read().decode("utf_8"))
        except:
            raise Exception("ERROR: Could not make request.")

    def _parseChannelSearchSource(self) -> None:
        try:
            self.response = self.response["contents"]["twoColumnBrowseResultsRenderer"][
                "tabs"
            ][-1]["expandableTabRenderer"]["content"]["sectionListRenderer"]["contents"]
        except:
            raise Exception("ERROR: Could not parse YouTube response.")

    def _makeChannelVideoSearchRequest(self, requestBody=None, timeout=None) -> None:
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

    def _parseChannelVideoSearchSource(self) -> None:
        try:
            if not self.continuationKey:
                elements = self._getValue(self.response, browseSearchContentPath)
            else:
                elements = self._getValue(self.response, continuationContentPath)

            if elements:
                responseSource = []
                for element in elements:
                    if itemSectionKey in element.keys():
                        videoElements = self._getValue(
                            element, [itemSectionKey, "contents"]
                        )
                        responseSource.extend(videoElements)

                    if continuationItemKey in element.keys():
                        self.continuationKey = self._getValue(
                            element, continuationKeyPath
                        )
            else:
                responseSource = self._getValue(
                    json.loads(self.response), fallbackContentPath
                )
                self.continuationKey = self._getValue(
                    responseSource[-1], continuationKeyPath
                )
            self.responseSource = responseSource
        except KeyError as e:
            raise Exception("ERROR: Could not parse YouTube response.")
