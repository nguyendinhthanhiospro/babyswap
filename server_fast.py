import math
from fastapi import FastAPI, Query, Request, APIRouter, Form, HTTPException
import re
from PIL import Image
from io import BytesIO
from flask import jsonify
from pydantic import BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydantic import BaseModel, EmailStr
import cv2
from email.message import EmailMessage
import face_recognition
from roop.face_analyser import get_one_face
from login.func import *
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from login.send_email import *
import zipfile
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from login.func import (
    save_user_to_mysql,
    send_mail,
    generate_token,
    verify_password,
    send_mail_reset,
    validate_token,
    send_mail_notifi,
    send_mail_del_account,
)
from test_fun import (
    gen_sk,
    gen_sk_ngam,
    gen_sk_swap,
    gen_sk_baby,
    gen_sk_noel,
)
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
    save_video_to_mysql_swap_imagevideo_growup,
)
from func_vid import (
    gen_video,
    gen_video_swap_imagevid,
    gen_video_swap_imagevid_growup,
    save_video_to_mysql_swap_imagevideo_growup,
    gen_video_swap_imagevid_growup_mom_baby,
)
import jwt
import pytz
from typing import Optional
from datetime import datetime
import uuid
from pydantic import BaseModel
from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from typing import List
import os, random, base64, shutil
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from authlib.integrations.starlette_client import OAuth

from postmarker.core import PostmarkClient

client = PostmarkClient(server_token="2c787e55-cd01-48d8-866a-f2915547adbf")

# from face_mask_detect.FaceMaskDetector import checking_img_gensk

# pip install insightface==0.2.1 onnxruntime moviepy
# app = FastAPI()
# app = FastAPI()
router = APIRouter()

origins = ["*"]
secret_key = "wefhoiwfhsfiug9034bfjkg47vdjk"  # token key
ALGORITHM = "HS256"

config = {
    "user": "sonpro",
    "password": "Ratiendi89",
    "host": "localhost",
    "port": 3306,
    "database": "FutureLove4",
    # 'auth_plugin': 'mysql_native_password'
}


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # SessionMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="!secret")


# Initialize our OAuth instance from the client ID and client secret specified in our .env file
config1 = Config(".env")
oauth = OAuth(config1)

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)


@app.get("/", tags=["authentication"])
async def home(request: Request):
    user = request.session.get("user")
    print(user)
    if user is not None:
        thong_tin = {}
        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor(buffered=True)
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
                print(user["email"])
                query = "SELECT * FROM user WHERE email = %s"
                values = (user["email"],)

                cursor.execute(query, values)
                user_inf = cursor.fetchall()
                if user_inf:
                    thong_tin["id_user"] = user_inf[0][0]
                    thong_tin["link_avatar"] = user_inf[0][1]
                    thong_tin["user_name"] = user_inf[0][2]
                    thong_tin["ip_register"] = user_inf[0][3]
                    thong_tin["device_register"] = user_inf[0][4]
                    thong_tin["email"] = user_inf[0][6]
                    thong_tin["count_sukien"] = int(user_inf[0][7])
                    thong_tin["count_comment"] = int(user_inf[0][8])
                    thong_tin["count_view"] = int(user_inf[0][9])
                    thong_tin["type"] = user_inf[0][11]
                    token = generate_token(user_inf[0][2])
                    thong_tin["token"] = token
                    return thong_tin
                else:
                    print("halo")
                    save_user_to_mysql(
                        str(user["name"]),
                        "123abc123",
                        str(user["email"]),
                        str(user["picture"]),
                        str(user["locale"]),
                        "device",
                        "google",
                    )
                    query = "SELECT * FROM user WHERE email = %s"
                    values = (user["email"],)
                    cursor.execute(query, values)
                    user2 = cursor.fetchall()
                    print(user2)
                    thong_tin["id_user"] = user2[0][0]
                    thong_tin["link_avatar"] = user2[0][1]
                    thong_tin["user_name"] = user2[0][2]
                    thong_tin["ip_register"] = user2[0][3]
                    thong_tin["device_register"] = user2[0][4]
                    thong_tin["email"] = user2[0][6]
                    thong_tin["count_sukien"] = int(user2[0][7])
                    thong_tin["count_comment"] = int(user2[0][8])
                    thong_tin["count_view"] = int(user2[0][9])
                    thong_tin["type"] = user2[0][12]
                    token = generate_token(user2[0][2])
                    thong_tin["token"] = token
                    return thong_tin
        except mysql.connector.Error as error:
            return f"Failed to connect to MySQL database: {error}"
        finally:
            if "connection" in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
    return HTMLResponse('<a href="/login/user">login</a>')


from starlette.datastructures import URL


@app.get(
    "/login/user", tags=["authentication"]
)  # Tag it as "authentication" for our docs
async def login_user(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for("auth")
    print(type(redirect_uri))
    print(redirect_uri)
    redirect_uri = redirect_uri.replace(scheme="https")
    print(redirect_uri)
    print(type(redirect_uri))
    # redirect_uri = 'https://metatechvn.store/auth'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route("/auth")
async def auth(request: Request):
    # Perform Google OAuth
    token = await oauth.google.authorize_access_token(request)
    # user = await oauth.google.parse_id_token(request, token)
    # Save the user
    request.session["user"] = token["userinfo"]
    return RedirectResponse(url="/")


@app.get("/logout", tags=["authentication"])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop("user", None)

    return RedirectResponse(url="/")


@app.get("/list_category", tags=["list data"])
async def get_list_category():
    list_category = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT * from categories_video")
        result = mycursor.fetchall()

        for item in result:
            data = {}
            data["id"] = item[0]
            data["name"] = item[1]
            data["detail"] = item[2]
            list_category.append(data)

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return list_category


@app.get("/lovehistory/sukien/video/{id_su_kien_video}")
async def get_data_love_history(id_su_kien_video: str):
    thong_tin = {}
    list_thong_tin = []
    base_url = "https://photo.gachmen.org/image/video_sk"
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(
            f"SELECT * from saved_sukien_video where id_saved={id_su_kien_video}"
        )
        result2 = mycursor.fetchall()

        for i in range(0, len(result2)):
            query1 = "SELECT IDCategories from listVideo where id=%s"
            mycursor.execute(query1, (result2[i][6],))
            result = mycursor.fetchall()
            query = "SELECT * from categories_video where idCateogries=%s"
            mycursor.execute(query, (result[0][0],))
            result3 = mycursor.fetchall()
            thong_tin["id_video"] = result2[i][0]
            thong_tin["link_image"] = result2[i][2]
            thong_tin["link_vid_swap"] = result2[i][3]
            thong_tin["link_video_goc"] = result2[i][13]
            thong_tin["thoigian_swap"] = result2[i][14]
            thong_tin["id_categories"] = result[0][0]
            thong_tin["name_categories"] = result3[0][1]
            thong_tin["detail"] = result3[0][2]
            thong_tin["ten_su_kien"] = result2[i][4]
            thong_tin["noidung_sukien"] = result2[i][5]
            thong_tin["id_video_swap"] = result2[i][6]
            thong_tin["thoigian_taosk"] = result2[i][7]
            thong_tin["id_user"] = result2[i][10]
            thong_tin["count_comment"] = int(result2[i][11])
            thong_tin["count_view"] = int(result2[i][12])
            list_thong_tin.append(thong_tin)
            thong_tin = {}

        print(mycursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"sukien_video": list_thong_tin})


@app.get("/images/{id_user}")
def get_image_links(request: Request, id_user: int):
    type = request.query_params.get("type")
    # if type != 'nu' or type != 'nam' or type != 'video':
    #     return f"Missing param!!!, your type is {type}"
    image_links = []
    folder_path_nam = f"/var/www/build_futurelove/image/image_user/{id_user}/nam"
    folder_path_video = f"/var/www/build_futurelove/image/image_user/{id_user}/video"
    folder_path_nu = f"/var/www/build_futurelove/image/image_user/{id_user}/nu"
    base_url = "https://photo.gachmen.org"
    if type == "nam":
        if os.path.isdir(folder_path_nam):
            for filename in os.listdir(folder_path_nam):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path_nam, filename)
                    image_links.append(image_path)
        updated_links = [
            link.replace("/var/www/build_futurelove", base_url) for link in image_links
        ]
        return {"image_links_nam": updated_links}

    if type == "nu":
        if os.path.isdir(folder_path_nu):
            for filename in os.listdir(folder_path_nu):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path_nu, filename)
                    image_links.append(image_path)
        updated_links = [
            link.replace("/var/www/build_futurelove", base_url) for link in image_links
        ]
        return {"image_links_nu": updated_links}

    if type == "video":
        if os.path.isdir(folder_path_video):
            for filename in os.listdir(folder_path_video):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path_video, filename)
                    image_links.append(image_path)
        if os.path.isdir(folder_path_nam):
            for filename in os.listdir(folder_path_nam):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path_nam, filename)
                    image_links.append(image_path)

        if os.path.isdir(folder_path_nu):
            for filename in os.listdir(folder_path_nu):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path_nu, filename)
                    image_links.append(image_path)
        updated_links = [
            link.replace("/var/www/build_futurelove", base_url) for link in image_links
        ]
        return {"image_links_video": updated_links}


@app.get("/lovehistory/listvideo/{page}")
async def get_data_list_video(request: Request, page: int):
    category = request.query_params.get("category")

    result = dict()
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        limit = 50
        offset = (page - 1) * limit
        total_page = 0
        result_listVideo = ""

        if category == "0":
            mycursor.execute("SELECT COUNT(listVideo.id) from listVideo")
            data_length = mycursor.fetchall()[0][0]
            total_page = math.ceil(data_length / limit)
            query = "SELECT * from listVideo"
            mycursor.execute(query)
            result_listVideo = mycursor.fetchall()

        elif category != "0":
            query = f"SELECT COUNT(listVideo.id) from listVideo WHERE IDCategories = {category} LIMIT {limit} OFFSET {offset}"
            mycursor.execute(query)
            data_fet = mycursor.fetchall()
            if len(data_fet) == 0:
                return result
            data_length = data_fet[0][0]
            total_page = math.ceil(data_length / limit)
            query = f"SELECT * FROM listVideo WHERE IDCategories = {category} LIMIT {limit} OFFSET {offset}"
            mycursor.execute(query)
            result_listVideo = mycursor.fetchall()

        list_video = []
        if page <= total_page:
            for item in result_listVideo:
                data = {}
                query = "SELECT * from categories_video where idCateogries=%s"
                mycursor.execute(query, (item[0],))
                result3 = mycursor.fetchall()
                number_of_rows = len(result3)
                if number_of_rows != 0:
                    data["name_categories"] = result3[0][1]
                    data["detail"] = result3[0][2]
                else:
                    data["name_categories"] = "No name categories"
                    data["detail"] = "No categories"
                data["id"] = item[4]
                data["link_video"] = item[5]
                data["age_video"] = item[6]
                data["chung_toc"] = item[9]
                data["gioi_tinh"] = item[7]
                data["id_categories"] = item[1]
                data["mau_da"] = item[8]
                data["noi_dung"] = item[2]
                data["thumbnail"] = item[9]
                list_video.append(data)
        else:
            return JSONResponse(content="exceed the number of pages!!!")

        result["list_video"] = list_video
        result["total_page"] = total_page

    except Exception as e:
        print(e)
        return f"Request failed: {e}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return result


@app.get("/lovehistory/{idlove}")
async def get_data_love_history(idlove: str):
    thong_tin = {}
    list_thong_tin = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(
            f"SELECT * from saved_sukien where id_toan_bo_su_kien={idlove}"
        )
        result2 = mycursor.fetchall()

        phantupro = mycursor.rowcount
        for i in range(0, phantupro):
            thong_tin["id"] = result2[i][0]
            thong_tin["link_nam_goc"] = result2[i][1]
            thong_tin["link_nu_goc"] = result2[i][2]
            thong_tin["link_nam_chua_swap"] = result2[i][3]
            thong_tin["link_nu_chua_swap"] = result2[i][4]
            thong_tin["link_da_swap"] = result2[i][5]
            thong_tin["real_time"] = result2[i][6]
            thong_tin["tom_luoc_text"] = result2[i][7]
            thong_tin["noi_dung_su_kien"] = result2[i][8]
            thong_tin["ten_su_kien"] = result2[i][15]
            thong_tin["so_thu_tu_su_kien"] = int(result2[i][10])
            thong_tin["id_user"] = result2[i][14]
            thong_tin["phantram_loading"] = result2[i][21]
            thong_tin["count_comment"] = int(result2[i][18])
            thong_tin["count_view"] = int(result2[i][19])
            thong_tin["ten_nam"] = result2[i][16]
            thong_tin["ten_nu"] = result2[i][17]
            thong_tin["id_template"] = int(result2[i][20])
            id_user = result2[i][14]
            mycursor.execute(f"SELECT user_name from user where id_user={id_user}")
            name = mycursor.fetchone()
            if name == None:
                name = "Anonymous people"
            else:
                name = name[0]
            thong_tin["user_name_tao_sk"] = name
            list_thong_tin.append(thong_tin)
            thong_tin = {}

        print(mycursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"sukien": list_thong_tin})


@app.get("/lovehistory/video/{page}")
async def get_data_video(page: int):
    list_toan_bo_sukien_saved = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = "SELECT id_saved, MAX(thoigian_sukien) AS max_thoigian_swap FROM saved_sukien_video GROUP BY id_saved ORDER BY max_thoigian_swap DESC"
        mycursor.execute(query)
        result = mycursor.fetchall()

        records = []
        for row in result:
            id_toan_bo_su_kien = row[0]
            records.append(id_toan_bo_su_kien)

        soPhanTuTrenMotTrang = 8
        soTrang = (len(records) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang

        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(records))
        else:
            return JSONResponse(content="exceed the number of pages!!!")

        for i in range(start, end):
            idItemPhanTu = records[i]
            Mot_LanQuerryData = []
            print("idItemPhanTu ____ " + str(idItemPhanTu))
            mycursor.execute(
                f"SELECT * from saved_sukien_video where id_saved={idItemPhanTu}"
            )
            result2 = mycursor.fetchall()
            thong_tin = {}
            phantupro = mycursor.rowcount
            for i in range(0, phantupro):
                thong_tin["id_video"] = result2[i][0]
                thong_tin["link_image"] = result2[i][2]
                thong_tin["link_vid_swap"] = result2[i][3]
                thong_tin["link_video_goc"] = result2[i][13]
                thong_tin["thoigian_swap"] = result2[i][14]
                thong_tin["ten_su_kien"] = result2[i][4]
                thong_tin["noidung_sukien"] = result2[i][5]
                thong_tin["id_video_swap"] = result2[i][6]
                thong_tin["thoigian_taosk"] = result2[i][7]
                thong_tin["id_user"] = result2[i][10]
                thong_tin["count_comment"] = int(result2[i][11])
                thong_tin["count_view"] = int(result2[i][12])
                Mot_LanQuerryData.append(thong_tin)
                thong_tin = {}

            list_toan_bo_sukien_saved.append({"sukien_video": Mot_LanQuerryData})

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_sukien_saved})


@app.get("/lovehistory/user/video/{id_user}")
async def get_data_video_user(request: Request, id_user: int, page: int):
    page = request.query_params.get("page")
    page = int(page)
    print("___ID_USEER " + str(id_user) + " TRANG " + str(page))
    list_toan_bo_sukien_saved = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = "SELECT id_saved, MAX(thoigian_sukien) AS max_thoigian_swap FROM saved_sukien_video WHERE id_user = %s GROUP BY id_saved ORDER BY max_thoigian_swap DESC"
        mycursor.execute(query, (id_user,))
        result = mycursor.fetchall()

        records = []
        for row in result:
            id_toan_bo_su_kien = row[0]
            records.append(id_toan_bo_su_kien)

        soPhanTuTrenMotTrang = 8
        soTrang = (len(records) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang

        start = 0
        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(records))
        else:
            return JSONResponse(content="exceed the number of pages!!!")
        print(start)
        print("soTrang " + str(soTrang))
        for i in range(start, end):
            idItemPhanTu = records[i]
            Mot_LanQuerryData = []

            mycursor.execute(
                f"SELECT * from saved_sukien_video where id_saved={idItemPhanTu}"
            )
            result2 = mycursor.fetchall()
            thong_tin = {}
            phantupro = mycursor.rowcount
            for i in range(0, phantupro):
                thong_tin["id_video"] = result2[i][0]
                thong_tin["link_image"] = result2[i][2]
                thong_tin["link_vid_swap"] = result2[i][3]
                thong_tin["link_video_goc"] = result2[i][13]
                thong_tin["thoigian_swap"] = result2[i][14]
                thong_tin["ten_su_kien"] = result2[i][4]
                thong_tin["noidung_sukien"] = result2[i][5]
                thong_tin["id_video_swap"] = result2[i][6]
                thong_tin["thoigian_taosk"] = result2[i][7]
                thong_tin["id_user"] = result2[i][10]
                thong_tin["count_comment"] = int(result2[i][11])
                thong_tin["count_view"] = int(result2[i][12])
                print("thongtin " + str(thong_tin))
                Mot_LanQuerryData.append(thong_tin)
                thong_tin = {}

            list_toan_bo_sukien_saved.append({"sukien_video": Mot_LanQuerryData})

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    print("list_toan_bo_sukien_saved " + str(list_toan_bo_sukien_saved))
    return JSONResponse(content={"list_sukien_video": list_toan_bo_sukien_saved})


# create comment
@app.post("/lovehistory/comment")
async def create_comment(request: Request):
    form_data = await request.form()
    noi_dung_cmt = form_data.get("noi_dung_cmt")
    device_cmt = form_data.get("device_cmt")
    id_toan_bo_su_kien = form_data.get("id_toan_bo_su_kien")
    so_thu_tu_su_kien = form_data.get("so_thu_tu_su_kien")
    ipComment = form_data.get("ipComment")
    imageattach = form_data.get("imageattach")
    id_user = form_data.get("id_user")
    id_user_comment = form_data.get("id_user_cmt")
    location = form_data.get("location")
    link_imagesk = form_data.get("link_imagesk")
    if imageattach is None:
        imageattach = ""
    if id_user:
        id_user = id_user
    else:
        id_user = 0

    thong_tin = {}
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        # Thực hiện truy vấn để chèn comment vào cơ sở dữ liệu
        mycursor.execute(f"SELECT MAX(id_Comment) from comment")

        ketqua = mycursor.fetchall()

        if ketqua:
            id_comment = ketqua[0][0] + 1
        else:
            id_comment = 1

        dt_utc = datetime.now()
        tz = pytz.timezone("Asia/Bangkok")
        dt_local = dt_utc.astimezone(tz)
        datetimenow = dt_local.strftime("%Y-%m-%d %H:%M:%S")
        mycursor.execute(f"SELECT * from user where id_user = {id_user}")
        ketqua_user = mycursor.fetchall()

        mycursor.execute(
            f"SELECT * FROM saved_sukien where id_toan_bo_su_kien={id_toan_bo_su_kien}"
        )
        saved_sukien = mycursor.fetchall()

        thong_tin["device_cmt"] = device_cmt
        thong_tin["dia_chi_ip"] = ipComment
        thong_tin["id_comment"] = id_comment
        thong_tin["id_toan_bo_su_kien"] = id_toan_bo_su_kien
        thong_tin["so_thu_tu_su_kien"] = int(so_thu_tu_su_kien)
        thong_tin["imageattach"] = imageattach
        thong_tin["link_nam_goc"] = saved_sukien[0][1]
        thong_tin["link_nu_goc"] = saved_sukien[0][2]
        thong_tin["noi_dung_cmt"] = noi_dung_cmt
        thong_tin["thoi_gian_release"] = datetimenow
        thong_tin["location"] = location
        thong_tin["user_name"] = "Guest"
        thong_tin["avatar_user"] = None
        thong_tin["id_user"] = int(id_user)
        if ketqua_user:
            thong_tin["user_name"] = ketqua_user[0][2]
            thong_tin["avatar_user"] = ketqua_user[0][1]
        # Trả về thông báo thành công nếu comment được chèn thành công

        lenhquery = f"INSERT INTO comment(id_Comment,noi_dung_Comment,IP_Comment,device_Comment,id_toan_bo_su_kien,imageattach, thoi_gian_release, id_user, user_name, avatar_user, so_thu_tu_su_kien, location) VALUES ( {id_comment} ,%s,%s,%s, {id_toan_bo_su_kien} ,%s , %s, {id_user}, %s, %s,{so_thu_tu_su_kien}, %s)"
        val = (
            noi_dung_cmt,
            ipComment,
            device_cmt,
            imageattach,
            datetimenow,
            thong_tin["user_name"],
            thong_tin["avatar_user"],
            thong_tin["location"],
        )
        mycursor.execute(lenhquery, val)
        connection.commit()

        mycursor.execute(
            "SELECT COUNT(id_Comment) FROM comment WHERE id_toan_bo_su_kien = {} and so_thu_tu_su_kien = {}".format(
                id_toan_bo_su_kien, so_thu_tu_su_kien
            )
        )
        # lấy kết quả
        results1 = mycursor.fetchone()[0]
        update_query = "UPDATE saved_sukien SET count_comment = {} WHERE id_toan_bo_su_kien = {} and so_thu_tu_su_kien = {}".format(
            results1, id_toan_bo_su_kien, so_thu_tu_su_kien
        )
        mycursor.execute(update_query)
        connection.commit()

        # insert to notifidb
        mycursor.execute(f"SELECT MAX(id) from saved_notification")

        id_notifi = mycursor.fetchall()
        id_notif = 0
        if id_notifi[0][0] is not None:
            id_notif = id_notifi[0][0] + 1
        else:
            id_notif = id_notif + 1
        mycursor.execute(f"SELECT * from user where id_user = {id_user}")

        profile_user = mycursor.fetchall()
        if profile_user:
            user_name = profile_user[0][2]
            link_avt = profile_user[0][1]
        else:
            user_name = "Guest"
            link_avt = None
        status = "chua xem"

        notifi_query = f"INSERT INTO saved_notification(id,id_user,id_toan_bo_su_kien,so_thu_tu_su_kien,user_name,link_avatar, link_imagesk, status, thoigian) VALUES ( {id_notif} ,{id_user_comment},%s,{so_thu_tu_su_kien},%s, %s, %s, %s, %s)"
        val_notif = (
            id_toan_bo_su_kien,
            user_name,
            link_avt,
            link_imagesk,
            status,
            datetimenow,
        )
        mycursor.execute(notifi_query, val_notif)
        connection.commit()

        link = (
            f"https://photo.gachmen.org/detail/{id_toan_bo_su_kien}/{so_thu_tu_su_kien}"
        )
        message = f"User {user_name} comment on your post, click {link} to view detail!"

        await send_email_to_notifi(ketqua_user[0][6], message)  # send email by email

        return JSONResponse(content={"comment": thong_tin})
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        return {"error": f"Failed to connect to MySQL database: {error}"}
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


@app.get("/notification/{id_user}")
async def show_notifi(id_user: int):
    print("hello")
    thong_tin = {}
    list_thong_tin = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM saved_notification WHERE id_user = {id_user} AND status != 'da vao link'"
        )
        result2 = cursor.fetchall()

        cursor.execute(
            f"SELECT COUNT(*) AS count FROM saved_notification WHERE id_user = {id_user} AND status != 'da vao link'"
        )
        result_toan_bo_su_kien = cursor.fetchall()
        print(result_toan_bo_su_kien)

        for i in range(result_toan_bo_su_kien[0][0]):
            thong_tin["id_notifi"] = result2[i][0]
            thong_tin["id_user"] = result2[i][1]
            thong_tin["id_toan_bo_su_kien"] = result2[i][2]
            thong_tin["so_thu_tu_su_kien"] = result2[i][3]
            thong_tin["user_name"] = result2[i][4]
            thong_tin["link_avatar"] = result2[i][5]
            thong_tin["link_imagesk"] = result2[i][6]
            thong_tin["status"] = result2[i][7]
            thong_tin["thoigian"] = result2[i][8]
            thong_tin["num_notif"] = result_toan_bo_su_kien[0][0]
            list_thong_tin.append(thong_tin)
            thong_tin = {}

        print(cursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return {"notifi": list_thong_tin}


@app.patch("/notification/update/{id_user}")
async def update_notifi(id_user: int):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            update_query = f"UPDATE saved_notification SET status = 'da xem' WHERE id_user= {id_user}"
            cursor.execute(update_query)
            connection.commit()
            cursor.close()
            return {"message": "notification updated successfully"}
    except Exception as e:
        return {"error": str(e)}


@app.delete("/notification/delete/{id_user}/{id_notifi}")
async def delete_notifi(id_user: int, id_notifi: int):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            update_query = f"DELETE FROM saved_notification WHERE id_user= {id_user} and id = {id_notifi}"
            cursor.execute(update_query)
            connection.commit()
            cursor.close()
            return {"message": "notification delete successfully"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/countview")
async def count_view(
    id_toan_bo_su_kien: str = Form(...), so_thu_tu_su_kien: str = Form(...)
):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT count_view from saved_sukien where id_toan_bo_su_kien = {id_toan_bo_su_kien} and so_thu_tu_su_kien = {so_thu_tu_su_kien}"
    )
    result = cursor.fetchone()
    result = int(result[0])
    print(result)
    result = result + 1

    cursor.execute(
        f"UPDATE saved_sukien SET count_view = {result} where id_toan_bo_su_kien = {id_toan_bo_su_kien} and so_thu_tu_su_kien = {so_thu_tu_su_kien}"
    )

    connection.commit()
    return {"count_view": result}


@app.post("/saveimage/{id_user}", dependencies=[Depends(validate_token)])
async def save_image(id_user: int, request: Request):
    print("hello")
    results1 = []
    list_img = []
    image_urls = await request.json()
    list_image = []

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor(buffered=True)
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor(buffered=True)

        json_str = json.dumps(image_urls)
        json_obj = json.loads(json_str)
        for key in json_obj:
            mycursor.execute("SELECT MAX(id) FROM saved_image")
            max_id_user = mycursor.fetchone()[0]
            if max_id_user:
                id_img = max_id_user + 1
            else:
                id_img = 1
            dt_utc = datetime.now()
            tz = pytz.timezone("Asia/Bangkok")
            dt_local = dt_utc.astimezone(tz)
            date = dt_local.strftime("%Y-%m-%d, %H:%M:%S")
            # Thêm một dict mới vào list_image
            image_dict = {"id": id_img, "image_url": json_obj[key], "date": date}
            list_image.append(image_dict)

        for image in list_image:
            mycursor.execute(
                "INSERT INTO saved_image (id, id_user ,link_image, thoigian) VALUES ( %s , %s , %s, %s)",
                (image["id"], id_user, image["image_url"], image["date"]),
            )
            connection.commit()

        mycursor.execute(f"SELECT * FROM saved_image WHERE id_user={id_user}")
        # lấy kết quả
        results1 = mycursor.fetchall()
        phantupro = mycursor.rowcount

        for i in range(0, phantupro):
            list_img.append(results1[i][2])

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        return JSONResponse(
            content={"error": "Failed to connect to MySQL database"}, status_code=500
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return {"list_img": list_img}


@app.post("/changeavatar/{id_user}", dependencies=[Depends(validate_token)])
async def change_avatar(request: Request, id_user: int):
    form_data = await request.form()
    link_img = form_data.get("link_img")
    check_img = form_data.get("check_img")

    if not link_img:
        return "Link img can not None!"
    if not check_img:
        return "Check img can not None!"
    if link_img.startswith("/var/www"):
        link_img = link_img.replace(
            "/var/www/build_futurelove/", "https://photo.gachmen.org/"
        )
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    mycursor = connection.cursor()
    update_query = "UPDATE user SET link_avatar = %s WHERE id_user = %s"
    update_values = (link_img, id_user)
    cursor.execute(update_query, update_values)
    connection.commit()

    if check_img == "upload":
        print("heloooo")
        mycursor.execute("SELECT MAX(id) FROM saved_image")
        max_id_user = mycursor.fetchone()[0]
        id_img = max_id_user + 1
        dt_utc = datetime.now()
        tz = pytz.timezone("Asia/Bangkok")
        dt_local = dt_utc.astimezone(tz)
        date = dt_local.strftime("%Y-%m-%d %H:%M:%S")
        mycursor.execute(
            "INSERT INTO saved_image (id, id_user, link_image, thoigian) VALUES (%s, %s, %s, %s)",
            (id_img, id_user, link_img, date),
        )
        connection.commit()

    return {"link_img": link_img}


@app.get("/search")
def search_word(request: Request):
    search_word = request.query_params.get("word")
    list_toan_bo_sukien_saved = []
    id_sukien = []
    stt_sukien = []
    thoi_gian_sk = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        cursor = connection.cursor()

        sql_query1 = f"SELECT * FROM comment WHERE UPPER(noi_dung_Comment) LIKE UPPER('%{search_word}%')"
        cursor.execute(sql_query1)
        search_results = cursor.fetchall()

        sql_query2 = f"SELECT * FROM add_sukien WHERE UPPER(noidung_su_kien) LIKE UPPER('%{search_word}%')"
        cursor.execute(sql_query2)
        search_results2 = cursor.fetchall()

        for row in search_results:
            id_sukien.append(row[4])
            stt_sukien.append(row[10])
            thoi_gian_sk.append(row[6])
        for row in search_results2:
            id_sukien.append(row[2])
            stt_sukien.append(row[13])
            thoi_gian_sk.append(row[12])

        combined_list = list(set(zip(id_sukien, stt_sukien, thoi_gian_sk)))

        # Sắp xếp danh sách theo thời gian
        sorted_list = sorted(
            combined_list,
            key=lambda x: datetime.strptime(x[2], "%Y-%m-%d %H:%M:%S"),
            reverse=True,
        )

        latest_dict = {}

        for item in sorted_list:
            first_two = item[:2]
            if first_two not in latest_dict:
                latest_dict[first_two] = item
            else:
                current_time = item[2]
                existing_time = latest_dict[first_two][2]
                if current_time > existing_time:
                    latest_dict[first_two] = item

        filtered_list = list(latest_dict.values())

        for i in range(len(filtered_list)):
            Mot_LanQuerryData = []

            cursor.execute(
                f"SELECT * from saved_sukien where id_toan_bo_su_kien = {filtered_list[i][0]} and so_thu_tu_su_kien = {filtered_list[i][1]}"
            )
            result2 = cursor.fetchall()
            thong_tin = {}
            phantupro = cursor.rowcount
            for i in range(0, phantupro):
                thong_tin["id"] = result2[i][0]
                thong_tin["link_nam_goc"] = result2[i][1]
                thong_tin["link_nu_goc"] = result2[i][2]
                thong_tin["link_nam_chua_swap"] = result2[i][3]
                thong_tin["link_nu_chua_swap"] = result2[i][4]
                thong_tin["link_da_swap"] = result2[i][5]
                thong_tin["real_time"] = result2[i][6]
                thong_tin["ten_su_kien"] = result2[i][15]
                thong_tin["noi_dung_su_kien"] = result2[i][8]
                thong_tin["id_toan_bo_su_kien"] = result2[i][9]
                thong_tin["so_thu_tu_su_kien"] = result2[i][10]
                thong_tin["id_user"] = result2[i][14]
                thong_tin["phantram_loading"] = result2[i][21]
                thong_tin["count_comment"] = result2[i][18]
                thong_tin["count_view"] = result2[i][19]
                thong_tin["ten_nam"] = result2[i][16]
                thong_tin["ten_nu"] = result2[i][17]
                thong_tin["id_template"] = result2[i][20]
                Mot_LanQuerryData.append(thong_tin)

                thong_tin = {}
            list_toan_bo_sukien_saved.append({"sukien": Mot_LanQuerryData})

        print(cursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return {"list_sukien": list_toan_bo_sukien_saved}


@app.get("/lovehistory/comment/{so_thu_tu_su_kien}")
async def get_comment_history(request: Request, so_thu_tu_su_kien: int, id_user: int):
    thong_tin = {}
    list_thong_tin = []
    id_toan_bo_su_kien = request.query_params.get("id_toan_bo_su_kien")
    id_user = request.query_params.get("id_user")

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM comment WHERE id_toan_bo_su_kien = {id_toan_bo_su_kien} AND so_thu_tu_su_kien = {so_thu_tu_su_kien}"
        )
        result2 = cursor.fetchall()
        cursor.execute(
            f"SELECT id_blocked_user FROM block_user WHERE id_user_report = {id_user}"
        )
        id_block_user = cursor.fetchall()
        # Lấy giá trị của phần tử thứ 7 trong mỗi item trong list2
        values_to_check = [item[0] for item in id_block_user]
        # Tạo danh sách mới chỉ chứa các phần tử không trùng khớp
        result2 = [item for item in result2 if item[7] not in values_to_check]
        # print(result_toan_bo_su_kien)
        for i in range(len(result2)):
            thong_tin["id_toan_bo_su_kien"] = result2[i][4]
            thong_tin["noi_dung_cmt"] = result2[i][1]
            thong_tin["dia_chi_ip"] = result2[i][2]
            thong_tin["device_cmt"] = result2[i][3]
            thong_tin["id_comment"] = int(result2[i][0])
            thong_tin["imageattach"] = result2[i][5]
            thong_tin["thoi_gian_release"] = result2[i][6]
            thong_tin["user_name"] = result2[i][8]
            thong_tin["id_user"] = int(result2[i][7])
            thong_tin["avatar_user"] = result2[i][9]
            thong_tin["so_thu_tu_su_kien"] = so_thu_tu_su_kien
            thong_tin["location"] = result2[i][11]
            cursor.execute(
                f"SELECT * FROM saved_sukien WHERE id_toan_bo_su_kien = {result2[i][4]}"
            )
            saved_sukien = cursor.fetchall()
            thong_tin["link_nam_goc"] = saved_sukien[0][1]
            thong_tin["link_nu_goc"] = saved_sukien[0][2]
            list_thong_tin.append(thong_tin)
            thong_tin = {}

        print(cursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return {"comment": list_thong_tin}


@app.get("/lovehistory/pageComment/{page}")
def get_page_comment_history(request: Request, page: int, id_user: int):
    thong_tin = {}
    id_user = request.query_params.get("id_user")
    if id_user:
        id_user = id_user
    else:
        id_user = 0
    Mot_LanQuerryData = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()

        cursor.execute(
            f"SELECT id_Comment, id_user FROM comment ORDER BY thoi_gian_release DESC"
        )
        id_user_comment = cursor.fetchall()

        cursor.execute(
            f"SELECT id_blocked_user FROM block_user WHERE id_user_report = {id_user}"
        )
        id_block_user = cursor.fetchall()

        values_to_check = [item[0] for item in id_block_user]
        # Tạo danh sách mới chỉ chứa các phần tử không trùng khớp
        result = [item for item in id_user_comment if item[1] not in values_to_check]

        # query = f"SELECT id_Comment FROM comment ORDER BY thoi_gian_release DESC"
        # mycursor.execute(query)
        # result = mycursor.fetchall()
        records = []
        for row in result:
            id_toan_bo_su_kien = row[0]
            records.append(id_toan_bo_su_kien)
        soPhanTuTrenMotTrang = 10
        soTrang = (len(records) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang
        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(records))
        else:
            return {"message": "exceed the number of pages"}
        print("hello")
        for i in range(start, end):
            idItemPhanTu = records[i]

            mycursor.execute(f"SELECT * from comment where id_Comment={idItemPhanTu}")
            result2 = mycursor.fetchall()
            thong_tin = {}
            phantupro = mycursor.rowcount
            for i in range(0, phantupro):
                thong_tin["id_toan_bo_su_kien"] = result2[i][4]
                thong_tin["so_thu_tu_su_kien"] = (
                    0 if result2[i][10] is None else int(result2[i][10])
                )
                thong_tin["noi_dung_cmt"] = result2[i][1]
                thong_tin["dia_chi_ip"] = result2[i][2]
                thong_tin["device_cmt"] = result2[i][3]
                thong_tin["id_comment"] = int(result2[i][0])
                thong_tin["imageattach"] = result2[i][5]
                thong_tin["thoi_gian_release"] = result2[i][6]
                thong_tin["user_name"] = result2[i][8]
                thong_tin["id_user"] = result2[i][7]
                thong_tin["avatar_user"] = result2[i][9]
                thong_tin["location"] = result2[i][11]
                thong_tin["link_nam_goc"] = "0"
                thong_tin["link_nu_goc"] = "0"

                mycursor.execute(
                    f"SELECT * from saved_sukien where id_toan_bo_su_kien={result2[i][4]}"
                )
                saved_sukien = mycursor.fetchall()

                if saved_sukien:
                    thong_tin["link_nam_goc"] = saved_sukien[0][1]
                    thong_tin["link_nu_goc"] = saved_sukien[0][2]

            Mot_LanQuerryData.append(thong_tin)
            thong_tin = {}

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"comment": Mot_LanQuerryData})


# tim theo id user
@app.get("/lovehistory/user/{id_user}")
async def get_data_love_history_user(request: Request, id_user: int):
    info = {}
    list_event = []

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = f"""
                SELECT id_toan_bo_su_kien, MAX(thoigian_swap) AS max_thoigian_swap 
                FROM saved_sukien WHERE id_user = {id_user} 
                GROUP BY id_toan_bo_su_kien 
                ORDER BY max_thoigian_swap DESC
                """
        mycursor.execute(query)
        result = mycursor.fetchall()

        query = f"""
                SELECT COUNT(DISTINCT id_toan_bo_su_kien) 
                FROM saved_sukien 
                WHERE id_user = {id_user};
                """
        mycursor.execute(query)
        data_length = mycursor.fetchall()[0][0]
        for index in range(0, data_length):
            idItem = result[index][0]
            data = []

            mycursor.execute(
                f"SELECT * from saved_sukien where id_toan_bo_su_kien={idItem}"
            )
            result2 = mycursor.fetchall()
            limit = mycursor.rowcount
            for i in range(0, limit):
                info = {}
                info["id"] = result2[i][0]
                info["link_nam_goc"] = result2[i][1]
                info["link_nu_goc"] = result2[i][2]
                info["link_nam_chua_swap"] = result2[i][3]
                info["link_nu_chua_swap"] = result2[i][4]
                info["link_da_swap"] = result2[i][5]
                info["real_time"] = result2[i][6]
                info["ten_su_kien"] = result2[i][15]
                info["noi_dung_su_kien"] = result2[i][8]
                info["id_toan_bo_su_kien"] = result2[i][9]
                info["so_thu_tu_su_kien"] = int(result2[i][10])
                info["id_user"] = result2[i][14]
                info["phantram_loading"] = result2[i][21]
                info["count_comment"] = int(result2[i][18])
                info["count_view"] = int(result2[i][19])
                info["ten_nam"] = result2[i][16]
                info["ten_nu"] = result2[i][17]
                info["id_template"] = int(result2[i][20])
                data.append(info)

            list_event.append({"sukien": data})

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien": list_event})


@app.get("/lovehistory/comment/user/{id_user}")
def get_Comment_History_User(id_user: int):
    thong_tin = {}
    list_thong_tin = []

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM comment where id_user = {id_user}")
        result2 = cursor.fetchall()

        cursor.execute(f"SELECT COUNT(*) FROM comment where id_user = {id_user}")
        result_toan_bo_comment = cursor.fetchall()
        print(result_toan_bo_comment[0][0])

        for i in range(0, result_toan_bo_comment[0][0]):
            thong_tin["id_toan_bo_su_kien"] = result2[i][4]
            thong_tin["noi_dung_cmt"] = result2[i][1]
            thong_tin["dia_chi_ip"] = result2[i][2]
            thong_tin["device_cmt"] = result2[i][3]
            thong_tin["id_comment"] = int(result2[i][0])
            thong_tin["imageattach"] = result2[i][5]
            thong_tin["thoi_gian_release"] = result2[i][6]
            thong_tin["user_name"] = result2[0][8]
            thong_tin["id_user"] = int(result2[0][7])
            thong_tin["avatar_user"] = result2[i][9]
            thong_tin["so_thu_tu_su_kien"] = result2[i][10]
            thong_tin["location"] = result2[i][11]
            thong_tin["link_nam_goc"] = "0"
            thong_tin["link_nu_goc"] = "0"

            cursor.execute(
                f"SELECT * from saved_sukien where id_toan_bo_su_kien = {result2[i][4]}"
            )
            saved_sukien = cursor.fetchall()

            if saved_sukien:
                thong_tin["link_nam_goc"] = saved_sukien[0][1]
                thong_tin["link_nu_goc"] = saved_sukien[0][2]
                cursor.execute(
                    f"SELECT * FROM user where id_user = {saved_sukien[0][14]}"
                )
                result3 = cursor.fetchall()
                thong_tin["user_taosk"] = result3[0][2]

            list_thong_tin.append(thong_tin)
            thong_tin = {}

        print(cursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"comment_user": list_thong_tin})


@app.get("/lovehistory/page/{page}")
async def get_page_love_history(request: Request, page: int, id_user: int):
    list_toan_bo_sukien_saved = []
    id_user = request.query_params.get("id_user")
    if id_user:
        id_user = id_user
    else:
        id_user = 0

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = "SELECT id_toan_bo_su_kien, MAX(thoigian_swap) AS max_thoigian_swap, id_user FROM saved_sukien GROUP BY id_user, id_toan_bo_su_kien ORDER BY max_thoigian_swap DESC"
        mycursor.execute(query)
        result = mycursor.fetchall()

        cursor.execute(
            f"SELECT id_blocked_user FROM block_user WHERE id_user_report = {id_user}"
        )
        id_block_user = cursor.fetchall()
        print(id_block_user)
        values_to_check = [item[0] for item in id_block_user]
        # Tạo danh sách mới chỉ chứa các phần tử không trùng khớp
        result = [item for item in result if item[2] not in values_to_check]

        records = []
        for row in result:
            id_toan_bo_su_kien = row[0]
            records.append(id_toan_bo_su_kien)

        soPhanTuTrenMotTrang = 8
        soTrang = (len(records) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang

        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(records))
        else:
            return JSONResponse(content="exceed the number of pages!!!")
        print("hello")
        for i in range(start, end):
            idItemPhanTu = records[i]
            Mot_LanQuerryData = []

            mycursor.execute(
                f"SELECT * from saved_sukien where id_toan_bo_su_kien={idItemPhanTu}"
            )
            result2 = mycursor.fetchall()
            thong_tin = {}
            phantupro = mycursor.rowcount
            for i in range(0, phantupro):
                thong_tin["id"] = result2[i][0]
                if result2[i][1].find("https://futurelove.online") > 0:
                    thong_tin["link_nam_goc"] = result2[i][1].replace(
                        "https://futurelove.online", "https://photo.gachmen.org"
                    )
                else:
                    thong_tin["link_nam_goc"] = result2[i][1]
                if result2[i][2].find("https://futurelove.online") > 0:
                    thong_tin["link_nu_goc"] = result2[i][2].replace(
                        "https://futurelove.online", "https://photo.gachmen.org"
                    )
                else:
                    thong_tin["link_nu_goc"] = result2[i][2]
                if result2[i][3].find("https://futurelove.online") > 0:
                    thong_tin["link_nam_chua_swap"] = result2[i][3].replace(
                        "https://futurelove.online", "https://photo.gachmen.org"
                    )
                else:
                    thong_tin["link_nam_chua_swap"] = result2[i][3]
                if result2[i][4].find("https://futurelove.online") > 0:
                    thong_tin["link_nu_chua_swap"] = result2[i][4].replace(
                        "https://futurelove.online", "https://photo.gachmen.org"
                    )
                else:
                    thong_tin["link_nu_chua_swap"] = result2[i][4]
                if result2[i][5].find("https://futurelove.online") > 0:
                    thong_tin["link_da_swap"] = result2[i][5].replace(
                        "https://futurelove.online", "https://photo.gachmen.org"
                    )
                else:
                    thong_tin["link_da_swap"] = result2[i][5]
                thong_tin["real_time"] = result2[i][6]
                thong_tin["ten_su_kien"] = result2[i][15]
                thong_tin["noi_dung_su_kien"] = result2[i][8]
                thong_tin["id_toan_bo_su_kien"] = result2[i][9]
                thong_tin["so_thu_tu_su_kien"] = int(result2[i][10])
                thong_tin["id_user"] = result2[i][14]
                thong_tin["phantram_loading"] = result2[i][21]
                thong_tin["count_comment"] = int(result2[i][18])
                thong_tin["count_view"] = int(result2[i][19])
                thong_tin["ten_nam"] = result2[i][16]
                thong_tin["ten_nu"] = result2[i][17]
                thong_tin["id_template"] = int(result2[i][20])
                Mot_LanQuerryData.append(thong_tin)
                thong_tin = {}

            list_toan_bo_sukien_saved.append({"sukien": Mot_LanQuerryData})

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien": list_toan_bo_sukien_saved})


@app.post(
    "/lovehistory/add/{id_toan_bo_su_kien}", dependencies=[Depends(validate_token)]
)
async def add_Them_Su_Kien_Tinh_Yeu(
    id_toan_bo_su_kien: int,
    request: Request,
    ten_sukien: str = Form(...),
    noidung_su_kien: str = Form(...),
    ten_nam: str = Form(...),
    ten_nu: str = Form(...),
    device_them_su_kien: str = Form(...),
    ip_them_su_kien: str = Form(...),
    link_img: str = Form(...),
    link_video: str = Form(...),
    id_user: int = Form(...),
    id_template: int = Form(...),
):
    link1 = request.headers.get("Link1")
    link2 = request.headers.get("Link2")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        cursor = connection.cursor()

        cursor.execute(f"SELECT MAX(id_add) from add_sukien")
        max_sql_id_saved = cursor.fetchall()
        print("idmas", max_sql_id_saved)
        if max_sql_id_saved[0][0] is not None:
            id_add_max = max_sql_id_saved[0][0] + 1
        else:
            id_add_max = 1
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            f"SELECT MAX(so_thu_tu_su_kien) from saved_sukien where id_toan_bo_su_kien={id_toan_bo_su_kien}"
        )
        max_stt_skien = cursor.fetchall()
        so_thu_tu_sk = max_stt_skien[0][0] + 1

        count_comment = 0
        count_view = 0
        status = "Ok!"
        lenhquery = f"INSERT INTO add_sukien(id_add,id_user,id_toan_bo_su_kien,ten_sukien,noidung_su_kien ,ten_nam, ten_nu, device_them_su_kien, ip_them_su_kien, link_img, link_video, id_template, thoigian_themsk, so_thu_tu_su_kien, count_comment, count_view, status) VALUES ( {id_add_max}, {id_user},{id_toan_bo_su_kien},%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, {so_thu_tu_sk},{count_comment}, {count_view}, %s )"
        val = (
            ten_sukien,
            noidung_su_kien,
            ten_nam,
            ten_nu,
            device_them_su_kien,
            ip_them_su_kien,
            link_img,
            link_video,
            id_template,
            date,
            status,
        )
        cursor.execute(lenhquery, val)

        connection.commit()

        link_nam_chua_swap = "abc"
        link_nu_chua_swap = "abc"

        if link_img is None:
            link_swap = link_video
        else:
            link_swap = link_img

        print(link_swap)
        phantram_loading = 0

        sql2 = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, tomLuocText, ten_nam, ten_nu, count_comment, count_view, id_template, phantram_loading) VALUES ( {id_toan_bo_su_kien}  ,%s  , %s  ,%s, %s, %s, %s, %s, %s, {id_toan_bo_su_kien},{so_thu_tu_sk}, %s, %s, %s, {id_user}, %s, %s, %s, {count_comment}, {count_view}, {id_template}, {phantram_loading})"
        val2 = (
            link1,
            link2,
            link_nam_chua_swap,
            link_nu_chua_swap,
            link_swap,
            date,
            ten_sukien,
            noidung_su_kien,
            date,
            device_them_su_kien,
            ip_them_su_kien,
            noidung_su_kien,
            ten_nam,
            ten_nu,
        )
        cursor.execute(sql2, val2)

        connection.commit()

        print(cursor.rowcount, "record inserted.")
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        return {"ketqua": "Failed to connect to MySQL database: " + str(error)}
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return {"message": "successfully added event"}


@app.get("/profile/{id_user}")
async def info_user(id_user: str):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    mycursor = connection.cursor()

    mycursor.execute(f"SELECT * FROM user where id_user='{id_user}'")
    ketquaEmail = mycursor.fetchall()
    phantupro = mycursor.rowcount

    mycursor.execute(
        "SELECT COUNT(id_Comment) FROM comment WHERE id_user = {}".format(id_user)
    )
    results = mycursor.fetchone()[0]
    update_query = "UPDATE user SET count_comment = {} WHERE id_user = {}".format(
        results, id_user
    )
    cursor.execute(update_query)
    connection.commit()

    mycursor.execute(
        "SELECT COUNT(DISTINCT id_toan_bo_su_kien) FROM saved_sukien WHERE id_user = {}".format(
            id_user
        )
    )
    count_sk = mycursor.fetchone()[0]
    update_query = "UPDATE user SET count_sukien = {} WHERE id_user = {}".format(
        count_sk, id_user
    )
    cursor.execute(update_query)
    connection.commit()

    thong_tin = {}
    if phantupro == 0:
        return JSONResponse(content={"ketqua": "This user is not available"})
    for i in range(0, phantupro):
        thong_tin["id_user"] = int(ketquaEmail[i][0])
        thong_tin["link_avatar"] = ketquaEmail[i][1]
        thong_tin["user_name"] = ketquaEmail[i][2]
        thong_tin["ip_register"] = ketquaEmail[i][3]
        thong_tin["device_register"] = ketquaEmail[i][4]
        thong_tin["email"] = ketquaEmail[i][6]
        thong_tin["count_sukien"] = int(ketquaEmail[i][7])
        thong_tin["count_comment"] = int(ketquaEmail[i][8])
        thong_tin["count_view"] = int(ketquaEmail[i][9])
        # thong_tin["cover_pic"] = ketquaEmail[i][10]

    return JSONResponse(content=thong_tin)


@app.get("/profile/user/{name}")
async def info(name: str):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    mycursor = connection.cursor()

    mycursor.execute(f"SELECT * FROM user where user_name LIKE '%{name}%'")
    ketquaEmail = mycursor.fetchall()
    phantupro = mycursor.rowcount
    if phantupro == 0:
        return JSONResponse(content={"ketqua": "khong co user nay"})
    for i in range(0, phantupro):
        mycursor.execute(
            "SELECT COUNT(id_Comment) FROM comment WHERE id_user = {}".format(
                ketquaEmail[i][0]
            )
        )
        results = mycursor.fetchone()[0]
        update_query = "UPDATE user SET count_comment = {} WHERE id_user = {}".format(
            results, ketquaEmail[i][0]
        )
        cursor.execute(update_query)
        connection.commit()

        mycursor.execute(
            "SELECT COUNT(DISTINCT id_toan_bo_su_kien) FROM saved_sukien WHERE id_user = {}".format(
                ketquaEmail[i][0]
            )
        )
        count_sk = mycursor.fetchone()[0]
        update_query = "UPDATE user SET count_sukien = {} WHERE id_user = {}".format(
            count_sk, ketquaEmail[i][0]
        )
        cursor.execute(update_query)
        connection.commit()

    list_thongtin = []
    for i in range(0, phantupro):
        thong_tin = {}
        thong_tin["id_user"] = int(ketquaEmail[i][0])
        thong_tin["link_avatar"] = ketquaEmail[i][1]
        thong_tin["user_name"] = ketquaEmail[i][2]
        thong_tin["ip_register"] = ketquaEmail[i][3]
        thong_tin["device_register"] = ketquaEmail[i][4]
        thong_tin["email"] = ketquaEmail[i][6]
        thong_tin["count_sukien"] = int(ketquaEmail[i][7])
        thong_tin["count_comment"] = int(ketquaEmail[i][8])
        thong_tin["count_view"] = int(ketquaEmail[i][9])
        # thong_tin["cover_pic"] = ketquaEmail[i][10]
        list_thongtin.append(thong_tin)
    return JSONResponse(content=list_thongtin)


@app.post("/register/user")
async def register_user(request: Request):
    form_data = await request.form()
    user_name = form_data.get("user_name")
    password = form_data.get("password")
    email = form_data.get("email")
    ip_register = form_data.get("ip_register")
    device_register = form_data.get("device_register")
    link_avatar = form_data.get("link_avatar")
    if link_avatar.startswith("/var/www/"):
        link_avatar = link_avatar.replace(
            "/var/www/build_futurelove/", "https://photo.gachmen.org/"
        )
    # print("______USERNAME: " + user_name, password)
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    match = re.match(pattern, password)
    if not user_name or not password or not email:
        return JSONResponse(content={"message": "Fields cannot be left blank."})

    if len(password) < 6:
        return JSONResponse(
            content={"message": "Password must have at least 6 characters."}
        )

    # if bool(match) == False:
    #     return JSONResponse(content={
    #         "message": "Password must contain at least one uppercase letter, one lowercase letter, number or special character."})

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.[\w-]+$", email):
        return JSONResponse(content={"message": "Email invalidate"})

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email = %s", [email])
    account = cursor.fetchone()
    if account:
        return JSONResponse(content={"message": "Account already exists!"})
    else:
        data = {
            "email": email,
            "password": password,
            "username": user_name,
            "linkavt": link_avatar,
            "ip": ip_register,
            "device": device_register,
        }
        #  "linkavatar": linkavatar, "ipregister": ipregister, "device": device
        token = jwt.encode(data, secret_key, algorithm="HS256")
        await save_user_to_mysql(
            user_name,
            password,
            email,
            link_avatar,
            ip_register,
            device_register,
            "email",
        )
        link = request.url_for("register_confirm", token=token)
        await send_mail_to_email(email, link, user_name, password)
        return JSONResponse(
            content={
                "message": "Successfully registered",
                "account": {"email": email},
            }
        )
        # link = request.url_for("register_confirm", token=token)
        # await send_mail_to_email(
        #     email, link, user_name, device_register
        # )  # send email by email
        # return JSONResponse(
        #     content={
        #         "message": "Please check your email or spam",
        #         "account": {"email": email},
        #     }
        # )


@router.get("/register_confirm/{token}")
async def register_confirm(token: str):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        # print(decoded_token)
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        mycursor = connection.cursor()
        emailCheck = decoded_token["email"]
        # print(emailCheck)
        mycursor.execute(f"SELECT * FROM user where email='{emailCheck}'")
        ketqua = mycursor.fetchall()
        # print("_____" + str(mycursor))
        # print("___SONPRO___" + str(ketqua))
        num_rows = mycursor.rowcount
        # print(str(num_rows))
        if num_rows > 0:
            return JSONResponse(
                content={
                    "message": "email register exist, please register another email"
                }
            )
        await save_user_to_mysql(
            decoded_token["username"],
            decoded_token["password"],
            decoded_token["email"],
            decoded_token["linkavt"],
            decoded_token["ip"],
            decoded_token["device"],
            "email",
        )

        return JSONResponse(content={"message": "Confirm successful registration"})

    except jwt.exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid token"})


app.include_router(router)


@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    user_name = form_data.get("email_or_username")
    password = form_data.get("password")
    print("______________user_name______", str(user_name))
    print("______________password______", str(password))

    if not user_name or not password:
        return JSONResponse(
            content={
                "message": "Fields email_or_username and password cannot be left blank."
            }
        )

    thong_tin = {}
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor(buffered=True)
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor(buffered=True)
            query = "SELECT * FROM user WHERE user_name = %s OR email = %s"
            values = (user_name, user_name)
            cursor.execute(query, values)
            user = cursor.fetchall()
            print("user_name___" + str(user_name) + "____email___" + str(password))
            print(
                "____@@@@@@@____" + str(user) + "__count__" + str(len(user)) + "+++___"
            )
            if len(user) == 0:
                thong_tin["id_user"] = ""
                thong_tin["link_avatar"] = ""
                thong_tin["user_name"] = ""
                thong_tin["ip_register"] = ""
                thong_tin["device_register"] = ""
                thong_tin["email"] = ""
                thong_tin["count_sukien"] = ""
                thong_tin["count_comment"] = ""
                thong_tin["count_view"] = ""
                thong_tin["message"] = (
                    "Account Not Found - Please Recheck Account " + str(user_name)
                )
                thong_tin["status"] = 300
                return thong_tin
            if user is not None:
                if user[0][5] == password:
                    thong_tin["id_user"] = user[0][0]
                    thong_tin["link_avatar"] = user[0][1]
                    thong_tin["user_name"] = user[0][2]
                    thong_tin["ip_register"] = user[0][3]
                    thong_tin["device_register"] = user[0][4]
                    thong_tin["email"] = user[0][6]
                    thong_tin["count_sukien"] = int(user[0][7])
                    thong_tin["count_comment"] = int(user[0][8])
                    thong_tin["count_view"] = int(user[0][9])
                    thong_tin["time_coin"] = int(user[0][13])
                    thong_tin["message"] = "Success Login Account"
                    if isinstance(thong_tin, dict):
                        token = generate_token(user_name)
                        thong_tin["token"] = token
                        thong_tin["status"] = 200
                        return thong_tin
                else:
                    thong_tin["id_user"] = ""
                    thong_tin["link_avatar"] = ""
                    thong_tin["user_name"] = ""
                    thong_tin["ip_register"] = ""
                    thong_tin["device_register"] = ""
                    thong_tin["email"] = ""
                    thong_tin["count_sukien"] = ""
                    thong_tin["count_comment"] = ""
                    thong_tin["count_view"] = ""
                    thong_tin["message"] = "Wrong Password! "
                    thong_tin["status"] = 301
                    return thong_tin
            else:
                thong_tin["id_user"] = ""
                thong_tin["link_avatar"] = ""
                thong_tin["user_name"] = ""
                thong_tin["ip_register"] = ""
                thong_tin["device_register"] = ""
                thong_tin["email"] = ""
                thong_tin["count_sukien"] = ""
                thong_tin["count_comment"] = ""
                thong_tin["count_view"] = ""
                thong_tin["message"] = (
                    "Account Not Found - Please Recheck Account " + str(user_name)
                )
                thong_tin["status"] = 302
                return thong_tin

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    thong_tin["id_user"] = ""
    thong_tin["link_avatar"] = ""
    thong_tin["user_name"] = ""
    thong_tin["ip_register"] = ""
    thong_tin["device_register"] = ""
    thong_tin["email"] = ""
    thong_tin["count_sukien"] = ""
    thong_tin["count_comment"] = ""
    thong_tin["count_view"] = ""
    thong_tin["message"] = "Account Not Found - Please Recheck Account " + str(
        user_name
    )
    thong_tin["status"] = 304
    return thong_tin


@app.post("/reset")
async def reset_password(request: Request):
    try:
        form_data = await request.form()
        email = form_data.get("email")

        # Establish database connection
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        print(email)
        # Check if the user with the provided email exists
        query = "SELECT email FROM user WHERE email = %s"
        values = (email,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        print(result)
        if result:
            # Generate a new password
            new_uuid = uuid.uuid4()
            uuid_str = str(new_uuid).replace("-", "")[:12]
            new_password = uuid_str
            # Send email with the new password
            await send_mail_to_email_reset(email, new_password)  # send email by email
            # Update the user's password in the database
            update_query = "UPDATE user SET password = %s WHERE email = %s"
            update_values = (new_password, email)
            cursor.execute(update_query, update_values)
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            return {"message": "Password reset successfully and email sent!"}
        else:
            # Close the cursor and connection
            cursor.close()
            connection.close()

            # Raise exception if no user with the provided email is found
            raise HTTPException(
                status_code=404, detail=f"No user with email found: {email}"
            )
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}", "status": 500})


@app.post("/changepassword/{id_user}", dependencies=[Depends(validate_token)])
async def change_password(request: Request, id_user: str):
    form_data = await request.form()
    old_password = form_data.get("old_password")
    new_password = form_data.get("new_password")
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    mycursor = connection.cursor()
    mycursor.execute(
        f"SELECT * FROM user WHERE id_user='{id_user}' AND password='{old_password}'"
    )
    ketqua = mycursor.fetchall()
    num_rows = mycursor.rowcount
    thong_tin = {}
    if num_rows == 0:
        raise HTTPException(status_code=400, detail="Password Incorrect!.")

    for row in ketqua:
        update_query = "UPDATE user SET password = %s WHERE id_user = %s"
        update_values = (new_password, id_user)
        cursor.execute(update_query, update_values)
        connection.commit()

        thong_tin = {
            "id_user": row[0],
            "link_avatar": row[1],
            "user_name": row[2],
            "ip_register": row[3],
            "device_register": row[4],
            "email": row[6],
            "count_sukien": int(row[7]),
            "count_comment": int(row[8]),
            "count_view": int(row[8]),
        }

    return JSONResponse(content=thong_tin)


@app.post("/deleteuser/{id_user}", dependencies=[Depends(validate_token)])
async def del_user(id_user: int, request: Request):
    form_data = await request.form()
    password = form_data.get("password")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            mycursor = connection.cursor()
            mycursor.execute(
                "SELECT password, email FROM user WHERE email = {}".format(id_user)
            )
            passw = mycursor.fetchone()
            print(passw)
            if passw is None:
                return JSONResponse(content="This user is not available!")
            sql_queries = [
                "DELETE FROM user WHERE id_user = %s",
                "DELETE FROM saved_image WHERE id_user = %s",
                "DELETE FROM comment WHERE id_user = %s",
                "DELETE FROM saved_sukien WHERE id_user = %s",
                "DELETE FROM saved_sukien_video WHERE id_user = %s",
                "DELETE FROM add_sukien WHERE id_user = %s",
                "DELETE FROM saved_notification WHERE id_user = %s",
            ]
            if password == passw[0]:
                for query in sql_queries:
                    mycursor.execute(query, (id_user,))
                connection.commit()
            else:
                return JSONResponse(content="Error Password!")
            message = "Thank you for using our Future Love service, we look forward to your return one day soon!"
            await send_email_to_del_account(passw[1], message)  # send email to email
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if "connection" in locals() and connection.is_connected():
            mycursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={"message": "Successfully deleted account with id = {}".format(id_user)}
    )


@app.patch("/lovehistory/edit/{id_comment}", dependencies=[Depends(validate_token)])
async def update_comment(request: Request, id_comment: int):
    new_content = await request.json()
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            update_query = (
                "UPDATE comment SET noi_dung_comment = %s WHERE id_Comment = %s "
            )
            cursor.execute(update_query, (new_content["content"], id_comment))
            connection.commit()
        cursor.close()
        return {"message": "Comment updated successfully"}
    except Exception as e:
        return {"error": str(e)}


@app.delete("/lovehistory/delete/{id_comment}", dependencies=[Depends(validate_token)])
def delete_comment(id_comment: int):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            update_query = "DELETE FROM comment WHERE id_Comment = %s "
            cursor.execute(update_query, (id_comment,))
            connection.commit()
        cursor.close()
        return {"message": "Comment deleted successfully"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/report/sukien/{id_toan_bo_su_kien}/{so_thu_tu_su_kien}")
async def report_event(
    request: Request, id_toan_bo_su_kien: int, so_thu_tu_su_kien: int
):
    form_data = await request.form()
    report_reason = form_data.get("report_reason")
    id_user_report = form_data.get("id_user_report")
    id_user_sukien = form_data.get("id_user_sukien")

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor()
            mycursor.execute(
                f"UPDATE add_sukien SET status = 'Report!' WHERE id_toan_bo_su_kien ={id_toan_bo_su_kien} and so_thu_tu_su_kien ={so_thu_tu_su_kien}"
            )
            connection.commit()
            sql = "INSERT INTO report_sukien (id_toan_bo_su_kien, so_thu_tu_su_kien, report_reason, id_user_report, id_user_sukien) VALUES ('{}', {}, '{}', {}, {})".format(
                id_toan_bo_su_kien,
                so_thu_tu_su_kien,
                report_reason,
                id_user_report,
                id_user_sukien,
            )
            mycursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"

    return {"message": "Successfully event reported!"}


@app.post("/buy_coin_inapp")
async def buy_coin_inapp(request: Request):
    try:
        form_data = await request.form()
        coin_number = form_data.get("coin_number")
        user_id = form_data.get("user_id")
        if user_id == None:
            return {"message": "Body must have: user_id", "coin": 0, "user_id": 0}
        if coin_number == None:
            return {"message": "Body must have: coin_number", "coin": 0, "user_id": 0}
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        update_query = "UPDATE user SET time_coin_in_app = %s WHERE id_user = %s"
        update_values = (coin_number, user_id)
        cursor.execute(update_query, update_values)
        connection.commit()
    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return {"message": "Done okie", "coin": coin_number, "user_id": user_id}


@app.get("/get_coin_inapp/{user_id}")
async def get_coin_inapp(user_id: str):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM user comment WHERE id_user = {user_id}")
        content = cursor.fetchone()
        coin_data = content[13]

        if coin_data == None:
            return {
                "message": "Successfully done data",
                "coin_number": 0,
                "user_id": user_id,
            }
        return {
            "message": "Successfully done data",
            "coin_number": coin_data,
            "user_id": user_id,
        }
    except mysql.connector.Error as error:
        return {
            "message": "False Database Connect ____ {error}",
            "coin_number": 0,
            "user_id": user_id,
        }
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


@app.post("/report/comment")
async def report_comment(request: Request):
    form_data = await request.form()
    id_comment = form_data.get("id_comment")
    report_reason = form_data.get("report_reason")
    id_user_report = form_data.get("id_user_report")
    id_user_comment = form_data.get("id_user_comment")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor()
            mycursor.execute(f"SELECT * FROM comment WHERE id_Comment = {id_comment}")
            result = mycursor.fetchone()
            mycursor.execute(f"SELECT MAX(id_report) FROM report_comment")
            id_rp = mycursor.fetchone()
            if id_rp[0]:
                id_report = id_rp[0]
            else:
                id_report = 1
            if result is not None:
                mycursor.execute(
                    f"SELECT noi_dung_Comment FROM comment WHERE id_Comment = {id_comment}"
                )
                content = mycursor.fetchone()
                content = content[0]
                sql = "INSERT INTO report_comment (id_report, id_comment, report_reason, content, id_user_report, id_user_comment) VALUES ({}, {}, '{}', '{}', {}, {})".format(
                    id_report,
                    id_comment,
                    report_reason,
                    content,
                    id_user_report,
                    id_user_comment,
                )
                mycursor.execute(sql)
                connection.commit()
            else:
                return {"message": "Comment not found"}
    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return {"message": "Successfully comment reported!"}


@app.post("/add/token")
async def add_token_ios(request: Request):
    form_data = await request.form()
    id_user = form_data.get("id_user")
    device_name = form_data.get("device_name")
    device_token = form_data.get("device_token")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor()
            mycursor.execute(
                "SELECT * FROM device_token_ios WHERE device_token = %s",
                (device_token,),
            )
            check_token = mycursor.fetchone()
            if check_token:
                return {"message": "Tokens are available!!"}
            else:
                sql = f"INSERT INTO device_token_ios (id_user, device_name, device_token) VALUES ({id_user}, %s, %s)"
                values = (device_name, device_token)
                mycursor.execute(sql, values)
                connection.commit()

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return {"message": "Successfully insert device_token!"}


def is_duplicate_image(src_img_path, folder_path):
    try:
        # print(src_img_path)
        with open(src_img_path, "rb") as f:
            src_img_data = f.read()
            src_img_base64 = base64.b64encode(src_img_data).decode("utf-8")
        # print("error here 1")
        for filename in os.listdir(folder_path):
            # print(f"filefilename)
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "rb") as f:
                file_data = f.read()
                file_base64 = base64.b64encode(file_data).decode("utf-8")
            if src_img_base64 == file_base64:
                return filename  # Trả về tên của tệp ảnh trùng lặp
        # print("error here 2")
        return None  # Trả về None nếu không có tệp ảnh trùng lặp
    except Exception as e:
        print(e)
        return JSONResponse(content=({"message": f"Error: {e}"}))


def copy_image(source_path, destination_path):
    try:
        shutil.copy2(source_path, destination_path)
        print("Tệp ảnh đã được sao chép thành công.")
    except FileNotFoundError:
        print(f"Tệp ảnh nguồn '{source_path}' không tồn tại.")
    except shutil.SameFileError:
        print(f"Tệp ảnh đích '{destination_path}' đã tồn tại.")


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


executor = ThreadPoolExecutor(max_workers=2)


@app.get("/getdata/Download", dependencies=[Depends(validate_token)])
async def run_task_in_background_growup_wedding(
    device_them_su_kien: str, ip_them_su_kien: str, id_user: str, folderLuu: str
):
    generated_uuid = uuid.uuid4().int
    id_download = str(generated_uuid)[-12:]
    link = f"https://makewedding.online/timeline/image/{id_download}"
    loop = asyncio.get_event_loop()

    zip_name = "video_image_" + str(id_user) + ".zip"
    data_zip = zip_images(folderLuu, zip_name)

    # return JSONResponse(content={"sukien_image": data})
    return data_zip


@app.post("/upload-gensk2/{id_user}")
async def update_comment(request: Request, id_user: int):
    new_json = await request.json()
    print(str(new_json))
    try:
        print(str(new_json))
    except Exception as e:
        return {"error": str(e)}
    return JSONResponse(content=({"message": f"Error: {str(new_json)}", "status": 500}))


@app.post("/upload-gensk/{id_user}")
async def upload_image(request: Request, id_user: int, src_img: UploadFile = File(...)):
    try:
        # image = face_recognition.load_image_file(src_img)
        # face_locations = face_recognition.face_locations(image)
        # print(face_locations)

        # if not face_locations:
        #     return jsonify({'message': "No faces found in the image"})
        # else:
        #     print("Face found")

        # print(src_img)
        print("______form_data__" + str(request.query_params))
        type = request.query_params.get("type")
        # Tạo folder để lưu ảnh (nếu chưa tồn tại)
        folder_path_temp = f"/var/www/build_futurelove/image/image_user/{id_user}/temp"
        folder_path_nam = f"/var/www/build_futurelove/image/image_user/{id_user}/nam"
        folder_path_video = (
            f"/var/www/build_futurelove/image/image_user/{id_user}/video"
        )
        folder_path_nu = f"/var/www/build_futurelove/image/image_user/{id_user}/nu"
        if not os.path.exists(folder_path_nam):
            os.makedirs(folder_path_nam)
        if not os.path.exists(folder_path_nu):
            os.makedirs(folder_path_nu)
        if not os.path.exists(folder_path_temp):
            os.makedirs(folder_path_temp)
        if not os.path.exists(folder_path_video):
            os.makedirs(folder_path_video)
        print("pass1")
        if type == "src_vid":
            file_name_video = f"{id_user}_vid_{random.randint(10000, 99999)}.jpg"
            src_video_path_temp = os.path.join(folder_path_temp, file_name_video)
            # print(src_video_path_temp)
            print("__________________IM IN__________________")
            with open(src_video_path_temp, "wb") as image:
                print("WRITE_IMAGE")
                image.write(src_img.file.read())

            source_face = get_one_face(cv2.imread(src_video_path_temp))
            print("I PASS THIS")
            if source_face is None:
                os.remove(src_video_path_temp)
                return {
                    "message": "We cannot identify the face in the photo you provided, please upload another photo"
                }

            is_duplicate = is_duplicate_image(src_video_path_temp, folder_path_video)
            print(is_duplicate)
            if is_duplicate:
                os.remove(src_video_path_temp)
                print("Vao 1")
                return f"{folder_path_video}/{is_duplicate}"
            else:
                src_vid_path = os.path.join(folder_path_video, file_name_video)
                copy_image(src_video_path_temp, src_vid_path)
                os.remove(src_video_path_temp)
                print("Vao 2")
                return f"{src_vid_path}"

        print("pass2")
        if type == "src_nam":
            # print("in")
            file_name_nam = f"{id_user}_nam_{random.randint(10000, 99999)}.jpg"
            src_nam_path_temp = os.path.join(folder_path_temp, file_name_nam)
            # print("pass 1")
            with open(src_nam_path_temp, "wb") as image:
                image.write(src_img.file.read())
            # print("pass 2")

            source_face = get_one_face(cv2.imread(src_nam_path_temp))
            if source_face is None:
                os.remove(src_nam_path_temp)
                return {
                    "message": "We cannot identify the face in the photo you provided, please upload another photo"
                }
            # print("pass 3")

            is_duplicate = is_duplicate_image(src_nam_path_temp, folder_path_nam)
            print(is_duplicate)
            if is_duplicate:
                os.remove(src_nam_path_temp)
                print("KHONG NONE")
                print(f"{folder_path_nam}/{is_duplicate}")
                return f"{folder_path_nam}/{is_duplicate}"
            else:
                src_nam_path = os.path.join(folder_path_nam, file_name_nam)
                copy_image(src_nam_path_temp, src_nam_path)
                os.remove(src_nam_path_temp)
                print(f"{src_nam_path}")
                print("Co NONE")
                return f"{src_nam_path}"

        if type == "src_nu":
            file_name_nu = f"{id_user}_nu_{random.randint(10000, 99999)}.jpg"
            src_nu_path_temp = os.path.join(folder_path_temp, file_name_nu)
            with open(src_nu_path_temp, "wb") as image:
                image.write(src_img.file.read())
            print("____path_woman___", src_nu_path_temp)
            source_face = get_one_face(cv2.imread(src_nu_path_temp))
            if source_face is None:
                os.remove(src_nu_path_temp)
                return {
                    "message": "We cannot identify the face in the photo you provided, please upload another photo"
                }

            is_duplicate = is_duplicate_image(src_nu_path_temp, folder_path_nu)
            print(is_duplicate)
            if is_duplicate:
                os.remove(src_nu_path_temp)
                print(f"{folder_path_nu}/{is_duplicate}")
                return f"{folder_path_nu}/{is_duplicate}"
            else:
                src_nu_path = os.path.join(folder_path_nu, file_name_nu)
                copy_image(src_nu_path_temp, src_nu_path)
                os.remove(src_nu_path_temp)
                print(f"{src_nu_path}")
                return f"{src_nu_path}"

        # print("pass3")
    except Exception as e:
        JSONResponse(content=({"message": f"Error: {e}", "status": 500}))


@app.post("/block/user")
async def block_user(request: Request):
    form_data = await request.form()
    user_report = form_data.get("user_report")
    block_account = form_data.get("block_account")
    report_reason = form_data.get("report_reason")

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor()

            mycursor.execute(
                f"SELECT status FROM block_user WHERE id_user_report = %s and id_blocked_user = %s",
                (
                    user_report,
                    block_account,
                ),
            )
            result = mycursor.fetchone()
            if result:
                if result[0] == "blocked":
                    return {"message": "Your account has been reported by you!!"}
                elif result[0] == "be_blocked":
                    return {"message": "You have been blocked by this user!!"}

            mycursor.execute(f"SELECT MAX(id_block) FROM block_user")

            id_rp = mycursor.fetchone()
            if id_rp[0]:
                id_report = id_rp[0] + 1
            else:
                id_report = 1
            status_report = "blocked"
            status_be_report = "be_blocked"
            sql = "INSERT INTO block_user (id_block, id_user_report, id_blocked_user, report_reason, status) VALUES ({}, {}, {}, '{}', '{}')".format(
                id_report, user_report, block_account, report_reason, status_report
            )
            mycursor.execute(sql)
            sql2 = "INSERT INTO block_user (id_block, id_user_report, id_blocked_user, report_reason, status) VALUES ({}, {}, {}, '{}', '{}')".format(
                id_report, block_account, user_report, report_reason, status_be_report
            )
            mycursor.execute(sql2)
            connection.commit()

    except mysql.connector.Error as error:
        f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return {"message": "Successfully comment reported!"}


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, id_user: int):
        await websocket.accept()
        websocket.id_user = id_user
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    # async def broadcast(self, message: str):
    #     for connection in self.active_connections:
    #         await connection.send_text(message)
    async def broadcast(self, message: str, id_user: int):
        for connection in self.active_connections:
            if int(id_user) == connection.id_user:  # Kiểm tra id_user của kết nối
                await connection.send_text(message)


manager = ConnectionManager()


# @app.get("/")
# def Home():
#     return "Hehehehhehe Longcule day"


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            print(data)
            id_user = 0
            start_index = data.find('"id_user":')
            if start_index != -1:
                # Tìm vị trí của ký tự đầu tiên sau dấu hai chấm (:)
                colon_index = data.find(":", start_index)
                # Tìm vị trí của ký tự đầu tiên sau dấu phẩy (,) hoặc dấu đóng ngoặc đơn (})
                comma_index = data.find(",", start_index)
                closing_brace_index = data.find("}", start_index)

                # Xác định vị trí kết thúc của giá trị "id_user"
                end_index = min(
                    filter(lambda x: x != -1, [comma_index, closing_brace_index])
                )

                # Trích xuất giá trị của "id_user"
                if colon_index != -1 and end_index != -1:
                    id_user = data[colon_index + 1 : end_index].strip()

            # message = {"message": data}
            await manager.broadcast(data, id_user)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"clientId": user_id, "message": "Offline"}
        await manager.broadcast(json.dumps(message), user_id)


def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username = payload.get("username")
        print(username)
        response = client.emails.send(
            From="admin@fakewedding.online",  # Địa chỉ email gửi
            To="long16072001@gmail.com",
            Subject="Swap wedding",
            TextBody="You swaped a album wedding ",
        )
    except Exception as e:
        # Handle JWT decoding error as needed
        return e


def get_data_list_sk_all_wedding():
    id_video_wedding = []
    number_album_wedding = []
    id_image_wedding = []
    count_wedding = 0
    album_wedding = 0

    # id_user = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        # Query for video wedding
        query_video = "SELECT * FROM saved_sukien_video_image_wedding ORDER BY thoigian_sukien DESC"
        cursor.execute(query_video)
        result_video_wedding = cursor.fetchall()

        for row in result_video_wedding:
            video_wedding = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
                "thoigian_sukien": row[4],
            }
            id_video_wedding.append(video_wedding)

        # Query for images wedding
        query_images = "SELECT * FROM saved_sukien_2_image WHERE loai_sukien= %s ORDER BY thoigian_sukien DESC"
        cursor.execute(query_images, ("wedding",))
        result_images_wedding = cursor.fetchall()

        for row in result_images_wedding:
            image_data_wedding = {
                "loai_sukien": row[12],
                "id_sk_album": row[14],
                "album": row[13],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
            }
            id_image_wedding.append(image_data_wedding)
            count_wedding += 1
            if count_wedding == 50:
                album_wedding += 1
                count_wedding = 0
                number_album_wedding.append({"album_wedding": id_image_wedding})
                id_image_wedding = []

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )

    return JSONResponse(
        content={
            "sk_fake_wedding": {
                "list_sukien_wedding_video": id_video_wedding,
                "list_sukien_wedding_image": number_album_wedding,
            },
        }
    )


@app.get("/get/list_2_image/id_image_swap_2face_all")
async def get_data_list_sk_all_futurelove(request: Request):
    id_video_wedding = []
    id_image_wedding = []

    id_user = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        # Query for video wedding
        query_video = "SELECT * FROM saved_sukien_video WHERE id_user= %s ORDER BY thoigian_sukien DESC"
        cursor.execute(query_video, (id_user,))
        result_video_wedding = cursor.fetchall()

        for row in result_video_wedding:
            video_wedding = {
                # "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[10],
                "thoigian_sukien": row[7],
            }
            id_video_wedding.append(video_wedding)

        # Query for images wedding
        query_images = "SELECT * FROM saved_sukien_2_image WHERE id_user= %s AND loai_sukien= %s  ORDER BY thoigian_sukien DESC"
        cursor.execute(query_images, (id_user, "swap_2face"))
        result_images_wedding = cursor.fetchall()

        for row in result_images_wedding:
            image_data_wedding = {
                "loai_sukien": row[12],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
                "thoi_gian_sk": row[5],
            }
            id_image_wedding.append(image_data_wedding)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )

    return JSONResponse(
        content={
            "sk_future_love": {
                "list_sukien_future_video": id_video_wedding,
                "list_sukien_future_image": id_image_wedding,
            }
        }
    )


def get_data_list_sk_all_noel():
    id_video_wedding = []
    number_album_wedding = []
    id_image_wedding = []
    count_wedding = 0
    album_wedding = 0

    # id_user = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        # Query for video wedding
        query_video = (
            "SELECT * FROM saved_sukien_video_swap_image ORDER BY thoigian_sukien DESC"
        )
        cursor.execute(query_video)
        result_video_wedding = cursor.fetchall()

        for row in result_video_wedding:
            video_wedding = {
                # "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
                "thoigian_sukien": row[4],
            }
            id_video_wedding.append(video_wedding)

        # Query for images wedding
        query_images = "SELECT * FROM saved_sukien_2_image WHERE loai_sukien= %s ORDER BY thoigian_sukien DESC"
        cursor.execute(query_images, ("noel",))
        result_images_wedding = cursor.fetchall()

        for row in result_images_wedding:
            image_data_wedding = {
                "loai_sukien": row[12],
                "id_sk_album": row[14],
                "album": row[13],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
            }
            id_image_wedding.append(image_data_wedding)
            count_wedding += 1
            if count_wedding == 50:
                album_wedding += 1
                count_wedding = 0
                number_album_wedding.append({"album_wedding": id_image_wedding})
                id_image_wedding = []

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )

    return JSONResponse(
        content={
            "sk_noel": {
                "list_sukien_noel_video": id_video_wedding,
                "list_sukien_noel_image": number_album_wedding,
            },
        }
    )


def get_data_list_sk_all_growup():
    id_video_grow_up_age = []
    number_album_wedding = []
    id_image_grow_up = []
    count_wedding = 0
    album_wedding = 0

    # id_user = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        # Query for video growup
        query_video = "SELECT * FROM saved_sukien_video_image_growup ORDER BY thoigian_sukien DESC"
        cursor.execute(query_video)
        result_video_grow_up = cursor.fetchall()

        for row in result_video_grow_up:
            video_grow_up_age = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
                "thoigian_sukien": row[4],
            }
            id_video_grow_up_age.append(video_grow_up_age)

        # Query for images growup
        query_images = "SELECT * FROM saved_sukien_2_image WHERE loai_sukien= %s ORDER BY thoigian_sukien DESC"
        cursor.execute(query_images, ("mom and baby",))
        result_images_wedding = cursor.fetchall()

        for row in result_images_wedding:
            image_data_wedding = {
                "loai_sukien": row[12],
                "id_sk_album": row[14],
                "album": row[13],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
            }
            id_image_grow_up.append(image_data_wedding)
            count_wedding += 1
            if count_wedding == 50:
                album_wedding += 1
                count_wedding = 0
                number_album_wedding.append({"album_wedding": id_image_grow_up})
                id_image_grow_up = []

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )

    return JSONResponse(
        content={
            "sk_grow_up": {
                "list_sukien_grow_up_video": id_video_grow_up_age,
                "list_sukien_grow_up_image": number_album_wedding,
            },
        }
    )


@app.get("/get/all_su_kien/id_user")
async def get_all_sk():
    data = []
    try:
        data_wedding = get_data_list_sk_all_wedding()
        data_futurelove = get_data_list_sk_all_futurelove()
        data_noel = get_data_list_sk_all_noel()
        data_growup = get_data_list_sk_all_growup()
        # data.append(data_wedding)
        return data_growup
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# SERVER WEDDING DATA


@app.get("/get/list_image_wedding/{album}")
async def get_data_list_image_wedding(request: Request, album: int):
    category = request.query_params.get("album")
    list_toan_bo_image = []

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        print("halo2")
        query = "SELECT * FROM listImage_wedding WHERE IDCategories = %s"
        mycursor.execute(query, (category,))
        result2 = mycursor.fetchall()

        for row in result2:
            linkImage = row[3].replace("main", "main/IMG_WEDDING")
            image = {}
            image["id"] = row[0]
            image["mask"] = row[1]
            image["thongtin"] = row[2]
            image["image"] = linkImage
            image["dotuoi"] = row[4]
            image["IDCategories"] = row[5]
            list_toan_bo_image.append(image)

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_image})


@app.get("/get/list_image/all_wedding")
async def get_data_list_image_all():
    list_toan_bo_image = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM listImage_wedding"
        mycursor.execute(query)
        result2 = mycursor.fetchall()

        for row in result2:
            linkImage = row[3].replace("main", "main/IMG_WEDDING")
            image = {
                "id": row[0],
                "mask": row[1],
                "thongtin": row[2],
                "image": linkImage,
                "dotuoi": row[4],
                "IDCategories": row[5],
            }
            list_toan_bo_image.append(image)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_image})


@app.get("/get/list_image_wedding/{album}")
async def get_data_list_image_wedding(request: Request, album: int):
    category = request.query_params.get("album")
    list_toan_bo_image = []

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        print("halo2")
        query = "SELECT * FROM listImage_wedding WHERE IDCategories = %s"
        mycursor.execute(query, (category,))
        result2 = mycursor.fetchall()

        for row in result2:
            linkImage = row[3].replace("main", "main/IMG_WEDDING")
            image = {}
            image["id"] = row[0]
            image["mask"] = row[1]
            image["thongtin"] = row[2]
            image["image"] = linkImage
            image["dotuoi"] = row[4]
            image["IDCategories"] = row[5]
            list_toan_bo_image.append(image)

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_image})


# GET VIDEO WEDDING TEMPLATE


@app.get("/get/list_video/all_video_wedding_template")
async def get_data_list_video_wedding_template():
    list_toan_bo_video_wedding = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM listvideo_wedding"
        mycursor.execute(query)
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id": row[0],
                "link_video": row[1],
                "noidung": row[2],
                "age_video": row[6],
                "gioitinh": row[7],
                "mau_da": row[8],
                "chung_toc": row[9],
                "thumbnail": row[3],
            }
            list_toan_bo_video_wedding.append(video)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(
        content={"list_sukien_video_wedding": list_toan_bo_video_wedding}
    )


@app.get("/get/list_video/video_wedding_detail")
async def get_data_video_wedding_detail(request: Request):
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
        query = f"SELECT * FROM listvideo_wedding WHERE id = {id}"
        mycursor.execute(query)
        result2 = mycursor.fetchall()

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return result2[0][1]


# GET ALL VIDEO SWAP
@app.get("/get/list_video/all_video_wedding_swap")
async def get_data_list_all_video_wedding_swap():
    list_toan_bo_video_wedding = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_video_image_wedding ORDER BY thoigian_sukien DESC"
        mycursor.execute(query)
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "thoigian_sukien": row[4],
                "id_user": row[7],
            }
            list_toan_bo_video_wedding.append(video)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(
        content={"list_sukien_video_wedding": list_toan_bo_video_wedding}
    )


# GET LIST VIDEO WEDDING THEO TIME


@app.get("/get/list_image/all_wedding_time")
async def get_data_list_video_all_wedding_swap(request: Request):
    list_toan_bo_video = []
    count = 0
    album = 0
    number_album = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_2_image WHERE loai_sukien='wedding' ORDER BY thoigian_sukien DESC"
        mycursor.execute(query)
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "loai_sukien": row[12],
                "id_sk_swap_album": row[14],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
                "album": row[13],
                "thoigian_sukien": row[5],
            }
            list_toan_bo_video.append(video)
            count += 1
            if count == 50:
                album += 1
                count = 0
                number_album.append(
                    {
                        "album": album,
                        "list_sukien_image": list_toan_bo_video,
                        "total": count,
                    }
                )
                list_toan_bo_video = []
    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content=number_album)


# GET LIST VIDEO THEO profile của user


@app.get("/get/list_video_wedding/id_video_swap")
async def get_data_list_video_wedding_id(request: Request):
    id_video = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_video_image_wedding WHERE id_user = %s ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_user_wedding_video,))
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
                "thoigian_sukien": row[4],
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


# get all video swap  https://photo.gachmen.org/gensk


@app.get("/get/list_video/all_video_swap_wedding")
async def get_data_list_video_all_wedding(request: Request):
    id_video = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_video_image_wedding WHERE id_user = %s ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_user_wedding_video,))
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
                "thoigian_sukien": row[4],
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


@app.get("/get/list_video/all_video_swap_future_love")
async def get_data_list_video_all_wedding(request: Request):
    id_video = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_video_swap_image WHERE id_user = %s ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_user_wedding_video,))
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
                "thoigian_sukien": row[4],
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


# GET SWAP VIDEO THEO ID SK
@app.get("/get/list_video/id_video_swap_all_id_sk")
async def get_data_list_video_wedding_all_id_sk(request: Request):
    id_video = []
    id_user_wedding_video = request.query_params.get("id_user")
    id_sk_wedding_image = request.query_params.get("id_sk")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_video_image_wedding WHERE id_user = %s  AND id_saved = %s ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_user_wedding_video, id_sk_wedding_image))
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
                "thoigian_sukien": row[4],
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

    return JSONResponse(content={"id_su_kien_swap_image": id_video})


# GET ALL IMAGE SWAP AND VIDEO SWAP  https://photo.gachmen.org/genvideo


@app.get("/get/list_video/all_video_image_swap_wedding")
async def get_data_list_video_image_all_futurelove(request: Request):
    id_video = []
    id_image = []
    count = 0
    album = 0
    number_album = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        # Query for video
        query_video = "SELECT * FROM saved_sukien_video_image_wedding WHERE id_user= %s ORDER BY thoigian_sukien DESC"
        cursor.execute(query_video, (id_user_wedding_video,))
        result_video = cursor.fetchall()

        for row in result_video:
            video = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
                "thoigian_sukien": row[4],
            }
            id_video.append(video)

        # Query for images
        query_images = "SELECT * FROM saved_sukien_2_image WHERE id_user= %s ORDER BY thoigian_sukien DESC"
        cursor.execute(query_images, (id_user_wedding_video,))
        result_images = cursor.fetchall()

        for row in result_images:
            image_data = {
                "loai_sukien": row[12],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
                "album": row[13],
            }
            id_image.append(image_data)
            count += 1
            if count == 50:
                album += 1
                count = 0
                number_album.append({"album": album, "list_sukien_video": id_image})
                id_image = []

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )

    return JSONResponse(
        content={"list_sukien_video": id_video, "list_sk_image": number_album}
    )


# ____SONPIPI______
def saved_album_wedding_swap(
    link1, link2, link_swap, device_them_su_kien, ip_them_su_kien, id_user
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0

    try:
        print("hallo")
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor(buffered=True)
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor(buffered=True)

            date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            id_template = random.randint(1, 4)
            Json_added = {
                "id_saved": id_toan_bo_sk,
                "link_src_goc": link1,
                "link_tar_goc": link2,
                "link_da_swap": link_swap,
                "id_toan_bo_su_kien": id_toan_bo_sk,
                "thoigian_sukien": date,
                "device_them_su_kien": device_them_su_kien,
                "ip_them_su_kien": ip_them_su_kien,
                "id_user": id_user,
                "count_comment": count_comment,
                "count_view": count_view,
                "id_template": id_template,
            }
            sql = f"INSERT INTO saved_wedding_album_swap (id_saved ,link_src_goc , link_tar_goc , link_da_swap  , id_toan_bo_su_kien , thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user,count_comment, count_view, id_template) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,{id_user},{count_comment}, {count_view},{id_template})"
            val = (
                id_toan_bo_sk,
                link1,
                link2,
                link_swap,
                id_toan_bo_sk,
                date,
                device_them_su_kien,
                ip_them_su_kien,
            )
            mycursor.execute(sql, val)
            connection.commit()

            return Json_added
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


@app.get("/allswap/{page}")
async def get_data_list_image_wedding(request: Request, page: int):
    category = request.query_params.get("page")
    list_toan_bo_image = []

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        print("halo2")
        query = "SELECT * FROM saved_wedding_album_swap"
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        biendem = page * 50
        print("bien dem_____" + str(biendem))
        for row in result2:
            biendem = biendem + 1
            print("bien dem_____" + str(biendem))
            if biendem > (page + 1) * 50:
                break
            link_src_goc = row[1].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            link_tar_goc = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            link_da_swap = row[3].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            image = {}
            image["id_saved"] = row[0]
            image["link_src_goc"] = link_src_goc
            image["link_tar_goc"] = link_tar_goc
            image["link_da_swap"] = link_da_swap
            image["id_toan_bo_su_kien"] = row[4]
            image["thoigian_sukien"] = row[5]
            image["device_them_su_kien"] = row[6]
            image["ip_them_su_kien"] = row[7]
            image["id_user"] = row[8]
            image["count_comment"] = row[9]
            image["count_view"] = row[10]
            image["id_template"] = row[11]
            list_toan_bo_image.append(image)

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_image})


# wedding_template
@app.get("/get/categories_wedding")
async def get_categories_wedding(request: Request):
    list_categories = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        print("halo2")
        query = "SELECT * FROM wedding_template "
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        # id_cate 	name_cate 	number_image 	folder_name 	selected_swap 	image_sample
        for row in result2:
            image = {}
            image["id_cate"] = row[0]
            image["name_cate"] = row[1]
            image["number_image"] = row[2]
            image["folder_name"] = row[3]
            image["selected_swap"] = row[4]
            image["image_sample"] = row[5]
            list_categories.append(image)

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"categories_all": list_categories})


# get lisst image by id user sk wedding theo  profile của use


@app.get("/get/list_2_image/id_image_swap")
async def get_data_list_image_wedding_id(request: Request):
    id_image = []
    count = 0
    album = 0
    number_album = []
    id_sk_album = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_2_image WHERE id_user = %s AND loai_sukien='wedding' ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_user_wedding_video,))
        result2 = mycursor.fetchall()
        # Group images by id_sk_album
        album_images = {}
        for row in result2:
            id_sk_album = row[14]
            if id_sk_album not in album_images:
                album_images[id_sk_album] = []
            video = {
                "loai_sukien": row[12],
                "id_sk_album": row[14],
                "album": row[13],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
            }
            album_images[id_sk_album].append(video)

        # Create albums
        for id_sk_album, images in album_images.items():
            album += 1
            number_album.append({"album": album, "list_sukien_image": images})

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content=number_album)


# get lisst image by id user sk wedding theo album
@app.get("/get/list_2_image/id_image_swap_album")
async def get_data_list_image_wedding_id_album(request: Request):
    id_video = []
    id_user_wedding_video = request.query_params.get("id_user")
    id_album = request.query_params.get("album")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_2_image WHERE id_user = %s AND album=%s AND loai_sukien='wedding' ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_user_wedding_video, id_album))
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "loai_sukien": row[12],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
                "album": row[13],
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


# get list all sk image by id user  https://photo.gachmen.org/genimg
@app.get("/get/list_2_image/id_image_swap_all")
async def get_data_list_image_wedding_all(request: Request):
    id_image = []
    count = 0
    album = 0
    number_album = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_2_image WHERE id_user = %s AND loai_sukien = %s ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_user_wedding_video, "wedding"))
        result2 = mycursor.fetchall()
        for row in result2:
            image = {
                "loai_sukien": row[12],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
                "album": row[13],
            }
            id_image.append(image)
            count += 1
            if count == 50:
                album += 1
                count = 0
                number_album.append({"album": album, "list_sukien_video": id_image})
                id_video = []

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content=number_album)


# GET IMAGE SK WEDDING THEO ID SU KIEN


@app.get("/get/list_2_image/id_image_swap_all_id_sk")
async def get_data_list_image_wedding_all_id_sk(request: Request):
    id_image = []
    id_user_wedding_video = request.query_params.get("id_user")
    id_sk_wedding_image = request.query_params.get("id_sk")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_2_image WHERE id_sk_album = %s ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_sk_wedding_image,))
        result2 = mycursor.fetchall()

        for row in result2:
            image = {
                "loai_sukien": row[12],
                "id_sk_swap_album": row[14],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
                "album": row[13],
                "thoi_gian_swap": row[5],
            }
            id_image.append(image)
    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"id_su_kien_swap_image": id_image})


# GET DETAL SK SWAP 2 image by id sk swap futurelove


@app.get("/get/list_2_image/id_image_swap_futurelove_all_id_sk")
async def get_data_list_image_wedding_futurelove_all_id_sk(request: Request):
    id_image = []
    id_user_wedding_video = request.query_params.get("id_user")
    id_sk_wedding_image = request.query_params.get("id_sk")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_2_image WHERE id_saved = %s ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_sk_wedding_image,))
        result2 = mycursor.fetchall()

        for row in result2:
            image = {
                "loai_sukien": row[12],
                "id_sk_swap_album": row[14],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
                "thoi_gian_swap": row[5],
            }
            id_image.append(image)
    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"id_su_kien_swap_image": id_image})


# GET DETAL SK SWAP image to video by id sk swap futurelove


@app.get("/get/list_video_image/id_video_swap_futurelove_all_id_sk")
async def get_data_list_image_wedding_futurelove_all_id_sk(request: Request):
    id_image = []
    id_sk_wedding_image = request.query_params.get("id_sk")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM saved_sukien_video WHERE id_saved = %s ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_sk_wedding_image,))
        result2 = mycursor.fetchall()

        for row in result2:
            image = {
                "loai_sukien": "swap video futurelove",
                "id_saved": row[0],
                "link_src_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[10],
                "thoi_gian_su_kien": row[7],
            }
            id_image.append(image)
    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"id_su_kien_swap_image": id_image})


# get all sk swap 2 face futurelove
@app.get("/get/list_2_image/id_image_swap_all_future_love")
async def get_data_list_image_wedding_all(request: Request):
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
        query = "SELECT * FROM saved_sukien_2_image WHERE id_user = %s AND loai_sukien = %s ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_user, "swap_2face"))
        result2 = mycursor.fetchall()

        for row in result2:
            image = {
                "loai_sukien": row[12],
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
                "thoigian_sukien": row[5],
            }
            id_image.append(image)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"id_su_kien_swap_image": id_image})


# get all sk swap baby futurelove
@app.get("/get/list_2_image/id_image_swap_baby_all_future_love")
async def get_data_list_image_wedding_all(request: Request):
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
        query = "SELECT * FROM saved_sukien_swap_baby WHERE id_user = %s ORDER BY thoigian_sukien DESC"
        mycursor.execute(query, (id_user,))
        result2 = mycursor.fetchall()

        for row in result2:
            image = {
                "id_saved": row[0],
                "link_nam_goc": row[1],
                "link_nu_goc": row[2],
                "link_baby_swap": row[3],
                "link_da_swap": row[4],
                "id_user": row[10],
                "thoigian_sukien": row[7],
            }
            id_image.append(image)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"id_su_kien_swap_image": id_image})


# SERVER SANTA_APP
@app.get("/get/list_image/{album}")
async def get_data_list_image(request: Request, album: int):
    category = request.query_params.get("album")
    list_toan_bo_image = []

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        print("halo2")
        query = "SELECT * FROM listimage_santa WHERE IDCategories = %s"
        mycursor.execute(query, (category,))
        result2 = mycursor.fetchall()

        for row in result2:
            image = {}
            image["id"] = row[0]
            image["mask"] = row[1]
            image["thongtin"] = row[2]
            image["image"] = row[3]
            image["dotuoi"] = row[4]
            image["IDCategories"] = row[5]
            list_toan_bo_image.append(image)

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_image})


# viet update code 17 oct 2024
@app.get("/lovehistory/listvideo/santa/{page}")
async def get_data_list_video_santa(request: Request, page: int):
    category = request.query_params.get("category")
    print(type(category))
    list_toan_bo_video = []
    thong_tin = {}
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        if category == "0":
            print("halo1")
            # query = "SELECT * from listVideo_santa"
            query = "SELECT * from listVideo_santa_video"  # viet update
            mycursor.execute(query)
            result2 = mycursor.fetchall()
            # print(result2)
        elif category != 0:
            print("halo2")
            # query = "SELECT * FROM listVideo_santa WHERE IDCategories = %s"
            query = "SELECT * FROM listVideo_santa_video WHERE IDCategories = %s"  # viet update
            mycursor.execute(query, (category,))
            result2 = mycursor.fetchall()
            # print(result2)

        # print(result2)
        soPhanTuTrenMotTrang = 50
        soTrang = (len(result2) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang
        print(len(result2))
        print(soTrang)
        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(result2))
        else:
            return JSONResponse(content="exceed the number of pages!!!")
        print("hello")
        for i in range(start, end):
            query = "SELECT * from categories_video where idCateogries=%s"
            mycursor.execute(query, (result2[i][5],))
            result3 = mycursor.fetchall()
            thong_tin["id"] = result2[i][0]
            thong_tin["id_categories"] = result2[i][0]
            thong_tin["name_categories"] = result3[0][1]
            thong_tin["detail"] = result3[0][2]
            thong_tin["age_video"] = result2[i][6]
            thong_tin["chung_toc"] = result2[i][9]
            thong_tin["gioi_tinh"] = result2[i][7]
            thong_tin["link_video"] = result2[i][1]
            thong_tin["mau_da"] = result2[i][8]
            thong_tin["noi_dung"] = result2[i][2]
            thong_tin["thumbnail"] = result2[i][3]
            list_toan_bo_video.append(thong_tin)
            thong_tin = {}

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_video})


# api new by viet 17 oct 2024
@app.get("/get/santa/list_temp/{page}")
async def get_data_list_temp_santa(request: Request, page: int):
    category = request.query_params.get("category")
    print(type(category))
    list_toan_bo_video = []
    thong_tin = {}
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        if category == "0":
            print("halo1")
            query = "SELECT * from listVideo_santa_video"
            mycursor.execute(query)
            result2 = mycursor.fetchall()
            # print(result2)
        elif category != 0:
            print("halo2")
            query = "SELECT * FROM listVideo_santa_video WHERE IDCategories = %s"
            mycursor.execute(query, (category,))
            result2 = mycursor.fetchall()
            # print(result2)

        # print(result2)
        soPhanTuTrenMotTrang = 50
        soTrang = (len(result2) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang
        print(len(result2))
        print(soTrang)
        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(result2))
        else:
            return JSONResponse(content="exceed the number of pages!!!")
        print("hello")
        for i in range(start, end):
            query = "SELECT * from categories_video where idCateogries=%s"
            mycursor.execute(query, (result2[i][5],))
            result3 = mycursor.fetchall()
            thong_tin["id"] = result2[i][0]
            thong_tin["id_categories"] = result2[i][0]
            thong_tin["name_categories"] = result3[0][1]
            thong_tin["detail"] = result3[0][2]
            thong_tin["age_video"] = result2[i][6]
            thong_tin["chung_toc"] = result2[i][9]
            thong_tin["gioi_tinh"] = result2[i][7]
            thong_tin["link_video"] = result2[i][1]
            thong_tin["mau_da"] = result2[i][8]
            thong_tin["noi_dung"] = result2[i][2]
            thong_tin["thumbnail"] = result2[i][3]
            list_toan_bo_video.append(thong_tin)
            thong_tin = {}

    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_video})


@app.get("/lovehistory/listimage/santa/{page}")
async def get_data_list_video_santa(request: Request, page: int):
    category = request.query_params.get("category")
    result = dict()
    # print(category)
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        limit = 50
        offset = (page - 1) * limit
        if category == "0":
            query = f"SELECT * from listimage_santa LIMIT {limit} OFFSET {offset}"
            mycursor.execute(query)
            data = mycursor.fetchall()
            query_info = f"SELECT COUNT(listimage_santa.id) from listimage_santa"
            mycursor.execute(query_info)
            data_length = mycursor.fetchall()[0][0]
            # print(data_length)
            total_page = math.ceil(int(data_length) / 10)

        elif category != "0":
            query = f"SELECT * FROM listimage_santa WHERE IDCategories = {category} LIMIT {limit} OFFSET {offset}"
            mycursor.execute(query)
            data = mycursor.fetchall()
            query_info = f"SELECT COUNT(listimage_santa.id) from listimage_santa WHERE IDCategories = {category}"
            mycursor.execute(query_info)
            data_length = mycursor.fetchall()[0][0]
            total_page = math.ceil(int(data_length) / 10)

        list_image = []
        for item in data:
            info = {}
            query = f"SELECT * from categories_video where idCateogries= {item[5]}"
            mycursor.execute(query)
            cat_info = mycursor.fetchall()
            info["id"] = item[0]
            info["mask"] = item[1]
            info["name_categories"] = cat_info[0][1]
            info["detail"] = cat_info[0][2]
            info["thongtin"] = item[2]
            info["image"] = item[3]
            info["do_tuoi"] = item[4]
            info["IDCategories"] = item[5]
            list_image.append(info)

        result["data"] = list_image
        result["total_page"] = total_page
    except mysql.connector.Error as error:
        return f"Failed to connect to MySQL database: {error}"
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return result


from typing import Optional


@app.get("/get/list_image/all_santa/{album}")
async def get_data_list_image_all(album: Optional[int] = None):
    list_toan_bo_image = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM listimage_santa"
        mycursor.execute(query)
        result2 = mycursor.fetchall()

        for row in result2:
            image = {
                "id": row[0],
                "mask": row[1],
                "thongtin": row[2],
                "image": row[3],
                "dotuoi": row[4],
                "IDCategories": row[5],
            }
            list_toan_bo_image.append(image)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": list_toan_bo_image})


@app.get("/get/list_video/all_santa")
async def get_data_list_video_all():
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
        query = "SELECT * FROM listVideo_santa"
        mycursor.execute(query)
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


@app.get("/get/list_video/id_santa")
async def get_data_list_video_id(request: Request):
    id_video = []
    id_video_santa = request.query_params.get("id_video_santa")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM listVideo_santa WHERE id = %s"
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


# get video, image theo id user


@app.get("/get/id_video/id_user")
async def get_data_list_video_id(request: Request):
    id_video = []
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
        query = "SELECT * FROM saved_sukien_video WHERE id_user = %s"
        mycursor.execute(query, (id_user,))
        result2 = mycursor.fetchall()

        for row in result2:
            video = {
                "id_saved": row[0],
                "link_video": row[1],
                "link_image": row[2],
                "link_da_swap": row[3],
                "ten_su_kien": row[4],
                "noidung_su_kien": row[5],
                "id_video": row[6],
                "id_user": row[10],
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


@app.get("/get/id_image/id_user")
async def get_data_list_video_id(request: Request):
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
        query = "SELECT * FROM saved_sukien_2_image WHERE id_user = %s"
        mycursor.execute(query, (id_user,))
        result2 = mycursor.fetchall()

        for row in result2:
            image = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
            }
            id_image.append(image)

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


# get thong tin album image


@app.get("/get/list_album")
async def get_data_list_video_id(request: Request):
    id_album = []
    server = request.query_params.get("server")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        mycursor = connection.cursor()
        query = "SELECT * FROM list_album WHERE server = %s"
        mycursor.execute(query, (server,))
        result2 = mycursor.fetchall()

        for row in result2:
            album = {
                "id ": row[0],
                "noidung": row[1],
                "id_album": row[2],
                "server": row[3],
                "thumpImage": row[4],
            }
            id_album.append(album)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": id_album})


@app.get("/get/list_album/id_album")
async def get_data_list_video_id(request: Request):
    id_album = []
    server = request.query_params.get("server")
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
        query = "SELECT * FROM list_album WHERE server = %s AND id_album= %s"
        mycursor.execute(query, (server, id))
        result2 = mycursor.fetchall()

        for row in result2:
            album = {
                "id ": row[0],
                "noidung": row[1],
                "id_album": row[2],
                "server": row[3],
            }
            id_album.append(album)

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return JSONResponse(content={"list_sukien_video": id_album})


@app.get("/get/list_video/all_video_baby_mom", tags=["list_video"])
async def get_data_list_video_all(request: Request):
    list_temp = dict()
    page = request.query_params.get("page")
    if page == None:
        page = "1"
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")

        limit = 30
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

        limit = 30
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


@app.get("/list_image/mom_baby_temp", tags=["list_image"])
async def get_mom_baby_temp(request: Request):
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


@app.get("/list_image/mom_baby_temp_detail", tags=["list_image"])
async def get_mom_baby_temp_detail(request: Request):
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


@app.get("/list_image/all_image_swap", tags=["list_image"])
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


@app.get("/list_image/all_image_swap_mom_baby", tags=["list_image"])
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
            link_da_swap = row[2].replace(
                "https://futurelove.online", "https://photo.gachmen.org"
            )
            data = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_da_swap": link_da_swap,
                "id_toan_bo_su_kien": row[3],
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
            link_da_swap = row[4].replace(
                "https://futurelove.online", "https://photo.gachmen.org"
            )
            data = {
                "id_saved": row[0],
                "link_nam_goc": row[1],
                "link_nu_goc": row[2],
                "link_baby_goc": row[3],
                "link_da_swap": link_da_swap,
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


# get list newborn, time machine, dad and mom
@app.get("/get/list_all_newborn/{id_user}", tags=["list_all_newborn"])
async def get_list_all_newborn(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_2_image WHERE loai_sukien='newborn' AND id_user = {id_user}"
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM saved_sukien_2_image WHERE loai_sukien='newborn' AND id_user = {id_user} ORDER BY `saved_sukien_2_image`.`thoigian_sukien` ASC LIMIT {limit} OFFSET {offset}"
        print("____Query_____", str(query))
        mycursor.execute(
            query,
        )
        result2 = mycursor.fetchall()
        for row in result2:
            link_src_goc = row[1].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            link_da_swap = row[3].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            link_tar_goc = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_src_goc": link_src_goc,
                "link_da_swap": link_da_swap,
                "link_tar_goc": link_tar_goc,
                "id_toan_bo_su_kien": row[4],
                # "thoigian_sukien": row[5],
                # "device_them_su_kien": row[6],
                # "ip_them_su_kien": row[7],
                "id_user": row[8],
                "count_comment": row[9],
                "count_view": row[10],
                # "id_template": row[11],
                "loai_sukien": row[12],
                # "album": row[13],
                # "id_sk_album": row[14],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_data,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


@app.get("/get/list_all_time_machine/{id_user}", tags=["list_all_timeMachine"])
async def get_list_all_timeMachine(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_video_image_growup WHERE id_user = {id_user}"
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_user = {id_user} ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC LIMIT {limit} OFFSET {offset} "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_data,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


@app.get("/get/list_all_dadandmom/{id_user}", tags=["list_all_dadandmom"])
async def get_list_all_dadandmom(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_video_swap_image WHERE id_user = {id_user}"
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM saved_sukien_video_swap_image WHERE id_user = {id_user} ORDER BY `saved_sukien_video_swap_image`.`id` DESC LIMIT {limit} OFFSET {offset}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_them_su_kien": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_data,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


@app.get("/get/list_all_time_machine/{id_user}", tags=["list_all_time_machine"])
async def get_list_all_time_machine(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk NOT IN('baby_catwalk', 'baby_funny','baby_hallowen','model','baby_future_love')"
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk NOT IN('baby_catwalk', 'baby_funny','baby_hallowen','model','baby_future_love') ORDER BY `saved_sukien_video_image_growup`.`id` DESC LIMIT {limit} OFFSET {offset}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_them_su_kien": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_data,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# get all su kien
@app.get("/get/list_all_sk/{id_sukien}", tags=["list_all_sk"])
async def get_list_all_sk(request: Request, id_sukien: int):
    list_all_sk = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = (
            f"SELECT COUNT(*) FROM saved_sukien WHERE id_toan_bo_su_kien = {id_sukien}"
        )
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM  saved_sukien WHERE id_toan_bo_su_kien ={id_sukien} ORDER BY `saved_sukien`.`thoigian_sukien`  ASC LIMIT {limit} OFFSET {offset}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_save": row[0],
                "ten_nam": row[16],
                "link_nam_goc": row[1],
                "ten_nu": row[17],
                "link_nu_goc": row[2],
                "link_nam_chua_swap": row[3],
                "link_nu_chua_swap": row[4],
                "link_da_swap": row[5],
                "thoigian_swap": row[6],
                "ten_su_kien": row[7],
                "noidung_su_kien": row[8],
                "id_toan_bo_su_kien": row[9],
                "so_thu_tu_su_kien": row[10],
                "thoigian_sukien": row[11],
                "id_user": row[14],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_all_sk": list_all_sk,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# get all mom and kid
@app.get("/get/list_all_kidandmom/{id_user}", tags=["list_all_kidandmom"])
async def get_list_all_kidandmom(request: Request, id_user: int):
    list_all_sk = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = (
            f"SELECT COUNT(*) FROM saved_sukien_alone WHERE id_user = {id_user}"
        )
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM  saved_sukien_alone WHERE id_user ={id_user} ORDER BY `saved_sukien_alone`.`thoigian_sukien`  ASC LIMIT {limit} OFFSET {offset}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_src_goc": row[1],
                "link_da_swap": row[2],
                "id_toan_bo_su_kien": row[3],
                "thoigian_sukien": row[4],
                # "device_them_su_kien": row[5],
                # "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                # "id_itemplate": row[10],
                "loai_sk": row[11],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_all_sk,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# get list generator
@app.get("/get/list_all_generator/{id_user}", tags=["list_all_generator"])
async def get_list_all_generator(request: Request, id_user: int):
    list_all_sk = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = (
            f"SELECT COUNT(*) FROM saved_sukien_swap_baby WHERE id_user = {id_user}"
        )
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM  saved_sukien_swap_baby WHERE id_user ={id_user} ORDER BY `saved_sukien_swap_baby`.`thoigian_sukien`  ASC LIMIT {limit} OFFSET {offset}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_nam_goc": row[1],
                # "link_nu_goc": row[2],
                # "link_baby_goc ": row[3],
                "link_da_swap": row[4],
                "id_toan_bo_su_kien": row[5],
                # " noi_dung_su_kien ": row[6],
                # "thoigian_sukien": row[7],
                "id_user": row[10],
                "tomLuocText": row[11],
                "count_comment": row[12],
                "count_view": row[13],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_all_sk,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# get detail
@app.get("/get/detail/newborn/{id_saved}", tags=["detail_newborn"])
async def detail_newborn(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM saved_sukien_2_image WHERE loai_sukien='newborn' AND id_saved = {id_saved} ORDER BY `saved_sukien_2_image`.`thoigian_sukien` ASC"
        print("____Query_____", str(query))
        mycursor.execute(
            query,
        )
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_da_swap": row[2],
                "link_tar_goc": row[3],
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
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail": list_data,
            "status": 200,
            "total_item": total_item,
        }
    )


@app.get("/get/detail/time_machine/{id_saved}", tags=["detail_timeMachine"])
async def detail_timeMachine(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_saved = {id_saved} AND loai_sk NOT IN('baby_catwalk', 'baby_funny','baby_hallowen','model','baby_future_love') ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail": list_data,
            "status": 200,
            "total_item": total_item,
        }
    )


@app.get("/get/detail/dadandmom/{id_saved}", tags=["detail_dadandmom"])
async def detail_dadandmom(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM saved_sukien_swap_baby WHERE id_saved = {id_saved} ORDER BY `saved_sukien_swap_baby`.`thoigian_sukien` ASC"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_nam_goc": row[1],
                "link_nu_goc": row[2],
                "link_baby_goc": row[3],
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
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_data,
            "status": 200,
            "total_item": total_item,
        }
    )


@app.get("/get/detail/kidandmom/{id_user}", tags=["detail_kidandmom"])
async def get_list_detail_kidandmom(request: Request, id_user: int):
    list_detail = []
    total_item = 0
    page = request.query_params.get("page")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = (
            f"SELECT COUNT(*) FROM saved_sukien_alone WHERE id_user = {id_user}"
        )
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM  saved_sukien_alone WHERE id_user ={id_user} ORDER BY `saved_sukien_alone`.`thoigian_sukien`  ASC LIMIT {limit} OFFSET {offset} "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_da_swap": row[2],
                "id_toan_bo_su_kien": row[3],
                "thoigian_sukien": row[4],
                "device_them_su_kien": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "id_itemplate": row[10],
                "loai_sk": row[11],
            }
            list_detail.append(data)
            total_item = len(list_detail)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_detail,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


@app.get("/get/detail/generator/{id_saved}", tags=["detail_generator"])
async def detail_generator(request: Request, id_saved: int):
    list_detail = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM  saved_sukien_swap_baby WHERE id_saved ={id_saved} ORDER BY `saved_sukien_swap_baby`.`thoigian_sukien`  ASC  "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_nam_goc": row[1],
                "link_nu_goc": row[2],
                "link_baby_goc ": row[3],
                "link_da_swap": row[4],
                "id_toan_bo_su_kien": row[5],
                " noi_dung_su_kien ": row[6],
                "thoigian_sukien": row[7],
                "id_user": row[10],
                "tomLuocText": row[11],
                "count_comment": row[12],
                "count_view": row[13],
            }
            list_detail.append(data)
            total_item = len(list_detail)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_detail,
            "status": 200,
            "total_item": total_item,
        }
    )


# API NEW BABY
# get list detail category baby catwalk
@app.get(
    "/get/baby_catwalk/detail_category/{id}", tags=["detail_category_baby_catwalk"]
)
async def get_detail_category_baby_catwalk(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM listVideo_Catwalk WHERE IDCategories={id} "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id": row[0],
                "image_URL": row[1],
                "name_category": row[2],
                "image_thumnail": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_all_category": list_detail_category,
            "status": 200,
            "total_item": total_item,
        }
    )


# get list category baby funny
@app.get("/get/baby_funny/detail_category/{id}", tags=["detail_category_baby_funny"])
async def get_detail_category_baby_funny(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM listVideo_baby_new_vui_ve WHERE IDCategories={id} "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id": row[0],
                "image_URL": row[1],
                "name_category": row[2],
                "image_thumnail": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail_category": list_detail_category,
            "status": 200,
            "total_item": total_item,
        }
    )


# get list category baby hallowen
@app.get(
    "/get/baby_hallowen/detail_category/{id}", tags=["detail_category_baby_hallowen"]
)
async def get_detail_category_baby_hallowen(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM listVideo_Hallowen WHERE IDCategories={id}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id": row[0],
                "image_URL": row[1],
                "name_category": row[2],
                "image_thumnail": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail_category": list_detail_category,
            "status": 200,
            "total_item": total_item,
        }
    )


# get list category baby model
@app.get("/get/model/detail_category/{id}", tags=["detail_category_model"])
async def get_detail_category_model(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM listVideo_nguoi_mau WHERE IDCategories={id}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id": row[0],
                "image_URL": row[1],
                "name_category": row[2],
                "image_thumnail": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail_category": list_detail_category,
            "status": 200,
            "total_item": total_item,
        }
    )


# get list category baby future love
@app.get(
    "/get/baby_future_love/detail_category/{id}",
    tags=["detail_category_baby_future_love"],
)
async def get_detail_category_baby_future_love(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM listVideo_baby_future_love WHERE IDCategories={id}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id": row[0],
                "image_URL": row[1],
                "name_category": row[2],
                "image_thumnail": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail_category": list_detail_category,
            "status": 200,
            "total_item": total_item,
        }
    )


# get all baby catwalk
@app.get("/get/list_all_baby_catwalk/{id_user}", tags=["list_all_baby_catwalk"])
async def get_list_all_baby_catwalk(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk ='baby_catwalk' "
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk ='baby_catwalk'  ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC LIMIT {limit} OFFSET {offset} "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_data,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# get all baby funny
@app.get("/get/list_all_baby_funny/{id_user}", tags=["list_all_baby_funny"])
async def get_list_all_baby_funny(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk ='baby_funny' "
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk ='baby_funny'  ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC LIMIT {limit} OFFSET {offset} "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_data,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# get all baby hallowen
@app.get("/get/list_all_baby_hallowen/{id_user}", tags=["list_all_baby_hallowen"])
async def get_list_all_baby_hallowen(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk ='baby_hallowen' "
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk ='baby_hallowen'  ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC LIMIT {limit} OFFSET {offset} "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_data,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# get all model
@app.get("/get/list_all_model/{id_user}", tags=["list_all_model"])
async def get_list_all_model(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk ='model' "
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk ='model'  ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC LIMIT {limit} OFFSET {offset} "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_data,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# get all baby future_love
@app.get("/get/list_all_baby_future_love/{id_user}", tags=["list_all_baby_future_love"])
async def get_list_all_baby_future_love(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk ='baby_future_love' "
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_user = {id_user} AND loai_sk ='baby_future_love'  ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC LIMIT {limit} OFFSET {offset} "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_data,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# detail baby_catwalk
@app.get("/get/detail/baby_catwalk/{id_saved}", tags=["detail_baby_catwalk"])
async def detail_baby_catwalk(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_saved = {id_saved} AND loai_sk = 'baby_catwalk' ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail": list_data,
            "status": 200,
            "total_item": total_item,
        }
    )


# detail baby_funny
@app.get("/get/detail/baby_funny/{id_saved}", tags=["detail_baby_funny"])
async def detail_baby_funny(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_saved = {id_saved} AND loai_sk = 'baby_funny' ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail": list_data,
            "status": 200,
            "total_item": total_item,
        }
    )


# detail baby_hallowen
@app.get("/get/detail/baby_hallowen/{id_saved}", tags=["detail_baby_hallowen"])
async def detail_baby_hallowen(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_saved = {id_saved} AND loai_sk = 'baby_hallowen' ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail": list_data,
            "status": 200,
            "total_item": total_item,
        }
    )


# detail model
@app.get("/get/detail/model/{id_saved}", tags=["detail_model"])
async def detail_model(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_saved = {id_saved} AND loai_sk = 'model' ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail": list_data,
            "status": 200,
            "total_item": total_item,
        }
    )


# detail baby_future_love
@app.get("/get/detail/baby_future_love/{id_saved}", tags=["detail_baby_future_love"])
async def detail_baby_future_love(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM saved_sukien_video_image_growup WHERE id_saved = {id_saved} AND loai_sk = 'baby_future_love' ORDER BY `saved_sukien_video_image_growup`.`thoigian_sukien` ASC "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail": list_data,
            "status": 200,
            "total_item": total_item,
        }
    )


# API FANCY
# get list category fancy ai


@app.get("/get/fancy/category", tags=["list_category_fancyAI"])
async def get_list_category_fancyAI(request: Request):
    list_all_category = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT DISTINCT IDCategories, thongtin FROM listimage_fancy_ai"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id": row[0],
                "name_category": row[1],
            }
            list_all_category.append(data)
            total_item = len(list_all_category)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_all_category": list_all_category,
            "status": 200,
            "total_item": total_item,
        }
    )


@app.get("/get/fancy/detail_category/{id}", tags=["list_detail_category_fancyAI"])
async def get_list_detail_category_fancyAI(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM listimage_fancy_ai WHERE IDCategories={id}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {"id": row[5], "name_category": row[2], "image_URL": row[3]}
            list_detail_category.append(data)
            total_item = len(list_detail_category)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail_category": list_detail_category,
            "status": 200,
            "total_item": total_item,
        }
    )


# get detail swap fancy ai
@app.get("/get/detail/fancy_ai/{id_saved}", tags=["detail_fancy_ai"])
async def detail_fancy_ai(request: Request, id_saved: int):
    list_detail = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM  saved_sukien_alone WHERE id_saved ={id_saved}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_goc": row[1],
                "link_da_swap": row[2],
                "id_toan_bo_su_kien": row[3],
                " thoigian_sukien ": row[4],
                "device_them_su_kien": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_detail.append(data)
            total_item = len(list_detail)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_detail,
            "status": 200,
            "total_item": total_item,
        }
    )


# get all swap fancy ai
@app.get("/get/list_all_fancy_ai/{id_user}", tags=["list_all_fancy_ai"])
async def get_list_all_fancy_ai(request: Request, id_user: int):
    list_all_sk = []
    page = request.query_params.get("page", default=1)
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_alone WHERE id_user = {id_user} AND loai_sukien = 'fancy_face'"
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM  saved_sukien_alone WHERE id_user ={id_user} AND loai_sukien = 'fancy_face' ORDER BY `saved_sukien_alone`.`thoigian_sukien`  ASC LIMIT {limit} OFFSET {offset}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_src_goc": row[1],
                "link_da_swap": row[2],
                "id_toan_bo_su_kien": row[3],
                "thoigian_sukien": row[4],
                # "device_them_su_kien": row[5],
                # "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                # "id_itemplate": row[10],
                "loai_sk": row[11],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_all_sk,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# get list video category fancy mebau
@app.get("/get/fancy/detail_category/mebau/{id}", tags=["list_detail_category_mebau"])
async def get_list_detail_category_mebau(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM listVideo_me_bau WHERE IDCategories ={id}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {"id": row[5], "name_category": row[3], "image_URL": row[2]}
            list_detail_category.append(data)
            total_item = len(list_detail_category)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_all_category": list_detail_category,
            "status": 200,
            "total_item": total_item,
        }
    )


# get detail fancy mebau
@app.get("/get/detail/fancy_mebau/{id_saved}", tags=["detail_fancy_mebau"])
async def detail_fancy_mebau(request: Request, id_saved: int):
    list_detail = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = (
            f"SELECT * FROM  saved_sukien_video_image_mebau WHERE id_saved ={id_saved}"
        )
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                "id": row[10],
                "link_video_goc": row[1],
                "link_image ": row[2],
                "link_video_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_them_su_kien ": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_detail.append(data)
            total_item = len(list_detail)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_detail,
            "status": 200,
            "total_item": total_item,
        }
    )


# get all swap video fancy mebau
@app.get(
    "/get/list_all_swap_video_fancy_mebau/{id_user}",
    tags=["list_all_video_fancy_mebau"],
)
async def get_list_all_video_fancy_mebau(request: Request, id_user: int):
    list_all_sk = []
    page = request.query_params.get("page", default=1)
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_video_image_mebau WHERE id_user={id_user}"
        mycursor.execute(query_count)
        limit = 50
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM  saved_sukien_video_image_mebau WHERE id_user={id_user} ORDER BY `saved_sukien_video_image_mebau`.`thoigian_sukien`  ASC LIMIT {limit} OFFSET {offset}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image_goc": row[2],
                "link_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_them_su_kien": row[5],
                # "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_all_sk,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


@app.get("/get/fancy_mebau/category", tags=["list_category_fancyMeBau"])
async def get_list_category_fancyMeBau(request: Request):
    list_all_category = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT DISTINCT IDCategories, thongtin FROM listimage_pregnant"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id": row[0],
                "name_category": row[1],
            }
            list_all_category.append(data)
            total_item = len(list_all_category)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_all_category": list_all_category,
            "status": 200,
            "total_item": total_item,
        }
    )


# api detail category fancy mebau
@app.get("/get/fancy_mebau/detail_category/{id}", tags=["list_category_fancyMeBau"])
async def get_list_detail_category_fancyMeBau(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM listimage_pregnant WHERE IDCategories ={id}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id": row[0],
                "name_category": row[2],
                "image_URL": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_detail_category": list_detail_category,
            "status": 200,
            "total_item": total_item,
        }
    )


# api swap 2 image fancy me bau
@app.get(
    "/get/list_all_swap_2image_fancy_mebau/{id_user}",
    tags=["list_all_2image_fancy_mebau"],
)
async def get_list_all_2image_fancy_mebau(request: Request, id_user: int):
    list_all_sk = []
    page = request.query_params.get("page", default=1)
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query_count = f"SELECT COUNT(*) FROM saved_sukien_2_image WHERE id_user={id_user} AND loai_sukien = 'baby_fancy' "
        mycursor.execute(query_count)
        limit = 20
        total_page = math.ceil(mycursor.fetchall()[0][0] / limit)
        offset = (int(page) - 1) * limit
        query = f"SELECT * FROM  saved_sukien_2_image WHERE id_user={id_user}  AND loai_sukien = 'baby_fancy' ORDER BY `saved_sukien_2_image`.`thoigian_sukien`  ASC LIMIT {limit} OFFSET {offset}"
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_goc_image1": row[1],
                # "link_goc_image2": row[2],
                "link_da_swap": row[3],
                "id_toan_bo_su_kien": row[4],
                "thoigian_sukien": row[5],
                # "device_them_su_kien": row[6],
                # "ip_them_su_kien": row[7],
                "id_user": row[8],
                "count_comment": row[9],
                "count_view": row[10],
                # "id_template": row[11],
                "loai_sk": row[12],
                # "id_sk_album": row[14],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_all_sk,
            "status": 200,
            "total_item": total_item,
            "total_page": total_page,
        }
    )


# get detail fancy mebau
@app.get(
    "/get/detail/fancy_mebau_2image/{id_saved}", tags=["detail_fancy_mebau_2image"]
)
async def detail_fancy_mebau_2image(request: Request, id_saved: int):
    list_detail = []
    total_item = 0
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("connected to MYSQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[
                0
            ]  # Fetch one result and get the first column (database name)
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        query = f"SELECT * FROM  saved_sukien_2_image WHERE id_saved ={id_saved} AND loai_sukien = 'baby_fancy' "
        print("____Query_____", str(query))
        mycursor.execute(query)
        result2 = mycursor.fetchall()
        for row in result2:
            data = {
                "id_saved": row[0],
                "id": row[10],
                "link_src_goc": row[1],
                "link_tar_goc ": row[2],
                "link_da_swap": row[3],
                "id_toan_bo_su_kien": row[4],
                "thoigian_sukien": row[5],
                "device_them_su_kien ": row[6],
                "ip_them_su_kien": row[7],
                "id_user": row[8],
                "count_comment": row[9],
                "count_view": row[10],
                "loai_sk": row[12],
                "id_album_sk": row[14],
            }
            list_detail.append(data)
            total_item = len(list_detail)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return JSONResponse(
        content={
            "list_data": list_detail,
            "status": 200,
            "total_item": total_item,
        }
    )


# run app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server_fast:app", host="0.0.0.0", port=9090)
