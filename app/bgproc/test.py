# GCVA_YOLOのmain処理みたいな単体テスト等はココで実行する
from .import YoloAnalyze
from .import GcvaAnalyze
from models import AnalyzeResult,AnalyzeResultList

from .import post_processing


def main() -> list[AnalyzeResult]:
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
        *original_yolo.run(IMG_PATH,0),
        *gcva.run(IMG_PATH),
        *custom_yolo.run(IMG_PATH,15),
    ]
    print(output)


    #===========post processing===========
    #parameters
    list_danger=[{0,1,2,3,7,9,10,11,12,13,16},
            {4,5,6,8,14,15,16,17,18}
            ]
    param1=3
    param2=3
    param=0.8
    cls_utilitypole=18
    cls_bluesign=17
    cls_letter=14
    list_labels=["person","bicycle","car","motorcycle","airplane","bus","train","trunk","boat","traffic light","fire hydrant","stop sign","parking meter","clock","letter","manhole","sun glass","blue sign","utility pole"]

    output= post_processing.except_person(output)
    output= post_processing.evaluate_danger(output,list_danger)
    output= post_processing.detect_duplicate(output,param1,param2)
    output= post_processing.find_letter_in_BandU(output,param,cls_utilitypole,cls_bluesign,cls_letter)
    output= post_processing.from_labes_to_objects(output,list_labels)
    output = post_processing.coord2size(output)
    print(output)

    #辞書型にするなら
    output = post_processing.list2dictionaly(output)
    output=AnalyzeResultList.parse_obj(output)
    print(output)
    


    return output


if __name__ == "__main__":
    main()
