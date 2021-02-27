import logging
from typing import Tuple, Optional

import mutagen

PREFERRED_MIME = {'audio/x-m4a', 'audio/mpeg', 'video/quicktime', 'video/mp4', 'video/x-m4v'}

logger = logging.getLogger('wwwsfi.common.audio_metadata')


def get_audio_metadata(file_path: str) -> Optional[Tuple[str, int]]:
    try:
        meta = mutagen.File(file_path)
        mime = next((m for m in meta.mime if m in PREFERRED_MIME), meta.mime[0])
        duration = int(meta.info.length)
        return mime, duration
    except Exception as ex:
        logger.info('Unsupported audio file {} - {}'.format(file_path, ex))
        return None
