

from pytube import YouTube

from .step import Step




class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        # download the package by:  pip install pytube
        for url in data:
            print('downloading caption for', url)
            if utils.caption_file_exists(url):
                print('found existing caption file')
                continue

            try:
                source = YouTube(url)
                en_caption = source.captions.get_by_language_code('en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (KeyError, AttributeError):
                print('Error when downloading caption for', url)
                continue
            # save the caption to a file named Output.txt

            text_file = open(utils.get_caption_filepath(url), "w", encoding="utf-8")
            text_file.write(en_caption_convert_to_srt)
            text_file.close()


