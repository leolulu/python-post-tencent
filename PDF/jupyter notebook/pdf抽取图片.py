from pdf2image import convert_from_path
import os
from tqdm import tqdm


def pdf_extract(pdf_path):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(os.path.dirname(pdf_path), f'{pdf_name}_image')
    try:
        os.mkdir(output_folder)
    except:
        pass

    pdf_pages = convert_from_path(pdf_path=pdf_path, dpi=200, output_folder=r'E:\python\python-post-tencent\PDF\temp', thread_count=4)

    for i, page in enumerate(tqdm(pdf_pages)):
        page.save(os.path.join(output_folder, f'{pdf_name}_{i}.png'), 'png')


if __name__ == "__main__":
    pdf_extract(r"E:\裏\图\OneDrive - Office.Inc\多模态处理文件夹\贫穷的本质\《贫穷的本质：我们为什么摆脱不了贫穷》.pdf")
