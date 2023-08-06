from __future__ import division

import os.path as osp
from pathlib import Path
import shutil
import subprocess
from tempfile import NamedTemporaryFile

import skvideo.io


def hhmmss_to_seconds(ts):
    try:
        return float(ts)
    except ValueError:
        return sum(
            float(x) * 60 ** i
            for i, x in enumerate(reversed(ts.split(':'))))


def get_video_duration(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    return float(metadata['video']['@duration'])


def get_video_avg_frame_rate(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    a, b = metadata['video']['@avg_frame_rate'].split('/')
    a = int(a)
    b = int(b)
    return a / b


def get_video_size(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    height = int(metadata['video']['@height'])
    width = int(metadata['video']['@width'])
    return width, height


def get_video_n_frame(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    if '@nb_frames' not in metadata['video']:
        fps = get_video_avg_frame_rate(video_path)
        return int(fps * get_video_duration(video_path))
    return int(metadata['video']['@nb_frames'])


def split_video(video_file_path, output_path=None,
                start_time=None, end_time=None):
    if start_time is None and end_time is None:
        raise ValueError
    start_time = start_time or 0.0
    end_time = end_time or get_video_duration(video_file_path)
    command = ['ffmpeg',
               '-y',
               '-ss', str(int(start_time)),
               '-t', str(int(end_time - start_time)),
               '-i', str(video_file_path)]
    if output_path is None:
        suffix = Path(video_file_path).suffix
        with NamedTemporaryFile(delete=True, suffix=suffix) as tmp:
            command.append(tmp.name)
            print(f'Running \"{" ".join(command)}\"')
            subprocess.call(command)
            shutil.copy(tmp.name, video_file_path)
    else:
        command.append(str(output_path))
        print(f'Running \"{" ".join(command)}\"')
        subprocess.call(command)
