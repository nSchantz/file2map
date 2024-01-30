IMAGE_TYPE = 0
VIDEO_TYPE = 1
TEXT_TYPE = 2

@dataclass
class FileData:
	id: int,
	tag: str,
	state: str,
	long: int,
	lat: int,
	url: str,
