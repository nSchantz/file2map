from dataclasses import dataclass

IMAGE_TYPE = 0
VIDEO_TYPE = 1
TEXT_TYPE = 2

@dataclass
class FileData:
	id: int=None
	tag: str=None
	long: float=None
	lat: float=None
	url: str=None
