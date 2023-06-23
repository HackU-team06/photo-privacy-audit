import itertools
from models import AnalyzeResult
from typing import Iterable


def except_low_rate(result_list: list[AnalyzeResult], threshold: float):
    """rateがthreshold未満の要素を削除する"""
    return [res for res in result_list if res.rate >= threshold]


def evaluate_danger(result_list: list[AnalyzeResult], danger_map: dict[str, int]):
    """danger_mapに基づき、result_listの各要素のrateを変更する"""
    for res in result_list:
        res.rate = danger_map.get(res.name, 0)
    return result_list


# find_letter_jn_BandU
# 下の　find_letter_in_BandUを使ってね


# 文字と被っているかチェック
def check(coorL, coorB, param):
    x1_L = coorL[1]
    y1_L = coorL[2]
    x2_L = coorL[3]
    y2_L = coorL[4]

    x1_B = coorB[1]
    y1_B = coorB[2]
    x2_B = coorB[3]
    y2_B = coorB[4]

    # 完全に文字が中に埋まってる場合
    if x1_B < x1_L and y1_B < y1_L and x2_B > y2_L and y2_B:
        return True

    width_L = abs(x2_L - x1_L)
    height_L = abs(y2_L - y1_L)

    width_B = abs(x2_B - x1_B)
    height_B = abs(y2_B - y1_B)

    x1_larger = max(x1_B, x1_L)
    x2_smaller = min(x2_B, x2_L)
    y1_larger = min(y1_B, y1_L)
    y2_smaller = min(y2_B, y2_L)

    if x2_smaller - x1_larger < 0 or y2_smaller - y1_larger < 0:
        return False

    area_cover = (x2_smaller - x1_larger) * (y2_smaller - y1_larger)
    area_letter = abs(x1_L - x2_L) * abs(y1_L - y2_L)

    if area_cover / area_letter > param:
        return True

    return False


# thretholdは0.8ぐらいを想定
def find_letter_in_BandU(
    result_list: list[AnalyzeResult], threthold: float, target_names: list[str]
) -> list[AnalyzeResult]:
    """
    文字と物体の重なりを判定し、重なっている場合はrateを変更する

    Args:
        result_list (list[AnalyzeResult]): 物体検出の結果
        threthold (float): 重なりの閾値
        target_names (list[str]): 重なりを判定する物体の名前
    """

    def object_contains_letter(object: AnalyzeResult, letter: AnalyzeResult, threthold: float) -> bool:
        """objectがletterを含んでいるかどうかを判定する"""

    coordinate_utilitypole = []
    Coordinate_bulesign = []
    Coordinate_letter = []
    for output in result_list:
        if output[0] == cls_utility_pole:
            coordinate_utilitypole.append(output)
        if output[0] == cls_bule_sign:
            Coordinate_bulesign.append(output)
        if output[0] == cls_letter:
            Coordinate_letter.append(output)

    for coorL in Coordinate_letter:
        for coorB in Coordinate_bulesign:
            if check(coorL, coorB, param):
                for output in result_list:
                    if output == coorL:
                        output[5] = 2
                    if output == coorB:
                        output[5] = 2

    for coorL in Coordinate_letter:
        for coorU in coordinate_utilitypole:
            if check(coorL, coorU, param):
                for output in result_list:
                    if output == coorL:
                        output[5] = 2
                    if output == coorU:
                        output[5] = 2

    return result_list

    # from_labels_to_objects


def from_labes_to_objects(result_list, list_labels):
    for i in range(len(result_list)):
        result_list[i][0] = list_labels[result_list[i][0]]
    return result_list
