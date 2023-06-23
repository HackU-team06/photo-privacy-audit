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
        
        
        x1_l = letter.x
        x2_l = x1_l + letter.w
        y1_l = letter.y
        y2_l = y1_l + letter.h

        x1_o = object.x
        x2_o = x1_l + object.w
        y1_o = object.y
        y2_o = y1_l + object.h


        x1_larger  = max(x1_o,x1_l)
        x2_smaller = min(x2_o,x2_l)
        y1_larger  = min(y1_o,y1_l)
        y2_smaller = min(y2_o,y2_l)

        area_letter = letter.w * letter.h
        area_cover = (x2_smaller-x1_larger)*(y2_smaller-y1_larger)

        #被っているか判定
        if(x2_smaller-x1_larger<0 or y2_smaller-y1_larger<0):
            return False

        
        if(area_cover >= area_letter*threshold):
            return True


        

    #　それぞれのターゲットに該当する座標を保持する辞書を作成
    Coordinate_dict={}
    for name in target_names:
        Coordinate[name]=[]

    #辞書にデータを格納
    for res in result_list:
        if res.name in target_names:
            Coordinate[res.name].append(res)

    for res in resut_list:
        if(res.name != "letter"):
            continue
        
        for k in Coordinate_dict.keys():
            for v in Coordinate_dict[k]:
                if(object_contains_letter(v,res,threshold)):
                    res.rate += 1.0
                    v.rate += 1.0
        

    

        


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
