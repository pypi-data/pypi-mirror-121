from enum import Enum

from codefast.utils import deprecated

from .pipe import author
from .toolkits.endecode import decode_with_keyfile, encode_with_keyfile


@deprecated('decode() is deprecated, use pipe.author.get() instead.')
def decode(keyword: str) -> str:
    from .pipe import author
    return author.get(keyword)


def fast_text_encode(text: str) -> str:
    ''' Encode text with passphrase in js[auth_file]'''
    return encode_with_keyfile(author.get('AUTH_FILE'), text)


def fast_text_decode(text: str):
    return decode_with_keyfile(author.get('AUTH_FILE'), text)


''' Channels:
1. Global_News_Podcast, t.me/messalert, personal, info on weather, data traffic.
2. cccache, t.me/cccache, public, share IT, video info
3. Global_Notices, t.me/plutoshare, fund alert.
'''
CHANNEL_MESSALERT = 'messalert'
CHANNEL_CCCACHE = 'cccache'
CHANNEL_PLUTOSHARE = 'plutoshare'



class BotEnum(Enum):
    COMMON = 1     # i.e., @vpsmoni714_bot, connected to channel Global_News_Podcast, Global_Notices and cccache.
    WECHAT = 2     # i.e., @wechat117Bot, connected to channel Global_Notices
    XB117BOT = 3     # i.e., @f117bot, connected to channel cccache
