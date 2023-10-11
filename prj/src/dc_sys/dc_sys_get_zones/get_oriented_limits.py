#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ..dc_sys_common_utils import *


__all__ = ["get_oriented_limits_of_zone"]


def get_oriented_limits_of_zone(obj_type_name: str, obj_name: str) -> Optional[list[tuple[str, float, bool]]]:
    oriented_zone_limits = get_obj_oriented_zone_limits(obj_type_name, obj_name)
    if oriented_zone_limits is not None:
        return convert_oriented_limits(oriented_zone_limits)

    zone_limits = get_obj_zone_limits(obj_type_name, obj_name)
    if zone_limits is None:
        return None

    oriented_zone_limits = list()
    for seg1, x1 in zone_limits:
        are_other_limits_downstream = [is_seg_downstream(seg1, seg2, x1, x2, downstream=True)
                                       for seg2, x2 in zone_limits if (seg2, x2) != (seg1, x1)]
        are_other_limits_upstream = [is_seg_downstream(seg1, seg2, x1, x2, downstream=False)
                                     for seg2, x2 in zone_limits if (seg2, x2) != (seg1, x1)]
        if any(are_other_limits_downstream) and not any(are_other_limits_upstream):
            direction = True
        elif any(are_other_limits_upstream) and not any(are_other_limits_downstream):
            direction = False
        elif any(are_other_limits_upstream) and any(are_other_limits_downstream):
            # TODO pas propre, faire plutôt une passe sur toutes les limites, celles qui sont triviales les prendre,
            #      et pour les autres faudrait regarder dans quelle direction tu y as accédé
            direction = get_limit_direction_with_distances(seg1, x1, zone_limits, are_other_limits_downstream,
                                                           are_other_limits_upstream)
        else:  # not any upstream and not any downstream
            print_error(f"Unable to find direction for limit {(seg1, x1)} of {obj_type_name} {obj_name}.")
            direction = None
        oriented_zone_limits.append((seg1, x1, direction))
    return oriented_zone_limits


def convert_oriented_limits(oriented_zone_limits: list[tuple[str, float, str]]) -> list[tuple[str, float, bool]]:
    zone_limits = [(seg, x, (direction == Direction.CROISSANT)) for seg, x, direction in oriented_zone_limits]
    return zone_limits


def get_limit_direction_with_distances(seg1: str, x1: float, zone_limits: list[tuple[str, float]],
                                       are_other_limits_downstream: list[bool],
                                       are_other_limits_upstream: list[bool]) -> bool:
    other_limits = [limit for limit in zone_limits if limit != (seg1, x1)]
    dist_downstream = [(get_dist_downstream(seg1, x1, seg2, x2, downstream=True) if are_other_limits_downstream[i]
                        else None) for i, (seg2, x2) in enumerate(other_limits)]
    dist_upstream = [(get_dist_downstream(seg1, x1, seg2, x2, downstream=False) if are_other_limits_upstream[i]
                      else None) for i, (seg2, x2) in enumerate(other_limits)]
    min_dist_downstream = min(d for d in dist_downstream if d is not None)
    min_dist_upstream = min(d for d in dist_upstream if d is not None)
    return min_dist_downstream <= min_dist_upstream
