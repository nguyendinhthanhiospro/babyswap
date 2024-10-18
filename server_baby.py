import math
from fastapi import FastAPI, Request, Header
import threading
import time
import asyncio
import shutil

import torch
from test_fun import gen_sk, gen_sk_ngam, gen_sk_swap, gen_sk_baby, gen_sk_noel
from server_wedding import merge_image
from test_csv import (
    get_random_data_noel,
    get_random_data,
    merge_image,
    save_to_mysql,
    get_random_data_skngam,
    save_to_mysql_anh_don,
    save_to_mysql_skngam,
    insert_svg_logo,
    save_to_mysql_2_image,
    get_random_data_swap_baby,
    save_to_mysql_swap_baby,
    save_to_mysql_2_image_mom_baby,
)
from server_fast import saved_album_wedding_swap
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, File, UploadFile
import uuid, os
from roop import core

from func_vid import (
    gen_video,
    gen_video_swap_imagevid,
    gen_video_swap_imagevid_growup,
    save_video_to_mysql_swap_imagevideo_growup,
    gen_video_swap_imagevid_growup_mom_baby,
    gen_video_mom_baby,
)
from server_fast import *
from login.func import validate_token, generate_token, send_mail_swap_done
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException


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

# SWAP VIDEO IMAGE GROWUP


@app.get("/getdata/swap/listimage_mom_baby", dependencies=[Depends(validate_token)])
async def gen_sk_swap_mom_baby(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    link1: Optional[str] = Header(None),
):
    print(link1)
    folder_time = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    folder_path_list_image = f"/home/thinkdiff/Documents/me-be/{list_folder}"
    print(folder_path_list_image)
    # folder_path_list_nu = f"/media/thinkdiff/Seagate Hub/server_grow_up_image/Album_image/Mom_Baby/BE/{list_folder}"
    # output_path_chuanbighep = f"/media/thinkdiff/Seagate Hub/server_grow_up_image/Album_image/out/{folder_time}/"
    # timkiem_path_chuanbighep = f"/media/thinkdiff/Seagate Hub/server_grow_up_image/Album_image/out/{folder_time}"
    folder_export_image = (
        f"/var/www/build_futurelove/image/image_user/"
        + str(id_user)
        + "/mom_baby/"
        + str(folder_time)
        + "/"
    )
    # os.makedirs(output_path_chuanbighep, exist_ok=True)
    os.makedirs(folder_export_image, exist_ok=True)
    print(f"________KET QUA TRA VE____: {folder_export_image}")
    # print(f"________thu MUC NAM_NU_TAO RA____: {output_path_chuanbighep}")
    print(f"________link_HEADer____: {link1}")
    try:
        core.run(link1, folder_path_list_image, folder_export_image)
    except:
        return JSONResponse(content={"sukien_2_image": "error images 1 have not face"})

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
    # folder_export_image = folder_export_image + f"/{list_folder}"
    if os.path.exists(folder_export_image):
        # Lấy danh sách tên file trong thư mục
        # /var/www/build_futurelove/
        demsolan = 0
        file_names = os.listdir(folder_export_image)
        if file_names:  # Check if the list is not empty
            print(file_names)
            for link in file_names:
                link_swap = f"{folder_export_image}/{link}"
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
                    "mom_and_baby",
                    "mom_and_baby",
                    "mom_and_baby",
                )
                data_list.append(link_swap)
                # if demsolan == 0:
                #     saved_album_wedding_swap(
                #         link_anh_mom,
                #         link2,
                #         link_swap,
                #         device_them_su_kien,
                #         ip_them_su_kien,
                #         id_user,
                #     )
                #     demsolan = demsolan + 1
                # print("SONPRO______" + str(Json_added))
    else:
        print("The list of file names is empty.")
    return JSONResponse(
        content={"sukien_2_image": Json_added, "link_anh_swap": data_list}
    )


@app.post(
    "/getdata/genvideo/swap/imagevid/grow_up_1", dependencies=[Depends(validate_token)]
)
async def gen_video_swap_image_with_video_grow_up_1(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    src_img: str,
    src_vid_path: str,
):
    folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    print(folder)
    folder_path = f"/media/thinkdiff/Seagate Hub/server_grow_up/video_user/{folder}"
    print(folder_path)
    os.makedirs(folder_path, exist_ok=True)

    src_video = os.path.join(folder_path, os.path.basename(src_vid_path))
    print(src_video)

    shutil.copy(src_vid_path, src_video)

    loop = asyncio.get_event_loop()

    # Sử dụng event loop của asyncio
    data = await loop.run_in_executor(
        executor,
        gen_video_swap_imagevid_growup,
        src_img,
        src_video,
        folder,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
    )
    return JSONResponse(content={"sukien_swap_video": data})


# GET ALL VIDEO BABY AND MOM


@app.get("/get/list_video/all_video_baby_mom", tags=["list_video"])
async def get_data_list_video_all(request: Request):
    list_temp = dict()
    page = request.query_params.get("page")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        limit = 10
        offset = (int(page) - 1) * limit
        mycursor = connection.cursor()
        query = "SELECT COUNT(listVideo_baby.id) FROM listVideo_baby"
        mycursor.execute(query)
        total_page = math.ceil(mycursor.fetchall()[0][0] / 10)

        query = f"SELECT * FROM listVideo_baby LIMIT {limit} OFFSET {offset}"
        mycursor.execute(query)
        result2 = mycursor.fetchall()

        temp = []
        for row in result2:
            video = {
                "id": row[0],
                "linkgoc": row[1],
                "noidung": row[2],
                "gioitinh": row[7],
                "mau_da": row[8],
                "chung_toc": row[9],
            }
            temp.append(video)
        list_temp["data"] = temp
        list_temp["total_page"] = total_page

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return list_temp


@app.get("/get/list_video/time_machine_temp", tags=["list_video"])
async def get_data_list_temp_video_all(request: Request):
    list_temp = dict()
    page = request.query_params.get("page")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        limit = 10
        offset = (int(page) - 1) * limit
        mycursor = connection.cursor()
        query = "SELECT COUNT(watchme_grow.id) FROM watchme_grow "
        mycursor.execute(query)
        data_length = mycursor.fetchall()[0][0]
        total_page = math.ceil(data_length / limit)

        query_data = f"SELECT * FROM watchme_grow LIMIT {limit} OFFSET {offset}"
        mycursor.execute(query_data)
        result2 = mycursor.fetchall()

        temp = []
        for row in result2:
            video = {
                "id": row[0],
                "linkgoc": row[1],
                "noidung": row[2],
                "gioitinh": row[7],
                "mau_da": row[8],
                "chung_toc": row[9],
            }
            temp.append(video)
        list_temp["data"] = temp
        list_temp["total_page"] = total_page

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return list_temp


@app.get("/get/list_video/time_machine_temp_detail", tags=["list_video"])
async def get_data_list_temp_video_detail(request: Request):
    list_temp = []
    id = request.query_params.get("id")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM watchme_grow WHERE id = %s"
        param = (id,)
        mycursor.execute(query, param)
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id": row[0],
                "linkgoc": row[1],
                "noidung": row[2],
                "gioitinh": row[7],
                "mau_da": row[8],
                "chung_toc": row[9],
            }
            list_temp.append(video)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return list_temp


@app.get("/get/list_image/mom_baby_temp", tags=["list_image"])
async def get_data_list_temp_img_all(request: Request):
    list_temp = dict()
    page = request.query_params.get("page")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT COUNT(Mother_baby.id_cate) FROM Mother_baby"
        mycursor.execute(query)
        total_page = math.ceil(mycursor.fetchall()[0][0] / 10)
        limit = 10
        offset = (int(page) - 1) * limit
        query_temp = f"SELECT * FROM Mother_baby LIMIT {limit} OFFSET {offset}"
        mycursor.execute(query_temp)
        result2 = mycursor.fetchall()
        temp = []
        for row in result2:
            data = {
                "id_cate": row[0],
                "name_cate": row[1],
                "number_image": row[2],
                "folder_name": row[3],
                "selected_swap": row[4],
                "image_sample": row[5],
            }
            temp.append(data)
        list_temp["data"] = temp
        list_temp["total_page"] = total_page

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return list_temp


@app.get("/get/list_image/mom_baby_temp_detail", tags=["list_image"])
async def get_data_list_temp_img_all_detail(request: Request):
    list_image = []
    try:
        id_cate = request.query_params.get("id")
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM listImage_Mother_baby WHERE IDCategories = %s"
        param = (id_cate,)
        mycursor.execute(query, param)
        result2 = mycursor.fetchall()

        for row in result2:
            data = {
                "id": row[0],
                "mask": row[1],
                "thongtin": row[2],
                "image": row[3],
                "dotuoi": row[4],
                "IDCategories": row[5],
            }
            list_image.append(data)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return list_image


@app.get("/get/list_video/id_video", tags=["list_video"])
async def get_data_list_video_id(request: Request):
    id_video = []
    id_video_santa = request.query_params.get("id_video")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM listVideo WHERE id = %s"
        mycursor.execute(query, (id_video_santa,))
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id": row[0],
                "linkgoc": row[1],
                "noidung": row[2],
                "IDCategories": row[3],
                "age_video": row[4],
                "gioitinh": row[5],
                "mau_da": row[6],
                "chung_toc": row[7],
            }
            id_video.append(video)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": id_video})


# GET ALL VIDEO SWAP


@app.get("/get/list_video/all_video_swap", tags=["list_video"])
async def get_data_list_video_all_swap(request: Request):
    list_toan_bo_video = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_video_image_growup "
        mycursor.execute(query)
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                # 'age_video': row[4],
                # 'gioitinh': row[5],
                # 'mau_da': row[6],
                "id_user": row[7],
            }
            list_toan_bo_video.append(video)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_video})


# GET VIDEO SWAP THEO ID
@app.get("/get/list_video/id_video_swap", tags=["list_video"])
async def get_data_list_video_id(request: Request):
    id_video = []
    id_video_santa = request.query_params.get("id_video_swap")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_video_image_growup WHERE id = %s"
        mycursor.execute(query, (id_video_santa,))
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
            }
            id_video.append(video)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": id_video})


# GET VIDEO SWAP  THEO ID USER
@app.get("/get/list_video/id_user_swap", tags=["list_video"])
async def get_data_list_video_mom_baby_id(request: Request):
    id_video = []
    id_video_santa = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_video_image_growup WHERE id_user = %s"
        mycursor.execute(query, (id_video_santa,))
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
            }
            id_video.append(video)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": id_video})


# GET album SWAP IMAGE THEO ALBUM
@app.get("/get/list_video/id_image_album_swap", tags=["list_video"])
async def get_data_list_swap_image_album(request: Request):
    id_image = []
    album_mom_baby = request.query_params.get("album")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_video_image_growup WHERE id = %s"
        mycursor.execute(query, (album_mom_baby,))
        result2 = mycursor.fetchall()
        print(result2)
        for row in result2:
            video = {
                "id": row[10],
                "album": row[10],
                "id_saved": row[0],
                "link_mom_goc": row[1],
                "link_baby_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[7],
            }
            id_image.append(video)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": id_image})


@app.get("/get/list_image/all_image_swap", tags=["list_image"])
async def get_data_list_swap_image_album(request: Request):
    id_image = []
    id_user = request.query_params.get("id_user")
    type = request.query_params.get("type")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_2_image WHERE id_user = %s AND loai_sukien LIKE %s"
        param = (id_user, f"%{type}%")
        mycursor.execute(query, param)
        result2 = mycursor.fetchall()
        for row in result2:
            link_da_swap = row[3].replace(
                "https://futurelove.online", "https://photo.gachmen.org"
            )

            data = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": link_da_swap,
                "id_toan_bo_su_kien": row[4],
                "thoigian_sukien": row[5],
                "device_them_su_kien": row[6],
                "ip_them_su_kien": row[7],
                "id_user": row[8],
                "count_comment": row[9],
                "count_view": row[10],
                "id_template": row[11],
                "loai_sukien": row[12],
                "album": row[13],
                "id_sk_album": row[14],
            }
            id_image.append(data)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return id_image


@app.get("/get/list_image/all_image_swap_mom_baby", tags=["list_image"])
async def get_data_list_swap_image_album(request: Request):
    id_image = []
    id_user = request.query_params.get("id_user")
    type = request.query_params.get("type")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_alone WHERE id_user = %s AND loai_sukien LIKE %s"
        param = (id_user, f"%{type}%")
        mycursor.execute(query, param)
        result2 = mycursor.fetchall()
        for row in result2:
            link_da_swap = row[3].replace(
                "https://futurelove.online", "https://photo.gachmen.org"
            )

            data = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_da_swap": row[2],
                "id_toan_bo_su_kien": link_da_swap,
                "thoigian_sukien": row[4],
                "device_them_su_kien": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "id_template": row[10],
                "loai_sukien": row[11],
                "album": row[12],
                "id_sk_album": row[13],
            }
            id_image.append(data)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return id_image


@app.get("/list_image/all_image_swap_generate", tags=["list_image"])
async def get_data_list_swap_image_album(request: Request):
    id_image = []
    id_user = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_swap_baby WHERE id_user = %s"
        param = (id_user,)
        mycursor.execute(query, param)
        result2 = mycursor.fetchall()
        for row in result2:
            link_da_swap = row[3].replace(
                "https://futurelove.online", "https://photo.gachmen.org"
            )
            data = {
                "id_saved": row[0],
                "link_nam_goc": row[1],
                "link_nu_goc": row[2],
                "link_baby_goc": link_da_swap,
                "link_da_swap": row[4],
                "id_toan_bo_su_kien": row[5],
                "noi_dung_su_kien": row[6],
                "thoigian_sukien": row[7],
                "device_them_su_kien": row[8],
                "ip_them_su_kien": row[9],
                "id_user": row[10],
                "tomLuocText": row[11],
                "count_comment": row[12],
                "count_view": row[13],
                "id_template": row[14],
            }
            id_image.append(data)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return id_image


# GET ALL VIDEO GROW UP


@app.get("/get/list_video/all_video", tags=["list_video"])
async def get_data_list_video_all(request: Request):
    print("pass")
    type_video = request.query_params.get("type_video")
    list_toan_bo_video = []
    print("pass1")
    try:
        print("pass2")
        connection = mysql.connector.connect(**config)
        print(connection)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM listVideo WHERE noidung LIKE %s"
        param = f"%{type_video}%"
        mycursor.execute(query, (param,))
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id": row[0],
                "linkgoc": row[1],
                "noidung": row[2],
                "gioitinh": row[7],
                "mau_da": row[8],
                "chung_toc": row[9],
            }
            list_toan_bo_video.append(video)

    except mysql.connector.Error as error:
        print("pass Error")
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_video})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5555)
