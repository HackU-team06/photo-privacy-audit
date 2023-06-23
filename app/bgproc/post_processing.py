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


def result_to_xyxy(result_list: AnalyzeResult) -> tuple[int, int, int, int]:
    """AnalyzeResultをx1, y1, x2, y2のタプルに変換する"""
    return (
        result_list.bounding_box.x,
        result_list.bounding_box.y,
        result_list.bounding_box.x + result_list.bounding_box.w,
        result_list.bounding_box.y + result_list.bounding_box.h,
    )


def merge_utility_poles(result_list: list[AnalyzeResult], threshold: float):
    """
    x軸方向に近い電柱をマージする

    x軸方向に近いとは、x1, x2の差が幅の平均のcoef倍より小さいことを指す
    """

    def is_x_axis_close(
        pole_i: AnalyzeResult, pole_j: AnalyzeResult, threshold: float
    ) -> bool:
        """
        2つの電柱がx軸方向に近いかどうかを判定する

        x軸方向に近いとは、x1, x2の差が width_ave * threshold より小さいことを指す
        """
        
        x1_i, _, x2_i, _ = result_to_xyxy(pole_i)
        x1_j, _, x2_j, _ = result_to_xyxy(pole_j)
        w_i = pole_i.bounding_box.w
        w_j = pole_j.bounding_box.w

        v = (w_i + w_j) / 2 * threshold

        return max(abs(x1_i - x1_j), abs(x2_i - x2_j)) < v

    def merge(pole_i: AnalyzeResult, pole_j: AnalyzeResult) -> AnalyzeResult:
        """pole_iとpole_jをマージする"""

        x1_i, x2_i, y1_i, y2_i = result_to_xyxy(pole_i)
        x1_j, x2_j, y1_j, y2_j = result_to_xyxy(pole_j)

        x1 = min(x1_i, x1_j)
        x2 = max(x2_i, x2_j)
        y1 = min(y1_i, y1_j)
        y2 = max(y2_i, y2_j)

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
            if is_x_axis_close(pole_i, pole_j, threshold):
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



# thretholdは0.8ぐらいを想定
def find_letter_in_object(
    result_list: list[AnalyzeResult], threshold: float, target_names: Iterable[str]
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

        x1_l, x2_l, y1_l, y2_l = result_to_xyxy(letter)
        x1_o, x2_o, y1_o, y2_o = result_to_xyxy(object)

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
