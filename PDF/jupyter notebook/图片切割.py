
from PIL import Image
import os
from tqdm import tqdm


def pic_cut(folder_path):
    pic_file_list = [os.path.join(folder_path, i) for i in os.listdir(folder_path)]

    for pic_path in tqdm(pic_file_list):
        img = Image.open(pic_path)
        img = img.crop((0, 139, img.size[0], 1733))  # [左] [上] [右(img.save[0])] [下(img.save(1))]
        img.save(pic_path)


if __name__ == "__main__":
    pic_cut(r'E:\裏\图\OneDrive - Office.Inc\多模态处理文件夹\贫穷的本质\《贫穷的本质：我们为什么摆脱不了贫穷》_image')
