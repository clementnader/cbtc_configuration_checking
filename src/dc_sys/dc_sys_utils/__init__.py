#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .cbtc_territory_utils import get_segs_within_cbtc_ter, is_point_in_cbtc_ter, get_limits_cbtc_ter, \
    is_seg_in_cbtc_ter_limits, print_in_cbtc
from .segments_utils import *
from .dist_utils import get_dist, get_dist_downstream, get_list_of_paths
from .block_utils import get_blocks_in_cbtc_ter, get_len_block
from .switch_utils import get_sws_in_cbtc_ter, is_sw_point_seg_upstream, give_sw_pos, give_sw_kp_pos
from .virtual_block_utils import *
from .platforms_utils import get_plts_in_cbtc_ter
from .signals_utils import get_sigs_in_cbtc_ter, get_sigs_outside_cbtc_ter
from .slope_utils import get_slopes_in_cbtc_ter, get_min_and_max_slopes_at_point, get_min_and_max_slopes_on_virtual_seg
from .links_utils import get_all_segs_linked, get_all_linked_segs, get_all_upstream_segs, get_all_downstream_segs, \
    is_seg_downstream
from .tag_utils import get_tags_in_cbtc_ter, get_tag_gr_in_cbtc_ter
