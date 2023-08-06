"""
Copyright (c) 2021 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__version__ = '0.0.5'
__title__ = 'MusicKuwo'
__author__ = 'Xiaocaicai'
__author_email__ = 'xiaocaicai_email@sina.com'
__description__ = 'Kuwo music Python API package.'
__url__ = 'https://github.com/xiaocaicai-github/MusicKuwo/'
__all__ = ['RequestError', 'Search', 'SearchPrompt', 'MusicDetailed', 'Comment', 'GroupComment', 'GroupMusic']

from json import dump, load
from sys import version
from urllib.parse import unquote
from warnings import warn

import requests


class EmptyUrlWaring(Warning):
    pass


class RequestError(BaseException):
    pass


class PythonVersionError(BaseException):
    pass


PythonVersion = version[0:5]
if PythonVersion[0] != '3':
    raise PythonVersionError(
        F'Your Python version is {PythonVersion}, but this module only applies to Python3 versions.')

Headers = {
    'Cookie': '_ga=GA1.2.1083049585.1590317697; _gid=GA1.2.2053211683.1598526974; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1597491567,1598094297,1598096480,1598526974; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1598526974; kw_token=HYZQI4KPK3P',
    'Referer': 'https://www.kuwo.cn/', 'csrf': 'HYZQI4KPK3P'}


def RequestSend(Url, Params, Key='code'):
    Request = requests.get(Url, headers=Headers, params=Params)
    if Request.status_code != 200:
        raise RequestError(F'Request failed, error code {Request.status_code}.')
    RequestJson = Request.json()
    if 'code' in RequestJson.keys():
        if RequestJson[Key] != 200:
            raise RequestError(F'Request failed, error code {RequestJson[Key]}.')
    return RequestJson


def DetectType(ObjectName, Object, Type):
    if not isinstance(Object, Type):
        raise TypeError(F'The "{ObjectName}" parameter should be {Type} type, but the type is {type(Object)}.')


def Search(Key, Page=1, Number=30):
    DetectType('Key', Key, str)
    DetectType('Page', Page, int)
    DetectType('Number', Number, int)
    SearchMusic = GroupMusic()
    Params = {'key': Key, 'pn': Page, 'rn': Number}
    SearchJson = RequestSend('https://www.kuwo.cn/api/www/search/searchMusicBykeyWord', Params)
    for SearchInfo in SearchJson['data']['list']:
        SearchMusic.Append(Music(SearchInfo))
    return SearchMusic


def SearchPrompt(Key):
    DetectType('Key', Key, str)
    Prompts = []
    Params = {'key': Key}
    PromptJson = RequestSend('https://www.kuwo.cn/api/www/search/searchKey', Params)
    for Prompt in PromptJson['data']:
        Prompts.append((Prompt.split('\r\n')[0])[8:])
    return Prompts


class Music:
    def __init__(self, InfoJson=None):
        if InfoJson:
            self.Code = InfoJson['rid']
            self.Name = InfoJson['name']
            self.Artist = InfoJson['artist']
            self.AlbumName = InfoJson['album']
            self.AlbumImage = InfoJson['albumpic']

    def Comment(self, Page, Number=20, Hot=False):
        DetectType('Hot', Hot, bool)
        DetectType('Page', Page, int)
        DetectType('Number', Number, int)
        if Hot:
            Type = 'get_comment'
        else:
            Type = 'get_res_comment'
        Comments = GroupComment()
        Params = {'page': Page, 'type': Type, 'rows': Number, 'sid': self.Code, 'f': 'web', 'uid': '0', 'digest': '15',
                  'prod': 'newWeb'}
        CommentJson = RequestSend('https://www.kuwo.cn/comment', Params)
        for CommentInfo in CommentJson['rows']:
            Comments.Append(Comment(CommentInfo))
        return Comments

    def Download(self, PathAlbumImage, PathLyrics, PathMusic, Encoding='GBK'):
        self.DownloadMusic(PathMusic)
        self.DownloadLyrics(PathLyrics, Encoding)
        if self.AlbumImage:
            self.DownloadAlbumImage(PathAlbumImage)

    def DownloadMusic(self, Path):
        DetectType('Path', Path, str)
        Params = {'rid': self.Code, 'format': 'mp3', 'type': 'convert_url3'}
        UrlJson = RequestSend('https://www.kuwo.cn/url', Params)
        Request = requests.get(UrlJson['url'])
        if Request.status_code != 200:
            raise RequestError(F'Request failed, error code {Request.status_code}.')
        with open(Path, mode='wb') as File:
            for Data in Request.iter_content(1000):
                File.write(Data)

    def DownloadAlbumImage(self, Path):
        DetectType('Path', Path, str)
        if not self.AlbumImage:
            warn('The image irl is empty.', EmptyUrlWaring)
            return None
        Request = requests.get(self.AlbumImage)
        if Request.status_code != 200:
            raise RequestError(F'Request failed, error code {Request.status_code}.')
        with open(Path, mode='wb') as File:
            for Data in Request.iter_content(1000):
                File.write(Data)

    def DownloadLyrics(self, Path, Encoding='GBK'):
        DetectType('Path', Path, str)
        DetectType('Encoding', Encoding, str)
        Params = {'musicId': self.Code}
        LyricsJson = RequestSend('https://m.kuwo.cn/newh5/singles/songinfoandlrc', Params)
        with open(Path, mode='w', encoding=Encoding) as File:
            for LyricInfo in LyricsJson['data']['lrclist']:
                LyricContent = LyricInfo['lineLyric']
                LyricTime = round(float(LyricInfo['time']), 2)
                LyricSecond = (LyricTime % 60)
                LyricMinute = (LyricTime // 60)
                File.write(F'[{LyricMinute}:{LyricSecond}]{LyricContent}\n')


class MusicDetailed(Music):
    def __init__(self, Code):
        Music.__init__(self)
        DetectType('Code', Code, int)
        Params = {'mid': Code}
        InfoJson = RequestSend('https://www.kuwo.cn/api/www/music/musicInfo', Params)
        self.Code = InfoJson['data']['rid']
        self.Name = InfoJson['data']['name']
        self.Date = InfoJson['data']['releaseDate']
        self.Time = InfoJson['data']['songTimeMinutes']
        self.Artist = InfoJson['data']['artist']
        self.AlbumName = InfoJson['data']['album']
        self.AlbumInfo = InfoJson['data']['albuminfo']
        self.AlbumImage = InfoJson['data']['albumpic']


class CommentAnswer:
    def __init__(self, InfoJson):
        self.Time = InfoJson['time']
        self.Content = InfoJson['msg']
        self.UserName = unquote(InfoJson['u_name'])
        self.ContentParser()

    def ContentParser(self):
        ParserComparison = {'[微笑]': '🙂', '[使坏]': '😁', '[大哭]': '😭', '[高兴]': '😃', '[猪头]': '🐷', '[大爱]': '😍',
                            '[尴尬]': '🤔', '[星星]': '✨'}
        for ParserKey in ParserComparison.keys():
            if ParserKey in self.Content:
                self.Content = self.Content.replace(ParserKey, ParserComparison[ParserKey])


class Comment(CommentAnswer):
    def __init__(self, InfoJson):
        CommentAnswer.__init__(self, InfoJson)
        self.CommentAnswer = None
        self.UserImage = InfoJson['u_pic']
        if 'reply' in InfoJson.keys():
            self.CommentAnswer = CommentAnswer(InfoJson['reply'])

    def DownloadUserImage(self, Path):
        DetectType('Path', Path, str)
        if not self.UserImage:
            raise RequestError('Url does not exist.')
        Request = requests.get(self.UserImage)
        if Request.status_code != 200:
            raise RequestError(F'Request failed, error code {Request.status_code}.')
        with open(Path, mode='wb') as File:
            for Data in Request.iter_content(1000):
                File.write(Data)


class GroupMusic:
    def __init__(self):
        self.Group = []

    def __iter__(self):
        return iter(self.Group)

    def Append(self, Item):
        if not (isinstance(Item, MusicDetailed) or isinstance(Item, Music)):
            raise TypeError(
                F'The "Item" parameter should be MusicDetailed or Music type, but the type is {type(Item)}.')
        self.Group.append(Item)

    def SaveFile(self, Path, Encoding='GBK'):
        DetectType('Path', Path, str)
        DetectType('Encoding', Encoding, str)
        WriteJson = []
        with open(Path, mode='w', encoding=Encoding) as File:
            for Item in self.Group:
                WriteJson.append(Item.Code)
            dump(WriteJson, File)

    def ReadFile(self, Path, Encoding='GBK'):
        DetectType('Path', Path, str)
        DetectType('Encoding', Encoding, str)
        with open(Path, mode='r', encoding=Encoding) as File:
            ReadJson = load(File)
            for Code in ReadJson:
                self.Group.append(MusicDetailed(Code))


class GroupComment:
    def __init__(self):
        self.Group = []

    def __iter__(self):
        return iter(self.Group)

    def Append(self, Item):
        DetectType('Item', Item, Comment)
        self.Group.append(Item)
