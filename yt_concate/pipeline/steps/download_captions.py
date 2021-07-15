from pytube import YouTube

from .step import Step


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        count = 0
        # download the package by:  pip install pytube
        for yt in data:
            # count += 1
            # if count > inputs['limit']:
            #     break
            print('downloading caption for', yt.id)
            if utils.caption_file_exists(yt):
                print('found existing caption file')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (KeyError, AttributeError):
                print('Error when downloading caption for', yt.url)
                continue
            # save the caption to a file named Output.txt

            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        return data
