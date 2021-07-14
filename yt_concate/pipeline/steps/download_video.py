import time
from .step import Step
from pytube import YouTube
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        yt_set = set([found.yt for found in data])
        print('videos to download=', len(yt_set))
        count = 0
        for yt in yt_set:
            url = yt.url
            count += 1
            print(count)
            if utils.video_file_exists(yt):
                print('found existing video file, skipping')
                continue
            print('downloading', url)

            YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
            time.sleep(1)

        return data
