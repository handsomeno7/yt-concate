import os, logging
from threading import Thread
import time

from .step import Step

from pytube import YouTube
from yt_concate.settings import VIDEOS_DIR


# 多線程有排隊拿票的感覺，下載過程中一個線程發現有檔案存在，就趕快再要求另外一個
# 有明顯感覺效率增加


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('main')
        start = time.time()
        threads = []
        cpu_count = os.cpu_count()
        for i in range(os.cpu_count()):
            logger.info('registering process %d' % i)
            threads.append(Thread(target=self.download_yt, args=(data[i::cpu_count], inputs, utils)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        end = time.time()
        logger.debug('took', end - start, 'seconds')

        return data

    def download_yt(self, data, inputs, utils, logger):
        yt_set = set([found.yt for found in data])
        logger.debug('videos to download=', len(yt_set))

        for yt in yt_set:
            url = yt.url

            if utils.video_file_exists(yt):
                logger.debug(f'found existing video file for {url}, skipping')
                continue

            logger.debug('downloading', url)
            YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
