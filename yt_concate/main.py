import sys
import getopt
import logging
from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_video import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils

sys.path.append('../')
CHANNEL_ID = 'UCWu6SQmC6nAZ-reuj3lF2eQ'


# 'UCKSVUHI9rbbkXhvAXK-2uxA'
# UCRrOsab_je2oAJmxGt4_Vgw
# UCWu6SQmC6nAZ-reuj3lF2eQ

def config_logger(level):
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)  # logger的level不能比handler高
    formatter = logging.Formatter('%(asctime)s - %(levelname) - %(filename)s - %(funcName)s - %(message)s')
    file_handler = logging.FileHandler('log.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger  # 不一定要return


def print_usage():
    print('python main.py -c <channel_id> -s <search_word> -l <int(limit)>')
    print('python main.py'
          '--channel_id <channel_id>'
          '--search_word <word>'
          '--limit <number>'
          '--cleanup <True/False>'
          '--fast <True/False>'
          '--log <DEBUG/INFO/WARNING/ERROR/CRITICAL>'
          )

    print('python3 main.py OPTIONS')
    print('OPTIONS: ')
    print('{:>6} {:<12}{}'.format('', '--cleanup', 'Remove captions and video dowloaded during run.'))
    print('{:>6} {:<12}{}'.format('', '--fast', 'skip downloaded captions and videos.'))
    print('{:>6} {:<12}{}'.format('', '--log', 'set the level of logger showed on stream.'))


def main():
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': 'volume',
        'limit': 15,
        'clean_up': False,
        'fast': True,
    }

    short_opts = 'hc:s:l'
    long_opts = 'help channel_id= search_word= limit= cleanup= fast='.split()

    print(sys.argv[1:])
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ('-c', '--channel_id'):
            inputs['channel_id'] = arg
        elif opt in ('-s', '--search_word'):
            inputs['search_word'] = arg
        elif opt in ('-l', '--limit'):
            inputs['limit'] = arg
        elif opt in ('--cleanup'):
            inputs['clean_up'] = bool(arg)
        elif opt in ('--fast'):
            inputs['fast'] = bool(arg)

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),

    ]
    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
