from youtubesearchpython import *


"""
Getting information about video or its formats using video link or video ID.

`Video.get` method will give both information & formats of the video
`Video.getInfo` method will give only information about the video.
`Video.getFormats` method will give only formats of the video.

You may either pass link or ID, method will take care itself.
"""
video_id = "P1Qtn6p6468"
video = Video.get("https://www.youtube.com/watch?v=" + video_id, mode=ResultMode.dict)
print(video)
videoInfo = Video.getInfo("https://youtu.be/" + video_id, mode=ResultMode.dict)
print(videoInfo)
videoFormats = Video.getFormats(video_id)
print(videoFormats)


"""
Search videos in specified channel from YouTube.
"""
search = ChannelVideosSearch("UC_a1ZYZ8ZTXpjg9xUY9sj8w", "怖い話")

channel_videos_search_results1 = search.result(mode=ResultMode.dict)

print(channel_videos_search_results1)


"""
Getting search results from the next pages on YouTube.
Generally you'll get maximum of 30 videos in one search, for getting subsequent results, you may call `next` method.
"""
search = ChannelVideosSearch("UC_a1ZYZ8ZTXpjg9xUY9sj8w", "怖い話")
index = 0
for video in search.result(mode=ResultMode.dict)["result"]:
    print(str(index) + " - " + video["title"])
    index += 1
"""Getting result on 2nd page."""
search.next()
for video in search.result(mode=ResultMode.dict)["result"]:
    print(str(index) + " - " + video["title"])
    index += 1


"""
List videos in specified channel from YouTube.
"""
list_ = ChannelVideosList("UC_a1ZYZ8ZTXpjg9xUY9sj8w")

channel_videos_list_results1 = list_.result(mode=ResultMode.dict)

print(channel_videos_list_results1)


"""
Getting list results from the next pages on YouTube.
Generally you'll get maximum of 30 videos in one list, for getting subsequent results, you may call `next` method.
"""
list_ = ChannelVideosList("UC_a1ZYZ8ZTXpjg9xUY9sj8w")
index = 0
for video in list_.result(mode=ResultMode.dict)["result"]:
    print(str(index) + " - " + video["title"])
    index += 1
"""Getting result on 2nd page."""
list_.next()
for video in list_.result(mode=ResultMode.dict)["result"]:
    print(str(index) + " - " + video["title"])
    index += 1
