import numpy as np
def calculate_points(b):
    x,y,w,h=b[0],b[1],b[2],b[3]
    return ((x-w/2,y+h/2),(x+w/2,y+h/2),(x+w/2,y-h/2),(x-w/2,y-h/2))
def compute_iou(b1,b2):

    b11,b12,b13,b14=calculate_points(b1)
    b21,b22,b23,b24=calculate_points(b2)

    if b11[1]>b21[1]:
        ext_y1=b11[1]
    elif b11[1]<=b21[1]:
        ext_y1=b21[1]

    if b14[1]>b24[1]:
        ext_y2=b24[1]
    else:
        ext_y2=b14[1]

    if b11[0]>b21[0]:
        ext_x1=b21[0]
    else:
        ext_x1=b11[0]

    if b12[0]>b22[0]:
        ext_x2=b12[0]
    else:
        ext_x2=b22[0]
    
    # print("Extrem y 2",ext_y2)
    # print("Extrem y 1",ext_y1)
    # print("Extrem x 2",ext_x2)
    # print("Extrem x 1",ext_x1)
    if ((b1[3]+b2[3])>(ext_y2-ext_y1) and ((b1[2]+b2[2]>(ext_x2-ext_x1)))):
        int_y=b1[3]+b2[3]-(ext_y1-ext_y2)
        int_x=b1[2]+b2[2]-(ext_x2-ext_x1)

        intersection=int_y*int_x
        union_area=b1[2]*b1[3] + b2[2]*b2[3]-intersection
        # print("IOU = ",intersection/union_area)
        return intersection/union_area
    else:
        # print("IOU=",0)
        return 0


def Non_maximum_supression(boxes,iou_threshold,prob_threshold):

    filtered_class=[]
    for i in boxes:
        if i[0]>prob_threshold:
            filtered_class.append(i)

    sorted_class=sorted(filtered_class,reverse=True,key=lambda x: x[0])
    final_class=[]
    print("sorted class",sorted_class)
    while len(sorted_class)>0:
        current=sorted_class.pop(0)

        for index,i in enumerate(sorted_class):
            print(i[1:5],current[1:5])
            iou=compute_iou(i[1:5],current[1:5])
            print(iou)
            if iou>iou_threshold:
                sorted_class.pop(index)
        final_class.append(current)
        
    return final_class

# boxs=[
#     [.9,1,2.5,2,3,0,0,0],
#     [.7,.5,2.5,2,3,0,0,0],
#     [.6,1.2,2.5,2,3,0,0,0],
#     [.9,1,6.5,2,3,0,0,0],
#     [.7,.5,6.5,2,3,0,0,0],
#     [.6,1.2,6.5,2,3,0,0,0]
# ]    
# Non_maximum_supression(boxes=boxs,iou_threshold=.5,prob_threshold=.7)