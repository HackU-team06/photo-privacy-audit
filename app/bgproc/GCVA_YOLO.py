import io
import os
from ultralytics import YOLO
from google.cloud import vision
from google.oauth2 import service_account

def main():
    # 身元証明書のjson path
    JSON_PATH ='/app/bgproc/content/google_cloud_account_service.json'
    # The name of the image file to annotate
    IMG_PATH = '/app/bgproc/content/IMG_6407.jpg'
    ORIGINAL_MODEL = 'yolov8n.pt'
    CUSTOM_MODEL = '/app/bgproc/content/train_model/using_model.pt'
    
    oriyolo_result = useYOLO(ORIGINAL_MODEL,IMG_PATH)#既存モデルyolo検出
    gcva_result = useGCVA(JSON_PATH,IMG_PATH)#GCVAによる文字検出
    custom_result = useYOLO(CUSTOM_MODEL,IMG_PATH)#新規モデルyolo検出
    custom_result = detect_duplicate(custom_result,3,3) #重複検出の除去

    OUTPUT = [] #結果の結合
    OUTPUT.extend(oriyolo_result)
    OUTPUT.extend(gcva_result)
    for i in range(0,len(custom_result)):
        custom_result[i][0] = custom_result[i][0]+15
    OUTPUT.extend(custom_result)
    print(OUTPUT)# <==最終出力



def useYOLO(MODEL_PATH,IMG_PATH):
    # モデルの関数作成(YOLO)
    model = YOLO(MODEL_PATH)
    #YOLO-customから座標データを抽出(YOLO)
    results = model(IMG_PATH,conf=0.25)
    result = results[0]
    # 後のオブジェクト名出力などのため
    names = results[0].names
    classes = results[0].boxes.cls
    boxes = results[0].boxes
    annotatedFrame = results[0].plot()
    # 検出したオブジェクトのバウンディングボックス座標とオブジェクト名を取得し、ターミナルに出力
    output = []
    for box, cls in zip(boxes, classes):
        name = names[int(cls)]
        x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
        output.append([int(cls),x1,y1,x2,y2])#配列に保存
    return(output)


def useGCVA(JSON_PATH,IMG_PATH):
    # 身元証明書のjson読み込み(GCVA)
    credentials = service_account.Credentials.from_service_account_file(JSON_PATH)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # Loads the image into memory(GCVA)
    with io.open(IMG_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file(GCVA)
    response =  client.document_text_detection(
            image=image,
            image_context={'language_hints': ['ja']}
        )
    
    # レスポンスからテキストデータを抽出(GCVA)
    #output_text = ''
    #for page in response.full_text_annotation.pages:
    #    for block in page.blocks:
    #        for paragraph in block.paragraphs:
    #            for word in paragraph.words:
    #                output_text += ''.join([
    #                    symbol.text for symbol in word.symbols
    #                ])
    #            output_text += '\n'
    #print(output_text)

    # レスポンスからテキストの位置座標を抽出(GCVA)
    output=[]
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    vertices = [(vertex.x, vertex.y) for vertex in word.bounding_box.vertices]
                    x1=abs(round((vertices[0][0]+vertices[3][0])/2))
                    y1=abs(round((vertices[0][1]+vertices[1][1])/2))
                    x2=abs(round((vertices[1][0]+vertices[2][0])/2))
                    y2=abs(round((vertices[2][1]+vertices[3][1])/2))
                    #画像として表示
                    #img = cv2.rectangle(img,vertices[0],vertices[2],(0, 255, 0),thickness=8)
                    output.append([14,x1,y1,x2-x1,y2-y1])
    return(output)    

    #param1,param２は試しながら調整する必要あり
def detect_duplicate(output_list,param1,param2):
    cls_utility_pole=2
    Coordinate_utilitypole=[]   
    for i in output_list:
        if(i[0] == cls_utility_pole+15):
            Coordinate_utilitypole.append(i)

    while True:
        cou=0
        Coor_remove=[]
        Coor_add=[]

        for coorA in Coordinate_utilitypole:
            for coorB in Coordinate_utilitypole:
                if(coorA == coorB):
                    continue

                flag,coor_remove=check1(coorA,coorB,cls_utility_pole,param1,param2)
                if(flag):
                    Coor_remove.add(coor_remove)
                    cou+=1
                
                flag,coor_add=check2(coorA,coorB,param1,param2)
                if(flag):
                    Coor_remove.add(coorA)
                    Coor_remove.add(coorB)
                    Coor_add.add(coor_add)
                    cou+=1

        for coor_remove in Coor_remove:
            Coordinate_utilitypole.remove(coor_remove)
            output_list.remove(coor_remove)

        for coor_add in Coor_add:
            Coordinate_utilitypole.append(coor_add)
            output_list.append(coor_add)
        if(cou == 0):
            break

    return output_list

#大は小を兼ねるパターン(片方を削除)
def check1(coorA,coorB,param1,param2):
    x1_A = coorA[1]
    y1_A = coorA[2]
    x2_A = coorA[3]
    y2_A = coorA[4]

    x1_B = coorB[1]
    y1_B = coorB[2]
    x2_B = coorB[3]
    y2_B = coorB[4]

    #削除する座標を選択
    if(abs(y1_A-y2_A) < abs(y1_B-y2_B)):
        coor_remove = coorA
    else:
        coor_remove = coorB


    width_ave = (abs(x1_A-x2_A)+abs(x1_B-x2_B))/2

    height_larger = max(abs(y1_A-y2_A),abs(y1_B-y2_B))

    height_notdup = abs(y1_A-y1_B) + abs(y2_A-y2_B)


    
    if(abs(x1_A-x1_B) > param1 * width_ave or abs(x2_A-x2_B) > param1*width_ave):
        return False,coor_remove


    if(height_notdup/height_larger < param2):
        return True,coor_remove
    
    return False,coor_remove


#小さい二つの四角形をマージするパターン(両方削除して、新しい座標を追加)
def check2(coorA,coorB,cls_utility_pole,param1,param2):

    x1_A = coorA[1]
    y1_A = coorA[2]
    x2_A = coorA[3]
    y2_A = coorA[4]

    x1_B = coorB[1]
    y1_B = coorB[2]
    x2_B = coorB[3]
    y2_B = coorB[4]


    width_ave     = (abs(x1_A-x2_A)+abs(x1_B-x2_B))/2

    height_larger = max(abs(y1_A-y2_A),abs(y1_B-y2_B))

    height_notdup = abs(y1_A-y1_B) + abs(y2_A-y2_B)

    #追加する座標の作成
    coor_add =[cls_utility_pole]

    x1_small = min(x1_A,x1_B)
    y1_small = min(y1_A,y1_B)

    x2_big = max(x2_A,x2_B)
    y2_big = max(y2_A,y2_B)

    coor_add.append(x1_small,y1_small,x2_big,y2_big)


    
    if(abs(x1_A-x1_B) > param1 * width_ave or abs(x2_A-x2_B) > param1*width_ave):
        return False,coor_add
    
    if(height_notdup/height_larger > param2):
        return True,coor_add
    
    return False,coor_add



if __name__ == "__main__":
    main()
