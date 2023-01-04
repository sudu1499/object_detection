import json
from sklearn.preprocessing import OneHotEncoder
import numpy as np

instance_train=json.load(open("instances_train2014.json",'r'))

annotations=instance_train['annotations']
categories=instance_train['categories']
images=instance_train['images']

req_cat=['car','bus','cat']
req_cat_ids={}
for i in categories:
    if i['name'] in req_cat:
        req_cat_ids[i['id']]=i['name']
ids=np.array(list(req_cat_ids.keys()))
ids=ids.reshape((-1,1))
ohe=OneHotEncoder()
ohe.fit(ids)

img_id_file_name={}
for i in images:
    img_id_file_name[i['id']]=i['file_name']

img_id_cat={}
for id in req_cat_ids:
    count=0
    for i in annotations:
        if i['category_id']== id:

            if img_id_file_name[i['image_id']] not in img_id_cat:
                class_ohe=ohe.transform([[i['category_id']]]).toarray()[0]
                class_ohe=class_ohe.tolist()
                img_id_cat[img_id_file_name[i['image_id']]]={'bbox':[[1]+i['bbox']+class_ohe]}
            elif len(img_id_cat[img_id_file_name[i['image_id']]]['bbox'])<5:
                class_ohe=ohe.transform([[i['category_id']]]).toarray()[0]
                class_ohe=class_ohe.tolist()
                img_id_cat[img_id_file_name[i['image_id']]]['bbox'].append([1]+i['bbox']+class_ohe)
            
final_data={}
for i,j in enumerate(img_id_cat):

    if i<600:
        final_data[j]=img_id_cat[j]
    else:
        break


for i in final_data:
    # print(i,final_data[i])
    # break
    if len(final_data[i]['bbox'])<5:
        diff=5-len(final_data[i]['bbox'])
        z=np.zeros((1,8)).tolist()
        print("yes",diff)
        for cnt in range(diff):
            final_data[i]['bbox']=final_data[i]['bbox']+z


json.dump(final_data,open("final_data.json","w"))
