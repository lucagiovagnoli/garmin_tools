import pytz
from geopy import distance
import sys
from dateutil import parser
import datetime
from dataclasses import dataclass
import xml.etree.ElementTree as ET


BREAK_SEC = 5 * 60  # 5 minutes
GHOST_SEGMENT_DISTANCE_M = 250  # meters
TIMEZONE = 'US/Pacific'

@dataclass
class Trkpt:
    lat: float
    lon: float
    time: str

    def distance(self, other):
        return dist(self.lat, self.lon, other.lat, other.lon)


@dataclass
class Segment:
    points: list[Trkpt]

    # duration of this segment in seconds
    def duration(self):
        return (self.points[-1].time - self.points[0].time).total_seconds()

    def repr_h_difference(self, time1: datetime.datetime, time2: datetime.datetime):
        return repr_timeframe((time1 - time2).total_seconds())

    def repr_duration(self):
        return self.repr_h_difference(self.points[-1].time, self.points[0].time)

    def __repr__(self):
        return f'seg: {to_h(self.points[0].time)} - {to_h(self.points[-1].time)}'


def repr_timeframe(seconds: int):
    return str(int(seconds // 3600)) + "h" + str(int((seconds // 60) % 60))


def get_trk_child(root):
    for child in root:
        if 'trk' in child.tag:
            return child

def get_trkseg_child(trk):
    for child in trk:
        if 'trkseg' in child.tag:
            return child

def long_break(current_time: datetime.datetime, previous_time: datetime.datetime):
    # import ipdb; ipdb.set_trace()
    return (current_time - previous_time).total_seconds() > BREAK_SEC


def to_h(time: datetime.datetime):
    return time.astimezone(pytz.timezone(TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S')

def h_difference(time1: datetime.datetime, time2: datetime.datetime):
    return str(int((time1 - time2).total_seconds() // 3600)
    ) + "h" + str(int(((time1 - time2).total_seconds() // 60) % 60))


def print_stats(segments):
    print(f"Total segments: {len(segments)}")
    total_moving_seconds = 0
    for index, segment in enumerate(segments):
        segment = Segment(segment)
        # import ipdb; ipdb.set_trace()
        print(segment, f'(total time: {segment.repr_duration()})')
        total_moving_seconds += segment.duration()

    print(f"Total time: {h_difference(segments[-1][-1].time, segments[0][0].time)}")
    print(f"Total moving time: {repr_timeframe(total_moving_seconds)}")


def dist(lat1: float, lon1: float, lat2: float, lon2: float):
    return distance.geodesic((lat1, lon1), (lat2, lon2)).m


def main(filename):
    root = ET.parse(filename).getroot()

    segments = []
    segment = []
    previous_trkpt = None
    trkseg = get_trkseg_child(get_trk_child(root))
    for item in trkseg:
        trkpt = Trkpt(
            lat=item.attrib['lat'],
            lon=item.attrib['lon'], 
            time=parser.parse(item[1].text),
        )
        if not previous_trkpt:
            previous_trkpt = trkpt

        if long_break(trkpt.time, previous_trkpt.time):
            segments.append(segment)
            segment = []
        # If points are really far, add the difference as its own segment
        if trkpt.distance(previous_trkpt) > GHOST_SEGMENT_DISTANCE_M:
            segments.append([previous_trkpt, trkpt])
            segment = []
        else:
            segment.append(trkpt)

        previous_trkpt = trkpt

    if segment:
        segments.append(segment)

    print_stats(segments)


def test_distance():
    assert dist(35.3524,135.0302, 35.3532,135.0305) == 92.85194331754518


if __name__ == '__main__':
    test_distance()
    main(sys.argv[1])

