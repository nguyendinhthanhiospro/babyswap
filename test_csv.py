import csv
import random
import time
import os
from PIL import Image
from gensk import skgendata, skgendatangam, skgendatanoel
from datetime import datetime
import csv
import asyncio
import mysql.connector
import uuid
import cairosvg
from PIL import Image
import io

# user_id = snowflake.generate_id()

config = {
    "user": "sonpro",
    "password": "Ratiendi89",
    "host": "localhost",
    "port": 3306,
    "database": "FutureLove4",
    "auth_plugin": "mysql_native_password",
}


def get_random_data():
    result_data = []
    list_sk = skgendata()
    print(list_sk)
    seed = int(time.time())

    # Thiết lập seed cho hàm random
    random.seed(seed)
    i = 0

    folder = "/var/www/build_futurelove/image/image_sk"

    for sk_filename in list_sk:
        csv_file_path = f"./sukien/{sk_filename}.csv"
        random_ids = random.sample(range(1, 25), 1)
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.DictReader(csvfile)

            for row in csv_reader:
                # print("ROW___" + str(row))
                # print("random_ids___" + str(random_ids))
                id = int(row["id"]) in random_ids
                if id != 0:
                    folder_path_nam = (
                        f'{folder}/{sk_filename}/{sk_filename}_nam/{row["id"]}.jpg'
                    )
                    folder_path_nu = (
                        f'{folder}/{sk_filename}/{sk_filename}_nu/{row["id"]}.jpg'
                    )
                    data = {
                        "id": row["id"],
                        "id_num": i + 1,
                        "tensukien": sk_filename,
                        "thongtin": row["thongtin"],
                        "image": row["image"],
                        "nu": folder_path_nu,
                        "nam": folder_path_nam,
                        "vtrinam": row["vtrinam"],
                        "tomLuocText": row["tomLuocText"],
                    }
                    i = i + 1
                    result_data.append(data)

    return result_data


def get_random_data_swap_baby():
    result_data = []
    seed = int(time.time())
    # Thiết lập seed cho hàm random
    random.seed(seed)
    csv_file_path = f"./sukien/file1.csv"
    random_ids = random.sample(range(1, 100), 1)
    with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if int(row["id"]) == random_ids[0]:
                data = {
                    "id": row["id"],
                    "thongtin": row["thongtin"],
                    "tomLuocText": row["tomLuocText"],
                }
                result_data.append(data)
                break
    return result_data


def get_random_data_check(sk_filename):
    result_data = []
    seed = int(time.time())

    # Thiết lập seed cho hàm random
    random.seed(seed)
    i = 0

    csv_file_path = f"./sukien/{sk_filename}.csv"

    with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            if int(row["id"]) in range(1, 26):
                data = {
                    "id": row["id"],
                    "id_num": i + 1,
                    "tensukien": sk_filename,
                    "thongtin": row["thongtin"],
                    "image": row["image"],
                    "nu": row["nu"],
                    "nam": row["nam"],
                    "vtrinam": row["vtrinam"],
                    "tomLuocText": row["tomLuocText"],
                }
                i = i + 1
                result_data.append(data)

    return result_data


def get_random_data_skngam():
    result_data = []
    list_sk = skgendatangam()
    print(list_sk)
    seed = int(time.time())

    # Thiết lập seed cho hàm random
    random.seed(seed)
    i = 0
    folder = "/var/www/build_futurelove/image/image_sk"
    for sk_filename in list_sk:
        csv_file_path = f"./sukien/{sk_filename}.csv"
        random_ids = random.sample(range(1, 25), 1)
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.DictReader(csvfile)

            for row in csv_reader:
                if int(row["id"]) in random_ids:
                    folder_path_nam = (
                        f'{folder}/{sk_filename}/{sk_filename}_nam/{row["id"]}.jpg'
                    )
                    folder_path_nu = (
                        f'{folder}/{sk_filename}/{sk_filename}_nu/{row["id"]}.jpg'
                    )
                    data = {
                        "id": row["id"],
                        "id_num": i + 1,
                        "tensukien": sk_filename,
                        "thongtin": row["thongtin"],
                        "image": row["image"],
                        "nu": folder_path_nu,
                        "nam": folder_path_nam,
                        "vtrinam": row["vtrinam"],
                        "tomLuocText": row["tomLuocText"],
                    }
                    i = i + 1
                    result_data.append(data)

    return result_data


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
                widths, heights = zip(*(i.size for i in images))
                total_width = sum(widths)
                max_height = max(heights)
                new_im = Image.new("RGB", (total_width, max_height))
                x_offset = 0
                for im in images:
                    new_im.paste(im, (x_offset, 0))
                    x_offset += im.size[0]
                new_im.save(os.path.join(folder_path, f"AI_gen_{key}.jpg"))
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
                new_im.save(os.path.join(folder_path, f"AI_gen_{key}.jpg"))

                for filename in filenames:
                    os.remove(os.path.join(folder_path, filename))

    print("Hoàn thành việc ghép ảnh.")


def insert_svg_logo(image_folder):
    logo_path = "./logo.svg"
    # Đọc nội dung của file SVG
    with open(logo_path, "r") as f:
        svg_content = f.read()

    text_path = "./text.png"

    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path)

            # Chuyển đổi SVG sang PNG
            svg_data = cairosvg.svg2png(bytestring=svg_content)
            logo = Image.open(io.BytesIO(svg_data))

            text = Image.open(text_path)

            text_width, text_height = text.size
            new_text_width = int(image.width * 0.2)
            new_text_height = int(text_height * (new_text_width / text_width))
            resized_text = text.resize((new_text_width, new_text_height))
            # Tính toán kích thước mới cho logo
            logo_width, logo_height = logo.size
            new_logo_width = int(image.width * 0.1)
            new_logo_height = int(logo_height * (new_logo_width / logo_width))
            resized_logo = logo.resize((new_logo_width, new_logo_height))

            # Thay thế nền trắng của logo bằng độ trong suốt
            resized_logo = resized_logo.convert("RGBA")
            logo_data = resized_logo.getdata()
            new_logo_data = []
            for item in logo_data:
                # Thay thế màu trắng (255, 255, 255) thành (255, 255, 255, 0)
                if item[:3] == (255, 255, 255):
                    new_logo_data.append((255, 255, 255, 0))
                else:
                    new_logo_data.append(item)
            resized_logo.putdata(new_logo_data)

            # Tính toán vị trí để chèn logo vào ảnh
            offset = (
                image.width - resized_logo.width - 10,
                image.height - resized_logo.height - 10,
            )

            offset_bottom_center = (
                (image.width - resized_text.width) // 2,
                image.height - resized_text.height - 5,
            )  # Vị trí trung tâm dưới cùng

            # Chèn logo vào ảnh
            image.paste(resized_logo, offset, resized_logo)

            image_with_logo_bottom_center = image.copy()
            image_with_logo_bottom_center.paste(
                resized_text, offset_bottom_center, resized_text
            )

            # Tạo đường dẫn đến thư mục xuất ra
            output_path = os.path.join(image_folder, filename)

            # Lưu ảnh đã chèn logo
            image_with_logo_bottom_center.save(output_path)

    print("Hoàn thành chèn logo vào ảnh!")


def save_to_mysql(
    data,
    link1,
    link2,
    device_them_su_kien,
    ip_them_su_kien,
    id_user_ne,
    ten_nam,
    ten_nu,
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0

    #     config = {
    #         'user': 'sammy',
    #         'password': 'Longcule1311!!',
    #         'host': 'localhost',
    #         'port': 3306,
    #         'database': 'futureLove3',
    #         'auth_plugin': 'caching_sha2_password'
    # }
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
            for items in data:
                items["numswap"] = items["vtrinam"]
                items["id_toan_bo_su_kien"] = id_toan_bo_sk
                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                id_template = random.randint(1, 4)
                sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, tomLuocText, ten_nam, ten_nu, count_comment, count_view, id_template, phantram_loading) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, {items['id_num']}, %s, %s, %s, {id_user_ne}, %s, %s, %s, {count_comment}, {count_view}, {id_template}, {items['id_num'] * 10})"
                val = (
                    id_toan_bo_sk,
                    link1,
                    link2,
                    items["nam"],
                    items["nu"],
                    items["link_img"],
                    date,
                    items["tensukien"],
                    items["thongtin"],
                    id_toan_bo_sk,
                    date,
                    device_them_su_kien,
                    ip_them_su_kien,
                    items["tomLuocText"],
                    ten_nam,
                    ten_nu,
                )
                mycursor.execute(sql, val)
                connection.commit()

        return data
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


def save_to_mysql_skngam(
    data,
    link1,
    link2,
    id_toan_bo_su_kien,
    device_them_su_kien,
    ip_them_su_kien,
    id_user_ne,
    ten_nam,
    ten_nu,
):
    count_comment = 0
    count_view = 0

    #     config = {
    #         'user': 'sammy',
    #         'password': 'Longcule1311!!',
    #         'host': 'localhost',
    #         'port': 3306,
    #         'database': 'futureLove3',
    #         'auth_plugin': 'caching_sha2_password'
    # }
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
            for items in data:
                items["numswap"] = items["vtrinam"]
                items["id_toan_bo_su_kien"] = id_toan_bo_su_kien
                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                id_template = random.randint(1, 4)
                sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, tomLuocText, ten_nam, ten_nu, count_comment, count_view, id_template, phantram_loading) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, {items['id_num'] + 6}, %s, %s, %s, {id_user_ne}, %s, %s, %s, {count_comment}, {count_view}, {id_template}, {(items['id_num'] + 6) * 10})"
                val = (
                    id_toan_bo_su_kien,
                    link1,
                    link2,
                    items["nam"],
                    items["nu"],
                    items["link_img"],
                    date,
                    items["tensukien"],
                    items["thongtin"],
                    id_toan_bo_su_kien,
                    date,
                    device_them_su_kien,
                    ip_them_su_kien,
                    items["tomLuocText"],
                    ten_nam,
                    ten_nu,
                )
                mycursor.execute(sql, val)
                connection.commit()

        return data
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


def save_to_mysql_anh_don(
    link,
    link_swap,
    device_them_su_kien,
    ip_them_su_kien,
    id_user,
    loai_sukien,
    album,
    id_sk_album,
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
            print(loai_sukien)
            Json_added = {
                "id_saved": id_toan_bo_sk,
                "link_src_goc": link,
                "link_da_swap": link_swap,
                "id_toan_bo_su_kien": id_toan_bo_sk,
                "thoigian_sukien": date,
                "device_them_su_kien": device_them_su_kien,
                "ip_them_su_kien": ip_them_su_kien,
                "id_user": id_user,
                "count_comment": count_comment,
                "count_view": count_view,
                "id_template": id_template,
                "loai_sukien": loai_sukien,
                "id_all_sk": id_sk_album,
            }
            sql = "INSERT INTO saved_sukien_alone (id_saved, link_src_goc, link_da_swap, id_toan_bo_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, count_comment, count_view, id_template, loai_sukien, album, id_sk_album) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (
                id_toan_bo_sk,
                link,
                link_swap,
                id_toan_bo_sk,
                date,
                device_them_su_kien,
                ip_them_su_kien,
                id_user,
                count_comment,
                count_view,
                id_template,
                loai_sukien,
                album,
                id_sk_album,
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


def save_to_mysql_2_image(
    link1,
    link2,
    link_swap,
    device_them_su_kien,
    ip_them_su_kien,
    id_user,
    loai_sukien,
    album,
    id_sk_album,
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
            print(loai_sukien)
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
                "loai_sukien": loai_sukien,
                "id_all_sk": id_sk_album,
            }
            sql = "INSERT INTO saved_sukien_2_image (id_saved, link_src_goc, link_tar_goc, link_da_swap, id_toan_bo_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, count_comment, count_view, id_template, loai_sukien, album, id_sk_album) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (
                id_toan_bo_sk,
                link1,
                link2,
                link_swap,
                id_toan_bo_sk,
                date,
                device_them_su_kien,
                ip_them_su_kien,
                id_user,
                count_comment,
                count_view,
                id_template,
                loai_sukien,
                album,
                id_sk_album,
            )
            mycursor.execute(sql, val)
            connection.commit()
            if "connection" in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
            return Json_added
    except mysql.connector.Error as error:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
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
            "loai_sukien": loai_sukien,
            "id_all_sk": id_sk_album,
            "message": "________________________________LOI EXPTION PHan MYSQL_______"
            + str(error),
        }
        print(f"Failed to connect to MySQL database: {error}")
        return Json_added


def save_to_mysql_swap_baby(data, device_them_su_kien, ip_them_su_kien, id_user):
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
            for items in data:
                items["id_toan_bo_su_kien"] = id_toan_bo_sk
                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                id_template = random.randint(1, 4)
                sql = "INSERT INTO saved_sukien_swap_baby (id_saved, link_nam_goc, link_nu_goc, link_baby_goc, link_da_swap, id_toan_bo_su_kien, noi_dung_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, tomLuocText, count_comment, count_view, id_template) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                    id_toan_bo_sk,
                    items["link_nam_goc"],
                    items["link_nu_goc"],
                    items["link_baby_goc"],
                    items["link_da_swap"],
                    id_toan_bo_sk,
                    items["thongtin"],
                    date,
                    device_them_su_kien,
                    ip_them_su_kien,
                    id_user,
                    items["tomLuocText"],
                    count_comment,
                    count_view,
                    id_template,
                )
                mycursor.execute(sql, val)
                connection.commit()

        return data
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        print(f"Failed to connect to MySQL database: {error}")
        return data


def save_video_to_mysql(
    link_vid_swap, thogian_swap, id_user, id_video, linkimg, ten_video, device, ip
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    base_url = "https://photo.gachmen.org"
    link_vid_goc = f"https://photo.gachmen.org/image/video_sk/{id_video}.mp4"
    linkimg = linkimg.replace("/var/www/build_futurelove", base_url)
    data = {}
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
            noidung = "abc"

            date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            data = {
                "id_sukien_video": id_toan_bo_sk,
                "id_video_swap": id_video,
                "linkimg": linkimg,
                "link_vid_swap": link_vid_swap,
                "link_vid_goc": link_vid_goc,
                "ten_video": ten_video,
                "noidung": noidung,
                "thoigian_sukien": date,
                "thoigian_swap": thogian_swap,
                "device_tao_vid": device,
                "ip_tao_vid": ip,
            }
            sql = f"INSERT INTO saved_sukien_video (id_saved ,link_video , link_image ,link_da_swap , ten_su_kien, noidung_su_kien, id_video, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, count_comment, count_view, link_video_goc, thoigian_swap) VALUES (%s, %s, %s, %s, %s, %s, {id_video}, %s, %s, %s, {id_user}, {count_comment}, {count_view}, %s, %s)"
            val = (
                id_toan_bo_sk,
                id_video,
                linkimg,
                link_vid_swap,
                ten_video,
                noidung,
                date,
                device,
                ip,
                link_vid_goc,
                thogian_swap,
            )
            mycursor.execute(sql, val)
            connection.commit()
            if "connection" in locals() and connection.is_connected():
                print("________CONNECTION_BI_DONG_KET_NOI________")
                cursor.close()
                connection.close()
            return data
    except mysql.connector.Error as error:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
        print("MySQL connection closed")
        print(
            f"_____________________________MySQL database: {error} ___________________-"
        )
        return data


def save_video_to_mysql_swap_imagevideo(
    src_image, src_video, link_vid_swap, id_user, device, ip
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    data = {}
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
            data = {
                "id_saved": id_toan_bo_sk,
                "link_video_goc": src_video,
                "link_image": src_image,
                "link_vid_da_swap": link_vid_swap,
                "thoigian_sukien": date,
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
            }
            sql = f"INSERT INTO saved_sukien_video_swap_image (id_saved ,link_video_goc , link_image ,link_video_da_swap , thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, count_comment, count_view) VALUES (%s, %s, %s, %s, %s, %s, %s,  {id_user}, {count_comment}, {count_view})"
            val = (id_toan_bo_sk, src_video, src_image, link_vid_swap, date, device, ip)
            mycursor.execute(sql, val)
            connection.commit()

            return data
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


def save_video_to_mysql_swap_imagevideo_growup(
    src_image, src_video, link_vid_swap, id_user, device, ip, loai_sk
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    data = {}
    try:
        print("_______________VAO PHAN LUU_DATABASE VIDEO SWAP_____________________")
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor(buffered=True)
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor(buffered=True)

            date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            data = {
                "id_saved": id_toan_bo_sk,
                "link_video_goc": src_video,
                "link_image": src_image,
                "link_vid_da_swap": link_vid_swap,
                "thoigian_sukien": date,
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": loai_sk,
            }
            sql = f"INSERT INTO saved_sukien_video_image_growup (id_saved ,link_video_goc , link_image ,link_video_da_swap , thoigian_sukien, device_them_su_kien, ip_them_su_kien, loai_sk, id_user, count_comment, count_view) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,  {id_user}, {count_comment}, {count_view})"
            val = (
                id_toan_bo_sk,
                src_video,
                src_image,
                link_vid_swap,
                date,
                device,
                ip,
                loai_sk,
            )
            mycursor.execute(sql, val)
            connection.commit()
            if "connection" in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
            return data
    except mysql.connector.Error as error:
        print(
            f"_____Loi exception ____ save_video_to_mysql_swap_imagevideo_growup_____ {error}"
        )
        data = {
            "id_saved": id_toan_bo_sk,
            "link_video_goc": src_video,
            "link_image": src_image,
            "link_vid_da_swap": link_vid_swap,
            "thoigian_sukien": date,
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
        }
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
        return data


# SAVE IMAGE VIDEO WEDDING SERVER


def save_video_to_mysql_swap_imagevideo_wedding(
    src_image, src_video, link_vid_swap, id_user, device, ip
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    data = {}
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
            data = {
                "id_saved": id_toan_bo_sk,
                "link_video_goc": src_video,
                "link_image": src_image,
                "link_vid_da_swap": link_vid_swap,
                "thoigian_sukien": date,
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
            }
            sql = f"INSERT INTO saved_sukien_video_image_wedding (id_saved ,link_video_goc , link_image ,link_video_da_swap , thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, count_comment, count_view) VALUES (%s, %s, %s, %s, %s, %s, %s,  {id_user}, {count_comment}, {count_view})"
            val = (id_toan_bo_sk, src_video, src_image, link_vid_swap, date, device, ip)
            mycursor.execute(sql, val)
            connection.commit()

            return data
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        data = {
            "id_saved": id_toan_bo_sk,
            "link_video_goc": src_video,
            "link_image": src_image,
            "link_vid_da_swap": link_vid_swap,
            "thoigian_sukien": date,
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
        }
        return data
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


# SAVE 2 IMAGE MOM AND BABY


def save_to_mysql_2_image_mom_baby(
    link1, link2, link_swap, device_them_su_kien, ip_them_su_kien, id_user, album
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
                "album": album,
            }

            sql = """INSERT INTO saved_sukien_image_growup 
                    (id_saved, link_src_goc, link_tar_goc, link_da_swap, 
                    id_toan_bo_su_kien, thoigian_sukien, device_them_su_kien, 
                    ip_them_su_kien, id_user, count_comment, count_view, 
                    id_template, album) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            val = (
                id_toan_bo_sk,
                link1,
                link2,
                link_swap,
                id_toan_bo_sk,
                date,
                device_them_su_kien,
                ip_them_su_kien,
                id_user,
                count_comment,
                count_view,
                id_template,
                album,
            )

            cursor.execute(sql, val)
            connection.commit()

            return Json_added

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


def get_images_alone(list_folder):
    try:
        # Kết nối đến cơ sở dữ liệu
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Tìm ID của folder_name "ANH_ALONE_1" trong bảng alone_template
        cursor.execute(
            "SELECT id_cate FROM alone_template WHERE folder_name = %s", (list_folder,)
        )
        alone_template_id = cursor.fetchone()[0]

        # Truy vấn cột image từ bảng listImage_alone với điều kiện IDCategories = alone_template_id
        cursor.execute(
            "SELECT image FROM listImage_alone WHERE IDCategories = %s",
            (alone_template_id,),
        )
        images = cursor.fetchall()
        image_links = [image[0] for image in images]
    except mysql.connector.Error as error:
        print("Error:", error)
        return None

    finally:
        # Đóng kết nối
        if "connection" in locals():
            cursor.close()
            connection.close()
    return image_links


def get_list_categoris_alone(list_folder):
    try:
        # Kết nối đến cơ sở dữ liệu
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Tìm các trường name_cate và image_sample của folder_name trong bảng alone_template
        cursor.execute(
            "SELECT id_cate, name_cate, image_sample FROM alone_template WHERE folder_name = %s",
            (list_folder,),
        )
        result = cursor.fetchone()
        if result:
            id_cate, name_cate, image_sample = result
        else:
            return None

        # Tạo một từ điển để chứa kết quả
        result_dict = {
            "id_cate": id_cate,
            "name_cate": name_cate,
            "image_sample": image_sample,
        }
        return result_dict
    except mysql.connector.Error as error:
        print("Error:", error)
        return None

    finally:
        # Đóng kết nối
        if "connection" in locals():
            cursor.close()
            connection.close()


def get_thiep_cuoi(
    name1,
    name2,
    date,
    link_image,
    location,
    link_location,
    link_qr,
    status,
    id_user,
    link1,
    link2,
):
    try:
        # Kết nối đến cơ sở dữ liệu
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Chèn dữ liệu vào bảng wedding_details
        insert_query = """
        INSERT INTO wedding_details (groom_name, bride_name, wedding_date, wedding_image, wedding_location, google_maps_link, qr_code_image, attendance_status, id_user, groom_image, bride_image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data_tuple = (
            name1,
            name2,
            date,
            link_image,
            location,
            link_location,
            link_qr,
            status,
            id_user,
            link1,
            link2,
        )
        cursor.execute(insert_query, data_tuple)

        connection.commit()
        print("Data inserted successfully into `wedding_details` table.")

        # Truy vấn dữ liệu đã chèn vào bảng
        select_query = """
        SELECT * FROM wedding_details WHERE id = LAST_INSERT_ID();
        """
        cursor.execute(select_query)
        result = cursor.fetchone()

        # Tạo dictionary chứa các giá trị đã lưu
        result_dict = {
            "id": result[0],
            "groom_name": result[1],
            "bride_name": result[2],
            "wedding_date": result[3],
            "wedding_image": result[4],
            "wedding_location": result[5],
            "google_maps_link": result[6],
            "qr_code_image": result[7],
            "attendance_status": result[8],
            "id_user": result[9],
            "groom_image": result[10],
            "bride_image": result[11],
        }

        return result_dict  # Trả về dictionary chứa kết quả của truy vấn
    except mysql.connector.Error as error:
        print(f"Failed to insert data into MySQL table: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def save_video_to_mysql_swap_imagevideo_mebau(
    src_image, src_video, link_vid_swap, id_user, device, ip, loai_sk
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    data = {}
    try:
        print("_______________VAO PHAN LUU_DATABASE VIDEO SWAP_____________________")
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor(buffered=True)
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            mycursor = connection.cursor(buffered=True)

            date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            data = {
                "id_saved": id_toan_bo_sk,
                "link_video_goc": src_video,
                "link_image": src_image,
                "link_vid_da_swap": link_vid_swap,
                "thoigian_sukien": date,
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": loai_sk,
            }
            sql = f"INSERT INTO saved_sukien_video_image_mebau (id_saved ,link_video_goc , link_image ,link_video_da_swap , thoigian_sukien, device_them_su_kien, ip_them_su_kien, loai_sk, id_user, count_comment, count_view) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,  {id_user}, {count_comment}, {count_view})"
            val = (
                id_toan_bo_sk,
                src_video,
                src_image,
                link_vid_swap,
                date,
                device,
                ip,
                loai_sk,
            )
            mycursor.execute(sql, val)
            connection.commit()
            if "connection" in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
            return data
    except mysql.connector.Error as error:
        print(
            f"_____Loi exception ____ save_video_to_mysql_swap_imagevideo_mebau_____ {error}"
        )
        data = {
            "id_saved": id_toan_bo_sk,
            "link_video_goc": src_video,
            "link_image": src_image,
            "link_vid_da_swap": link_vid_swap,
            "thoigian_sukien": date,
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
        }
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
        return data


def get_random_data_noel():
    return


def test():
    return ""
