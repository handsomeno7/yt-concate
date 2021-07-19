import os
import logging
from multiprocessing import Process, process
import time
from pytube import YouTube

from .step import Step


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('main')
        count = 0
        start = time.time()
        processes = []
        cpu_count = os.cpu_count()
        for i in range(cpu_count):
            processes.append(Process(target=self.download_cap, args=(data[i::cpu_count], inputs, utils)))

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        end_time = time.time()
        logger.info('took', end_time - start, 'seconds')




        # download the package by:  pip install pytube

        return data

    def download_cap(self, data, inputs, utils, logger):
        for yt in data:
            # count += 1
            # if count > inputs['limit']:
            #     break
            logger.debug('downloading caption for', yt.id)
            if utils.caption_file_exists(yt):
                print('found existing caption file')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (KeyError, AttributeError):
                logger.error('Error when downloading caption for', yt.url)
                continue
            # save the caption to a file named Output.txt

            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()