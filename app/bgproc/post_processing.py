import itertools
from models import AnalyzeResult
from typing import Iterable
from collections import deque


def except_low_rate(result_list: list[AnalyzeResult], threshold: float):
    """rateがthreshold未満の要素を削除する"""
    return [res for res in result_list if res.rate >= threshold]


def evaluate_danger(result_list: list[AnalyzeResult], danger_map: dict[str, int]):
    """danger_mapに基づき、result_listの各要素のrateを変更する"""
    for res in result_list:
        res.rate = danger_map.get(res.name, 0)
    return result_list


def merge_utility_poles(result_list: list[AnalyzeResult], coef: float):
    """
    x軸方向に近い電柱をマージする

    x軸方向に近いとは、x1, x2の差が幅の平均のcoef倍より小さいことを指す
    """

    def is_x_axis_close(
        pole_i: AnalyzeResult, pole_j: AnalyzeResult, coef: float
    ) -> bool:
        """
        2つの電柱がx軸方向に近いかどうかを判定する

        x軸方向に近いとは、x1, x2の差がwidth_aveのthreshold倍より小さいことを指す
        """

        x1_i = pole_i.bounding_box.x
        w_i = pole_i.bounding_box.w
        x2_i = x1_i + w_i

        x1_j = pole_j.bounding_box.x
        w_j = pole_j.bounding_box.w
        x2_j = x1_j + w_j

        threshold = (w_i + w_j) / 2 * coef

        return abs(x1_i - x1_j) < threshold and abs(x2_i - x2_j) < threshold

    def merge(pole_i: AnalyzeResult, pole_j: AnalyzeResult) -> AnalyzeResult:
        x1 = min(pole_i.bounding_box.x, pole_j.bounding_box.x)
        x2 = max(
            pole_i.bounding_box.x + pole_i.bounding_box.w,
            pole_j.bounding_box.x + pole_j.bounding_box.w,
        )
        y1 = min(pole_i.bounding_box.y, pole_j.bounding_box.y)
        y2 = max(
            pole_i.bounding_box.y + pole_i.bounding_box.h,
            pole_j.bounding_box.y + pole_j.bounding_box.h,
        )
        pole_i.bounding_box.x = x1
        pole_i.bounding_box.y = y1
        pole_i.bounding_box.w = x2 - x1
        pole_i.bounding_box.h = y2 - y1
        return pole_i

    pole_results = [res for res in result_list if res.name == "utility pole"]
    other_results = [res for res in result_list if res.name != "utility pole"]

    # confidenceが高い順のキュー
    pole_results = deque(
        sorted(pole_results, key=lambda res: res.confidence, reverse=True)
    )
    merged_pole_results = []

    while pole_results:
        # confidenceが最大のものを取り出す
        pole_i = pole_results.popleft()

        # 次のループで使うキュー
        new_pole_results = deque()
        update_flag = False

        for pole_j in pole_results:
            if is_x_axis_close(pole_i, pole_j, coef):
                # x軸方向に近い場合はマージ
                pole_i = merge(pole_i, pole_j)
                update_flag = True
            else:
                new_pole_results.append(pole_j)

        if update_flag:
            # 更新があった場合は先頭に追加
            new_pole_results.appendleft(pole_i)
        else:
            # 更新がなかった場合はマージ済みリストに追加
            merged_pole_results.append(pole_i)

        pole_results = new_pole_results

    return other_results + merged_pole_results


# find_letter_jn_BandU


# thretholdは0.8ぐらいを想定
def find_letter_in_object(
    result_list: list[AnalyzeResult], threshold: float, target_names: list[str]
) -> list[AnalyzeResult]:
    """
    文字と物体の重なりを判定し、重なっている場合はrateを変更する

    Args:
        result_list (list[AnalyzeResult]): 物体検出の結果

        threshold (float): 重なりの閾値

        target_names (list[str]): 重なりを判定する物体の名前
    """

    def object_contains_letter(
        object: AnalyzeResult, letter: AnalyzeResult, threshold: float
    ) -> bool:
        """objectがletterを含んでいるかどうかを判定する"""

        x1_l = letter.bounding_box.x
        x2_l = x1_l + letter.bounding_box.w
        y1_l = letter.bounding_box.y
        y2_l = y1_l + letter.bounding_box.h

        x1_o = object.bounding_box.x
        x2_o = x1_o + object.bounding_box.w
        y1_o = object.bounding_box.y
        y2_o = y1_o + object.bounding_box.h

        x1_larger = max(x1_o, x1_l)
        x2_smaller = min(x2_o, x2_l)
        y1_larger = min(y1_o, y1_l)
        y2_smaller = min(y2_o, y2_l)

        area_letter = letter.bounding_box.w * letter.bounding_box.h
        area_cover = (x2_smaller - x1_larger) * (y2_smaller - y1_larger)

        return area_cover >= area_letter * threshold
    

    target_names = set(target_names)
    target_list = [res for res in result_list if res.name in target_names]
    letter_list = [res for res in result_list if res.name == "letter"]

    for target in target_list:
        for letter in letter_list:
            if object_contains_letter(target, letter, threshold):
                target.rate += 1.0
                break

    return result_list
