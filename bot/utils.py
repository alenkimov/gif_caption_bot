import os
from contextlib import contextmanager
from pathlib import Path

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

from bot.config import DEFAULT_FONT


@contextmanager
def captioned_mp4(
        path: Path,
        caption: str,
        font: str = DEFAULT_FONT,
        font_size=10,
        font_color='white',
        stroke=True,
        stroke_color='black',
        position='bottom',
        transition=True,
) -> Path:
    """
    Добавляет текст на видео.
    """
    mp4 = VideoFileClip(path.as_posix())
    output_video_path = path.parent / f'{path.stem}-output.mp4'

    font_size = mp4.w * font_size // 100

    if transition:  # Перенос строк для длинного текста
        caption_parts = caption.split()
        max_len = mp4.w // (font_size * 1.2)
        len_sum = 0
        for i in range(len(caption_parts) - 1):
            len_sum += len(caption_parts[i])
            if len_sum > max_len:
                len_sum = 0
                caption_parts[i] += '\n'
        caption = ' '.join(caption_parts)

    text_clip_params = {
        'txt': caption,
        'font': font,
        'fontsize': font_size,
        'color': font_color,
    }
    if stroke and font_size > 30:  # Текст будет без обводки, если размер шрифта слишком маленький
        text_clip_params.update({'stroke_color': stroke_color, 'stroke_width': font_size // 20})
    caption_clip = TextClip(**text_clip_params).set_position(position).set_duration(mp4.duration)

    # Сохранение видео по пути output_video_path
    CompositeVideoClip([mp4, caption_clip]).write_videofile(output_video_path.as_posix())

    yield output_video_path
    os.remove(output_video_path)
