import os
from contextlib import contextmanager
from pathlib import Path
import textwrap

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

from bot.config import DEFAULT_FONT


@contextmanager
def captioned_mp4(
        path: Path,
        caption: str,
        font: str = DEFAULT_FONT,
        font_size=36,
        font_color='white',
        stroke=True,
        stroke_color='black',
        position='bottom',
        stroke_limit=20
) -> Path:
    """
    Добавляет текст на видео.
    """
    mp4 = VideoFileClip(path.as_posix())
    output_video_path = path.parent / f'{path.stem}-output.mp4'
    text_clip_params = {
        'txt': caption,
        'font': font,
        'fontsize': font_size,
        'color': font_color,
    }
    if stroke and font_size >= stroke_limit:  # Текст будет без обводки, если размер шрифта слишком маленький
        text_clip_params.update({'stroke_color': stroke_color, 'stroke_width': int(font_size // stroke_limit)})
    caption_clip = TextClip(**text_clip_params).set_position(position).set_duration(mp4.duration)

    # Сохранение видео по пути output_video_path
    CompositeVideoClip([mp4, caption_clip]).write_videofile(output_video_path.as_posix())

    yield output_video_path
    os.remove(output_video_path)
