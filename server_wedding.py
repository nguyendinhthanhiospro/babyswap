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
from pathlib import Path

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

# pip install insightface==0.2.1 onnxruntime moviepy
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = {
    "user": "sonpro",
    "password": "Ratiendi89",
    "host": "localhost",
    "port": 3306,
    "database": "FutureLove4",
    # 'auth_plugin': 'mysql_native_password'
}

from concurrent.futures import ThreadPoolExecutor
from typing import Optional

# Create a ThreadPoolExecutor with a maximum of 2 concurrent processes
executor = ThreadPoolExecutor(max_workers=10)


def merge_image(list_data, folder_path):
    print(list_data)
    # Tạo một dictionary để lưu trữ các ảnh theo chỉ số "i"
    image_dict = {}
    print("folder", folder_path)
    # Lặp qua tất cả các tệp trong thư mục
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            parts = filename.split("_")
            if len(parts) == 2:
                key = parts[1].split(".")[0]  # Lấy chỉ số "i" từ tên file
                if key not in image_dict:
                    image_dict[key] = []
                image_dict[key].append(filename)

    combined_dict = {}
    sorted_dict = {}
    for key, values in image_dict.items():
        nam_values = []
        nu_values = []
        for value in values:
            if value.startswith("nam_"):
                nam_values.append(value)
            elif value.startswith("nu_"):
                nu_values.append(value)
        sorted_dict[key] = nam_values + nu_values

    combined_dict = sorted_dict.copy()  # Sao chép dict ban đầu để tạo dict mới
    print("imagedict: ", image_dict)
    for item in list_data:
        id_value = str(item["id"])  # Chuyển id từ int sang str để so sánh
        vtrinam_value = item["vtrinam"]

        if id_value in combined_dict:
            combined_dict[id_value].append(vtrinam_value)
    print(combined_dict)
    # Lặp qua các cặp ảnh cùng chỉ số "i" và ghép chúng lại
    for key, filenames in combined_dict.items():
        if len(filenames) == 3:
            if filenames[2] == "1":
                filenames.remove("1")
                images = [
                    Image.open(os.path.join(folder_path, filename))
                    for filename in filenames
                ]
                widths, heights = zip(*(imaItem.size for imaItem in images))
                total_width = sum(widths)
                max_height = max(heights)
                new_im = Image.new("RGB", (total_width, max_height))
                x_offset = 0
                for im in images:
                    new_im.paste(im, (x_offset, 0))
                    x_offset += im.size[0]
                new_im.save(os.path.join(folder_path, f"AI_GEN_{key}.jpg"))
                for filename in filenames:
                    os.remove(os.path.join(folder_path, filename))

            elif filenames[2] == "0":
                filenames.remove("0")
                images = [
                    Image.open(os.path.join(folder_path, filename))
                    for filename in filenames
                ]
                images.reverse()
                widths, heights = zip(*(i.size for i in images))
                total_width = sum(widths)
                max_height = max(heights)
                new_im = Image.new("RGB", (total_width, max_height))
                x_offset = 0
                for im in images:
                    new_im.paste(im, (x_offset, 0))
                    x_offset += im.size[0]
                new_im.save(os.path.join(folder_path, f"AI_GEN_{key}.jpg"))

                for filename in filenames:
                    os.remove(os.path.join(folder_path, filename))
    print("Hoàn thành việc ghép ảnh.")


# SWAP LIST IMAGE
def gen_sk_swap_wedding(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    id_sk_all: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    print("hello")
    folder_time = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    # /var/www/build_futurelove/image/image_user/236/nam/236_nam_85168.jpg
    folder_path_list_nam = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/NAM/{list_folder}"
    )
    folder_path_list_nu = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/NU/{list_folder}"
    )
    output_path_chuanbighep = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/out/{folder_time}/"
    )
    timkiem_path_chuanbighep = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/out/{folder_time}"
    )
    folder_export_wedding = (
        f"/var/www/build_futurelove/image/image_user/" + str(id_user) + "/wedding"
    )
    os.makedirs(output_path_chuanbighep, exist_ok=True)
    os.makedirs(folder_export_wedding, exist_ok=True)
    print(f"______________________________KET QUA TRA VE____: {folder_path_list_nam}")
    print(
        f"______________________________thu MUC NAM_NU_TAO RA____: {output_path_chuanbighep}"
    )
    print(f"________linkNAM_HEADer____: {link1}")
    print(f"________linkNU_HEADER____: {link2}")
    try:
        core.run(link1, folder_path_list_nam, output_path_chuanbighep)
    except:
        return JSONResponse(content={"sukien_2_image": "error images 1 have not face"})
    try:
        core.run(link2, folder_path_list_nu, output_path_chuanbighep)
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
    data_list = []
    Json_added = {
        "id_saved": 0,
        "link_src_goc": link1,
        "link_tar_goc": link2,
        "link_da_swap": "link_swap",
        "id_toan_bo_su_kien": 0,
        "thoigian_sukien": "date",
        "device_them_su_kien": device_them_su_kien,
        "ip_them_su_kien": ip_them_su_kien,
        "id_user": id_user,
        "count_comment": 0,
        "count_view": 0,
        "id_template": 0,
    }
    folderLuu = folder_export_wedding + f"/{list_folder}"
    if os.path.exists(folderLuu):
        # Lấy danh sách tên file trong thư mục
        # /var/www/build_futurelove/
        demsolan = 0
        file_names = os.listdir(folderLuu)
        if file_names:  # Check if the list is not empty
            print(file_names)
            for link in file_names:
                link_swap = f"{folderLuu}/{link}"
                link_swap = link_swap.replace(
                    "/var/www/build_futurelove/", "https://photo.gachmen.org/"
                )
                print(link_swap)
                # Continue with the rest of your code...
                Json_added = save_to_mysql_2_image(
                    link1,
                    link2,
                    link_swap,
                    device_them_su_kien,
                    ip_them_su_kien,
                    id_user,
                    "wedding",
                    list_folder,
                    id_sk_all,
                )
                data_list.append(link_swap)
                if demsolan == 0:
                    saved_album_wedding_swap(
                        link1,
                        link2,
                        link_swap,
                        device_them_su_kien,
                        ip_them_su_kien,
                        id_user,
                    )
                    demsolan = demsolan + 1
                print("SONPRO______demsolan_____" + str(demsolan))
    else:
        print("The list of file names is empty.")
    return JSONResponse(
        content={"sukien_2_image": Json_added, "link_anh_swap": data_list}
    )


def load_img(image_file):
    image = tf.io.read_file(image_file)
    image = tf.image.decode_jpeg(image)

    real_image = tf.cast(image, tf.float32)

    return real_image


def gen_sk_swap_wedding_fix(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    id_sk_all: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    print("hello")
    folder_time = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    # /var/www/build_futurelove/image/image_user/236/nam/236_nam_85168.jpg
    folder_path_list_nam = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/NAM/{list_folder}"
    )
    folder_path_list_nu = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/NU/{list_folder}"
    )
    output_path_chuanbighep = (
        f"/home/thinkdiff/Documents/wedding-cut-template-cut/out/{folder_time}/"
    )
    timkiem_path_chuanbighep = (
        f"/home/thinkdiff/Documents/wedding-cut-template-cut/out/{folder_time}"
    )
    folder_export_wedding = (
        f"/var/www/build_futurelove/image/image_user/"
        + str(id_user)
        + "/wedding/"
        + str(folder_time)
    )
    if (
        link1.find("/https:") > 0
    ):  # /var/www/build_futurelove/https://photo.gachmen.org/image/image_user/262/nu/262_nu_75969.jpg
        link1 = link1.replace("https://photo.gachmen.org/", "")
    if (
        link2.find("/https:") > 0
    ):  # /var/www/build_futurelove/https://photo.gachmen.org/image/image_user/262/nu/262_nu_75969.jpg
        link2 = link2.replace("https://photo.gachmen.org/", "")
    print("____________________TAO THU MUC WEdding")
    print(output_path_chuanbighep)
    os.makedirs(output_path_chuanbighep, exist_ok=True)
    os.makedirs(folder_export_wedding, exist_ok=True)
    print(f"________KET QUA TRA VE____: {folder_path_list_nam}")
    print(f"________thu MUC NAM_NU_TAO RA____: {output_path_chuanbighep}")
    print(f"________linkNAM_HEADer____: {link1}")
    print(f"________linkNU_HEADER____: {link2}")
    try:
        print("vao tryyyyyyyyyyyyyyyy111111")
        core.run(link1, folder_path_list_nam, output_path_chuanbighep)
    except:
        print("vao exceptttttttttttttttt")
        return JSONResponse(content={"sukien_2_image": "error images 1 have not face"})
    try:
        core.run(link2, folder_path_list_nu, output_path_chuanbighep)
    except:
        return JSONResponse(content={"sukien_2_image": "error images 2 have not face"})
    for filename in os.listdir(timkiem_path_chuanbighep):
        if filename.endswith("_a.jpg"):
            name_xoa_ky_tu = filename.rstrip("_a.jpg")
            print(str(filename))
            image1Pro = str(output_path_chuanbighep) + str(name_xoa_ky_tu) + "_a.jpg"
            image2Pro = str(output_path_chuanbighep) + str(name_xoa_ky_tu) + "_b.jpg"
            print("______ANH_A___" + str(image1Pro))
            print("______ANH_B___" + str(image2Pro))
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
            image1Pro = load_img(image1Pro)
            image2Pro = load_img(image2Pro)
            image2Pro = image2Pro[:, 1:, :]
            image1Pro = image1Pro[:, : image1Pro.shape[1] - 1, :]

            new_im = np.zeros(
                (image2Pro.shape[0], image2Pro.shape[1] + image1Pro.shape[1], 3),
                dtype=np.uint8,
            )

            x_offset = 0
            for im in image2FileCombine:
                # Copy ảnh 1 vào nửa trái của ảnh kết quả
                new_im[: image1Pro.shape[0], : image1Pro.shape[1], :] = image1Pro

                # Copy ảnh 2 vào nửa phải của ảnh kết quả
                new_im[: image2Pro.shape[0], image1Pro.shape[1] :, :] = image2Pro
                fileStr = os.path.join(
                    timkiem_path_chuanbighep,
                    f"AI_GEN_{name_xoa_ky_tu}.jpg",
                )
                print("___SON___" + fileStr)
                new_im_pil = Image.fromarray(new_im)
                new_im_pil.save(fileStr)
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
            # os.remove(image1Pro)
            # os.remove(image2Pro)
            # os.remove(fileStr)
    data_list = []
    Json_added = {
        "id_saved": 0,
        "link_src_goc": link1,
        "link_tar_goc": link2,
        "link_da_swap": "link_swap",
        "id_toan_bo_su_kien": 0,
        "thoigian_sukien": "date",
        "device_them_su_kien": device_them_su_kien,
        "ip_them_su_kien": ip_them_su_kien,
        "id_user": id_user,
        "count_comment": 0,
        "count_view": 0,
        "id_template": 0,
    }
    folderLuu = folder_export_wedding + f"/{list_folder}"
    if os.path.exists(folderLuu):
        # Lấy danh sách tên file trong thư mục
        # /var/www/build_futurelove/
        demsolan = 0
        file_names = os.listdir(folderLuu)
        if file_names:  # Check if the list is not empty
            print(file_names)
            for link in file_names:
                link_swap = f"{folderLuu}/{link}"
                link_swap = link_swap.replace(
                    "/var/www/build_futurelove/", "https://photo.gachmen.org/"
                )
                print(link_swap)
                # Continue with the rest of your code...
                Json_added = save_to_mysql_2_image(
                    link1,
                    link2,
                    link_swap,
                    device_them_su_kien,
                    ip_them_su_kien,
                    id_user,
                    "wedding",
                    list_folder,
                    id_sk_all,
                )
                data_list.append(link_swap)
                if demsolan == 0:
                    saved_album_wedding_swap(
                        link1,
                        link2,
                        link_swap,
                        device_them_su_kien,
                        ip_them_su_kien,
                        id_user,
                    )
                    demsolan = demsolan + 1
                print("SONPRO______demsolan_____" + str(demsolan))
    else:
        print("The list of file names is empty.")
    return (
        JSONResponse(content={"sukien_2_image": Json_added, "link_anh_swap": data_list})
    ), folderLuu


# tao video tu anh

import cv2
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import glob
import ffmpeg


def resize_with_padding(image, target_width, target_height):
    # Lấy kích thước của ảnh
    image_height, image_width = image.shape[:2]

    # Tính tỷ lệ khung hình của ảnh
    aspect_ratio = image_width / image_height

    # Tính toán kích thước mới sao cho giữ nguyên tỷ lệ khung hình
    if aspect_ratio > target_width / target_height:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    # Resize ảnh với kích thước mới
    resized_image = cv2.resize(image, (new_width, new_height))

    # Tạo một ảnh trống với kích thước mục tiêu và đặt ảnh đã resize vào giữa
    padded_image = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    start_x = (target_width - new_width) // 2
    start_y = (target_height - new_height) // 2
    padded_image[start_y : start_y + new_height, start_x : start_x + new_width] = (
        resized_image
    )

    return padded_image


def create_video_folder(list_folder):
    # Lấy thư mục cha của list_folder
    parent_folder = os.path.dirname(list_folder)

    # Thêm "video" vào thư mục cha
    video_folder = os.path.join(parent_folder, "video")

    # Kiểm tra xem thư mục đã tồn tại chưa
    if not os.path.exists(video_folder):
        # Nếu không tồn tại, tạo thư mục mới
        os.makedirs(video_folder)
        print(f"Thư mục 'video' đã được tạo thành công trong '{parent_folder}'.")
    else:
        print(f"Thư mục 'video' đã tồn tại trong '{parent_folder}'.")
    return video_folder


def generatex(list_folder):
    image_directory = list_folder
    # Input and output settings for image video generation
    image_display_duration = 3000  # milliseconds (3 seconds)
    transition_duration = 50  # Frames (0.5 seconds)
    frame_rate = 60
    video_width = 1920
    video_height = 1080

    directoryback = "/var/www/build_futurelove/image/test_music_background/hihi"
    mp3_files_back = glob.glob(os.path.join(directoryback, "*.mp3"))
    background_audio_path = random.choice(mp3_files_back) if mp3_files_back else None
    print("Background audio path:", background_audio_path)

    speech_audio_path = background_audio_path

    video_folder = create_video_folder(list_folder)
    print(video_folder)
    output_path = video_folder + "/final_output.mp4"
    my_file = Path(output_path)

    if my_file.is_file():
        return output_path
    # Create an in-memory video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_video = cv2.VideoWriter(
        "memory.mp4", fourcc, frame_rate, (video_width, video_height)
    )

    # Generate image video
    image_files = sorted(
        [
            f
            for f in os.listdir(image_directory)
            if f.lower().endswith((".jpg", ".png", ".jpeg"))
        ]
    )
    random.shuffle(image_files)

    for i in range(len(image_files) - 1):
        image1 = cv2.imread(os.path.join(image_directory, image_files[i]))
        image2 = cv2.imread(os.path.join(image_directory, image_files[i + 1]))

        image1 = resize_with_padding(image1, video_width, video_height)
        image2 = resize_with_padding(image2, video_width, video_height)

        for _ in range(int(image_display_duration * frame_rate / 1000)):
            output_video.write(np.uint8(image1))

        for frame in range(transition_duration + 1):
            alpha = frame / transition_duration
            blended = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
            output_video.write(np.uint8(blended))
    output_video.release()

    # Add audio to the generated video
    def crop_audio(audio_clip, target_duration):
        return audio_clip.subclip(0, target_duration)

    def repeat_audio(audio_clip, target_duration):
        audio_duration = audio_clip.duration
        loops_needed = int(target_duration / audio_duration)
        looped_audio = CompositeAudioClip([audio_clip] * loops_needed)
        return looped_audio

    # Create a video clip from the in-memory video
    memory_video = cv2.VideoCapture("memory.mp4")
    memory_video.set(cv2.CAP_PROP_FPS, frame_rate)
    memory_video.set(cv2.CAP_PROP_FRAME_WIDTH, video_width)
    memory_video.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height)

    video_clip = VideoFileClip("memory.mp4")

    background_audio_clip = AudioFileClip(background_audio_path)
    speech_audio_clip = AudioFileClip(speech_audio_path)

    video_duration = video_clip.duration
    background_audio_duration = background_audio_clip.duration
    speech_audio_duration = speech_audio_clip.duration

    if video_duration < speech_audio_duration:
        adjusted_speech_audio = crop_audio(speech_audio_clip, video_duration)
    else:
        adjusted_speech_audio = speech_audio_clip.subclip(0, video_duration)

    if video_duration > background_audio_duration:
        adjusted_background_audio = repeat_audio(background_audio_clip, video_duration)
    else:
        adjusted_background_audio = background_audio_clip.subclip(0, video_duration)

    final_audio = CompositeAudioClip(
        [adjusted_background_audio.volumex(1.0), adjusted_speech_audio.volumex(0.1)]
    )

    final_clip = video_clip.set_audio(final_audio)
    final_clip.write_videofile(output_path, audio_codec="aac")
    os.remove("memory.mp4")

    print("Final video with audio created:", output_path)
    # Chuyển đổi video thành định dạng 1080p
    input_video_path = output_path
    output_video_path = video_folder + "/output_video_1080p.mp4"
    # Sử dụng ffmpeg để chuyển đổi video
    (
        ffmpeg.input(input_video_path)
        .output(output_video_path, vf="scale=1920:1080", acodec="copy")
        .run()
    )

    print("Video đã được chuyển đổi thành 1080p và lưu tại:", output_video_path)
    # Remove the original video output
    if os.path.exists(output_path):
        os.remove(output_path)
    return output_video_path


import zipfile


# ham zip file anh va video
def zip_images(base_dir, zip_name):
    # Đảm bảo rằng zip_name không chứa đường dẫn
    zip_name = os.path.basename(zip_name)

    # Tạo đường dẫn đầy đủ cho tệp zip trong thư mục codetime
    zip_path = os.path.join(base_dir, "..", zip_name)
    zip_path = os.path.abspath(zip_path)  # Đảm bảo đường dẫn tuyệt đối

    # Mở tệp zip để ghi
    with zipfile.ZipFile(zip_path, "w") as zipf:
        # Đi qua tất cả các tệp trong thư mục base_dir
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                # Kiểm tra xem tệp có phải là hình ảnh không (có phần mở rộng là .jpg hoặc .png)
                if file.endswith(".jpg") or file.endswith(".png"):
                    # Xác định đường dẫn đầy đủ của tệp
                    file_path = os.path.join(root, file)
                    # Tạo đường dẫn tương đối để thêm vào tệp zip
                    relative_path = os.path.relpath(file_path, base_dir)
                    # Thêm tệp vào tệp zip
                    zipf.write(file_path, relative_path)

    return zip_path


def gen_sk_swap_alone(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    id_sk_all: str,
    link1: Optional[str] = Header(None),
):
    print("hello")
    folder_time = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    # /var/www/build_futurelove/image/image_user/236/nam/236_nam_85168.jpg
    folder_path_list = (
        f"/media/thinkdiff/Seagate Hub/template_alone/target/{list_folder}"
    )
    folder_export_swap = (
        f"/var/www/build_futurelove/image/image_user/"
        + str(id_user)
        + "/Anh_don/"
        + str(folder_time)
    )
    folderLuu = folder_export_swap + f"/{list_folder}"
    os.makedirs(folderLuu, exist_ok=True)
    print(f"________KET QUA TRA VE____: {folder_path_list}")
    print(f"________Thu muc sau khi ghep____: {folderLuu}")
    print(f"________link_HEADer____: {link1}")
    try:
        core.run(link1, folder_path_list, folderLuu)
    except:
        return JSONResponse(content={"sukien_2_image": "error image have not face"})
    for filename in os.listdir(folder_export_swap):
        source_file = os.path.join(folder_export_swap, filename)
        # Chỉ di chuyển tệp nếu nó là một tệp hình ảnh
        if os.path.isfile(source_file) and filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".bmp")
        ):
            shutil.move(source_file, folderLuu)
    data_list = []
    Json_added = {
        "id_saved": 0,
        "link_src_goc": link1,
        "link_da_swap": "link_swap",
        "id_toan_bo_su_kien": 0,
        "thoigian_sukien": "date",
        "device_them_su_kien": device_them_su_kien,
        "ip_them_su_kien": ip_them_su_kien,
        "id_user": id_user,
        "count_comment": 0,
        "count_view": 0,
        "id_template": 0,
    }
    if os.path.exists(folderLuu):
        # Lấy danh sách tên file trong thư mục
        # /var/www/build_futurelove/
        demsolan = 0
        file_names = os.listdir(folderLuu)
        if file_names:  # Check if the list is not empty
            print(file_names)
            for link in file_names:
                link_swap = f"{folderLuu}/{link}"
                link_swap = link_swap.replace(
                    "/var/www/build_futurelove/", "https://photo.gachmen.org/"
                )
                print(link_swap)
                # Continue with the rest of your code...
                Json_added = save_to_mysql_anh_don(
                    link1,
                    link_swap,
                    device_them_su_kien,
                    ip_them_su_kien,
                    id_user,
                    "Anh_don",
                    list_folder,
                    id_sk_all,
                )
                data_list.append(link_swap)
    else:
        print("The list of file names is empty.")
    return folderLuu


def make_qr(link, id_user):
    # Tạo đường dẫn cho thư mục lưu trữ hình ảnh QR code
    user_folder = os.path.join(
        "/var/www/build_futurelove/image/image_user/" + "{id_user}"
    )
    qrcode_folder = os.path.join(user_folder, "QRcode")

    # Tạo thư mục QRcode nếu chưa tồn tại
    os.makedirs(qrcode_folder, exist_ok=True)

    # Tạo tên tệp ngẫu nhiên cho hình ảnh QR code
    random_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    qr_image_path = os.path.join(qrcode_folder, f"{random_name}.png")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Tạo hình ảnh từ QR Code
    img = qr.make_image(fill_color="black", back_color="white")

    # Lưu hình ảnh
    img.save(qr_image_path)

    return qr_image_path


def gen_sk_swap_thiep_cuoi(
    id_user: int,
    list_folder: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    print("hello")
    folder_time = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    # /var/www/build_futurelove/image/image_user/236/nam/236_nam_85168.jpg
    folder_path_list_nam = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/NAM/{list_folder}"
    )
    folder_path_list_nu = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/NU/{list_folder}"
    )
    output_path_chuanbighep = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/out/{folder_time}/"
    )
    timkiem_path_chuanbighep = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/out/{folder_time}"
    )
    folder_export_wedding = (
        f"/var/www/build_futurelove/image/image_user/" + str(id_user) + "/wedding"
    )
    os.makedirs(output_path_chuanbighep, exist_ok=True)
    os.makedirs(folder_export_wedding, exist_ok=True)
    print(f"________KET QUA TRA VE____: {folder_path_list_nam}")
    print(f"________thu MUC NAM_NU_TAO RA____: {output_path_chuanbighep}")
    print(f"________linkNAM_HEADer____: {link1}")
    print(f"________linkNU_HEADER____: {link2}")
    try:
        core.run(link1, folder_path_list_nam, output_path_chuanbighep)
    except:
        return JSONResponse(content={"sukien_2_image": "error images 1 have not face"})
    try:
        core.run(link2, folder_path_list_nu, output_path_chuanbighep)
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
    folderLuu = folder_export_wedding + f"/{list_folder}"
    return folderLuu


def gen_sk_swap_iudi(id_user: int, gioi_tinh: str, list_folder: str, link1: str):
    print("hello")
    folder_time = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"

    folder_path_list_nam = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/NAM/{list_folder}"
    )
    folder_path_list_nam_tam_thoi = (
        "/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/tam_thoi/NAM"
    )
    folder_path_list_nu = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/NU/{list_folder}"
    )
    folder_path_list_nu_tam_thoi = (
        "/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/tam_thoi/NU"
    )

    # Kiểm tra xem các thư mục có tồn tại hay không
    if not os.path.exists(folder_path_list_nam):
        raise FileNotFoundError(f"The directory {folder_path_list_nam} does not exist.")
    if not os.path.exists(folder_path_list_nu):
        raise FileNotFoundError(f"The directory {folder_path_list_nu} does not exist.")

    # Lấy danh sách các ảnh trong folder_path_list_nam
    nam_images = [
        f
        for f in os.listdir(folder_path_list_nam)
        if os.path.isfile(os.path.join(folder_path_list_nam, f))
    ]
    # Kiểm tra xem có đủ ảnh để chọn không
    if len(nam_images) < 5:
        raise ValueError(
            "Not enough images in folder_path_list_nam to select 5 random images."
        )

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
        if filename.endswith("_a.jpg"):
            return filename.replace("_a.jpg", "_b.jpg")
        elif filename.endswith("_b.jpg"):
            return filename.replace("_b.jpg", "_a.jpg")
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
    if gioi_tinh == "nam":
        try:
            core.run(link1, folder_path_list_nam_tam_thoi, output_path_chuanbighep)
            # Di chuyển các ảnh từ folder_path_list_nam_tam_thoi vào output_path_chuanbighep
            for img in os.listdir(folder_path_list_nu_tam_thoi):
                src_path = os.path.join(folder_path_list_nu_tam_thoi, img)
                dest_path = os.path.join(output_path_chuanbighep, img)
                shutil.move(src_path, dest_path)
        except:
            return JSONResponse(
                content={"sukien_2_image": "error images 1 have not face"}
            )

    else:
        try:
            core.run(link1, folder_path_list_nu_tam_thoi, output_path_chuanbighep)
            # Di chuyển các ảnh từ folder_path_list_nam_tam_thoi vào output_path_chuanbighep
            for img in os.listdir(folder_path_list_nam_tam_thoi):
                src_path = os.path.join(folder_path_list_nam_tam_thoi, img)
                dest_path = os.path.join(output_path_chuanbighep, img)
                shutil.move(src_path, dest_path)
        except:
            return JSONResponse(
                content={"sukien_2_image": "error images 2 have not face"}
            )

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
    if gioi_tinh == "nam":
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


def gen_sk_swap_baby_family(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    id_sk_all: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    print("hello")
    folder_time = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    # /var/www/build_futurelove/image/image_user/236/nam/236_nam_85168.jpg
    folder_path_list_nam = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/baby_giadinh/nam/{list_folder}"
    folder_path_list_nu = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/baby_giadinh/nu/{list_folder}"
    output_path_chuanbighep = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/out/{folder_time}/"
    )
    timkiem_path_chuanbighep = (
        f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/out/{folder_time}"
    )
    folder_export_wedding = (
        f"/var/www/build_futurelove/image/image_user/"
        + str(id_user)
        + "/baby_giadinh/"
        + str(folder_time)
    )
    os.makedirs(output_path_chuanbighep, exist_ok=True)
    os.makedirs(folder_export_wedding, exist_ok=True)
    print(f"________KET QUA TRA VE____: {folder_path_list_nam}")
    print(f"________thu MUC NAM_NU_TAO RA____: {output_path_chuanbighep}")
    print(f"________linkNAM_HEADer____: {link1}")
    print(f"________linkNU_HEADER____: {link2}")
    try:
        core.run(link1, folder_path_list_nam, output_path_chuanbighep)
    except:
        return JSONResponse(content={"sukien_2_image": "error images 1 have not face"})
    try:
        core.run(link2, folder_path_list_nu, output_path_chuanbighep)
    except:
        return JSONResponse(content={"sukien_2_image": "error images 2 have not face"})
    for filename in os.listdir(timkiem_path_chuanbighep):
        if filename.endswith("_a.jpg"):
            name_xoa_ky_tu = filename.rstrip("_a.jpg")
            print(str(filename))
            image1Pro = str(output_path_chuanbighep) + str(name_xoa_ky_tu) + "_a.jpg"
            image2Pro = str(output_path_chuanbighep) + str(name_xoa_ky_tu) + "_b.jpg"
            print("______ANH_A___" + str(image1Pro))
            print("______ANH_B___" + str(image2Pro))
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
            image1Pro = load_img(image1Pro)
            image2Pro = load_img(image2Pro)
            image2Pro = image2Pro[:, 1:, :]
            image1Pro = image1Pro[:, : image1Pro.shape[1] - 1, :]

            new_im = np.zeros(
                (image2Pro.shape[0], image2Pro.shape[1] + image1Pro.shape[1], 3),
                dtype=np.uint8,
            )

            x_offset = 0
            for im in image2FileCombine:
                # Copy ảnh 1 vào nửa trái của ảnh kết quả
                new_im[: image1Pro.shape[0], : image1Pro.shape[1], :] = image1Pro

                # Copy ảnh 2 vào nửa phải của ảnh kết quả
                new_im[: image2Pro.shape[0], image1Pro.shape[1] :, :] = image2Pro
                fileStr = os.path.join(
                    timkiem_path_chuanbighep,
                    f"AI_GEN_{name_xoa_ky_tu}.jpg",
                )
                print("___SON___" + fileStr)
                new_im_pil = Image.fromarray(new_im)
                new_im_pil.save(fileStr)
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
            # os.remove(image1Pro)
            # os.remove(image2Pro)
            # os.remove(fileStr)
    data_list = []
    Json_added = {
        "id_saved": 0,
        "link_src_goc": link1,
        "link_tar_goc": link2,
        "link_da_swap": "link_swap",
        "id_toan_bo_su_kien": 0,
        "thoigian_sukien": "date",
        "device_them_su_kien": device_them_su_kien,
        "ip_them_su_kien": ip_them_su_kien,
        "id_user": id_user,
        "count_comment": 0,
        "count_view": 0,
        "id_template": 0,
    }
    folderLuu = folder_export_wedding + f"/{list_folder}"
    if os.path.exists(folderLuu):
        # Lấy danh sách tên file trong thư mục
        # /var/www/build_futurelove/
        demsolan = 0
        file_names = os.listdir(folderLuu)
        if file_names:  # Check if the list is not empty
            print(file_names)
            for link in file_names:
                link_swap = f"{folderLuu}/{link}"
                link_swap = link_swap.replace(
                    "/var/www/build_futurelove/", "https://photo.gachmen.org/"
                )
                print(link_swap)
                # Continue with the rest of your code...
                Json_added = save_to_mysql_2_image(
                    link1,
                    link2,
                    link_swap,
                    device_them_su_kien,
                    ip_them_su_kien,
                    id_user,
                    "wedding",
                    list_folder,
                    id_sk_all,
                )
                data_list.append(link_swap)
                # if demsolan == 0:
                #     saved_album_wedding_swap(
                #         link1,
                #         link2,
                #         link_swap,
                #         device_them_su_kien,
                #         ip_them_su_kien,
                #         id_user,
                #     )
                #     demsolan = demsolan + 1
                # print("SONPRO______demsolan_____" + str(demsolan))
    else:
        print("The list of file names is empty.")
    return JSONResponse(
        content={"sukien_2_image": Json_added, "link_anh_swap": data_list}
    )  # , folderLuu


def gen_sk_swap_baby_newborn(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    id_sk_all: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    # print("hello")
    folder_time = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    # /var/www/build_futurelove/image/image_user/236/nam/236_nam_85168.jpg
    folder_path_list_nam = f"/home/thinkdiff/Documents/wedding-cut-template-cut/new-born-data/nam/{list_folder}"
    folder_path_list_nu = f"/home/thinkdiff/Documents/wedding-cut-template-cut/new-born-data/nu/{list_folder}"
    folder_export_wedding = (
        f"/var/www/build_futurelove/image/image_user/"
        + str(id_user)
        + "/baby_giadinh/"
        + str(folder_time)
    )
    folderLuu = folder_export_wedding + f"/{list_folder}/"
    os.makedirs(folderLuu, exist_ok=True)
    os.makedirs(folder_export_wedding, exist_ok=True)
    print(f"________KET QUA TRA VE____: {folder_path_list_nam}")
    print(f"________thu MUC NAM_NU_TAO RA____: {folderLuu}")
    print(f"________linkNAM_HEADer____: {link1}")
    print(f"________linkNU_HEADER____: {link2}")
    try:
        core.run(link1, folder_path_list_nam, folderLuu)
    except:
        return JSONResponse(content={"sukien_2_image": "error images 1 have not face"})
    try:
        core.run(link2, folder_path_list_nu, folderLuu)
    except:
        return JSONResponse(content={"sukien_2_image": "error images 2 have not face"})
    data_list = []
    Json_added = {
        "id_saved": 0,
        "link_src_goc": link1,
        "link_tar_goc": link2,
        "link_da_swap": "link_swap",
        "id_toan_bo_su_kien": 0,
        "thoigian_sukien": "date",
        "device_them_su_kien": device_them_su_kien,
        "ip_them_su_kien": ip_them_su_kien,
        "id_user": id_user,
        "count_comment": 0,
        "count_view": 0,
        "id_template": 0,
    }

    if os.path.exists(folderLuu):
        # Lấy danh sách tên file trong thư mục
        # /var/www/build_futurelove/
        demsolan = 0
        file_names = os.listdir(folderLuu)
        if file_names:  # Check if the list is not empty
            # print(file_names)
            for link in file_names:
                link_swap = f"{folderLuu}/{link}"
                link_swap = link_swap.replace(
                    "/var/www/build_futurelove/", "https://photo.gachmen.org/"
                )
                # print(link_swap)
                # Continue with the rest of your code...
                Json_added = save_to_mysql_2_image(
                    link1,
                    link2,
                    link_swap,
                    device_them_su_kien,
                    ip_them_su_kien,
                    id_user,
                    "newborn",
                    list_folder,
                    id_sk_all,
                )
                data_list.append(link_swap)
                # if demsolan == 0:
                #     saved_album_wedding_swap(
                #         link1,
                #         link2,
                #         link_swap,
                #         device_them_su_kien,
                #         ip_them_su_kien,
                #         id_user,
                #     )
                #     demsolan = demsolan + 1
                # print("SONPRO______demsolan_____" + str(demsolan))
    else:
        print("The list of file names is empty.")
    return JSONResponse(
        content={"sukien_2_image": Json_added, "link_anh_swap": data_list}
    )  # , folderLuu
