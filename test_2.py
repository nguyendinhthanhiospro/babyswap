from fastapi import FastAPI, Request, Header
import threading
import tensorflow as tf
import time
import asyncio
import shutil
from PIL import Image
import shutil
import time
from datetime import datetime
import random
import numpy as np
from test_fun import gen_sk, gen_sk_ngam, gen_sk_swap, gen_sk_baby, gen_sk_noel
from test_csv import (
    get_random_data_noel,
    get_random_data,
    merge_image,
    save_to_mysql,
    get_random_data_skngam,
    save_to_mysql_skngam,
    insert_svg_logo,
    save_to_mysql_2_image,
    get_random_data_swap_baby,
    save_to_mysql_swap_baby,
    save_video_to_mysql_swap_imagevideo_wedding,
    save_to_mysql_anh_don,
    get_images_alone,
    get_list_categoris_alone,
    get_thiep_cuoi,
)
from server_fast import saved_album_wedding_swap
from func_vid import gen_video, gen_video_swap_imagevid_wedding
from login.func import send_mail_swap_done
from login.func import validate_token, generate_token
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, File, UploadFile
import uuid, os
from roop import core
import qrcode
import string
def gen_sk_swap_iudi(
    id_user: int,
    gioi_tinh:str,
    list_folder: str,
    link1: str
):
    print("hello")
    folder_time = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"

    folder_path_list_nam = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/NAM/{list_folder}"
    folder_path_list_nam_tam_thoi = "/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/tam_thoi/NAM"
    folder_path_list_nu = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/NU/{list_folder}"
    folder_path_list_nu_tam_thoi = "/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/tam_thoi/NU"

    # Kiểm tra xem các thư mục có tồn tại hay không
    if not os.path.exists(folder_path_list_nam):
        raise FileNotFoundError(f"The directory {folder_path_list_nam} does not exist.")
    if not os.path.exists(folder_path_list_nu):
        raise FileNotFoundError(f"The directory {folder_path_list_nu} does not exist.")

    # Lấy danh sách các ảnh trong folder_path_list_nam
    nam_images = [f for f in os.listdir(folder_path_list_nam) if os.path.isfile(os.path.join(folder_path_list_nam, f))]
    # Kiểm tra xem có đủ ảnh để chọn không
    if len(nam_images) < 5:
        raise ValueError("Not enough images in folder_path_list_nam to select 5 random images.")

    # Chọn ngẫu nhiên 5 ảnh
    selected_nam_images = random.sample(nam_images, 5)

    # Tạo thư mục tạm thời nếu chưa tồn tại
    os.makedirs(folder_path_list_nam_tam_thoi, exist_ok=True)

    # Di chuyển các ảnh được chọn vào folder_path_list_nam_tam_thoi
    for img in selected_nam_images:
        src_path = os.path.join(folder_path_list_nam, img)
        dest_path = os.path.join(folder_path_list_nam_tam_thoi, img)
        shutil.move(src_path, dest_path)

    # Hàm để thay đổi phần mở rộng của tên ảnh
    def swap_suffix(filename):
        if filename.endswith('_a.jpg'):
            return filename.replace('_a.jpg', '_b.jpg')
        elif filename.endswith('_b.jpg'):
            return filename.replace('_b.jpg', '_a.jpg')
        else:
            return filename

    # Tìm các ảnh có tên tương ứng trong folder_path_list_nu
    matching_nu_images = []
    for img in selected_nam_images:
        matching_img = swap_suffix(img)
        if os.path.exists(os.path.join(folder_path_list_nu, matching_img)):
            matching_nu_images.append(matching_img)

    # Tạo thư mục tạm thời nếu chưa tồn tại
    os.makedirs(folder_path_list_nu_tam_thoi, exist_ok=True)

    # Di chuyển các ảnh phù hợp vào folder_path_list_nu_tam_thoi
    for img in matching_nu_images:
        src_path = os.path.join(folder_path_list_nu, img)
        dest_path = os.path.join(folder_path_list_nu_tam_thoi, img)
        shutil.move(src_path, dest_path)

    print("Images have been successfully moved.")
    output_path_chuanbighep = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/out/{folder_time}/"
    )
    timkiem_path_chuanbighep = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/out/{folder_time}"
    )
    folder_export_wedding = (
        f"/var/www/build_futurelove/image/image_user/{id_user}/wedding/{folder_time}"
    )
    os.makedirs(output_path_chuanbighep, exist_ok=True)
    os.makedirs(folder_export_wedding, exist_ok=True)
    print(f"________KET QUA TRA VE____: {folder_path_list_nam_tam_thoi}")
    print(f"________thu MUC NAM_NU_TAO RA____: {output_path_chuanbighep}")
    print(f"________link_HEADer____: {link1}")
    if(gioi_tinh=="nam"):
        try:
            core.run(link1, folder_path_list_nam_tam_thoi, output_path_chuanbighep)
            # Di chuyển các ảnh từ folder_path_list_nam_tam_thoi vào output_path_chuanbighep
            for img in os.listdir(folder_path_list_nu_tam_thoi):
                src_path = os.path.join(folder_path_list_nu_tam_thoi, img)
                dest_path = os.path.join(output_path_chuanbighep, img)
                shutil.move(src_path, dest_path)
        except:
            return JSONResponse(content={"sukien_2_image": "error images 1 have not face"})
        
    else:
        try:
            core.run(link1, folder_path_list_nu_tam_thoi, output_path_chuanbighep)
            # Di chuyển các ảnh từ folder_path_list_nam_tam_thoi vào output_path_chuanbighep
            for img in os.listdir(folder_path_list_nam_tam_thoi):
                src_path = os.path.join(folder_path_list_nam_tam_thoi, img)
                dest_path = os.path.join(output_path_chuanbighep, img)
                shutil.move(src_path, dest_path)
        except:
            return JSONResponse(content={"sukien_2_image": "error images 2 have not face"})
    
    for filename in os.listdir(timkiem_path_chuanbighep):
        if filename.endswith("_a.jpg"):
            name_xoa_ky_tu = filename.rstrip("_a.jpg")
            print(str(filename))
            image1Pro = str(output_path_chuanbighep) + str(name_xoa_ky_tu) + "_a.jpg"
            image2Pro = str(output_path_chuanbighep) + str(name_xoa_ky_tu) + "_b.jpg"
            print(str(image1Pro))
            print(str(image2Pro))
            if os.path.isfile(image1Pro) == False:
                print("khong tim thay file: " + str(image1Pro))
                continue
            if os.path.isfile(image2Pro) == False:
                print("khong tim thay file: " + str(image2Pro))
                continue
            image2FileCombine = [
                Image.open(image1Pro),
                Image.open(image2Pro),
            ]
            widths, heights = zip(*(imaItem.size for imaItem in image2FileCombine))
            total_width = sum(widths)
            max_height = max(heights)
            new_im = Image.new("RGB", (total_width, max_height))
            x_offset = 0
            for im in image2FileCombine:
                new_im.paste(im, (x_offset, 0))
                x_offset += im.size[0]
                fileStr = os.path.join(
                    timkiem_path_chuanbighep,
                    f"AI_GEN_{name_xoa_ky_tu}.jpg",
                )
                print("___SON___" + fileStr)
                new_im.save(fileStr)
                folderLuu = folder_export_wedding + f"/{list_folder}"
                os.makedirs(folderLuu, exist_ok=True)
                dest = folderLuu + f"/AI_GEN_{name_xoa_ky_tu}.jpg"
                print("_______SONPRO_____" + dest)
                shutil.copyfile(fileStr, dest)
                print(
                    str(
                        os.path.join(
                            output_path_chuanbighep,
                            f"AI_GEN_{list_folder}_{name_xoa_ky_tu}.jpg",
                        )
                    )
                )
            os.remove(image1Pro)
            os.remove(image2Pro)
            os.remove(fileStr)
    if(gioi_tinh == "nam"):
        if os.path.exists(folder_path_list_nam_tam_thoi):
        # Lặp qua từng tệp trong thư mục
            for file_name in os.listdir(folder_path_list_nam_tam_thoi):
                file_path = os.path.join(folder_path_list_nam_tam_thoi, file_name)
                # Kiểm tra xem tệp đó là một tệp (không phải thư mục)
                if os.path.isfile(file_path):
                    # Nếu là tệp, thực hiện xóa
                    os.remove(file_path)
    else:
        if os.path.exists(folder_path_list_nu_tam_thoi):
            # Lặp qua từng tệp trong thư mục
            for file_name in os.listdir(folder_path_list_nu_tam_thoi):
                file_path = os.path.join(folder_path_list_nu_tam_thoi, file_name)
                # Kiểm tra xem tệp đó là một tệp (không phải thư mục)
                if os.path.isfile(file_path):
                    # Nếu là tệp, thực hiện xóa
                    os.remove(file_path)

    return folderLuu

id_user=262
gioi_tinh="nam"
list_folder = "weddingface10"
link1= "/var/www/build_futurelove/image/image_user/262/nam/262_nam_26193.jpg"
path = gen_sk_swap_iudi(id_user, gioi_tinh, list_folder, link1)
print(path)