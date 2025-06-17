from typing import Protocol, type_check_only

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
