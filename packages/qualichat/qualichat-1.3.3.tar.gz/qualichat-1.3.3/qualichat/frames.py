"""
MIT License

Copyright (c) 2021 Qualichat

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

import types
import inspect
from functools import partial
from pathlib import Path
from collections import defaultdict
from typing import (
    ClassVar,
    Dict,
    List,
    Optional,
    Union,
    Set,
    Any,
    DefaultDict
)

# Fix matplotlib backend warning.
import matplotlib
matplotlib.use('TkAgg')

import questionary
import spacy
import qualitube # type: ignore
import matplotlib.pyplot as plt
from pandas import DataFrame
from pandas.core.generic import NDFrame
from plotly.subplots import make_subplots # type: ignore
from plotly.graph_objects import Scatter # type: ignore
from wordcloud.wordcloud import WordCloud, STOPWORDS # type: ignore
from tldextract import extract # type: ignore
from rich.style import Style
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn
)

from .chat import Chat
from .models import Message
from .enums import MessageType
from .utils import log, parse_domain
from .regex import SHORT_YOUTUBE_LINK_RE, YOUTUBE_LINK_RE


__all__ = ('BaseFrame', 'KeysFrame')


ChatsData = Dict[str, Dict[str, List[Message]]]
DataFrames = Dict[str, Union[DataFrame, NDFrame]]
WordClouds = Dict[str, WordCloud]



input = partial(questionary.text, qmark='[qualichat]')
select = partial(questionary.select, qmark='[qualichat]')

progress_bar = Progress(
    SpinnerColumn(),
    TextColumn('[progress.description]{task.description}'),
    BarColumn(complete_style=Style(color='red')),
    TextColumn('[progress.percentage]{task.percentage:>3.0f}%'),
    TimeRemainingColumn(),
    TimeElapsedColumn()
)


def generate_chart(
    data: DataFrames,
    *,
    bars: Optional[List[str]] = None,
    lines: Optional[List[str]] = None,
    title: Optional[str] = None
) -> None:
    if bars is None:
        bars = []

    if lines is None:
        lines = []

    specs = [[{'secondary_y': True}]]
    fig = make_subplots(specs=specs) # type: ignore

    filename, dataframe = list(data.items())[0]
    index = dataframe.index # type: ignore

    # buttons: List[Dict[str, Any]] = []

    # for filename, dataframe in data.items():
    #     index = list(dataframe.index) # type: ignore

    #     button: Dict[str, Any] = {}
    #     button['label'] = filename
    #     button['method'] = 'update'

    #     args: List[Dict[str, Any]] = []
    #     args.append({})
    #     args.append({'title': {'text': f'{title} ({filename})'}})
    #     button['args'] = args

    #     buttons.append(button)

    # updatemenus = [{'buttons': buttons}]
    # fig.update_layout(updatemenus=updatemenus) # type: ignore

    #     for bar in bars:
    #         filtered = list(getattr(dataframe, bar))
    #         options = dict(x=index, y=filtered, name=bar) # type: ignore
    #         fig.add_bar(**options) # type: ignore

    #     # for line in lines:
    #     #     filtered = getattr(dataframe, line)
    #     #     scatter = Scatter(x=index, y=list(filtered), name=line) # type: ignore
    #     #     fig.add_trace(scatter, secondary_y=True) # type: ignore

    #     button: Dict[str, Any] = {}
    #     button['label'] = filename
    #     button['method'] = 'update'

    #     args: Dict[str, Any] = {}

    #     visibles: List[bool] = [False] * len(data)
    #     visibles[i] = True

    #     args['visible'] = visibles
    #     button['args'] = [args]

    #     buttons.append(button)
        
    # updatemenus = [{'buttons': buttons, 'showactive': False}]
    # fig.update_layout(updatemenus=updatemenus) # type: ignore

    for bar in bars:
        filtered = getattr(dataframe, bar)
        options = dict(x=index, y=list(filtered), name=bar) # type: ignore
        fig.add_bar(**options) # type: ignore

    for line in lines:
        filtered = getattr(dataframe, line)
        scatter = Scatter(x=index, y=list(filtered), name=line) # type: ignore
        fig.add_trace(scatter, secondary_y=True) # type: ignore

    title_text = f'{title} ({filename})'
    fig.update_layout(title_text=title_text) # type: ignore

    fig.update_xaxes(rangeslider_visible=True) # type: ignore
    fig.show() # type: ignore


stopwords: Set[str] = set(STOPWORDS)
stopwords.update([
    'da', 'meu', 'em', 'você', 'de', 'ao', 'os', 'eu', 'Siga-nos'
])


def generate_wordcloud(data: WordClouds, *, title: str):
    for filename, wordcloud in data.items():
        wordcloud.stopwords = stopwords

        plt.figure()
        plt.axis('off')
        plt.title(f'Wordcloud - {title} ({filename})')

        plt.imshow(wordcloud, interpolation='bilinear') # type: ignore
        plt.show()


def generate_table(data: DataFrames, *, title: str):
    fig = make_subplots() # type: ignore
    filename, dataframe = list(data.items())[0]

    table: List[Any] = []

    for column in dataframe.columns: # type: ignore
        table.append(dataframe[column].tolist()) # type: ignore

    header = {'values': dataframe.columns} # type: ignore
    cells = {'values': table}

    fig.add_table(header=header, cells=cells) # type: ignore

    title_text = f'{title} ({filename})'
    fig.update_layout(title_text=title_text) # type: ignore

    fig.show() # type: ignore


def _normalize_frame_name(name: str) -> str:
    return name.replace('_', ' ').capitalize()


class BaseFrame:
    """Represents the base of a Qualichat frame.
    Generally, you should use the built-in frames that Qualichat
    offers you. However, you can subclass this class and create your
    own frames.

    .. note::

        To automatically generate charts, you must create a method
        decorated with :meth:`generate_chart` that returns a
        :class:`pandas.DataFrame`.

    Attributes
    ----------
    chats: List[:class:`.Chat`]
        All the chats loaded via :meth:`qualichat.load_chats`.
    """

    __slots__ = ('chats', 'charts')

    fancy_name: ClassVar[str]

    def __init__(self, chats: List[Chat]) -> None:
        def predicate(object: object) -> bool:
            if not inspect.ismethod(object):
                return False

            return not object.__name__.startswith('_')

        methods = inspect.getmembers(self, predicate=predicate)
        charts = {}

        for name, method in methods:
            charts[_normalize_frame_name(name)] = method

        self.chats = chats
        self.charts: Dict[str, types.FunctionType] = charts

    def __repr__(self) -> str:
        return '<%s>' % self.__class__.__name__


nlp = spacy.load('pt_core_news_sm') # type: ignore


class KeysFrame(BaseFrame):
    """
    """

    __slots__ = ('api_key')

    fancy_name = 'Keys'

    def __init__(self, chats: List[Chat], api_key: Optional[str]) -> None:
        super().__init__(chats)
        self.api_key = api_key

    def messages(self, chats: ChatsData):
        """
        """
        wordclouds: WordClouds = {}
        title = 'Keys Frame (Messages)'

        for filename, data in chats.items():
            wordcloud_data: List[str] = []
            parsed_messages: List[Message] = []

            for messages in data.values():
                for message in messages:
                    if message['Type'] is not MessageType.default:
                        continue

                    parsed_messages.append(message)

            types = {'Verbs': 'VERB', 'Nouns': 'NOUN', 'Adjectives': 'ADJ'}

            word_type = select('Choose your word cloud type:', types).ask()
            pos = types[word_type]

            with progress_bar as progress:
                for message in progress.track(parsed_messages):
                    text = message['Qty_char_text'] # type: ignore
                    doc = nlp(text) # type: ignore

                    for token in doc: # type: ignore
                        if token.pos_ == pos: # type: ignore
                            wordcloud_data.append(token.text) # type: ignore

            parent = Path(__file__).resolve().parent
            path = parent / 'fonts' / 'Roboto-Regular.ttf'

            configs: Dict[str, Any] = {}
            configs['width'] = 1920
            configs['height'] = 1080
            configs['font_path'] = str(path)
            configs['background_color'] = 'white'

            all_words = ' '.join(wordcloud_data)
            wordcloud = WordCloud(**configs).generate(all_words) # type: ignore

            wordclouds[filename] = wordcloud

        generate_wordcloud(wordclouds, title=title)

    def keyword(self, chats: ChatsData):
        """
        """
        wordclouds: WordClouds = {}

        title = 'Keys Frame (Keyword)'
        keyword: str = input('Enter the keyword you want to analyze:').ask() # type: ignore

        for filename, data in chats.items():
            wordcloud_data: List[str] = []
            parsed_messages: List[Message] = []

            for messages in data.values():
                for message in messages:
                    if message['Type'] is not MessageType.default:
                        continue

                    if keyword.lower() not in message.content.lower():
                        continue

                    parsed_messages.append(message)

            types = {'Verbs': 'VERB', 'Nouns': 'NOUN', 'Adjectives': 'ADJ'}

            word_type = select('Choose your word cloud type:', types).ask()
            pos = types[word_type]

            with progress_bar as progress:
                for message in progress.track(parsed_messages):
                    text = message['Qty_char_text'] # type: ignore
                    doc = nlp(text) # type: ignore

                    for token in doc: # type: ignore
                        if token.pos_ == pos: # type: ignore
                            wordcloud_data.append(token.text) # type: ignore

            parent = Path(__file__).resolve().parent
            path = parent / 'fonts' / 'Roboto-Regular.ttf'

            configs: Dict[str, Any] = {}
            configs['width'] = 1920
            configs['height'] = 1080
            configs['font_path'] = str(path)
            configs['background_color'] = 'white'

            all_words = ' '.join(wordcloud_data)
            wordcloud = WordCloud(**configs).generate(all_words) # type: ignore

            wordclouds[filename] = wordcloud

        generate_wordcloud(wordclouds, title=title)

    # def ratings(self, chats: ChatsData):
    #     """
    #     """
    #     title = 'Keys Frame (Ratings)'
    #     dataframes: DataFrames = {}

    #     columns = [
    #         'Media', 'Actor', 'Date', 'Link',
    #         'Views', 'Likes', 'Comments', 'Title'
    #     ]

    #     if not self.api_key:
    #         log('info', 'No API Key provided. Please provide one.')
    #         return None

    #     client = qualitube.Client(self.api_key)

    #     for filename, data in chats.items():
    #         rows: List[List[Any]] = []

    #         youtube_regex = {
    #             ('youtu', 'be'): SHORT_YOUTUBE_LINK_RE,
    #             ('youtube', 'com'): YOUTUBE_LINK_RE
    #         }

    #         domains_count: DefaultDict[str, int] = defaultdict(int)

    #         views_count: DefaultDict[str, int] = defaultdict(int)
    #         likes_count: DefaultDict[str, int] = defaultdict(int)
    #         comments_count: DefaultDict[str, int] = defaultdict(int)
    #         titles: DefaultDict[str, str] = defaultdict(str)

    #         for messages in data.values():
    #             for message in messages:
    #                 for url in message['Qty_char_links']:
    #                     domain = parse_domain(url)

    #                     if domain == 'YouTube':
    #                         domains_count[url] += 1

    #                         if domains_count[url] != 2:
    #                             continue

    #                         _, domain, suffix = extract(url) # type: ignore
    #                         regex = youtube_regex[(domain, suffix)] # type: ignore

    #                         if not (match := regex.match(url)):
    #                             continue

    #                         id = match.group(1)
    #                         videos = client.get_videos([id])
    #                         print(videos)

    #                         if not videos.videos:
    #                             continue

    #                         video = videos.videos[0]

    #                         views_count[url] = video.view_count # type: ignore
    #                         likes_count[url] = video.like_count # type: ignore
    #                         comments_count[url] = video.comment_count # type: ignore
    #                         titles[url] = video.title # type: ignore

    #                     views = views_count[url] or None
    #                     likes = likes_count[url] or None
    #                     comments = comments_count[url] or None
    #                     video_title = titles[url] or None

    #                     actor = message.actor.display_name
    #                     created_at = str(message.created_at)

    #                     rows.append([
    #                         domain, actor, created_at, url,
    #                         views, likes, comments, video_title
    #                     ])

    #         dataframe = DataFrame(rows, columns=columns)
    # #         dataframes[filename] = dataframe

    #     generate_table(dataframes, title=title)

    def laminations(self, chats: ChatsData):
        """
        """
        title = 'Keys Frame (Laminations)'
        dataframes: DataFrames = {}

        bars = [
            'Qty_char_links', 'Qty_char_emails', 'Qty_char_marks',
            'Qty_char_mentions', 'Qty_char_emoji'
        ]
        lines = ['Qty_messages']

        for filename, data in chats.items():
            rows: List[List[int]] = []

            for messages in data.values():
                links = 0
                marks = 0
                emojis = 0
                emails = 0
                mentions = 0
                total_messages = 0

                for message in messages:
                    links += len(message['Qty_char_links'])
                    marks += len(message['Qty_char_marks'])
                    emojis += len(message['Qty_char_emoji'])
                    emails += len(message['Qty_char_emails'])
                    mentions += len(message['Qty_char_mentions'])
                    total_messages += 1

                rows.append(
                    [links, marks, emojis, emails, mentions, total_messages]
                )

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=bars + lines)
            dataframes[filename] = dataframe

        generate_chart(dataframes, lines=lines, bars=bars, title=title)

    # def test(self, chats: ChatsData):
    #     dataframes: DataFrames = {}

    #     bars = ['Qty_stickers', 'Qty_videos', 'Qty_char_net', 'Qty_char_links']
    #     lines = ['Qty_messages']

    #     for filename, data in chats.items():
    #         rows: List[List[int]] = []

    #         for messages in data.values():
    #             stickers = videos = net_content = links = total_messages = 0

    #             for message in messages:
    #                 if message.actor.display_name != 'As Lavadeiras':
    #                     continue

    #                 if message['Type'] is MessageType.sticker_omitted:
    #                     stickers += 1
    #                 elif message['Type'] is MessageType.video_omitted:
    #                     videos += 1

    #                 if message['Type'] is MessageType.default:
    #                     net_content += len(message['Qty_char_net'].split(' '))
    #                     links += len(message['Qty_char_links'])

    #                 total_messages += 1

    #             rows.append(([stickers, videos, net_content, links, total_messages]))

    #         index = list(data.keys())

    #         dataframe = DataFrame(rows, index=index, columns=bars + lines)
    #         dataframes[filename] = dataframe

    #     generate_chart(dataframes, lines=lines, bars=bars, title='Stickers')

    def links(self, chats: ChatsData):
        """
        """
        title = 'Keys Frame (Links)'
        dataframes: DataFrames = {}

        bars = ['Qty_char_links']
        lines = ['Qty_messages']

        for filename, data in chats.items():
            rows: List[List[int]] = []

            for messages in data.values():
                links = 0
                total_messages = 0

                for message in messages:
                    links += len(message['Qty_char_links'])
                    total_messages += 1

                rows.append([links, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=bars + lines)
            dataframes[filename] = dataframe

        generate_chart(dataframes, lines=lines, bars=bars, title=title)

    def mentions(self, chats: ChatsData):
        """
        """
        title = 'Keys Frame (Mentions)'
        dataframes: DataFrames = {}

        bars = ['Qty_char_mentions']
        lines = ['Qty_messages']

        for filename, data in chats.items():
            rows: List[List[int]] = []

            for messages in data.values():
                mentions = 0
                total_messages = 0

                for message in messages:
                    mentions += len(message['Qty_char_mentions'])
                    total_messages += 1

                rows.append([mentions, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=bars + lines)
            dataframes[filename] = dataframe

        generate_chart(dataframes, lines=lines, bars=bars, title=title)

    def emails(self, chats: ChatsData):
        """
        """
        title = 'Keys Frame (E-mails)'
        dataframes: DataFrames = {}

        bars = ['Qty_char_emails']
        lines = ['Qty_messages']

        for filename, data in chats.items():
            rows: List[List[int]] = []

            for messages in data.values():
                emails = 0
                total_messages = 0

                for message in messages:
                    emails += len(message['Qty_char_emails'])
                    total_messages += 1

                rows.append([emails, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=bars + lines)
            dataframes[filename] = dataframe

        generate_chart(dataframes, lines=lines, bars=bars, title=title)

    def textual_symbols(self, chats: ChatsData):
        """
        """
        title = 'Keys Frame (Textual symbols)'
        dataframes: DataFrames = {}

        bars = ['Qty_char_marks', 'Qty_char_emoji']
        lines = ['Qty_messages']

        for filename, data in chats.items():
            rows: List[List[int]] = []

            for messages in data.values():
                marks = 0
                emojis = 0
                total_messages = 0

                for message in messages:
                    marks += len(message['Qty_char_marks'])
                    emojis += len(message['Qty_char_emoji'])
                    total_messages += 1

                rows.append([marks, emojis, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=bars + lines)
            dataframes[filename] = dataframe

        generate_chart(dataframes, lines=lines, bars=bars, title=title)

#     @word_cloud()
#     def keyword(self, sort_function: SortingFunction) -> WordClouds:
#         """Analyzes the keyword and returns a word cloud with the
#         desired type (word cloud of verbs, adjectives or nouns).
#         """
#         word_clouds: WordClouds = {}

#         log('info', 'Enter the keyword you want to analyze:')
#         keyword = input('» ')

#         for chat in self.chats:
#             data: List[str] = []

#             messages_list: MessagesData = sort_function(chat.messages)
#             parsed_messages: List[Message] = []

#             for messages in messages_list.values():
#                 for message in messages:
#                     if message['Type'] is not MessageType.default:
#                         continue

#                     if keyword.lower() not in message.content.lower():
#                         continue

#                     parsed_messages.append(message)

#             types = {'Verbs': 'VERB', 'Nouns': 'NOUN', 'Adjectives': 'ADJ'}

#             menu = Menu('Choose your word cloud type:', types)
#             pos = menu.run()

#             for i, message in enumerate(parsed_messages, start=1):
#                 text = message['Qty_char_text'] # type: ignore
#                 doc = nlp(text) # type: ignore

#                 for token in doc: # type: ignore
#                     if token.pos_ == pos: # type: ignore
#                         data.append(token.text) # type: ignore

#                 prefix = f'{CYAN}[{chat.filename}]{RESET} Progress'
#                 progress_bar(i, len(parsed_messages), prefix=prefix)

#             parent = Path(__file__).resolve().parent
#             path = parent / 'fonts' / 'Roboto-Regular.ttf'

#             configs = {}
#             configs['width'] = 1920
#             configs['height'] = 1080
#             configs['font_path'] = str(path)
#             configs['background_color'] = 'white'
            
        #     all_words = ' '.join(data)
        #     word_cloud = WordCloud(**configs).generate(all_words) # type: ignore

        #     word_clouds[chat.filename] = word_cloud

        # return word_clouds

#     @word_cloud()
#     def messages(self, sort_function: SortingFunction) -> WordClouds:
#         """Analyzes the chats and returns a word cloud with the desired
#         type (word cloud of verbs, adjectives or nouns).
#          """
#         word_clouds: WordClouds = {}

#         for chat in self.chats:
#             data: List[str] = []

#             messages_list: MessagesData = sort_function(chat.messages)
#             parsed_messages: List[Message] = []

#             for messages in messages_list.values():
#                 for message in messages:
#                     if message['Type'] is not MessageType.default:
#                         continue

#                     parsed_messages.append(message)

#             types = {'Verbs': 'VERB', 'Nouns': 'NOUN', 'Adjectives': 'ADJ'}

#             menu = Menu('Choose your word cloud type:', types)
#             pos = menu.run()

#             for i, message in enumerate(parsed_messages, start=1):
#                 text = message['Qty_char_text']
#                 doc = nlp(text) # type: ignore

#                 for token in doc: # type: ignore
#                     if token.pos_ == pos: # type: ignore
#                         data.append(token.text) # type: ignore

#                 prefix = f'{CYAN}[{chat.filename}]{RESET} Progress'
#                 progress_bar(i, len(parsed_messages), prefix=prefix)

#             parent = Path(__file__).resolve().parent
#             path = parent / 'fonts' / 'Roboto-Regular.ttf'

#             configs = {}
#             configs['width'] = 1920
#             configs['height'] = 1080
#             configs['font_path'] = str(path)
#             configs['background_color'] = 'white'
            
#             all_words = ' '.join(data)
#             word_cloud = WordCloud(**configs).generate(all_words) # type: ignore

#             word_clouds[chat.filename] = word_cloud

#         return word_clouds

#     @generate_table()
#     def rating(self, sort_function: SortingFunction) -> DataFrames:
#         """Analyze the links and bring up YouTube link statistics.
        
#         Only repeated YouTube links are analyzed.
#         """
#         dataframes: DataFrames = {}
#         columns = [
#             'Media', 'Actor', 'Date', 'Link', 'Views', 'Likes', 'Comments', 'Title'
#         ]

#         client = qualitube.Client(self.api_key)

#         for chat in self.chats:
#             data = sort_function(chat.messages)
#             rows: List[List[Any]] = []

#             youtube_regex = {
#                 ('youtu', 'be'): SHORT_YOUTUBE_LINK_RE,
#                 ('youtube', 'com'): YOUTUBE_LINK_RE
#             }

#             domains_count = defaultdict(int) # type: ignore

#             views_count = defaultdict(int) # type: ignore
#             likes_count = defaultdict(int) # type: ignore
#             comments_count = defaultdict(int) # type: ignore
#             titles = defaultdict(str) # type: ignore

#             for messages in data.values():
#                 for message in messages:
#                     for url in message['Qty_char_links']:
#                         domain = parse_domain(url)
#                         actor = message.actor.display_name
#                         created_at = str(message.created_at)

#                         if domain == 'YouTube':
#                             domains_count[url] += 1
                            
#                             if domains_count[url] == 2:
#                                 _, domain, suffix = extract(url) # type: ignore
#                                 regex = youtube_regex[(domain, suffix)] # type: ignore

#                                 if not (match := regex.match(url)):
#                                     continue

#                                 id = match.group(1)
#                                 videos = client.get_videos([id])

#                                 if not videos.videos:
#                                     continue

#                                 video = videos.videos[0]

#                                 views_count[url] = video.view_count # type: ignore
#                                 likes_count[url] = video.like_count # type: ignore
#                                 comments_count[url] = video.comment_count # type: ignore
#                                 titles[url] = video.title # type: ignore

#                         views = views_count[url] or None
#                         likes = likes_count[url] or None
#                         comments = comments_count[url] or None
#                         title = titles[url] or None
                            
#                         rows.append([domain, actor, created_at, url, views, likes, comments, title])

#             dataframe = DataFrame(rows, columns=columns)
#             dataframes[chat.filename] = dataframe

#         return dataframes

#     # @generate_chart(
#     #     bars=[
#     #         'Qty_char_emails', 'Qty_char_marks',
#     #         'Qty_char_mentions', 'Qty_char_emoji',
#     #     ],
#     #     lines=['Qty_messages'],
#     #     title='Keys Frame (Without links)'
#     # )
#     # def without_links(self, sort_function: SortingFunction) -> DataFrames:
#     #     """Shows the amount of lamination elements *except links*
#     #     sent in the chat per month and it will be compared with the
#     #     total messages sent.
#     #     """
#     #     dataframes: DataFrames = {}
#     #     columns = [
#     #         'Qty_char_emails', 'Qty_char_marks',
#     #         'Qty_char_mentions', 'Qty_char_emoji',
#     #         'Qty_messages'
#     #     ]

#     #     for chat in self.chats:
#     #         data = sort_function(chat.messages)
#     #         rows: List[List[int]] = []

#     #         for messages in data.values():
#     #             emails = 0
#     #             marks = 0
#     #             emojis = 0
#     #             mentions = 0
#     #             total_messages = 0

#     #             for message in messages:
#     #                 if message['Qty_char_links']:
#     #                     continue

#     #                 emails += len(message['Qty_char_emails'])
#     #                 marks += len(message['Qty_char_marks'])
#     #                 emojis += len(message['Qty_char_emoji'])
#     #                 mentions += len(message['Qty_char_mentions'])
#     #                 total_messages += 1

#     #             rows.append([emails, marks, emojis, mentions, total_messages])

#     #         index = list(data.keys())

#     #         dataframe = DataFrame(rows, index=index, columns=columns)
#     #         dataframes[chat.filename] = dataframe

#     #     return dataframes

#     # @generate_chart(
#     #     bars=[
#     #         'Qty_char_links', 'Qty_char_emails',
#     #         'Qty_char_marks', 'Qty_char_emoji',
#     #     ],
#     #     lines=['Qty_messages'],
#     #     title='Keys Frame (Without mentions)'
#     # )
#     # def without_mentions(self, sort_function: SortingFunction) -> DataFrames:
#     #     """Shows the amount of lamination elements *except mentions*
#     #     sent in the chat per month and it will be compared with the
#     #     total messages sent.
#     #     """
#     #     dataframes: DataFrames = {}
#     #     columns = [
#     #         'Qty_char_links', 'Qty_char_emails',
#     #         'Qty_char_marks', 'Qty_char_emoji',
#     #         'Qty_messages'
#     #     ]

#     #     for chat in self.chats:
#     #         data = sort_function(chat.messages)
#     #         rows: List[List[int]] = []

#     #         for messages in data.values():
#     #             links = 0
#     #             emails = 0
#     #             marks = 0
#     #             emojis = 0
#     #             total_messages = 0

#     #             for message in messages:
#     #                 if message['Qty_char_mentions']:
#     #                     continue
                    
#     #                 links += len(message['Qty_char_links'])
#     #                 emails += len(message['Qty_char_emails'])
#     #                 marks += len(message['Qty_char_marks'])
#     #                 emojis += len(message['Qty_char_emoji'])
#     #                 total_messages += 1

#     #             rows.append([links, emails, marks, emojis, total_messages])

#     #         index = list(data.keys())

#     #         dataframe = DataFrame(rows, index=index, columns=columns)
#     #         dataframes[chat.filename] = dataframe

#     #     return dataframes

#     # @generate_chart(
#     #     bars=[
#     #         'Qty_char_links', 'Qty_char_marks',
#     #         'Qty_char_emoji', 'Qty_char_mentions',
#     #     ],
#     #     lines=['Qty_messages'],
#     #     title='Keys Frame (Without e-mails)'
#     # )
#     # def without_emails(self, sort_function: SortingFunction) -> DataFrames:
#     #     """Shows the amount of laminations elements *except e-mails*
#     #     sent in the chat per month and it will be compared with the
#     #     total messages sent.
#     #     """
#     #     dataframes: DataFrames = {}
#     #     columns = [
#     #         'Qty_char_links', 'Qty_char_marks',
#     #         'Qty_char_emoji', 'Qty_char_mentions',
#     #         'Qty_messages'
#     #     ]

#     #     for chat in self.chats:
#     #         data = sort_function(chat.messages)
#     #         rows: List[List[int]] = []

#     #         for messages in data.values():
#     #             links = 0
#     #             marks = 0
#     #             emojis = 0
#     #             mentions = 0
#     #             total_messages = 0

#     #             for message in messages:
#     #                 if message['Qty_char_emails']:
#     #                     continue
                    
#     #                 links += len(message['Qty_char_links'])
#     #                 marks += len(message['Qty_char_marks'])
#     #                 emojis += len(message['Qty_char_emoji'])
#     #                 mentions += len(message['Qty_char_mentions'])
#     #                 total_messages += 1

#     #             rows.append(
#     #                 [links, marks, emojis, mentions, total_messages]
#     #             )

#     #         index = list(data.keys())

#     #         dataframe = DataFrame(rows, index=index, columns=columns)
#     #         dataframes[chat.filename] = dataframe

#     #     return dataframes

#     # @generate_chart(
#     #     bars=['Qty_char_links', 'Qty_char_emails', 'Qty_char_mentions',],
#     #     lines=['Qty_messages'],
#     #     title='Keys Frame (Without textual symbols)'
#     # )
#     # def without_textual_symbols(self, sort_function: SortingFunction) -> DataFrames:
#     #     """Shows the amount of laminations elements *except textual
#     #     symbols* sent in the chat per month and it will be compared
#     #     with the total messages sent.
#     #     """
#     #     dataframes: DataFrames = {}
#     #     columns = [
#     #         'Qty_char_links', 'Qty_char_emails',
#     #         'Qty_char_mentions', 'Qty_messages'
#     #     ]

#     #     for chat in self.chats:
#     #         data = sort_function(chat.messages)
#     #         rows: List[List[int]] = []

#     #         for messages in data.values():
#     #             links = 0
#     #             emails = 0
#     #             mentions = 0
#     #             total_messages = 0

#     #             for message in messages:
#     #                 if message['Qty_char_marks'] or message['Qty_char_emoji']:
#     #                     continue
                    
#     #                 links += len(message['Qty_char_links'])
#     #                 emails += len(message['Qty_char_emails'])
#     #                 mentions += len(message['Qty_char_mentions'])
#     #                 total_messages += 1

#     #             rows.append([links, emails, mentions, total_messages])

#     #         index = list(data.keys())

#     #         dataframe = DataFrame(rows, index=index, columns=columns)
#     #         dataframes[chat.filename] = dataframe

#     #     return dataframes
