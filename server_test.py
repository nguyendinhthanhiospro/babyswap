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
)
from func_vid import gen_video
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


def gen_sk_swap_bikini_test(
    device_them_su_kien, ip_them_su_kien, id_user, list_folde, link1, link2, list_folder
):
    print("hello")
    folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    folder_path_list = (
        f"/media/thinkdiff/Seagate Hub/server_bikini/album_bikini/{list_folder}"
    )
    folder_path = (
        f"/media/thinkdiff/Seagate Hub/server_bikini/image_sukien_bikini/{folder}"
    )
    output_path = (
        f"/media/thinkdiff/Seagate Hub/server_bikini/image_sukien_bikini/{folder}/out/"
    )
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
    # core.run(src_1,image_paths, output_path)
    for src_2_single in image_paths:
        shutil.copy(src_2_single, folder_path)  # copy ảnh ra file mới
        #     # print(folder_path)
        # print(src_2_single)
        print(f"src_1: {src_1}")
        print(f"src_2_single: {src_2_single}")
        print(f"output_path: {output_path}")
    core.run(src_1, folder_path, output_path)
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
                    "/media/thinkdiff/Seagate Hub/server_bikini/",
                    "https://photo.gachmen.org/",
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
                    "bikini",
                    "bikini",
                )
                data_list.append(link_swap)
                print(data)
    else:
        print("The list of file names is empty.")
    # return JSONResponse(content={"sukien_2_image": data,"link anh da swap":data_list})
    return JSONResponse(content={"sukien_2_image": data_list})


@app.get("/getdata/swap/listimage/test", dependencies=[Depends(validate_token)])
async def gen_sk_swap_baby_noel1(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    if link1 is None:
        return "link header bi thieu roi kia"
    # Sử dụng event loop của asyncio
    loop = asyncio.get_event_loop()
    # data = gen_sk(request, link_full1, link_full2, device_them_su_kien, ip_them_su_kien, id_user, ten_nam, ten_nu)
    # # Chạy công việc bất đồng bộ trong executor
    data = await loop.run_in_executor(
        executor,
        gen_sk_swap_bikini_test,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
        list_folder,
        link1,
        link2,
    )

    return data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
