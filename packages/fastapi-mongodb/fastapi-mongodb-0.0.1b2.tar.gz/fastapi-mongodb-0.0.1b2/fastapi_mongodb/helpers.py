"""Classes and functions to provide common timezones, profiling etc."""
import datetime
import functools
import time
import tracemalloc
import typing
import zoneinfo

from fastapi_mongodb.logging import simple_logger

__all__ = ["get_utc_timezone", "utc_now", "as_utc", "BaseProfiler"]


@functools.lru_cache()
def get_utc_timezone() -> zoneinfo.ZoneInfo:
    """Return UTC zone info."""
    return zoneinfo.ZoneInfo(key="UTC")


def utc_now() -> datetime.datetime:
    """Return current datetime with UTC zone info."""
    return datetime.datetime.now(tz=get_utc_timezone())


def as_utc(date_time: datetime.datetime) -> datetime.datetime:
    """Get datetime object and convert it to datetime with UTC zone info."""
    return date_time.astimezone(tz=get_utc_timezone())


class BaseProfiler:
    def __init__(
        self,
        number_frames: int = 10,
        include_files: list[str] = None,
        exclude_files: list[str] = None,
        show_timing: bool = True,
        show_memory: bool = True,
    ):
        self.number_frames = number_frames
        self.include_files = include_files or []
        self.exclude_files = exclude_files or []
        self.show_timing = show_timing
        self.show_memory = show_memory
        self._start_time = None
        self._end_time = None

    def __call__(self, func):
        """Call function to work with profiler as decorator."""

        @functools.wraps(func)
        def decorated(*args, **kwargs):
            self._start_trace_malloc()
            self._set_start_time()
            result = func(*args, **kwargs)
            self._set_end_time()
            self._print_timing(name=func.__name__)
            self._end_trace_malloc()
            return result

        return decorated

    def _set_start_time(self):
        """Set time start point."""
        self._start_time = time.time()

    def _set_end_time(self):
        """Set time end point."""
        self._end_time = time.time()

    def __enter__(self):
        """Start profiling."""
        self._start_trace_malloc()
        self._set_start_time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End profiling."""
        self._set_end_time()
        self._print_timing(name="CODE BLOCK")
        self._end_trace_malloc()

    def _start_trace_malloc(self):
        if not self.show_memory:
            return

        tracemalloc.start(self.number_frames) if self.number_frames else tracemalloc.start()

    def _end_trace_malloc(self):
        if not self.show_memory:
            return

        simple_logger.debug(msg="=== START SNAPSHOT ===")
        snapshot = tracemalloc.take_snapshot()
        snapshot = snapshot.filter_traces(filters=self._get_trace_malloc_filters())
        for stat in snapshot.statistics(key_type="lineno", cumulative=True):
            simple_logger.debug(msg=f"{stat}")
        size, peak = tracemalloc.get_traced_memory()
        snapshot_size = tracemalloc.get_tracemalloc_memory()
        simple_logger.debug(
            msg=f"❕size={self._bytes_to_megabytes(size=size)}, "
            f"❗peak={self._bytes_to_megabytes(size=peak)}, "
            f"💾snapshot_size={self._bytes_to_megabytes(size=snapshot_size)}"
        )
        tracemalloc.clear_traces()
        simple_logger.debug(msg="=== END SNAPSHOT ===")

    def _get_trace_malloc_filters(
        self,
    ) -> list[typing.Union[tracemalloc.Filter, tracemalloc.DomainFilter]]:
        filters = [tracemalloc.Filter(inclusive=True, filename_pattern=file_name) for file_name in self.include_files]

        for file_name in self.exclude_files:
            filters.append(tracemalloc.Filter(inclusive=False, filename_pattern=file_name))
        return filters

    @staticmethod
    def _bytes_to_megabytes(size: int, precision: int = 3):
        return f"{size / 1024.0 / 1024.0:.{precision}f} MB"

    def _print_timing(self, name: str, precision: int = 6):
        if not self.show_timing:
            return
        simple_logger.debug(
            f"📊Execution timing of: '{name}' ⏱: {self._end_time - self._start_time:.{precision}f} seconds"
        )
