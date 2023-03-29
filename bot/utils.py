import os
from contextlib import contextmanager
from pathlib import Path

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

from bot.logger import logger

@contextmanager
def watermarked_mp4(path: Path, watermark_text: str) -> Path:
    """
    Добавляет текст на видео.
    """
    mp4 = VideoFileClip(path.as_posix())
    output_video_path = path.parent / f'{path.stem}-output.mp4'

    # Сборка текста-вотермарки
    fontsize = mp4.w // 10

    # Перенос строк для длинного текста
    watermark_text_parts = watermark_text.split()
    max_len = mp4.w // (fontsize * 1.2)
    len_sum = 0
    for i in range(len(watermark_text_parts) - 1):
        len_sum += len(watermark_text_parts[i])
        if len_sum > max_len:
            len_sum = 0
            watermark_text_parts[i] += '\n'
    watermark_text = ' '.join(watermark_text_parts)

    text_clip_params = {
        'txt': watermark_text,
        'font': 'Arial-Black',
        'fontsize': fontsize,
        'color': 'white',
    }
    if fontsize > 30:  # Текст будет без обводки, если размер шрифта слишком маленький
        text_clip_params.update({'stroke_color': 'black', 'stroke_width': fontsize // 20})
    watermark = TextClip(**text_clip_params).set_position('bottom').set_duration(mp4.duration)

    logger.info(text_clip_params)

    # Сохранение видео по пути output_video_path
    CompositeVideoClip([mp4, watermark]).write_videofile(output_video_path.as_posix())

    yield output_video_path
    os.remove(output_video_path)
