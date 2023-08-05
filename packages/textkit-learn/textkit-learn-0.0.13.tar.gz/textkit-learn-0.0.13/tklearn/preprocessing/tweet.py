import enum
import re
import string
from typing import Text, List
from xml.sax import saxutils
import emoji
from six import string_types
from collections.abc import Iterable

from tklearn.preprocessing import TextPreprocessor

__all__ = [
    'Normalize',
    'TweetPreprocessor',
]


@enum.unique
class Normalize(enum.Enum):
    NONE = 0
    ALL = 1
    LINKS = 2
    HASHTAGS = 3
    MENTIONS = 4
    IMAGES = 5


class TweetPreprocessor(TextPreprocessor):
    """ Preprocessor for Tweets.

    Instance of this class can be used to create a preprocessor for tour tweet data.
    Several options are provided and you might be using them according to your use case.
    """
    RE_LINKS = re.compile(r'(https?://\S+)')
    RE_IMAGE_LINKS = re.compile(r'(pic.twitter.com\S+)')
    RE_MENTIONS = re.compile(r'(@[a-zA-Z0-9_]{1,15})')
    RE_HASHTAGS = re.compile(r'(#\w+)')

    def __init__(self, normalize=Normalize.NONE, lowercase=False, **kwargs):
        """ Initialize `TweetPreprocessor` object.

        Parameters
        ----------
        kwargs
            Parameters
        """
        super(TweetPreprocessor, self).__init__()
        self.normalize = []
        self.lowercase = lowercase
        if normalize == Normalize.ALL:
            self.normalize = [
                Normalize.LINKS,
                Normalize.HASHTAGS,
                Normalize.MENTIONS,
                Normalize.IMAGES,
            ]
        elif (normalize != Normalize.NONE) and isinstance(normalize, Iterable):
            for item in normalize:
                if isinstance(item, string_types):
                    if not item.endswith('s'):
                        item = '{}s'.format(item)
                    item = Normalize[item.upper()]
                self.normalize.append(item)

    @staticmethod
    def _replace(s: List[Text], old: Text, new: Text) -> List[Text]:
        return [new if x == old else x for x in s if x.strip() != '']

    def preprocess(self, s: Text) -> Text:
        """ Preprocess the input text. Expected input is a Tweet text.

        Parameters
        ----------
        s
            Input Tweet text.

        Returns
        -------
            Preprocessed tweet.
        """
        s = self._clean_tweet(s)
        if Normalize.LINKS in self.normalize:
            s = self.RE_LINKS.sub('<link>', s)
        if Normalize.IMAGES in self.normalize:
            s = self.RE_IMAGE_LINKS.sub('<image>', s)
        if Normalize.HASHTAGS in self.normalize:
            s = self.RE_HASHTAGS.sub('<hashtag>', s)
        if Normalize.MENTIONS in self.normalize:
            s = self.RE_MENTIONS.sub('<mention>', s)
        tokens = s.split()
        for ns in self.normalize:
            if isinstance(ns, str):
                pass
            elif isinstance(ns, tuple):
                assert len(ns) == 2, \
                    'Required a tuple of size 2 indicating (new_word, old_words) values for the normalization.'
                assert isinstance(ns[1], list), \
                    'Required a list of old values to replace with the new value.'
                for n in ns[1]:
                    tokens = self._replace(tokens, n, ns[0])
        if self.lowercase:
            return ' '.join(tokens).lower()
        else:
            return ' '.join(tokens)

    @staticmethod
    def _clean_tweet(x):
        """ Cleans a given text (tweet) while keeping important characters.

        Parameters
        ----------
        x
            Input String.
        Returns
        -------
            Cleaned Text.
        """
        x = saxutils.unescape(x)
        x = x.replace('\xa0', ' ')
        x = emoji.demojize(x)
        x = ''.join(filter(lambda item: item in set(string.printable), x))
        x = emoji.emojize(x)
        return x
