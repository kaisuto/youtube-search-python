from typing import Union
import json
from youtubesearchpython.handlers.requesthandler import RequestHandler
from youtubesearchpython.handlers.componenthandler import ComponentHandler
from youtubesearchpython.internal.constants import *


class SearchInternal(RequestHandler, ComponentHandler):
    response = None
    responseSource = None
    resultComponents = []
    timeout = None

    def __init__(
        self,
        query: str,
        limit: int,
        language: str,
        region: str,
        searchPreferences: str,
        timeout: int,
    ):
        self.query = query
        self.limit = limit
        self.language = language
        self.region = region
        self.searchPreferences = searchPreferences
        self.continuationKey = None
        self.timeout = timeout
        self._makeRequest(timeout=self.timeout)
        self._parseSource()

    def result(self, mode: int = ResultMode.dict) -> Union[str, dict]:
        """Returns the search result.

        Args:
            mode (int, optional): Sets the type of result. Defaults to ResultMode.dict.

        Returns:
            Union[str, dict]: Returns JSON or dictionary.
        """
        if mode == ResultMode.json:
            return json.dumps({"result": self.resultComponents}, indent=4)
        elif mode == ResultMode.dict:
            return {"result": self.resultComponents}

    def next(self) -> bool:
        """Gets the subsequent search result. Call result

        Args:
            mode (int, optional): Sets the type of result. Defaults to ResultMode.dict.

        Returns:
            Union[str, dict]: Returns True if getting more results was successful.
        """
        if self.continuationKey:
            self.response = None
            self.responseSource = None
            self.resultComponents = []
            self._makeRequest(timeout=self.timeout)
            self._parseSource()
            self._getComponents(*self.searchMode)
            return True
        else:
            return False

    def _getComponents(
        self, findVideos: bool, findChannels: bool, findPlaylists: bool
    ) -> None:
        self.resultComponents = []
        for element in self.responseSource:
            if videoElementKey in element.keys() and findVideos:
                self.resultComponents.append(self._getVideoComponent(element))
            if gridVideoElementKey in element.keys() and findVideos:
                self.resultComponents.append(self._getGridVideoComponent(element))
            if channelElementKey in element.keys() and findChannels:
                self.resultComponents.append(self._getChannelComponent(element))
            if playlistElementKey in element.keys() and findPlaylists:
                self.resultComponents.append(self._getPlaylistComponent(element))
            if shelfElementKey in element.keys() and findVideos:
                for shelfElement in self._getShelfComponent(element)["elements"]:
                    self.resultComponents.append(
                        self._getVideoComponent(
                            shelfElement,
                            shelfTitle=self._getShelfComponent(element)["title"],
                        )
                    )
            if richItemKey in element.keys() and findVideos:
                richItemElement = self._getValue(element, [richItemKey, "content"])
                """ Initial fallback handling for VideosSearch """
                if videoElementKey in richItemElement.keys():
                    videoComponent = self._getVideoComponent(richItemElement)
                    self.resultComponents.append(videoComponent)
            if self.limit is not None and len(self.resultComponents) >= self.limit:
                break


class ChannelVideoSearchInternal(SearchInternal):
    def __init__(
        self,
        browseId: str,
        query: str,
        limit: int,
        language: str,
        region: str,
        searchPreferences: str,
        timeout: int,
    ):
        self.response = None
        self.responseSource = None
        self.resultComponents = []

        self.browseId = browseId
        self.query = query
        self.limit = limit
        self.language = language
        self.region = region
        self.searchPreferences = searchPreferences
        self.continuationKey = None
        self.timeout = timeout

        self._makeBrowseRequest(timeout=self.timeout)
        self._parseBrowseSearchSource()

    def next(self) -> bool:
        """Gets the subsequent search result. Call result

        Args:
            mode (int, optional): Sets the type of result. Defaults to ResultMode.dict.

        Returns:
            Union[str, dict]: Returns True if getting more results was successful.
        """
        if self.continuationKey:
            self.response = None
            self.responseSource = None
            self.resultComponents = []
            self._makeBrowseRequest(timeout=self.timeout)
            self._parseBrowseSearchSource()
            self._getComponents(*self.searchMode)
            return True
        else:
            return False


class ChannelVideoListInternal(SearchInternal):
    def __init__(
        self,
        browseId: str,
        limit: int,
        language: str,
        region: str,
        searchPreferences: str,
        timeout: int,
    ):
        self.response = None
        self.responseSource = None
        self.resultComponents = []

        self.browseId = browseId
        self.query = None
        self.limit = limit
        self.language = language
        self.region = region
        self.searchPreferences = searchPreferences
        self.continuationKey = None
        self.timeout = timeout

        self._makeBrowseRequest(timeout=self.timeout)
        self._parseBrowseListSource()

    def next(self) -> bool:
        """Gets the subsequent search result. Call result

        Args:
            mode (int, optional): Sets the type of result. Defaults to ResultMode.dict.

        Returns:
            Union[str, dict]: Returns True if getting more results was successful.
        """
        if self.continuationKey:
            self.response = None
            self.responseSource = None
            self.resultComponents = []
            self._makeBrowseRequest(timeout=self.timeout)
            self._parseBrowseListSource()
            self._getComponents(*self.searchMode)
            return True
        else:
            return False
