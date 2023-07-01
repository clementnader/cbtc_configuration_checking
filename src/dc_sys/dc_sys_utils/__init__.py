#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .block_utils import get_blocks_in_cbtc_ter, get_list_len_block, get_block_associated_to_sw, \
    find_upstream_n_downstream_limits, does_path_exist_within_block
from .cbtc_territory_utils import get_segs_within_cbtc_ter, is_point_in_cbtc_ter, get_limits_cbtc_ter, \
    is_seg_in_cbtc_ter_limits, print_in_cbtc
from .dist_utils import get_dist, get_dist_downstream, get_list_of_paths, get_min_dist_and_list_of_paths, \
    get_smallest_path, get_path_len
from .kp_utils import from_seg_offset_to_kp, from_kp_to_seg_offset
from .maz_utils import get_maz_in_cbtc_ter
from .overlap_utils import get_overlap
from .path_utils import get_all_accessible_segs, is_seg_downstream, are_segs_linked, get_all_paths_from
from .platforms_utils import get_plts_in_cbtc_ter
from .route_utils import get_routes
from .segments_utils import *
from .signals_utils import get_sigs_in_cbtc_ter, get_sigs_outside_cbtc_ter
from .slope_utils import get_slopes_in_cbtc_ter, get_min_and_max_slopes_at_point, get_min_and_max_slopes_on_virtual_seg
from .switch_utils import get_sws_in_cbtc_ter, is_sw_point_seg_upstream, give_sw_pos, give_sw_kp_pos, \
    get_heel_position, get_switch_position_dict, get_point_seg
from .tag_utils import get_tags_in_cbtc_ter, get_tag_gr_in_cbtc_ter
from .track_utils import get_track_limits, get_track_in_cbtc_ter
from .virtual_block_utils import give_point_seg_vb, get_len_vb, get_segs_in_vb, is_seg_in_vb, get_vb_associated_to_sw
from .zsm_utils import get_zsm_in_cbtc_ter
