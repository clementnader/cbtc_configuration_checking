#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *


__all__ = ["get_all_accessible_segments_from", "get_all_upstream_segments", "get_all_downstream_segments",
           "update_all_accessible_segments", "get_all_positions_at_a_distance_from_a_point",
           "get_next_objects_from_a_point"]


DOWNSTREAM_ACCESSIBLE_SEGMENTS = dict()
UPSTREAM_ACCESSIBLE_SEGMENTS = dict()


def get_all_upstream_segments(seg: str) -> set[tuple[str, bool]]:
    global UPSTREAM_ACCESSIBLE_SEGMENTS
    if not UPSTREAM_ACCESSIBLE_SEGMENTS:
        update_all_accessible_segments()
    return UPSTREAM_ACCESSIBLE_SEGMENTS[seg]


def get_all_downstream_segments(seg: str) -> set[tuple[str, bool]]:
    global DOWNSTREAM_ACCESSIBLE_SEGMENTS
    if not DOWNSTREAM_ACCESSIBLE_SEGMENTS:
        update_all_accessible_segments()
    return DOWNSTREAM_ACCESSIBLE_SEGMENTS[seg]


def update_all_accessible_segments() -> None:
    global DOWNSTREAM_ACCESSIBLE_SEGMENTS, UPSTREAM_ACCESSIBLE_SEGMENTS
    if DOWNSTREAM_ACCESSIBLE_SEGMENTS and UPSTREAM_ACCESSIBLE_SEGMENTS:
        return
    seg_dict = load_sheet(DCSYS.Seg)
    for seg in seg_dict:
        DOWNSTREAM_ACCESSIBLE_SEGMENTS[seg] = get_all_accessible_segments_from(seg, downstream=True)
        UPSTREAM_ACCESSIBLE_SEGMENTS[seg] = get_all_accessible_segments_from(seg, downstream=False)


def get_all_accessible_segments_from(start_seg: str, downstream: bool) -> set[tuple[str, bool]]:
    list_segs = set()

    def inner_recurs_next_seg(seg: str, inner_downstream: bool, path: list[str]):
        nonlocal list_segs
        list_segs.add((seg, inner_downstream))
        for next_seg in get_linked_segments(seg, inner_downstream):
            if is_segment_depolarized(next_seg) and seg in get_associated_depolarization(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            if next_seg in path or (next_seg, next_inner_downstream) in list_segs:
                # We check if we have made a full turn and reach a segment that we have already run through
                # in the current path,
                # and we check if we have not already made the work for this segment and direction
                continue
            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [next_seg])

    inner_recurs_next_seg(start_seg, downstream, [start_seg])
    return list_segs


def get_all_positions_at_a_distance_from_a_point(seg: str, x: float, direction: str, distance: float
                                                 ) -> list[tuple[str, float, str]]:
    list_positions = list()

    def inner_recurs_next_seg(inner_seg: str, inner_x: float, inner_downstream: bool, path: list[str],
                              remaining_distance: float):
        inner_direction = Direction.CROISSANT if inner_downstream else Direction.DECROISSANT
        shifted_x = round(inner_x + (1 if inner_downstream else -1) * remaining_distance, 5)
        if 0 <= shifted_x <= get_segment_length(inner_seg):
            list_positions.append((inner_seg, shifted_x, inner_direction))
            return

        linked_segs = get_linked_segments(inner_seg, inner_downstream)
        if not linked_segs:
            # shifting by the distance results beyond end of track, we consider end of track as the position
            list_positions.append((inner_seg, get_segment_length(inner_seg) if inner_downstream else 0,
                                   inner_direction))
            return

        remaining_distance = round(shifted_x - get_segment_length(inner_seg), 5) if inner_downstream else -shifted_x
        for next_seg in linked_segs:
            if is_segment_depolarized(next_seg) and inner_seg in get_associated_depolarization(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream
            if next_seg in path:
                # We stop if we have made a full turn in the current path to avoid infinite loop with ring configuration
                continue
            next_inner_x = 0 if next_inner_downstream else get_segment_length(next_seg)
            inner_recurs_next_seg(next_seg, next_inner_x, next_inner_downstream, path + [next_seg], remaining_distance)

    downstream = direction == Direction.CROISSANT
    inner_recurs_next_seg(seg, x, downstream, [seg], distance)
    return list_positions


def get_next_objects_from_a_point(seg: str, x: float, direction: str, obj_type: str, obj_direction: str = None
                                  ) -> list[tuple[str, bool, float]]:
    """ Return a list of the first objects reached in the given downstream direction starting from the given point.
    If a switch is met before reaching an object, the list will be composed of multiple objects for each path.
    It returns in addition the polarity (in the object is reached in the same direction as the start direction)
     and the distance to the object. """
    downstream = direction == Direction.CROISSANT
    list_objects = list()

    def inner_recurs_next_seg(inner_seg: str, inner_downstream: bool, path: list[str], path_len: float,
                              inner_x: float = None) -> None:
        nonlocal list_objects
        obj_on_seg = _is_object_defined_on_seg(inner_seg, inner_x, inner_downstream, inner_downstream == downstream,
                                               obj_type, obj_direction)
        if obj_on_seg is not False:
            obj_name, obj_x = obj_on_seg
            final_path_len = path_len - ((get_segment_length(inner_seg) - obj_x) if inner_downstream else obj_x)
            list_objects.append((obj_name, inner_downstream == downstream, final_path_len))
            return

        for next_seg in get_linked_segments(inner_seg, inner_downstream):
            if is_segment_depolarized(next_seg) and inner_seg in get_associated_depolarization(next_seg):
                next_inner_downstream = not inner_downstream
            else:
                next_inner_downstream = inner_downstream

            if next_seg in path:
                # We check if we have made a full turn and reach a segment that we have already run through
                # in the current path.
                continue
            inner_recurs_next_seg(next_seg, next_inner_downstream, path + [next_seg],
                                  round(path_len + get_segment_length(next_seg), 3))

    start_path_len = (get_segment_length(seg) - x) if downstream else x
    inner_recurs_next_seg(seg, downstream, [seg], start_path_len, x)
    return list_objects


def _is_object_defined_on_seg(seg: str, x: Optional[float], downstream: bool, polarity: bool,
                              obj_type: str, obj_direction: str = None) -> Union[bool, tuple[str, float]]:
    """ Return the first object on the segment in the given downstream direction (or first object after the offset x
     if it is specified),
     return False if there is no object on the segment (or no object after the offset x if it is specified).
    Check also that the object matches the object direction if it is specified."""
    obj_list = get_objects_list(obj_type)
    list_objects = list()
    for obj_name in obj_list:
        obj_position = get_object_position(obj_type, obj_name)
        if isinstance(obj_position, tuple):  # single-point object
            obj_seg = obj_position[0]
            obj_x = obj_position[1]
            if obj_direction is not None and len(obj_position) > 2:
                if (obj_position[2] != obj_direction) == polarity:  # if the direction is not matching
                    # we take into account if we pass a depolarization point on the path
                    continue
            if seg == obj_seg:
                if downstream:
                    if x is None or x <= obj_x:
                        list_objects.append((obj_name, obj_x))
                else:
                    if x is None or x >= obj_x:
                        list_objects.append((obj_name, obj_x))
        else:  # zone object
            for obj_limit in obj_position:
                lim_seg = obj_limit[0]
                lim_x = obj_limit[1]
                if seg == lim_seg:
                    if downstream:
                        if x is None or x <= lim_x:
                            list_objects.append((obj_name, lim_x))
                    else:
                        if x is None or x >= lim_x:
                            list_objects.append((obj_name, lim_x))

    if not list_objects:
        return False
    # Return closest object
    list_objects.sort(key=lambda a: a[1])  # sort according to offset value
    if downstream:
        return list_objects[0]  # return the object closest from the segment start
    else:
        return list_objects[-1]  # return the object closest from the segment end
