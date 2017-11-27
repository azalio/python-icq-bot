from collections import namedtuple

from baseconv import BaseConverter

from icq.constant import ImageType, VideoType, AudioType

BASE62_ICQ_CONVERTER = BaseConverter("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")


def decode_file_id(file_id):
    file_type = file_id[0]
    for t in (ImageType, VideoType, AudioType):
        try:
            file_type = t(file_type)
            break
        except ValueError:
            pass
    else:
        file_type = None

    width = height = length = color = None
    if file_type:
        type_class = type(file_type)
        if type_class in (ImageType, VideoType):
            # TWWHHCCCxxxxxxxxxxxxxxxxxxxxxxxxx
            width = int(BASE62_ICQ_CONVERTER.decode(file_id[1:3]))
            height = int(BASE62_ICQ_CONVERTER.decode(file_id[3:5]))
            if file_type not in (VideoType.PTS, VideoType.PTS_B):
                color = hex(int(BASE62_ICQ_CONVERTER.decode(file_id[5:8])))

        if file_type in (VideoType.PTS, VideoType.PTS_B):
            # TWWHHLLLLCCCxxxxxxxxxxxxxxxxxxxxx
            length = int(BASE62_ICQ_CONVERTER.decode(file_id[5:9]))
            color = hex(int(BASE62_ICQ_CONVERTER.decode(file_id[9:12])))
        elif file_type in (AudioType.PTT, AudioType.PTT_J):
            # TLLLLxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            length = int(BASE62_ICQ_CONVERTER.decode(file_id[1:5]))

    return namedtuple("_", ("file_type", "width", "height", "length", "color"))(file_type, width, height, length, color)
