from fastapi import FastAPI, Request, Header
import threading
import time
import asyncio
import shutil
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
    save_video_to_mysql_swap_imagevideo,
)
from func_vid import gen_video, gen_video_swap_imagevid
from login.func import send_mail_swap_done
from login.func import validate_token, generate_token
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, File, UploadFile
import uuid, os
from roop import core

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


@app.get("/getdata/swap/listimage", dependencies=[Depends(validate_token)])
async def gen_sk_swap_noel1(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    print("hello")
    folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    generated_uuid = uuid.uuid4().int
    id_sk_all = str(generated_uuid)[-12:]
    folder_path_list = f"/var/www/build_futurelove/image/image_sknoel/{list_folder}"
    folder_path = f"/var/www/build_futurelove/image/gen_image/{folder}"
    output_path = f"/var/www/build_futurelove/image/gen_image/{folder}/out/"
    src_1 = link1
    image_paths = []
    for filename in os.listdir(folder_path_list):
        # Kiểm tra nếu file là ảnh (có thể thêm các điều kiện kiểm tra phần mở rộng)
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            # Xây dựng đường dẫn đầy đủ và thêm vào danh sách
            image_path = os.path.join(folder_path_list, filename)
            image_paths.append(image_path)
    print(image_paths)
    os.makedirs(folder_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    for src_2_single in image_paths:
        shutil.copy(src_2_single, folder_path)  # copy ảnh ra file mới
    try:
        core.run(src_1, folder_path, output_path)
    except:
        JSONResponse(content={"sukien_list_image": "error images 1 have not face"})
    print(f"output_path: {output_path}")
    print(1)
    print("1.1")
    data_list = []
    if os.path.exists(output_path):
        # Lấy danh sách tên file trong thư mục
        file_names = os.listdir(output_path)
        if file_names:  # Check if the list is not empty
            print(file_names)
            for link in file_names:
                link_swap = f"{output_path}{link}"
                link_swap = link_swap.replace(
                    "/var/www/build_futurelove/", "https://photo.gachmen.org/"
                )
                print(link_swap)
                # Continue with the rest of your code...
                data = save_to_mysql_2_image(
                    link1,
                    link2,
                    link_swap,
                    device_them_su_kien,
                    ip_them_su_kien,
                    id_user,
                    "noel",
                    list_folder,
                    id_sk_all,
                )
                data_list.append(link_swap)
                print(data)
    else:
        print("The list of file names is empty.")
    return JSONResponse(content={"sukien_2_image": data, "link anh da swap": data_list})


@app.get("/getdata/swap/listimage/baby", dependencies=[Depends(validate_token)])
async def gen_sk_swap_baby_noel1(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    print("hello")
    folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    generated_uuid = uuid.uuid4().int
    id_sk_all = str(generated_uuid)[-12:]
    folder_path_list = "/var/www/build_futurelove/image/image_sknoel_baby/{list_folder}"
    folder_path = f"/var/www/build_futurelove/image/gen_image/{folder}"
    output_path = f"/var/www/build_futurelove/image/gen_image/{folder}/out/"
    src_1 = link1
    image_paths = []
    for filename in os.listdir(folder_path_list):
        # Kiểm tra nếu file là ảnh (có thể thêm các điều kiện kiểm tra phần mở rộng)
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            # Xây dựng đường dẫn đầy đủ và thêm vào danh sách
            image_path = os.path.join(folder_path_list, filename)
            image_paths.append(image_path)
    print(image_paths)
    os.makedirs(folder_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    for src_2_single in image_paths:
        shutil.copy(src_2_single, folder_path)  # copy ảnh ra file mới
        #     # print(folder_path)
        # print(src_2_single)
        print(f"src_1: {src_1}")
        print(f"src_2_single: {src_2_single}")
        print(f"output_path: {output_path}")
    try:
        core.run(src_1, folder_path, output_path)
    except:
        JSONResponse(content={"sukien_list_image": "error images 1 have not face"})
    print(f"output_path: {output_path}")
    print(1)
    print("1.1")
    data_list = []
    if os.path.exists(output_path):
        # Lấy danh sách tên file trong thư mục
        file_names = os.listdir(output_path)
        if file_names:  # Check if the list is not empty
            print(file_names)
            for link in file_names:
                link_swap = f"{output_path}{link}"
                link_swap = link_swap.replace(
                    "/var/www/build_futurelove/", "https://photo.gachmen.org/"
                )
                print(link_swap)
                # Continue with the rest of your code...
                data = save_to_mysql_2_image(
                    link1,
                    link2,
                    link_swap,
                    device_them_su_kien,
                    ip_them_su_kien,
                    id_user,
                    "noel_baby",
                    list_folder,
                    id_sk_all,
                )
                data_list.append(link_swap)
                print(data)
    else:
        print("The list of file names is empty.")
    return JSONResponse(content={"sukien_2_image": data, "link anh da swap": data_list})


def gen_video_swap_imagevid_santa(
    src_img, src_video, folder, device_them_su_kien, ip_them_su_kien, id_user
):
    print("hallo")
    folder_path = f"/var/www/build_futurelove/image/gen_video/{folder}"
    try:
        core.runvid(src_img, src_video, folder_path)
        link_vid = f"https://photo.gachmen.org/image/gen_video/{folder}/temp.mp4"
    except Exception as e:
        return f"Error occurred during video generation: {str(e)}"

    src_img = src_img.replace(
        "/var/www/build_futurelove/", "https://photo.gachmen.org/"
    )
    src_video = src_video.replace(
        "/var/www/build_futurelove/", "https://photo.gachmen.org/"
    )
    data = save_video_to_mysql_swap_imagevideo(
        src_img, src_video, link_vid, id_user, device_them_su_kien, ip_them_su_kien
    )

    return data


@app.post(
    "/getdata/genvideo/swap/imagevid/santa", dependencies=[Depends(validate_token)]
)
async def gen_video_swap_image_with_video_santa(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    src_img: str,
    src_vid: UploadFile = File(...),
):
    try:
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        print(folder)
        folder_path = f"/var/www/build_futurelove/image/gen_video/{folder}"
        print(folder_path)
        os.makedirs(folder_path, exist_ok=True)
        # Lưu tệp tin video
        src_video = os.path.join(folder_path, src_vid.filename)
        print(src_video)
        with open(src_video, "wb") as f:
            f.write(await src_vid.read())

        loop = asyncio.get_event_loop()
        # Sử dụng event loop của asyncio
        data = await loop.run_in_executor(
            executor,
            gen_video_swap_imagevid_santa,
            src_img,
            src_video,
            folder,
            device_them_su_kien,
            ip_them_su_kien,
            id_user,
        )

        return JSONResponse(content={"sukien_swap_video": data})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": f"error{e}"})


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


@app.get("/lovehistory/listvideo/santa/{trang}")
async def get_data_list_video_santa(request: Request, trang: int):
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
            query = "SELECT * from listVideo_santa"
            mycursor.execute(query)
            result2 = mycursor.fetchall()
            # print(result2)
        elif category != 0:
            print("halo2")
            query = "SELECT * FROM listVideo_santa WHERE IDCategories = %s"
            mycursor.execute(query, (category,))
            result2 = mycursor.fetchall()
            # print(result2)

        # print(result2)
        soPhanTuTrenMotTrang = 50
        soTrang = (len(result2) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang
        print(len(result2))
        print(soTrang)
        if trang <= soTrang:
            start = (trang - 1) * soPhanTuTrenMotTrang
            end = min(trang * soPhanTuTrenMotTrang, len(result2))
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5001)
