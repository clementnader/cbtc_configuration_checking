#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...dc_sys import *
from ...dc_sys_sheet_utils.consist_osp_utils import get_max_train_len_at_plt_osp
from ...dc_sys_draw_path.dc_sys_path_and_distances import get_dist_downstream


__all__ = ["get_closest_vsp_in_rear"]


def get_closest_vsp_in_rear():
    plt_dict = load_sheet(DCSYS.Quai)
    civil_infrastructure_vsp_dict = _get_civil_infrastructure_vsp_dict()

    res_dict = dict()

    for plt_name, plt_info in plt_dict.items():
        for osp_name, osp_seg, osp_x, osp_type, osp_dir, osp_approach_dir in get_dc_sys_zip_values(
                plt_info, DCSYS.Quai.PointDArret.Name, DCSYS.Quai.PointDArret.Seg, DCSYS.Quai.PointDArret.X,
                DCSYS.Quai.PointDArret.TypePtArretQuai, DCSYS.Quai.PointDArret.SensAssocie,
                DCSYS.Quai.PointDArret.SensApproche):
            rear_pos_list = _get_train_rear_position(osp_name, osp_seg, osp_x, osp_type, osp_dir, osp_approach_dir)
            for direction, (rear_pos_seg, rear_pos_x) in rear_pos_list:
                vsp_in_rear = _get_closest_civil_infrastructure_vsp_upstream(rear_pos_seg, rear_pos_x, direction,
                                                                             civil_infrastructure_vsp_dict)
                if vsp_in_rear is None:
                    print_log(f"No VSP in rear for {osp_name} of {plt_name} in direction {direction}.")
                    continue
                vsp_seg = civil_infrastructure_vsp_dict[vsp_in_rear]["vsp_seg"]
                vsp_x = civil_infrastructure_vsp_dict[vsp_in_rear]["vsp_x"]
                downstream = False if osp_dir == Direction.CROISSANT else True
                dist = get_dist_downstream(rear_pos_seg, rear_pos_x, vsp_seg, vsp_x, downstream)
                if dist is None:
                    print_log(f"Not able to compute the distance for VSP in rear for {osp_name} of {plt_name} "
                              f"in direction {direction} with VSP of signal {vsp_in_rear}.")
                    continue
                res_dict[f"{osp_name}__{direction}"] = {"plt_name": plt_name, "osp_name": osp_name,
                                                        "direction": direction, "vsp_in_rear_sig": vsp_in_rear,
                                                        "dist": dist}
    res_dict = {key_name: res_dict[key_name] for key_name in sorted(res_dict.keys(), key=lambda a: res_dict[a]["dist"])}

    closest = res_dict[list(res_dict.keys())[0]]
    print(f"The closest VSP in rear is for {Color.blue}OSP {closest['osp_name']} in Platform {closest['plt_name']}"
          f"{Color.reset} in direction {Color.green}{closest['direction']}{Color.reset}.\n"
          f"The VSP is the one of signal {closest['vsp_in_rear_sig']}.\n"
          f"The distance between the rear of the train stationed at this OSP and the VSP in rear is {closest['dist']}.")
    return res_dict


def _get_train_rear_position(osp_name: str, osp_seg: str, osp_x: float, osp_type: str,
                             osp_dir: str, osp_approach_dir: str) -> Optional[list[tuple[str, tuple[str, float]]]]:

    max_train_length_at_osp = get_max_train_len_at_plt_osp(osp_name)

    if osp_type == StoppingPointType.AVANT:
        train_front = (osp_seg, osp_x)
        if osp_dir == Direction.CROISSANT:
            train_rear = get_correct_seg_offset(osp_seg, osp_x - max_train_length_at_osp)
        else:
            train_rear = get_correct_seg_offset(osp_seg, osp_x + max_train_length_at_osp)
    elif osp_type == StoppingPointType.ARRIERE:
        train_rear = (osp_seg, osp_x)
        if osp_dir == Direction.CROISSANT:
            train_front = get_correct_seg_offset(osp_seg, osp_x + max_train_length_at_osp)
        else:
            train_front = get_correct_seg_offset(osp_seg, osp_x - max_train_length_at_osp)
    elif osp_type == StoppingPointType.CENTRE:
        if osp_dir == Direction.CROISSANT:
            train_front = get_correct_seg_offset(osp_seg, osp_x + max_train_length_at_osp/2)
            train_rear = get_correct_seg_offset(osp_seg, osp_x - max_train_length_at_osp/2)
        else:
            train_front = get_correct_seg_offset(osp_seg, osp_x - max_train_length_at_osp/2)
            train_rear = get_correct_seg_offset(osp_seg, osp_x + max_train_length_at_osp/2)
    else:
        return None

    if osp_approach_dir == StoppingPointApproachType.DOUBLE_SENS:
        return [(osp_dir, train_rear), (get_reverse_direction(osp_dir), train_front)]

    return [(osp_dir, train_rear)]


def _get_closest_civil_infrastructure_vsp_upstream(seg: str, x: float, direction: str,
                                                   civil_infrastructure_vsp_dict: dict[str, dict[str, Any]]):
    aligned_civil_infrastructure_vsp_dict = {sig_name: vsp_info for sig_name, vsp_info
                                             in civil_infrastructure_vsp_dict.items()
                                             if vsp_info["vsp_direction"] == get_reverse_direction(direction)}

    vsp_in_rear = _vsp_upstream_on_seg(seg, direction, aligned_civil_infrastructure_vsp_dict, ref_x=x)

    downstream = False if direction == Direction.CROISSANT else True
    while vsp_in_rear is None:
        next_segs = get_linked_segments(seg, downstream)
        if not next_segs or len(next_segs) == 2:
            break
        seg = next_segs[0]
        vsp_in_rear = _vsp_upstream_on_seg(seg, direction, aligned_civil_infrastructure_vsp_dict)
    return vsp_in_rear


def _vsp_upstream_on_seg(ref_seg, ref_direction: str, vsp_dict: dict[str, dict[str, Any]], ref_x: float = None
                         ) -> Optional[str]:
    vsps_on_seg = list()
    for sig_name, vsp_info in vsp_dict.items():
        test_seg, test_x = vsp_info["vsp_seg"], vsp_info["vsp_x"]
        if test_seg == ref_seg:
            if (ref_x is None or (ref_direction == Direction.CROISSANT and test_x <= ref_x)
                    or (ref_direction == Direction.DECROISSANT and test_x >= ref_x)):
                vsps_on_seg.append((sig_name, test_x))
    if not vsps_on_seg:
        return None
    return sorted(vsps_on_seg, key=lambda x: x[1], reverse=(ref_direction == Direction.CROISSANT))[0][0]
# If we are in "CROISSANT", the closest sig upstream will be the one with the largest offset, the reverse otherwise.


def _get_civil_infrastructure_vsp_dict() -> dict[str, dict[str, Any]]:
    sig_dict = load_sheet(DCSYS.Sig)
    civil_infrastructure_vsp = dict()
    for sig_name, sig_info in sig_dict.items():
        sig_seg, sig_x, sig_type, sig_direction, vsp_type, dist_vsp = get_dc_sys_values(
            sig_info, DCSYS.Sig.Seg, DCSYS.Sig.X, DCSYS.Sig.Type, DCSYS.Sig.Sens, DCSYS.Sig.VspType,
            DCSYS.Sig.DistPap)
        if sig_type != SignalType.MANOEUVRE or vsp_type != VSPType.CIVIL_INFRASTRUCTURE:
            continue

        if sig_direction == Direction.CROISSANT:
            vsp_seg, vsp_x = get_correct_seg_offset(sig_seg, sig_x + dist_vsp)
        else:
            vsp_seg, vsp_x = get_correct_seg_offset(sig_seg, sig_x - dist_vsp)
        civil_infrastructure_vsp[sig_name] = {"vsp_seg": vsp_seg, "vsp_x": vsp_x, "vsp_direction": sig_direction}
    return civil_infrastructure_vsp
