# ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus output.webm
import ffmpeg


def main():
    input_stream = ffmpeg.input("")
    print()
    print(repr(input_stream))
    print(type(input_stream))


# def convert_to_webm(input_file: str, output_file: str):
#     """Converts a video file to WebM format using FFmpeg."""
#     input_stream = ffmpeg.input(input_file)

#     input_stream['a']

#     input_stream.output(
#     output_file,
#     vcodec='libvpx-vp9',
#     crf=30,
#     b='0',  # Bitrate for video
#     audio_bitrate='128k',
#     acodec='libopus'
# ).run()


# def input(filename, **kwargs):
#     """Input file URL (ffmpeg ``-i`` option)

#     Any supplied kwargs are passed to ffmpeg verbatim (e.g. ``t=20``,
#     ``f='mp4'``, ``acodec='pcm'``, etc.).

#     To tell ffmpeg to read from stdin, use ``pipe:`` as the filename.

#     Official documentation: `Main options <https://ffmpeg.org/ffmpeg.html#Main-options>`__
#     """
#     kwargs['filename'] = filename
#     fmt = kwargs.pop('f', None)
#     if fmt:
#         if 'format' in kwargs:
#             raise ValueError("Can't specify both `format` and `f` kwargs")
#         kwargs['format'] = fmt
#     return InputNode(input.__name__, kwargs=kwargs).stream()

# # noinspection PyMethodOverriding
# class InputNode(Node):
#     """InputNode type"""

#     def __init__(self, name, args=[], kwargs={}):
#         super(InputNode, self).__init__(
#             stream_spec=None,
#             name=name,
#             incoming_stream_types={},
#             outgoing_stream_type=FilterableStream,
#             min_inputs=0,
#             max_inputs=0,
#             args=args,
#             kwargs=kwargs,
#         )

#     @property
#     def short_repr(self):
#         return os.path.basename(self.kwargs['filename'])


# class FilterableStream(Stream):
#     def __init__(self, upstream_node, upstream_label, upstream_selector=None):
#         super(FilterableStream, self).__init__(
#             upstream_node, upstream_label, {InputNode, FilterNode}, upstream_selector
#         )
