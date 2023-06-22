
def except_person(output_list):
    Coor_human=[]
    for output in output_list:
        if(output[0] == 0):
            Coor_human.append(output)

    for coor_human in Coor_human:
        output_list.remove(coor_human)
    
    return output_list

def evaluate_danger(output_list,list_danger):

    for output in output_list:
        for i in range(len(list_danger)):
            if(output[0] in list_danger[i]):
                output.append(i)
                break

    return output_list

def detect_duplicate(output_list,param1,param2):
    cls_utility_pole=18
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

##find_letter_jn_BandU
#下の　find_letter_in_BandUを使ってね


#文字と被っているかチェック
def check(coorL,coorB,param):
    x1_L = coorL[1]
    y1_L = coorL[2]
    x2_L = coorL[3]
    y2_L = coorL[4]

    x1_B = coorB[1]
    y1_B = coorB[2]
    x2_B = coorB[3]
    y2_B = coorB[4]

    #完全に文字が中に埋まってる場合
    if(x1_B < x1_L and y1_B < y1_L and x2_B > y2_L and y2_B):
        return True
    
    width_L  = abs(x2_L-x1_L)
    height_L = abs(y2_L-y1_L)
    
    width_B  = abs(x2_B-x1_B)
    height_B = abs(y2_B-y1_B)

    x1_larger  = max(x1_B,x1_L)
    x2_smaller = min(x2_B,x2_L)
    y1_larger  = min(y1_B,y1_L)
    y2_smaller = min(y2_B,y2_L)

    if(x2_smaller-x1_larger<0 or y2_smaller-y1_larger<0):
        return False

    area_cover = (x2_smaller-x1_larger)*(y2_smaller-y1_larger)
    area_letter = abs(x1_L-x2_L)*abs(y1_L-y2_L)

    if(area_cover/area_letter>param):
        return True
    
    return False

    


#paramは0.8ぐらいを想定
def find_letter_in_BandU(output_list,param,cls_utility_pole,cls_bule_sign,cls_letter):
    
    Coordinate_utilitypole=[] 
    Coordinate_bulesign=[] 
    Coordinate_letter=[] 
    for output in output_list:
        if(output[0] == cls_utility_pole):
            Coordinate_utilitypole.append(output)
        if(output[0] == cls_bule_sign):
            Coordinate_bulesign.append(output)
        if(output[0] == cls_letter):
            Coordinate_letter.append(output)


    for coorL in Coordinate_letter:
        for coorB in Coordinate_bulesign:
            if(check(coorL,coorB,param)):

                for output in output_list:
                    if(output == coorL):
                        output[5] = 2
                    if(output == coorB):
                        output[5] = 2
    
    for coorL in Coordinate_letter:
        for coorU in Coordinate_utilitypole:
            if(check(coorL,coorU,param)):

                for output in output_list:
                    if(output == coorL):
                        output[5] = 2
                    if(output == coorU):
                        output[5] = 2

    return output_list

    #from_labels_to_objects
def from_labes_to_objects(output_list,list_labels):
    for i in range(len(output_list)):
        output_list[i][0] = list_labels[output_list[i][0]]
    return output_list

def coord2size(output_list):
    for i in range(len(output_list)):
        #x2->w
        output_list[i][3] = output_list[i][3]-output_list[i][1]
        #y2->h
        output_list[i][4] = output_list[i][4]-output_list[i][2]
    return output_list


def list2dictionaly(output_list):
  output_dic = []
  anaResult = ["bounding_box","name","description","rate"]
  BouBox = ["x","y","w","h"]
  for i in range(0,len(output_list)):
    output_boubox = dict(zip(BouBox, output_list[i][1:5]))
    output_anaResult = dict(zip(anaResult, [output_boubox,output_list[i][0],"sample description",output_list[i][5]]))
    output_dic.append(output_anaResult)
  return output_dic
