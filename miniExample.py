from youtubesearchpython import *


"""
Can be used to get search results with custom defined filters.

Setting second parameter as VideoSortOrder.uploadDate, to get video results sorted according to upload date.

Few of the predefined filters for you to use are:
SearchMode.videos
VideoUploadDateFilter.lastHour
VideoDurationFilter.long
VideoSortOrder.viewCount
There are many other for you to check out.

If this much control isn't enough then, you may pass custom string yourself by seeing the YouTube query in any web browser e.g. 
"EgQIBRAB" from "https://www.youtube.com/results?search_query=NoCopyrightSounds&sp=EgQIBRAB" may be passed as second parameter to get only videos, which are uploaded this year.
"""
customSearch = CustomSearch(
    "NoCopyrightSounds", VideoSortOrder.uploadDate, language="en", region="US"
)
print(customSearch.result())


"""
Getting search results from the next pages on YouTube.
Generally you'll get maximum of 20 videos in one search, for getting subsequent results, you may call `next` method.
"""
search = VideosSearch("NoCopyrightSounds")
index = 0
for video in search.result()["result"]:
    print(str(index) + " - " + video["title"])
    index += 1
"""Getting result on 2nd page."""
search.next()
for video in search.result()["result"]:
    print(str(index) + " - " + video["title"])
    index += 1
"""Getting result on 3rd page."""
search.next()
for video in search.result()["result"]:
    print(str(index) + " - " + video["title"])
    index += 1


"""
Getting information about video or its formats using video link or video ID.

`Video.get` method will give both information & formats of the video
`Video.getInfo` method will give only information about the video.
`Video.getFormats` method will give only formats of the video.

You may either pass link or ID, method will take care itself.
"""
video = Video.get("https://www.youtube.com/watch?v=z0GKGpObgPY", mode=ResultMode.json)
print(video)
videoInfo = Video.getInfo("https://youtu.be/z0GKGpObgPY", mode=ResultMode.json)
print(videoInfo)
videoFormats = Video.getFormats("z0GKGpObgPY")
print(videoFormats)


channel = ChannelSearch("Watermelon Sugar", "UCZFWPqqPkFlNwIxcpsLOwew")

print(channel.result(mode=ResultMode.json))


"""
Search videos in specified channel from YouTube.
"""
search = ChannelVideosSearch("Watermelon Sugar", "UCZFWPqqPkFlNwIxcpsLOwew")

print(search.result(mode=ResultMode.json))


"""
You may add/omit the optional parameters according to your requirement & use case.
"""


"""
Thanks for your support & love!

- github.com/alexmercerind
"""
