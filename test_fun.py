import os, re
import random
import shutil
from fastapi.responses import JSONResponse
import torch

# from test_wholeimage_swapmulti import swapface_image
import base64, requests


import asyncio
from fastapi.responses import JSONResponse
from queue import Queue
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
import threading
from roop import core

# from threading import Pool
import uuid
import concurrent.futures
from fastapi import Depends, HTTPException, Header
from typing import Optional


def download_image_link(url, filename):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


def download_image(url, folder):
    link, filename = url
    tar_nam_folder = os.path.join(folder, "tar_nam")
    tar_nu_folder = os.path.join(folder, "tar_nu")

    if "nam" in filename:
        file_path = os.path.join(tar_nam_folder, filename)
    elif "nu" in filename:
        file_path = os.path.join(tar_nu_folder, filename)
    else:
        # Xử lý trường hợp khác (nếu cần)
        return

    with requests.get(link, stream=True) as response:
        response.raise_for_status()
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


def upload_image(file_info):
    image_path, api_key = file_info
    filename = os.path.basename(image_path)
    direct_link = upload_image_to_imgbb(image_path, api_key)
    i = filename.split("_")[1].split(".")[0]
    return [direct_link, i]


def upload_images_from_folder(folder, api_key):
    file_list = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder, filename)
            file_list.append((image_path, api_key))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(upload_image, file_list)

    return results


def check_imgbb_api_key(api_key):
    url = f"https://api.imgbb.com/1/upload?key={api_key}"
    response = requests.get(url)
    if str(response.content)[41:60] == "Empty upload source":
        return True
    else:
        return False


api_key = "1bdabc1c147e864f326b9ecb3eb4dd50"


def upload_image_to_imgbb(image_path, api_key):
    # Tải dữ liệu ảnh
    with open(image_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": api_key,
            "image": base64.b64encode(file.read()),
        }
        # Gửi yêu cầu POST tải lên ảnh đến API của ImgBB
        response = requests.post(url, payload)

    # Trích xuất đường dẫn trực tiếp đến ảnh từ JSON response
    json_data = response.json()
    direct_link = json_data["data"]["url"]

    # Trả về đường dẫn trực tiếp đến ảnh
    return direct_link


def swap(
    src_nam,
    src_nu,
    url_list_nam,
    url_list_nu,
    folder,
    input_tar_nam,
    input_tar_nu,
    swapsk,
):
    if url_list_nam:
        try:
            # Tạo đường dẫn và sao chép tệp tin video và hình ảnh vào thư mục tạm thời
            folder_path = f"/var/www/build_futurelove/image/gen_image/{folder}"
            # print("pass1")
            os.makedirs(input_tar_nam, exist_ok=True)
            os.makedirs(input_tar_nu, exist_ok=True)
            # print("pass2")

            for source_file, new_filename in url_list_nam:
                destination_file = input_tar_nam + new_filename + ".jpg"
                shutil.copy(source_file, destination_file)
            # print("pass3")

            for source_file, new_filename in url_list_nu:
                destination_file = input_tar_nu + new_filename + ".jpg"
                shutil.copy(source_file, destination_file)

            # print("Images copied successfully.")

            os.makedirs(f"{folder_path}/{swapsk}", exist_ok=True)
            # ouput_video = f"./output/"
            ouput_tar = f"{folder_path}/{swapsk}/"
            # print("pass4")

            core.run(src_nam, input_tar_nam, ouput_tar)
            core.run(src_nu, input_tar_nu, ouput_tar)

            return folder_path
        except Exception as e:
            return f"Error when swap: {str(e)}, maybe can not found image!!"
    else:
        return None


def list_link(random_data):
    url_list_nam = []
    url_list_nu = []
    for i, data in enumerate(random_data):
        if data["nam"] != "0":
            name = f"nam_{i+1}"
            url_list_nam.append((data["nam"], name))
        if data["nu"] != "0":
            name = f"nu_{i+1}"
            url_list_nu.append((data["nu"], name))
    return url_list_nam, url_list_nu


def gen_list_data(random_data):
    list_data_gen = []
    for i, data in enumerate(random_data):
        id_value = i + 1  # Lấy giá trị "id" từ tên ảnh

        vtrinam_value = (
            data["vtrinam"] if data["vtrinam"] == "0" else "1"
        )  # Lấy giá trị "vtrinam"
        list_data_gen.append({"id": id_value, "vtrinam": vtrinam_value})
    return list_data_gen


def gen_sk(
    link_nam, link_nu, device_them_su_kien, ip_them_su_kien, id_user, ten_nam, ten_nu
):
    folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    folder_path = f"/var/www/build_futurelove/image/gen_image/{folder}"
    src_nam = link_nam
    src_nu = link_nu
    random_data = get_random_data()
    url_list_nam = list_link(random_data)[0]
    url_list_nu = list_link(random_data)[1]

    # if url_list is None:
    #     random_data = []
    #     random_data = get_random_data()
    #     url_list = list_link(random_data)

    print("Start Processing....")
    swapsk = "sk_swaped"
    input_tar_nam = f"{folder_path}/sk_tar_nam/"
    input_tar_nu = f"{folder_path}/sk_tar_nu/"

    # path = swap(src_nam, src_nu, url_list_nam, url_list_nu, folder,input_tar_nam, input_tar_nu, swapsk)
    try:
        path = swap(
            src_nam,
            src_nu,
            url_list_nam,
            url_list_nu,
            folder,
            input_tar_nam,
            input_tar_nu,
            swapsk,
        )
    except Exception as e:
        # Xử lý lỗi tại đây
        print("Error when swap():", str(e))

    list_data = []
    list_data = gen_list_data(random_data)

    print("pathneeeeeee", path)
    if path.startswith("Error when swap"):
        return path
    else:
        swap_path = f"{path}/{swapsk}/"
        merge_image(list_data, swap_path)
        insert_svg_logo(swap_path)

        link_path = f"https://photo.gachmen.org/image/gen_image/{folder}/sk_swaped/"
        for item in random_data:
            item["nam"] = item["nam"].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            item["nu"] = item["nam"].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            id_value = str(item["id_num"])
            item["folder"] = folder
            for filename in os.listdir(swap_path):

                if filename.startswith("AI_gen_") and filename.endswith(".jpg"):
                    file_id = filename.split("_")[2].split(".")[0]
                    if file_id == id_value:
                        item["link_img"] = link_path + filename

    torch.cuda.empty_cache()
    link1 = link_nam.replace("/var/www/build_futurelove", "https://photo.gachmen.org")
    link2 = link_nu.replace("/var/www/build_futurelove", "https://photo.gachmen.org")
    data = save_to_mysql(
        random_data,
        link1,
        link2,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
        ten_nam,
        ten_nu,
    )
    for items in data:
        items["folder"] = folder

    # return random_data
    return JSONResponse(content={"sukien": data})

    # return jsonify(sukien=data)


def gen_sk_ngam(
    link_nam,
    link_nu,
    id_toan_bo_su_kien,
    folder,
    device_them_su_kien,
    ip_them_su_kien,
    id_user,
    ten_nam,
    ten_nu,
):
    folder_path = f"/var/www/build_futurelove/image/gen_image/{folder}"
    src_nam = link_nam
    src_nu = link_nu

    random_data = get_random_data_skngam()
    url_list_nam = list_link(random_data)[0]
    url_list_nu = list_link(random_data)[1]

    # print(url_list_nam)
    # print(url_list_nu)
    print("Start Processing....")
    swapsk = "skngam_swaped"
    input_tar_nam = f"{folder_path}/skngam_tar_nam/"
    input_tar_nu = f"{folder_path}/skngam_tar_nu/"
    # path = swap(src_nam, src_nu, url_list_nam, url_list_nu, folder,input_tar_nam, input_tar_nu, swapsk)
    try:
        path = swap(
            src_nam,
            src_nu,
            url_list_nam,
            url_list_nu,
            folder,
            input_tar_nam,
            input_tar_nu,
            swapsk,
        )
    except Exception as e:
        print("Error when swap():", str(e))
    list_data = []
    list_data = gen_list_data(random_data)

    print("pathneeeeeee", path)
    if path.startswith("Error when swap"):
        return path
    else:
        swap_path = f"{path}/{swapsk}/"
        merge_image(list_data, swap_path)
        insert_svg_logo(swap_path)

        link_path = f"https://photo.gachmen.org/image/gen_image/{folder}/skngam_swaped/"
        for item in random_data:
            item["nam"] = item["nam"].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            item["nu"] = item["nam"].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            id_value = str(item["id_num"])
            item["folder"] = folder
            for filename in os.listdir(swap_path):
                if filename.startswith("AI_gen_") and filename.endswith(".jpg"):
                    file_id = filename.split("_")[2].split(".")[0]
                    if file_id == id_value:
                        item["link_img"] = link_path + filename

    # torch.cuda.empty_cache()
    link1 = f"https://photo.gachmen.org/image/image_user/{id_user}/nam/{os.path.basename(link_nam)}"
    link2 = f"https://photo.gachmen.org/image/image_user/{id_user}/nu/{os.path.basename(link_nu)}"
    data = save_to_mysql_skngam(
        random_data,
        link1,
        link2,
        id_toan_bo_su_kien,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
        ten_nam,
        ten_nu,
    )
    # for items in data:
    #     print(items['link_img'])

    # return random_data
    return JSONResponse(content={"sukien": data})


def gen_sk_swap(link_1, link_2, device_them_su_kien, ip_them_su_kien, id_user):
    print("hello")
    torch.cuda.empty_cache()
    folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    folder_path = f"/var/www/build_futurelove/image/gen_image/{folder}"
    output_path = f"/var/www/build_futurelove/image/gen_image/{folder}/out/"
    src_1 = link_1
    os.makedirs(folder_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    print(link_2)
    shutil.copy(link_2, folder_path)
    core.run(src_1, folder_path, output_path)
    if os.path.exists(folder_path):
        # Lấy danh sách tên file trong thư mục
        file_names = os.listdir(output_path)
        link_swap = f"{output_path}{file_names[0]}"
        link_swap = link_swap.replace(
            "/var/www/build_futurelove/", "https://photo.gachmen.org/"
        )
    else:
        print("Đường dẫn thư mục không tồn tại.")

    data = save_to_mysql_2_image(
        link_1,
        link_2,
        link_swap,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
        "swap_2face",
        "null",
        "null",
    )
    torch.cuda.empty_cache()
    return JSONResponse(content={"sukien_2_image": data})


def find_images(image_list, folder_path):
    # Pattern để tìm kiếm tên tệp tin ảnh
    pattern = re.compile(r"(nam|nu)_(\d+)\.jpg")

    found_images = []

    for image_info in image_list:
        image_id = image_info["id"]

        # Tìm kiếm tệp tin ảnh theo pattern
        for filename in os.listdir(folder_path):
            match = pattern.match(filename)
            if match:
                gender = match.group(1)  # Lấy giá trị "nam" hoặc "nu"
                file_id = match.group(2)
                if file_id == image_id:
                    image_path = os.path.join(folder_path, filename)
                    found_images.append(gender)
                    found_images.append(image_path)
                    break
        else:
            found_images.append({"ID": image_id, "Thông báo": "Không tìm thấy ảnh"})

    return found_images


# , device_them_su_kien, ip_them_su_kien, id_user, ten_nam, ten_nu


def gen_sk_baby(link_nam, link_nu, device_them_su_kien, ip_them_su_kien, id_user):
    folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    folder_path = f"/var/www/build_futurelove/image/gen_image/{folder}"
    os.makedirs(folder_path, exist_ok=True)
    src_nam = link_nam
    src_nu = link_nu

    random_data = get_random_data_swap_baby()

    folder_baby_path = "/var/www/build_futurelove/image/image_sk_baby/"

    results = find_images(random_data, folder_baby_path)
    shutil.copy(results[1], folder_path)
    output_path = f"/var/www/build_futurelove/image/gen_image/{folder}/out/"
    os.makedirs(output_path, exist_ok=True)
    if results[0] == "nam":
        core.run(src_nam, folder_path, output_path)
    else:
        core.run(src_nu, folder_path, output_path)

    if os.path.exists(output_path):
        # Lấy danh sách tên file trong thư mục
        file_names = os.listdir(output_path)
        link_swap = f"{output_path}{file_names[0]}"
        link_swap = link_swap.replace(
            "/var/www/build_futurelove/", "https://photo.gachmen.org/"
        )
    else:
        print("Đường dẫn thư mục không tồn tại.")
    src_nam = src_nam.replace(
        "/var/www/build_futurelove/", "https://photo.gachmen.org/"
    )
    src_nu = src_nu.replace("/var/www/build_futurelove/", "https://photo.gachmen.org/")
    src_baby = results[1].replace(
        "/var/www/build_futurelove/", "https://photo.gachmen.org/"
    )
    random_data.append(
        {
            "link_nam_goc": src_nam,
            "link_nu_goc": src_nu,
            "link_baby_goc": src_baby,
            "link_da_swap": link_swap,
            "nguoi_swap": results[0],
        }
    )

    result = {}
    for item in random_data:
        result.update(item)
    data_src = []
    data_src.append(result)
    data = save_to_mysql_swap_baby(
        data_src, device_them_su_kien, ip_them_su_kien, id_user
    )

    return JSONResponse(content={"sukien_baby": data})


def gen_sk_noel(
    link_nam, link_nu, device_them_su_kien, ip_them_su_kien, id_user, ten_nam, ten_nu
):
    folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
    folder_path = f"/var/www/build_futurelove/image/gen_image/{folder}"
    src_nam = link_nam
    src_nu = link_nu

    random_data = get_random_data()
    url_list_nam = list_link(random_data)[0]
    url_list_nu = list_link(random_data)[1]

    # if url_list is None:
    #     random_data = []
    #     random_data = get_random_data()
    #     url_list = list_link(random_data)

    print("Start Processing....")
    swapsk = "sk_swaped"
    input_tar_nam = f"{folder_path}/sk_noel_tar_nam/"
    input_tar_nu = f"{folder_path}/sk_noel_tar_nu/"
    # path = swap(src_nam, src_nu, url_list_nam, url_list_nu, folder,input_tar_nam, input_tar_nu, swapsk)
    try:
        path = swap(
            src_nam,
            src_nu,
            url_list_nam,
            url_list_nu,
            folder,
            input_tar_nam,
            input_tar_nu,
            swapsk,
        )
    except Exception as e:
        # Xử lý lỗi tại đây
        print("Error when swap():", str(e))
    list_data = []
    list_data = gen_list_data(random_data)

    print("pathneeeeeee", path)
    if path.startswith("Error when swap"):
        return path
    else:
        swap_path = f"{path}/{swapsk}/"
        merge_image(list_data, swap_path)
        insert_svg_logo(swap_path)

        link_path = (
            f"https://photo.gachmen.org/image/gen_image/{folder}/sk_noel_swaped/"
        )
        for item in random_data:
            item["nam"] = item["nam"].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            item["nu"] = item["nam"].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            id_value = str(item["id_num"])
            item["folder"] = folder
            for filename in os.listdir(swap_path):
                if filename.startswith("AI_GEN_") and filename.endswith(".jpg"):
                    file_id = filename.split("_")[1].split(".")[0]
                    if file_id == id_value:
                        item["link_img"] = link_path + filename

    # torch.cuda.empty_cache()
    link1 = f"https://photo.gachmen.org/image/image_user/{id_user}/nam/{os.path.basename(link_nam)}"
    link2 = f"https://photo.gachmen.org/image/image_user/{id_user}/nu/{os.path.basename(link_nu)}"
    data = save_to_mysql(
        random_data,
        link1,
        link2,
        device_them_su_kien,
        ip_them_su_kien,
        id_user,
        ten_nam,
        ten_nu,
    )
    for items in data:
        items["folder"] = folder

    # return random_data
    return JSONResponse(content={"sukien": data})

    # return jsonify(sukien=data)


def get_random_data_noel():
    return
