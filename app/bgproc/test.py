# GCVA_YOLOのmain処理みたいな単体テスト等はココで実行する
from .import YoloAnalyze
from .import GcvaAnalyze
from models import AnalyzeResult, AnalyzeResultList

#from . import post_processing
from . import post_processing2 as post_processing

def proc_test() -> list[AnalyzeResult]:
    # 身元証明書のjson path
    JSON_PATH = "/app/bgproc/content/google_cloud_account_service.json"
    # The name of the image file to annotate
    IMG_PATH = "/app/bgproc/content/IMG_7695.jpg"
    ORIGINAL_MODEL = "yolov8n.pt"
    CUSTOM_MODEL = "/app/bgproc/content/train_model/using_model.pt"

    original_yolo = YoloAnalyze(ORIGINAL_MODEL)
    gcva = GcvaAnalyze(JSON_PATH)
    custom_yolo = YoloAnalyze(CUSTOM_MODEL)

    output = [
        *original_yolo.run(IMG_PATH),
        *custom_yolo.run(IMG_PATH),
        *gcva.run(IMG_PATH),
    ]
    print(output)

    # ===========post processing===========
    # parameters
    list_danger = [{0, 1, 2, 3, 7, 9, 10, 11, 12, 13, 16},
                   {4, 5, 6, 8, 14, 15, 16, 17, 18}
                   ]
    param1 = 3
    param2 = 3
    param = 0.8

    denger_map = {
        "bicycle": 1.0,
        "car": 1.0,
        "motorcycle": 1.0,
        "airplane": 2.0,
        "bus": 2.0,
        "train": 2.0,
        "truck": 1.0,
        "boat": 2.0,
        "traffic light": 1.0,
        "fire hydrant": 1.0,
        "stop sign": 1.0,
        "parking meter": 1.0,
        "clock": 1.0,
        "letter": 2.0,
        "manhole" : 2.0,
        "sun glass" : 2.0,
        "blue sign" : 2.0,
        "utility pole" : 2.0,
    }

    output = post_processing.evaluate_danger(output, denger_map)
    output = post_processing.except_low_rate(output, 0.5)

    # detect_duplicate と find_letter_in_BandU を動くようにしたい
    output = post_processing.merge_utility_poles(output, 0.4)
    output = post_processing.find_letter_in_object(output, 0.8, ['blue sign', 'utility pole'])

    return output


def merge_utility_poles_test():
    result_list = [
        AnalyzeResult(
            bounding_box={"x": 0, "y": 0, "w": 20, "h": 10},
            name="utility pole",
            description="0",
        ),
        AnalyzeResult(
            bounding_box={"x": 5, "y": 0, "w": 10, "h": 10},
            name="utility pole",
            description="1",
        ),
        AnalyzeResult(
            bounding_box={"x": 20, "y": 100, "w": 50, "h": 10},
            name="utility pole",
            description="2",
        ),
        AnalyzeResult(
            bounding_box={"x": 30, "y": 0, "w": 50, "h": 10},
            name="utility pole",
            description="3",
        ),
        AnalyzeResult(
            bounding_box={"x": 40, "y": 0, "w": 10, "h": 10},
            name="utility pole",
            description="4",
        ),
        AnalyzeResult(
            bounding_box={"x": 50, "y": 0, "w": 10, "h": 10},
            name="utility pole",
            description="5",
        ),
        AnalyzeResult(
            bounding_box={"x": 60, "y": 0, "w": 20, "h": 10},
            name="utility pole",
            description="6",
        ),
        AnalyzeResult(
            bounding_box={"x": 70, "y": 0, "w": 20, "h": 10},
            name="utility pole",
            description="7",
        ),
    ]
    new_result_list = post_processing.merge_utility_poles(result_list, 0.4)
    print(len(result_list), len(new_result_list))




if __name__ == "__main__":
    proc_test()
    #merge_utility_poles_test()
