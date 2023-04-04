import os
import asyncio
from functools import partial
from concurrent.futures import ProcessPoolExecutor
from contextlib import asynccontextmanager
from pathlib import Path

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

from bot.config import DEFAULT_FONT, MAX_WORKERS


EXECUTOR = ProcessPoolExecutor(max_workers=MAX_WORKERS)


def add_text_to_mp4(
        input_path: Path,
        output_path: Path,
        text: str,
        font: str = DEFAULT_FONT,
        font_size=36,
        font_color='white',
        stroke=True,
        stroke_color='black',
        position='bottom',
        stroke_limit=20,
):
    """
    Добавляет текст на видео.
    """
    mp4 = VideoFileClip(input_path.as_posix())
    if mp4.audio:
        mp4 = mp4.without_audio()
    text_clip_params = {
        'txt': text,
        'font': font,
        'fontsize': font_size,
        'color': font_color,
    }
    if stroke and font_size >= stroke_limit:  # Текст будет без обводки, если размер шрифта слишком маленький
        text_clip_params.update({'stroke_color': stroke_color, 'stroke_width': int(font_size // stroke_limit)})
    caption_clip = TextClip(**text_clip_params).set_position(position).set_duration(mp4.duration)

    # Сохранение видео по пути output_video_path
    CompositeVideoClip([mp4, caption_clip]).write_videofile(output_path.as_posix())


async def add_text_to_mp4_async(input_path: Path, output_path: Path, text: str, **kwargs):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(EXECUTOR, partial(add_text_to_mp4, **kwargs), input_path, output_path, text)


@asynccontextmanager
async def captioned_mp4(input_path: Path, caption: str, **kwargs):
    output_path = input_path.parent / f'{input_path.stem}-output.mp4'
    await add_text_to_mp4_async(input_path, output_path, caption, **kwargs)
    yield output_path
    os.remove(output_path)
