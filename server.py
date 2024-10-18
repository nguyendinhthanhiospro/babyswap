from fastapi import FastAPI, Request, Header
import threading
import time
import asyncio
from test_fun import gen_sk, gen_sk_ngam, gen_sk_swap, gen_sk_baby, gen_sk_noel
from server_wedding import *
from func_vid import gen_video
from login.func import send_mail_swap_done
from login.send_email import get_id_user_receved_email
from login.send_email import get_id_user_send_fakewedding_email
from login.func import validate_token, generate_token
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, File, UploadFile
import uuid, os
from server_fast import decode_token
from os import walk
import json
from os import listdir
from os.path import isfile, join


# pip install insightface==0.2.1 onnxruntime moviepy
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import jwt
from postmarker.core import PostmarkClient

# client = PostmarkClient(server_token="2c787e55-cd01-48d8-866a-f2915547adbf")
# secret_key = "wefhoiwfhsfiug9034bfjkg47vdjk"#token key
# ALGORITHM = "HS256"
# Create a ThreadPoolExecutor with a maximum of 2 concurrent processes
executor = ThreadPoolExecutor(max_workers=10)


@app.get("/getdata", dependencies=[Depends(validate_token)])
async def run_task_in_background(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    ten_nam: str,
    ten_nu: str,
    linknam: Optional[str] = Header(None),
    linknu: Optional[str] = Header(None),
):
    # link_full1 = 'https://raw.githubusercontent.com/thuykieu06012002/futurelove/main/111.jpg'
    # link_full2 = 'https://luv.vn/wp-content/uploads/2021/09/hinh-anh-nu-sinh-dep-nhat-69.jpg'
    # link_full1 = request.headers.get('Link1')
    # link_full2 = request.headers.get('Link2')
    # print(linknam, linknu)
    try:
        if linknam is None or linknu is None:
            return "link header header bi thieu roi kia"
        # Sử dụng event loop của asyncio
        loop = asyncio.get_event_loop()
        # data = gen_sk(request, link_full1, link_full2, device_them_su_kien, ip_them_su_kien, id_user, ten_nam, ten_nu)
        # # Chạy công việc bất đồng bộ trong executor
        data = await loop.run_in_executor(
            executor,
            gen_sk,
            linknam,
            linknu,
            device_them_su_kien,
            ip_them_su_kien,
            id_user,
            ten_nam,
            ten_nu,
        )

        return data
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}", "status": 500})


@app.get("/getdata/noel", dependencies=[Depends(validate_token)])
async def run_task_in_background(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    ten_nam: str,
    ten_nu: str,
    linknam: Optional[str] = Header(None),
    linknu: Optional[str] = Header(None),
):
    # link_full1 = 'https://raw.githubusercontent.com/thuykieu06012002/futurelove/main/111.jpg'
    # link_full2 = 'https://luv.vn/wp-content/uploads/2021/09/hinh-anh-nu-sinh-dep-nhat-69.jpg'
    # link_full1 = request.headers.get('Link1')
    # link_full2 = request.headers.get('Link2')

    if linknam is None or linknu is None:
        return "link header header bi thieu roi kia"
    # Sử dụng event loop của asyncio
    loop = asyncio.get_event_loop()
    # data = gen_sk(request, link_full1, link_full2, device_them_su_kien, ip_them_su_kien, id_user, ten_nam, ten_nu)
    # # Chạy công việc bất đồng bộ trong executor
    data = await loop.run_in_executor(
        executor,
        gen_sk_noel,
        linknam,
        linknu,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
        ten_nam,
        ten_nu,
    )

    return data


@app.get("/getdata/skngam", dependencies=[Depends(validate_token)])
async def run_task_in_background(
    id_toan_bo_su_kien: str,
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    ten_nam: str,
    ten_nu: str,
    folder: Optional[str] = Header(None),
    linknam: Optional[str] = Header(None),
    linknu: Optional[str] = Header(None),
):
    try:
        # link_full1 = 'https://raw.githubusercontent.com/thuykieu06012002/futurelove/main/111.jpg'
        # link_full2 = 'https://luv.vn/wp-content/uploads/2021/09/hinh-anh-nu-sinh-dep-nhat-69.jpg'
        # Sử dụng event loop của asyncio
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            executor,
            gen_sk_ngam,
            linknam,
            linknu,
            id_toan_bo_su_kien,
            folder,
            device_them_su_kien,
            ip_them_su_kien,
            id_user,
            ten_nam,
            ten_nu,
        )
        # data = gen_sk_ngam(id_toan_bo_su_kien, folder, device_them_su_kien, ip_them_su_kien, id_user, ten_nam,ten_nu)
        link = f"https://makewedding.online/detail/{id_toan_bo_su_kien}/1"
        await get_id_user_receved_email(id_user, link)
        return data
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}", "status": 500})


@app.get("/getdata/swap/2/image", dependencies=[Depends(validate_token)])
async def run_task_in_background(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    try:
        # link_full1 = 'https://raw.githubusercontent.com/thuykieu06012002/futurelove/main/111.jpg'
        # link_full2 = 'https://luv.vn/wp-content/uploads/2021/09/hinh-anh-nu-sinh-dep-nhat-69.jpg'
        # link_full1 = request.headers.get('Link1')
        # link_full2 = request.headers.get('Link2')

        if link1 is None or link2 is None:
            return "link header bi thieu roi kia"
        # Sử dụng event loop của asyncio
        loop = asyncio.get_event_loop()
        # data = gen_sk(request, link_full1, link_full2, device_them_su_kien, ip_them_su_kien, id_user, ten_nam, ten_nu)
        # # Chạy công việc bất đồng bộ trong executor
        data = await loop.run_in_executor(
            executor,
            gen_sk_swap,
            link1,
            link2,
            device_them_su_kien,
            ip_them_su_kien,
            id_user,
        )

        return data
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}", "status": 500})


# @app.get("/getdata/genvideo")
# async def run_task_in_background( id_video: str,  device_them_su_kien: str,ip_them_su_kien: str,id_user: int,
#                                  link_img: str, ten_video: str):
#     # link_full1 = 'https://raw.githubusercontent.com/thuykieu06012002/futurelove/main/111.jpg'
#     # link_full2 = 'https://luv.vn/wp-content/uploads/2021/09/hinh-anh-nu-sinh-dep-nhat-69.jpg'
#     loop = asyncio.get_event_loop()
#     # Sử dụng event loop của asyncio
#     data = await loop.run_in_executor(executor, gen_video, id_user, id_video, link_img, ten_video, device_them_su_kien, ip_them_su_kien)
#     return data


@app.get("/getdata/sukien/baby", dependencies=[Depends(validate_token)])
async def run_task_in_background(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    linknam: Optional[str] = Header(None),
    linknu: Optional[str] = Header(None),
):
    print(linknam)
    print(linknu)
    # link_full1 = 'https://raw.githubusercontent.com/thuykieu06012002/futurelove/main/111.jpg'
    # link_full2 = 'https://luv.vn/wp-content/uploads/2021/09/hinh-anh-nu-sinh-dep-nhat-69.jpg'
    # link_full1 = request.headers.get('Link1')
    # link_full2 = request.headers.get('Link2')
    try:
        if linknam is None or linknu is None:
            return "link header header bi thieu roi kia"
        # Sử dụng event loop của asyncio
        loop = asyncio.get_event_loop()
        # data = gen_sk(request, link_full1, link_full2, device_them_su_kien, ip_them_su_kien, id_user, ten_nam, ten_nu)
        # # Chạy công việc bất đồng bộ trong executor
        data = await loop.run_in_executor(
            executor,
            gen_sk_baby,
            linknam,
            linknu,
            device_them_su_kien,
            ip_them_su_kien,
            id_user,
        )

        return data
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}", "status": 500})


# SWAP IMAGE TO ALBUM WEDDING


@app.get("/getdata/swap/listimage_wedding", dependencies=[Depends(validate_token)])
async def run_task_in_background_growup_wedding(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    print(link1)
    generated_uuid = uuid.uuid4().int
    id_sk_all = str(generated_uuid)[-12:]
    link = f"https://makewedding.online/timeline/event/{id_sk_all}"
    loop = asyncio.get_event_loop()
    print(link1)
    print(link2)

    data, folder_anh = await loop.run_in_executor(
        executor,
        gen_sk_swap_wedding_fix,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
        list_folder,
        id_sk_all,
        link1,
        link2,
    )
    # await generatex(folder_anh)  # ham tao video tu anh tra ve duong dan den thu muc chua video
    # await zip_images(folder_anh,list_folder)  # ham zip file anh va video, tra ve duong dan den file zip
    await get_id_user_send_fakewedding_email(id_user, link)

    # return JSONResponse(content={"sukien_image": data})
    return data


@app.get("/getdata/makevideofromfolder", dependencies=[Depends(validate_token)])
async def run_task_in_background_growup_wedding(
    device_them_su_kien: str, ip_them_su_kien: str, id_user: str, folderLuu: str
):
    generated_uuid = uuid.uuid4().int
    id_video_gen = str(generated_uuid)[-12:]
    parent_folder = os.path.dirname(folderLuu)
    video_folder = os.path.join(parent_folder, "video")
    output_path = video_folder + "/output_video_1080p.mp4"
    linkURL_download = output_path.replace(
        "/var/www/build_futurelove", "https://photo.gachmen.org"
    )

    link = f"https://makewedding.online/timeline/video/{id_video_gen}"
    loop = asyncio.get_event_loop()

    data_anh = await loop.run_in_executor(executor, generatex, folderLuu)

    await get_id_user_send_fakewedding_email(id_user, linkURL_download)

    # return JSONResponse(content={"sukien_image": data})
    return data_anh


@app.get("/getdata/Download", dependencies=[Depends(validate_token)])
async def run_task_in_background_growup_wedding(
    device_them_su_kien: str, ip_them_su_kien: str, id_user: str, folderLuu: str
):
    generated_uuid = uuid.uuid4().int
    id_download = str(generated_uuid)[-12:]
    link = f"https://makewedding.online/timeline/image/{id_download}"
    loop = asyncio.get_event_loop()

    zip_name = "video_image_" + str(id_user) + ".zip"
    data_zip = await loop.run_in_executor(executor, zip_images, folderLuu, zip_name)

    # return JSONResponse(content={"sukien_image": data})
    return data_zip


def json_list(list):
    lst = []
    for link in list:
        lst.append(link)
    return json.dumps(lst)


@app.get("/getdata/swap/listimage_alone", dependencies=[Depends(validate_token)])
async def run_task_in_background_alone(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    link1: Optional[str] = Header(None),
):
    generated_uuid = uuid.uuid4().int
    id_sk_all = str(generated_uuid)[-12:]
    link = f"https://makewedding.online/timeline/event/{id_sk_all}"
    loop = asyncio.get_event_loop()
    print(link)

    folder_anh = await loop.run_in_executor(
        executor,
        gen_sk_swap_alone,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
        list_folder,
        id_sk_all,
        link1,
    )
    # await get_id_user_send_fakewedding_email(id_user, link)
    listImage = []
    for dirpath, dirnames, filenames in walk(folder_anh):
        print(filenames)
        break

    # return JSONResponse(content={"sukien_image": data})
    for item in filenames:
        pathfolder = folder_anh.replace(
            "/var/www/build_futurelove/", "https://photo.gachmen.org/"
        )
        pathFile = pathfolder + "/" + item
        listImage.append(pathFile)
    return json_list(listImage)


@app.get("/getdata/event_categories", dependencies=[Depends(validate_token)])
async def run_task_in_background_alone_ket_qua(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
):
    loop = asyncio.get_event_loop()

    data = await loop.run_in_executor(
        executor,
        get_images_alone,
        list_folder,
    )

    return data


@app.get("/getdata/list_categories", dependencies=[Depends(validate_token)])
async def run_task_in_background_list_categories(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
):
    loop = asyncio.get_event_loop()

    data = await loop.run_in_executor(
        executor,
        get_list_categoris_alone,
        list_folder,
    )

    return data


@app.get("/getdata/image_from_folder")
async def image_from_folder(
    list_folder: str,
):
    print(list_folder)
    arr = []
    for directory_name, _, files in os.walk(list_folder):
        for file in files:
            arr.append(os.path.join(list_folder, file))

    for f in arr:
        print(f)
    return {"linkImage": arr}


@app.get("/getdata/save_thiep_cuoi", dependencies=[Depends(validate_token)])
async def run_task_in_background_thiep_cuoi(
    name1: str,
    name2: str,
    date: str,
    location: str,
    link_location: str,
    status: str,
    id_user: int,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):

    generated_uuid = uuid.uuid4().int
    id_sk_all = str(generated_uuid)[-12:]
    link = f"https://makewedding.online/invitation/{id_sk_all}"
    # Chọn ngẫu nhiên một con số từ 1 đến 45
    random_number = random.randint(1, 45)
    list_folder = f"weddingface{random_number}"
    qr_code = make_qr(link, id_user)

    loop = asyncio.get_event_loop()
    link_image = await loop.run_in_executor(
        executor,
        gen_sk_swap_thiep_cuoi,
        id_user,
        list_folder,
        link1,
        link2,
    )

    data = await loop.run_in_executor(
        executor,
        get_thiep_cuoi,
        name1,
        name2,
        date,
        link_image,
        location,
        link_location,
        qr_code,
        status,
        id_user,
        link1,
        link2,
    )

    return data


@app.get("/getdata/swap/event_iudi")
async def run_task_in_background_swap_iudi(
    id_user: int,
    gioi_tinh: str,
    link1: Optional[str] = Header(None),
):
    id_user = 262
    random_number = random.randint(1, 45)
    list_folder = f"weddingface{random_number}"
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(
        executor,
        gen_sk_swap_iudi,
        id_user,
        gioi_tinh,
        list_folder,
        link1,
    )
    listImage = []
    for dirpath, dirnames, filenames in walk(data):
        print(filenames)
        break

    # return JSONResponse(content={"sukien_image": data})
    for item in filenames:
        pathfolder = data.replace(
            "/var/www/build_futurelove/", "https://photo.gachmen.org/"
        )
        pathFile = pathfolder + "/" + item
        listImage.append(pathFile)
    return {"images": listImage}


# BABY GROW UP


@app.get("/getdata/swap/listimage_baby_family", dependencies=[Depends(validate_token)])
async def run_task_in_background_listimage_baby_family(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    print(link1)
    generated_uuid = uuid.uuid4().int
    id_sk_all = str(generated_uuid)[-12:]
    link = f"https://makewedding.online/timeline/event/{id_sk_all}"
    loop = asyncio.get_event_loop()
    print(link1)
    print(link2)

    data = await loop.run_in_executor(
        executor,
        gen_sk_swap_baby_family,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
        list_folder,
        id_sk_all,
        link1,
        link2,
    )
    # await generatex(folder_anh)  # ham tao video tu anh tra ve duong dan den thu muc chua video
    # await zip_images(folder_anh,list_folder)  # ham zip file anh va video, tra ve duong dan den file zip
    await get_id_user_send_fakewedding_email(id_user, link)
    print(data)
    # return JSONResponse(content={"sukien_image": data})
    return data


@app.get("/getdata/swap/listimage_baby_newborn", dependencies=[Depends(validate_token)])
async def run_task_in_background_listimage_baby_newborn(
    device_them_su_kien: str,
    ip_them_su_kien: str,
    id_user: int,
    list_folder: str,
    link1: Optional[str] = Header(None),
    link2: Optional[str] = Header(None),
):
    print(link1)
    generated_uuid = uuid.uuid4().int
    id_sk_all = str(generated_uuid)[-12:]
    link = f"https://makewedding.online/timeline/event/{id_sk_all}"
    loop = asyncio.get_event_loop()
    print(link1)
    print(link2)

    data = await loop.run_in_executor(
        executor,
        gen_sk_swap_baby_newborn,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
        list_folder,
        id_sk_all,
        link1,
        link2,
    )
    # await generatex(folder_anh)  # ham tao video tu anh tra ve duong dan den thu muc chua video
    # await zip_images(folder_anh,list_folder)  # ham zip file anh va video, tra ve duong dan den file zip
    await get_id_user_send_fakewedding_email(id_user, link)
    # print(data)
    # return JSONResponse(content={"sukien_image": data})
    return data


# SANTA APP


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=6789)
