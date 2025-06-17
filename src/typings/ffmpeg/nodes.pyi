from .__helper_types import CLIValue
from collections.abc import Callable
from typing import (
    Any,
    Literal,
    Optional,
    TypeVar,
    Callable,
    ParamSpec,
    Protocol,
    type_check_only,
)
from .dag import KwargReprNode

type StreamSelector = Literal["a", "v"]
type StreamLabel = str | int | None

# We only define this as a dict for now, we can provide a better definition later
type StreamMap = dict[StreamLabel, Stream]

type StreamSpec = None | Stream | list[Stream] | tuple[Stream] | StreamMap

class Stream:
    """Represents the outgoing edge of an upstream node; may be used to create more downstream nodes."""

    def __init__(
        self,
        upstream_node: Node,
        upstream_label: StreamLabel,
        node_types: dict[Node, Node],
        upstream_selector: Optional[StreamSelector] = None,
    ) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __getitem__(self, index: StreamSelector) -> Stream:
        """
        Select a component (audio, video) of the stream.

        Example:
            Process the audio and video portions of a stream independently::

                input = ffmpeg.input('in.mp4')
                audio = input['a'].filter("aecho", 0.8, 0.9, 1000, 0.3)
                video = input['v'].hflip()
                out = ffmpeg.output(audio, video, 'out.mp4')
        """
        ...

    @property
    def audio(self) -> Stream:
        """Select the audio-portion of a stream.

        Some ffmpeg filters drop audio streams, and care must be taken
        to preserve the audio in the final output.  The ``.audio`` and
        ``.video`` operators can be used to reference the audio/video
        portions of a stream so that they can be processed separately
        and then re-combined later in the pipeline.  This dilemma is
        intrinsic to ffmpeg, and ffmpeg-python tries to stay out of the
        way while users may refer to the official ffmpeg documentation
        as to why certain filters drop audio.

        ``stream.audio`` is a shorthand for ``stream['a']``.

        Example:
            Process the audio and video portions of a stream independently::

                input = ffmpeg.input('in.mp4')
                audio = input.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
                video = input.video.hflip()
                out = ffmpeg.output(audio, video, 'out.mp4')
        """
        ...

    @property
    def video(self) -> Stream:
        """Select the video-portion of a stream.

        Some ffmpeg filters drop audio streams, and care must be taken
        to preserve the audio in the final output.  The ``.audio`` and
        ``.video`` operators can be used to reference the audio/video
        portions of a stream so that they can be processed separately
        and then re-combined later in the pipeline.  This dilemma is
        intrinsic to ffmpeg, and ffmpeg-python tries to stay out of the
        way while users may refer to the official ffmpeg documentation
        as to why certain filters drop audio.

        ``stream.video`` is a shorthand for ``stream['v']``.

        Example:
            Process the audio and video portions of a stream independently::

                input = ffmpeg.input('in.mp4')
                audio = input.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
                video = input.video.hflip()
                out = ffmpeg.output(audio, video, 'out.mp4')
        """
        ...

def get_stream_map(
    stream_spec: StreamSpec,
) -> StreamMap: ...
def get_stream_map_nodes(stream_map: StreamMap) -> list[Node]: ...
def get_stream_spec_nodes(stream_spec: StreamSpec) -> list[Node]: ...

class Node(KwargReprNode):
    """Node base"""

    __incoming_stream_types: Stream
    __outgoing_stream_type: Stream

    def __init__(
        self,
        stream_spec: StreamSpec,
        name: str,
        incoming_stream_types: Stream,
        outgoing_stream_type: Stream,
        min_inputs: int,
        max_inputs: int,
        args: CLIValue = ...,
        kwargs: CLIValue = ...,
    ) -> None: ...
    def stream(
        self,
        label: Optional[StreamLabel] = None,
        selector: Optional[StreamSelector] = None,
    ) -> Stream:
        """Create an outgoing stream originating from this node.

        More nodes may be attached onto the outgoing stream.
        """
        ...

    def __getitem__(self, item: slice) -> Stream:
        """Create an outgoing stream originating from this node; syntactic sugar for ``self.stream(label)``.
        It can also be used to apply a selector: e.g. ``node[0:'a']`` returns a stream with label 0 and
        selector ``'a'``, which is the same as ``node.stream(label=0, selector='a')``.

        Example:
            Process the audio and video portions of a stream independently::

                input = ffmpeg.input('in.mp4')
                audio = input[:'a'].filter("aecho", 0.8, 0.9, 1000, 0.3)
                video = input[:'v'].hflip()
                out = ffmpeg.output(audio, video, 'out.mp4')
        """
        ...

class FilterableStream(Stream, FilterOperatorProtocol):
    def __init__(
        self,
        upstream_node: Node,
        upstream_label: StreamLabel,
        upstream_selector: StreamSelector = ...,
    ) -> None: ...

class InputNode(Node):
    """InputNode type"""

    def __init__(
        self, name: str, args: CLIValue = ..., kwargs: CLIValue = ...
    ) -> None: ...
    @property
    def short_repr(self) -> str: ...

class FilterNode(Node):
    def __init__(
        self,
        stream_spec: StreamSpec,
        name: str,
        max_inputs: int = ...,
        args: CLIValue = ...,
        kwargs: CLIValue = ...,
    ) -> None: ...

class OutputNode(Node):
    def __init__(
        self, stream: Stream, name: str, args: CLIValue = ..., kwargs: CLIValue = ...
    ) -> None: ...
    @property
    def short_repr(self) -> str: ...

class OutputStream(Stream):
    def __init__(
        self,
        upstream_node: Node,
        upstream_label: StreamLabel,
        upstream_selector: StreamSelector = ...,
    ) -> None: ...

class MergeOutputsNode(Node):
    def __init__(self, streams: set[Stream], name: str) -> None: ...

class GlobalNode(Node):
    def __init__(
        self, stream: Stream, name: str, args: CLIValue = ..., kwargs: CLIValue = ...
    ) -> None: ...

DecoratorParamSpec = ParamSpec("DecoratorParamSpec")
DecoratorReturn = TypeVar("DecoratorReturn")

# This decorator assigns the given function to the given stream class.
def stream_operator(
    stream_classes: set[type[Stream]] = {Stream}, name: str | None = None
) -> Callable[
    [Callable[DecoratorParamSpec, DecoratorReturn]],
    Callable[DecoratorParamSpec, DecoratorReturn],
]:
    """Assigns methods (like .view, etc.) to a given Stream"""
    ...

def filter_operator(
    name: str | None = None,
) -> Callable[
    [Callable[DecoratorParamSpec, DecoratorReturn]],
    Callable[DecoratorParamSpec, DecoratorReturn],
]:
    """Assigns methods (like .output, .filter, etc.) to FilterableStream"""
    ...

def output_operator(
    name: str | None = None,
) -> Callable[
    [Callable[DecoratorParamSpec, DecoratorReturn]],
    Callable[DecoratorParamSpec, DecoratorReturn],
]:
    """Assigns methods (like .compile, .run, etc.) to OutputStream"""
    ...

@type_check_only
class FilterOperatorProtocol(Protocol):
    """
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.filter_multi_output = filter_multi_output
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.filter = filter
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.filter_ = filter_
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.split = split
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.asplit = asplit
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.setpts = setpts
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.trim = trim
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.overlay = overlay
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.hflip = hflip
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.vflip = vflip
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.crop = crop
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawbox = drawbox
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawtext = drawtext
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.overlay = overlay
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.hflip = hflip
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.vflip = vflip
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.crop = crop
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawbox = drawbox
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawtext = drawtext
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.hflip = hflip
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.vflip = vflip
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.crop = crop
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawbox = drawbox
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawtext = drawtext
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.crop = crop
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawbox = drawbox
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawtext = drawtext
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawbox = drawbox
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawtext = drawtext
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.drawtext = drawtext
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.concat = concat
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.zoompan = zoompan
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.hue = hue
    stream_operator applying: <class 'ffmpeg.nodes.FilterableStream'>.colorchannelmixer = colorchannelmixer
    """

    def output(*streams_and_filename: str | Stream, **kwargs: CLIValue) -> OutputStream:
        """Output file URL

        Syntax:
            `ffmpeg.output(stream1[, stream2, stream3...], filename, **ffmpeg_args)`

        Any supplied keyword arguments are passed to ffmpeg verbatim (e.g.
        ``t=20``, ``f='mp4'``, ``acodec='pcm'``, ``vcodec='rawvideo'``,
        etc.).  Some keyword-arguments are handled specially, as shown below.

        Args:
            video_bitrate: parameter for ``-b:v``, e.g. ``video_bitrate=1000``.
            audio_bitrate: parameter for ``-b:a``, e.g. ``audio_bitrate=200``.
            format: alias for ``-f`` parameter, e.g. ``format='mp4'``
                (equivalent to ``f='mp4'``).

        If multiple streams are provided, they are mapped to the same
        output.

        To tell ffmpeg to write to stdout, use ``pipe:`` as the filename.

        Official documentation: `Synopsis <https://ffmpeg.org/ffmpeg.html#Synopsis>`__
        """
        ...

__all__ = ["Stream"]
