import os
from io import BytesIO
from contextlib import contextmanager
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


@contextmanager
def watermarked_photo(photo: BytesIO, watermark_text: str) -> BytesIO:
    """
    Добавляет текст на изображение.
    """
    image = Image.open(photo)
    font = ImageFont.truetype("arial.ttf", 50)
    drawer = ImageDraw.Draw(image)
    drawer.text((50, 100), watermark_text, font=font, fill='black')
    with BytesIO() as output:
        image.save(output, format="JPEG")
        yield output


@contextmanager
def watermarked_mp4(path: Path, watermark_text: str) -> Path:
    """
    Добавляет текст на видео.
    """
    mp4 = VideoFileClip(path.as_posix())
    output_video_path = path.parent / f'{path.stem}-output.mp4'

    watermark = (
        TextClip(txt=watermark_text,
                 font='Arial-Black', fontsize=40, color='white',
                 stroke_color='black', stroke_width=1)
        .set_position('bottom')
        .set_duration(mp4.duration)
    )

    watermarked_mp4 = CompositeVideoClip([mp4, watermark])
    watermarked_mp4.write_videofile(output_video_path.as_posix())
    yield output_video_path
    os.remove(output_video_path)
