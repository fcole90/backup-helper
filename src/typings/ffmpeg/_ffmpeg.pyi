from .nodes import (
    filter_operator,
    output_operator,
    Stream,
    FilterableStream,
    OutputStream,
)
from .__helper_types import CLIValue

def input(filename: str, **kwargs: CLIValue) -> FilterableStream:
    """Input file URL (ffmpeg ``-i`` option)

    Any supplied kwargs are passed to ffmpeg verbatim (e.g. ``t=20``,
    ``f='mp4'``, ``acodec='pcm'``, etc.).

    To tell ffmpeg to read from stdin, use ``pipe:`` as the filename.

    Official documentation: `Main options <https://ffmpeg.org/ffmpeg.html#Main-options>`__
    """

@output_operator()
def global_args(stream: Stream, *args: CLIValue) -> None:
    """Add extra global command-line argument(s), e.g. ``-progress``."""
    ...

@output_operator()
def overwrite_output(stream: Stream) -> None:
    """Overwrite output files without asking (ffmpeg ``-y`` option)

    Official documentation: `Main options <https://ffmpeg.org/ffmpeg.html#Main-options>`__
    """
    ...

@output_operator()
def merge_outputs(*streams: Stream) -> None:
    """Include all given outputs in one ffmpeg command line"""
    ...

@filter_operator()
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

__all__ = ["input", "merge_outputs", "output", "overwrite_output"]
