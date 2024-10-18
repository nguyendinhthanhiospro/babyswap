# from upload_video import upload_vid
import torch
from roop import core
from test_csv import (
    save_video_to_mysql,
    save_video_to_mysql_swap_imagevideo,
    save_video_to_mysql_swap_imagevideo_growup,
    save_to_mysql_2_image_mom_baby,
    save_video_to_mysql_swap_imagevideo_wedding,
    test,
    save_video_to_mysql_swap_imagevideo_mebau,
)
import os, random
import time
import shutil
import os, uuid
from login.func import validate_token, generate_token, send_mail_swap_done


def copy_and_rename_video(source_path: str, target_path: str) -> None:
    shutil.copy2(source_path, target_path)  # Copy video từ nguồn đến đích

    # Đổi tên tệp mới
    target_directory = os.path.dirname(target_path)
    target_name, _ = os.path.splitext(os.path.basename(target_path))
    new_target_name = target_name
    new_target_path = os.path.join(target_directory, new_target_name)
    os.rename(target_path, new_target_path)


def check_image_existence(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False


# swap video santa cu
def swap_video(id_user, id_video, image):
    result = check_image_existence(image)
    if result:
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        path_folder = f"/var/www/build_futurelove/image/gen_video/{folder}/"
        os.makedirs(path_folder, exist_ok=True)
        file_name = (
            "christmas_user="
            + str(id_user)
            + "_"
            + str(random.randint(1, 200000))
            + "_"
            + str(id_video)
            + ".mp4"
        )
        # vid_path = f"/var/www/build_futurelove/image/video_sk/{id_video}.mp4"
        vid_path = f"/media/thinkdiff/Seagate Hub/build_futurelove/image/santa_christmas/{id_video}.mp4"
        src_path = image
        out_path = f"/var/www/build_futurelove/image/gen_video/{folder}/{file_name}"
        print("VIDEO_____" + str(vid_path) + "___KET_QUA_____" + str(path_folder))
        start_time = time.time()
        link_vid = f"https://photo.gachmen.org/image/gen_video/{folder}/{file_name}"
        try:
            core.runvid(src_path, vid_path, out_path)
            execution_time = time.time() - start_time

        except Exception as e:
            print(
                f"________Exception_______Error occurred during video generation: {str(e)}"
            )
            return link_vid, execution_time
        # link_vid = upload_vid(out_path, file_name)
        # os.remove(vid_fake_path)
        return link_vid, execution_time
    else:
        return None


# viet update santa 17 oct 2024
def gen_video(id_user, id_video, linkimg, ten_video, device, ip):
    print("hello")
    print("ID_VIDEO " + str(id_video))
    print("linkimg " + str(linkimg))
    link = swap_video(id_user, id_video, linkimg)
    print(str(link) + "____" + str(id_user) + "____" + str(id_video) + "____" + linkimg)
    if link is None:
        return "SONPIPI : Cannot find images or no face input swap!!, Please change images have face"
    else:
        data = save_video_to_mysql(
            link[0], link[1], id_user, id_video, linkimg, ten_video, device, ip
        )
        return data


def gen_video_swap_imagevid(
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


# SWAP VIDEO IMAGE GROW UP


def gen_video_swap_imagevid_growup(
    src_img, src_video, folder, device_them_su_kien, ip_them_su_kien, id_user
):
    print("hallo")
    folder_path = f"/media/thinkdiff/Seagate Hub/server_grow_up/video_user/{folder}"
    try:
        core.runvid(src_img, src_video, folder_path)
        link_vid = f"https://photo.gachmen.org/image/gen_video/{folder}/temp.mp4"
    except Exception as e:
        return f"Error occurred during video generation: {str(e)}"

    src_img = src_img.replace(
        "/media/thinkdiff/Seagate Hub/server_grow_up/", "https://photo.gachmen.org/"
    )
    src_video = src_video.replace(
        "/media/thinkdiff/Seagate Hub/server_grow_up/", "https://photo.gachmen.org/"
    )
    data = save_video_to_mysql_swap_imagevideo_growup(
        src_img, src_video, link_vid, id_user, device_them_su_kien, ip_them_su_kien
    )
    return data


def gen_video_swap_imagevid_growup_mom_baby(
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
    data = save_to_mysql_2_image_mom_baby(
        src_img, src_video, link_vid, id_user, device_them_su_kien, ip_them_su_kien
    )
    return data


# SWAP VIDEO IMAGE WEDDING


def gen_video_swap_imagevid_wedding(
    src_img, src_video, folder, device_them_su_kien, ip_them_su_kien, id_user
):
    print("hallo")
    folder_path = (
        f"/var/www/build_futurelove/image/image_user/{id_user}/wedding_video/{folder}"
    )
    src_video = f"/media/thinkdiff/Seagate Hub/server_wedding/video_detal/VIDEO_WD/VIDEOWD{src_video}/VIDEOWD{src_video}.mp4"
    os.makedirs(folder_path, exist_ok=True)
    try:
        core.runvid(src_img, src_video, folder_path)
        link_vid = f"https://photo.gachmen.org/image/image_user/{id_user}/wedding_video/{folder}/temp.mp4"
    except Exception as e:
        return f"Error occurred during video generation: {str(e)}"

    src_img = src_img.replace(
        "/var/www/build_futurelove/", "https://photo.gachmen.org/"
    )
    src_video = src_video.replace(
        "/media/thinkdiff/Seagate Hub/", "https://mail.fakewedding.online/"
    )

    print(folder_path)
    data = save_video_to_mysql_swap_imagevideo_wedding(
        src_img, src_video, link_vid, id_user, device_them_su_kien, ip_them_su_kien
    )
    return data


def swap_video_wedding(id_user, id_video, image, device, ip):
    if image.find("/https:") > 0:
        image = image.replace("https://photo.gachmen.org/", "")
        print("______KETQUA______")
        print(image)
    result = check_image_existence(image)
    # error 1 - note by Nhat: duong dan file dang sai
    if result:
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        folder_link_web = f"/var/www/build_futurelove/image/image_user/{id_user}/wedding_video/{folder}"
        print("FOLDER_LUU_DU_LIEU__" + folder_link_web)
        os.makedirs(folder_link_web, exist_ok=True)
        file_name = (
            "user_"
            + str(id_user)
            + "_"
            + str(random.randint(1, 200000))
            + "_"
            + str(id_video)
            + ".mp4"
        )
        # /media/thinkdiff/Seagate Hub/server_wedding/video_cuoi/5
        video_path_folder = (
            f"/media/thinkdiff/Seagate Hub/server_wedding/video_cuoi/{id_video}"
        )
        allfiles = os.listdir(video_path_folder)
        files = [fname for fname in allfiles if fname.endswith(".mp4")]
        vid_path = (
            f"/media/thinkdiff/Seagate Hub/server_wedding/video_cuoi/{id_video}/"
            + files[0]
        )
        print("______" + vid_path)
        src_path = image
        out_path = f"/var/www/build_futurelove/image/image_user/{id_user}/wedding_video/{folder}/{file_name}"
        print(
            "______VIDEO_____"
            + str(vid_path)
            + "___KET_QUA_________"
            + str(folder_link_web)
        )
        start_time = time.time()
        try:
            core.runvid(src_path, vid_path, out_path)
            execution_time = time.time() - start_time
            link_vid = f"https://photo.gachmen.org/image/image_user/{id_user}/wedding_video/{folder}/{file_name}"
            dataReturn = save_video_to_mysql_swap_imagevideo_wedding(
                image, vid_path, link_vid, id_user, device, ip
            )
            return dataReturn
        except Exception as e:
            print("____LOI EXCEPTION______" + str(e))
            data = {
                "id_saved": "",
                "link_video_goc": vid_path,
                "link_image": image,
                "link_vid_da_swap": link_vid,
                "thoigian_sukien": "",
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": "",
                "message": "ket qua khong thanh cong, Bi Exeption: " + str(e),
            }
            return data
    else:
        print("ket qua khong thanh cong, khong tim thay image: " + str(image))
        data = {
            "id_saved": "",
            "link_video_goc": vid_path,
            "link_image": image,
            "link_vid_da_swap": link_vid,
            "thoigian_sukien": "",
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "loai_sk": "",
            "message": "ket qua khong thanh cong, khong tim thay image: " + str(image),
        }
        return data


def swap_video_mom_baby(id_user, id_video, image, device, ip):
    result = check_image_existence(image)
    if result:
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        path_folder = (
            f"/var/www/build_futurelove/image/image_user/{id_user}/mom_baby/{folder}"
        )
        os.makedirs(path_folder, exist_ok=True)
        file_name = (
            "user_"
            + str(id_user)
            + "_"
            + str(random.randint(1, 200000))
            + "_"
            + str(id_video)
            + ".mp4"
        )
        # vid_path = f"/media/thinkdiff/Seagate Hub/server_mom_baby_growup/Video/VdMB{id_video}/VdMB{id_video}.mp4"
        vid_path = f"/home/thinkdiff/Documents/server_mom_baby_growup/Video/VdMB{id_video}/VdMB{id_video}.mp4"
        src_path = image
        out_path = f"/var/www/build_futurelove/image/image_user/{id_user}/mom_baby/{folder}/{file_name}"
        link_vid = f"https://photo.gachmen.org/image/image_user/{id_user}/mom_baby/{folder}/{file_name}"

        print(
            "_________________mom_baby______VIDEO_____"
            + str(vid_path)
            + "___KET_QUA"
            + str(path_folder)
        )
        start_time = time.time()
        try:
            core.runvid(src_path, vid_path, out_path)
            execution_time = time.time() - start_time
            dataReturn = save_video_to_mysql_swap_imagevideo_growup(
                image, vid_path, link_vid, id_user, device, ip, "mom_baby"
            )
            return dataReturn
        except Exception as e:
            print(
                str(out_path)
                + "___________________________BI_EXPTION_KHI_SWAP_VIDEO___Error occurred during video generation:____"
                + str(e)
            )
            data = {
                "id_saved": "",
                "link_video_goc": vid_path,
                "link_image": image,
                "link_vid_da_swap": link_vid,
                "thoigian_sukien": "",
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": "",
                "message": "ket qua khong thanh cong, Bi Exeption: " + str(e),
            }
            return data
    else:
        print("ket qua khong thanh cong, khong tim thay image: " + str(image))
        data = {
            "id_saved": "",
            "link_video_goc": vid_path,
            "link_image": image,
            "link_vid_da_swap": link_vid,
            "thoigian_sukien": "",
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "loai_sk": "",
            "message": "ket qua khong thanh cong, khong tim thay image: " + str(image),
        }
        return data


def swap_video_time_machine(id_user, id_video, image, device, ip):
    result = check_image_existence(image)
    if result:
        # print("hello1")
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        path_folder = (
            f"/var/www/build_futurelove/image/image_user/{id_user}/nam/{folder}"
        )
        os.makedirs(path_folder, exist_ok=True)
        file_name = (
            "user_"
            + str(id_user)
            + "_"
            + str(random.randint(1, 200000))
            + "_"
            + str(id_video)
            + ".mp4"
        )
        vid_path = ""
        if id_video >= 37:
            vid_path = f"/media/thinkdiff/Seagate Hub/server_grow_up/video_grow_up/video {id_video-1}.mp4"
        else:
            vid_path = f"/media/thinkdiff/Seagate Hub/server_grow_up/video_grow_up/video {id_video}.mp4"
        src_path = image
        out_path = f"/var/www/build_futurelove/image/image_user/{id_user}/nam/{folder}/{file_name}"
        link_vid = f"https://photo.gachmen.org/image/image_user/{id_user}/nam/{folder}/{file_name}"
        print("VIDEO_____" + str(vid_path) + "___KET_QUA" + str(path_folder))
        start_time = time.time()
        try:
            core.runvid(src_path, vid_path, out_path)
            execution_time = time.time() - start_time

            dataReturn = save_video_to_mysql_swap_imagevideo_growup(
                image, vid_path, link_vid, id_user, device, ip, "vid_age"
            )
            print("_____LINKVIDEO____" + str(link_vid))
            return dataReturn

        except Exception as e:
            print(
                str(out_path)
                + "___________________________BI_EXPTION_KHI_SWAP_VIDEO___Error occurred during video generation:____"
                + str(e)
            )
            data = {
                "id_saved": "",
                "link_video_goc": vid_path,
                "link_image": image,
                "link_vid_da_swap": link_vid,
                "thoigian_sukien": "",
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": "",
                "message": "ket qua khong thanh cong, Bi Exeption: " + str(e),
            }
        return data
    else:
        print("ket qua khong thanh cong, khong tim thay image: " + str(image))
        data = {
            "id_saved": "",
            "link_video_goc": vid_path,
            "link_image": image,
            "link_vid_da_swap": link_vid,
            "thoigian_sukien": "",
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "loai_sk": "",
            "message": "ket qua khong thanh cong, khong tim thay image: " + str(image),
        }
        return data


def gen_video_wedding(id_user, id_video, linkimg, device, ip):
    print("gen_video_wedding_____ID_VIDEO_______" + str(id_video))
    print("gen_video_wedding_____linkimg____" + str(linkimg))
    data = swap_video_wedding(id_user, id_video, linkimg, device, ip)
    torch.cuda.empty_cache()
    return data


def gen_video_mom_baby(id_user, id_video, linkimg, device, ip):
    print("ID_VIDEO " + str(id_video))
    print("linkimg " + str(linkimg))
    data = swap_video_mom_baby(id_user, id_video, linkimg, device, ip)
    print(
        "_____KET_QUA_______swap_video_mom_baby_________"
        + str(data)
        + "____"
        + str(id_user)
        + "____"
        + str(id_video)
        + "____"
        + linkimg
    )
    torch.cuda.empty_cache()
    return data


def gen_video_time_machine(id_user, id_video, linkimg, device, ip):
    print("ID_VIDEO " + str(id_video))
    print("_____________________linkimg____" + str(linkimg))
    data = swap_video_time_machine(id_user, id_video, linkimg, device, ip)

    torch.cuda.empty_cache()
    return data


# babycatwalk
def swap_video_baby_catwalk(id_user, id_video, image, device, ip):
    result = check_image_existence(image)
    if result:
        # print("hello1")
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        path_folder = f"/var/www/build_futurelove/image/image_user/{id_user}/baby_catwalk/{folder}"
        os.makedirs(path_folder, exist_ok=True)
        file_name = (
            "baby_catwalk_user="
            + str(id_user)
            + "_"
            + str(random.randint(1, 200000))
            + "_"
            + str(id_video)
            + ".mp4"
        )
        vid_path = ""
        if id_video >= 37:
            vid_path = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/baby/baby_catwalk/{id_video-1}.mp4"
        else:
            vid_path = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/baby/baby_catwalk/{id_video}.mp4"
        src_path = image
        out_path = f"/var/www/build_futurelove/image/image_user/{id_user}/baby_catwalk/{folder}/{file_name}"
        link_vid = f"https://photo.gachmen.org/image/image_user/{id_user}/baby_catwalk/{folder}/{file_name}"
        print("VIDEO_____" + str(vid_path) + "___KET_QUA" + str(path_folder))
        start_time = time.time()
        try:
            core.runvid(src_path, vid_path, out_path)
            execution_time = time.time() - start_time

            dataReturn = save_video_to_mysql_swap_imagevideo_growup(
                image, vid_path, link_vid, id_user, device, ip, "baby_catwalk"
            )
            print("_____LINKVIDEO____" + str(link_vid))
            return dataReturn

        except Exception as e:
            print(
                str(out_path)
                + "___________________________BI_EXPTION_KHI_SWAP_VIDEO___Error occurred during video generation:____"
                + str(e)
            )
            data = {
                "id_saved": "",
                "link_video_goc": vid_path,
                "link_image": image,
                "link_vid_da_swap": link_vid,
                "thoigian_sukien": "",
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": "",
                "message": "ket qua khong thanh cong, Bi Exeption: " + str(e),
            }
        return data
    else:
        print("ket qua khong thanh cong, khong tim thay image: " + str(image))
        data = {
            "id_saved": "",
            "link_video_goc": vid_path,
            "link_image": image,
            "link_vid_da_swap": link_vid,
            "thoigian_sukien": "",
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "loai_sk": "",
            "message": "ket qua khong thanh cong, khong tim thay image: " + str(image),
        }
        return data


def gen_video_baby_catwalk(id_user, id_video, linkimg, device, ip):
    print("ID_VIDEO " + str(id_video))
    print("_____________________linkimg____" + str(linkimg))
    data = swap_video_baby_catwalk(id_user, id_video, linkimg, device, ip)

    torch.cuda.empty_cache()
    return data


# baby funny
def swap_video_baby_funny(id_user, id_video, image, device, ip):
    result = check_image_existence(image)
    if result:
        # print("hello1")
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        path_folder = (
            f"/var/www/build_futurelove/image/image_user/{id_user}/baby_funny/{folder}"
        )
        os.makedirs(path_folder, exist_ok=True)
        file_name = (
            "baby_funny_user="
            + str(id_user)
            + "_"
            + str(random.randint(1, 200000))
            + "_"
            + str(id_video)
            + ".mp4"
        )
        vid_path = ""
        if id_video >= 37:
            vid_path = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/baby/baby_funny/{id_video-1}.mp4"
        else:
            vid_path = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/baby/baby_funny/{id_video}.mp4"
        src_path = image
        out_path = f"/var/www/build_futurelove/image/image_user/{id_user}/baby_funny/{folder}/{file_name}"
        link_vid = f"https://photo.gachmen.org/image/image_user/{id_user}/baby_funny/{folder}/{file_name}"
        print("VIDEO_____" + str(vid_path) + "___KET_QUA" + str(path_folder))
        start_time = time.time()
        try:
            core.runvid(src_path, vid_path, out_path)
            execution_time = time.time() - start_time

            dataReturn = save_video_to_mysql_swap_imagevideo_growup(
                image, vid_path, link_vid, id_user, device, ip, "baby_funny"
            )
            print("_____LINKVIDEO____" + str(link_vid))
            return dataReturn

        except Exception as e:
            print(
                str(out_path)
                + "___________________________BI_EXPTION_KHI_SWAP_VIDEO___Error occurred during video generation:____"
                + str(e)
            )
            data = {
                "id_saved": "",
                "link_video_goc": vid_path,
                "link_image": image,
                "link_vid_da_swap": link_vid,
                "thoigian_sukien": "",
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": "",
                "message": "ket qua khong thanh cong, Bi Exeption: " + str(e),
            }
        return data
    else:
        print("ket qua khong thanh cong, khong tim thay image: " + str(image))
        data = {
            "id_saved": "",
            "link_video_goc": vid_path,
            "link_image": image,
            "link_vid_da_swap": link_vid,
            "thoigian_sukien": "",
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "loai_sk": "",
            "message": "ket qua khong thanh cong, khong tim thay image: " + str(image),
        }
        return data


def gen_video_baby_funny(id_user, id_video, linkimg, device, ip):
    print("ID_VIDEO " + str(id_video))
    print("_____________________linkimg____" + str(linkimg))
    data = swap_video_baby_funny(id_user, id_video, linkimg, device, ip)

    torch.cuda.empty_cache()
    return data


# baby hallowen
def swap_video_baby_hallowen(id_user, id_video, image, device, ip):
    result = check_image_existence(image)
    if result:
        # print("hello1")
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        path_folder = f"/var/www/build_futurelove/image/image_user/{id_user}/baby_hallowen/{folder}"
        os.makedirs(path_folder, exist_ok=True)
        file_name = (
            "baby_hallowen_user="
            + str(id_user)
            + "_"
            + str(random.randint(1, 200000))
            + "_"
            + str(id_video)
            + ".mp4"
        )
        vid_path = ""
        if id_video >= 37:
            vid_path = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/baby/baby_hallowen/{id_video-1}.mp4"
        else:
            vid_path = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/baby/baby_hallowen/{id_video}.mp4"
        src_path = image
        out_path = f"/var/www/build_futurelove/image/image_user/{id_user}/baby_hallowen/{folder}/{file_name}"
        link_vid = f"https://photo.gachmen.org/image/image_user/{id_user}/baby_hallowen/{folder}/{file_name}"
        print("VIDEO_____" + str(vid_path) + "___KET_QUA" + str(path_folder))
        start_time = time.time()
        try:
            core.runvid(src_path, vid_path, out_path)
            execution_time = time.time() - start_time

            dataReturn = save_video_to_mysql_swap_imagevideo_growup(
                image, vid_path, link_vid, id_user, device, ip, "baby_hallowen"
            )
            print("_____LINKVIDEO____" + str(link_vid))
            return dataReturn

        except Exception as e:
            print(
                str(out_path)
                + "___________________________BI_EXPTION_KHI_SWAP_VIDEO___Error occurred during video generation:____"
                + str(e)
            )
            data = {
                "id_saved": "",
                "link_video_goc": vid_path,
                "link_image": image,
                "link_vid_da_swap": link_vid,
                "thoigian_sukien": "",
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": "",
                "message": "ket qua khong thanh cong, Bi Exeption: " + str(e),
            }
        return data
    else:
        print("ket qua khong thanh cong, khong tim thay image: " + str(image))
        data = {
            "id_saved": "",
            "link_video_goc": vid_path,
            "link_image": image,
            "link_vid_da_swap": link_vid,
            "thoigian_sukien": "",
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "loai_sk": "",
            "message": "ket qua khong thanh cong, khong tim thay image: " + str(image),
        }
        return data


def gen_video_baby_hallowen(id_user, id_video, linkimg, device, ip):
    print("ID_VIDEO " + str(id_video))
    print("_____________________linkimg____" + str(linkimg))
    data = swap_video_baby_hallowen(id_user, id_video, linkimg, device, ip)

    torch.cuda.empty_cache()
    return data


# baby hallowen
def swap_video_model(id_user, id_video, image, device, ip):
    result = check_image_existence(image)
    if result:
        # print("hello1")
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        path_folder = (
            f"/var/www/build_futurelove/image/image_user/{id_user}/model/{folder}"
        )
        os.makedirs(path_folder, exist_ok=True)
        file_name = (
            "model_user="
            + str(id_user)
            + "_"
            + str(random.randint(1, 200000))
            + "_"
            + str(id_video)
            + ".mp4"
        )
        vid_path = ""
        if id_video >= 37:
            vid_path = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/model/{id_video-1}.mp4"
        else:
            vid_path = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/model/{id_video}.mp4"
        src_path = image
        out_path = f"/var/www/build_futurelove/image/image_user/{id_user}/model/{folder}/{file_name}"
        link_vid = f"https://photo.gachmen.org/image/image_user/{id_user}/model/{folder}/{file_name}"
        print("VIDEO_____" + str(vid_path) + "___KET_QUA" + str(path_folder))
        start_time = time.time()
        try:
            core.runvid(src_path, vid_path, out_path)
            execution_time = time.time() - start_time

            dataReturn = save_video_to_mysql_swap_imagevideo_growup(
                image, vid_path, link_vid, id_user, device, ip, "model"
            )
            print("_____LINKVIDEO____" + str(link_vid))
            return dataReturn

        except Exception as e:
            print(
                str(out_path)
                + "___________________________BI_EXPTION_KHI_SWAP_VIDEO___Error occurred during video generation:____"
                + str(e)
            )
            data = {
                "id_saved": "",
                "link_video_goc": vid_path,
                "link_image": image,
                "link_vid_da_swap": link_vid,
                "thoigian_sukien": "",
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": "",
                "message": "ket qua khong thanh cong, Bi Exeption: " + str(e),
            }
        return data
    else:
        print("ket qua khong thanh cong, khong tim thay image: " + str(image))
        data = {
            "id_saved": "",
            "link_video_goc": vid_path,
            "link_image": image,
            "link_vid_da_swap": link_vid,
            "thoigian_sukien": "",
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "loai_sk": "",
            "message": "ket qua khong thanh cong, khong tim thay image: " + str(image),
        }
        return data


def gen_video_model(id_user, id_video, linkimg, device, ip):
    print("ID_VIDEO " + str(id_video))
    print("_____________________linkimg____" + str(linkimg))
    data = swap_video_model(id_user, id_video, linkimg, device, ip)

    torch.cuda.empty_cache()
    return data


# baby hallowen
def swap_video_baby_future_love(id_user, id_video, image, device, ip):
    result = check_image_existence(image)
    if result:
        # print("hello1")
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        path_folder = f"/var/www/build_futurelove/image/image_user/{id_user}/baby_future_love/{folder}"
        os.makedirs(path_folder, exist_ok=True)
        file_name = (
            "baby_future_love_user="
            + str(id_user)
            + "_"
            + str(random.randint(1, 200000))
            + "_"
            + str(id_video)
            + ".mp4"
        )
        vid_path = ""
        if id_video >= 37:
            vid_path = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/baby/baby_future_love/{id_video-1}.mp4"
        else:
            vid_path = f"/media/thinkdiff/Seagate Hub/wedding-cut-template-cut/baby/baby_future_love/{id_video}.mp4"
        src_path = image
        out_path = f"/var/www/build_futurelove/image/image_user/{id_user}/baby_future_love/{folder}/{file_name}"
        link_vid = f"https://photo.gachmen.org/image/image_user/{id_user}/baby_future_love/{folder}/{file_name}"
        print("VIDEO_____" + str(vid_path) + "___KET_QUA" + str(path_folder))
        start_time = time.time()
        try:
            core.runvid(src_path, vid_path, out_path)
            execution_time = time.time() - start_time

            dataReturn = save_video_to_mysql_swap_imagevideo_growup(
                image, vid_path, link_vid, id_user, device, ip, "baby_future_love"
            )
            print("_____LINKVIDEO____" + str(link_vid))
            return dataReturn

        except Exception as e:
            print(
                str(out_path)
                + "___________________________BI_EXPTION_KHI_SWAP_VIDEO___Error occurred during video generation:____"
                + str(e)
            )
            data = {
                "id_saved": "",
                "link_video_goc": vid_path,
                "link_image": image,
                "link_vid_da_swap": link_vid,
                "thoigian_sukien": "",
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": "",
                "message": "ket qua khong thanh cong, Bi Exeption: " + str(e),
            }
        return data
    else:
        print("ket qua khong thanh cong, khong tim thay image: " + str(image))
        data = {
            "id_saved": "",
            "link_video_goc": vid_path,
            "link_image": image,
            "link_vid_da_swap": link_vid,
            "thoigian_sukien": "",
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "loai_sk": "",
            "message": "ket qua khong thanh cong, khong tim thay image: " + str(image),
        }
        return data


def gen_video_baby_future_love(id_user, id_video, linkimg, device, ip):
    print("ID_VIDEO " + str(id_video))
    print("_____________________linkimg____" + str(linkimg))
    data = swap_video_baby_future_love(id_user, id_video, linkimg, device, ip)

    torch.cuda.empty_cache()
    return data


# fancy app
def swap_video_fancy_mebau(id_user, id_video, image, device, ip):
    result = check_image_existence(image)
    if result:
        # print("hello1")
        folder = f"{os.getpid()}_{str(uuid.uuid4().int)[-12:]}"
        path_folder = (
            f"/var/www/build_futurelove/image/image_user/{id_user}/mebau/{folder}"
        )
        os.makedirs(path_folder, exist_ok=True)
        file_name = (
            "user_"
            + str(id_user)
            + "_"
            + str(random.randint(1, 200000))
            + "_"
            + str(id_video)
            + ".mp4"
        )
        vid_path = ""
        if id_video >= 37:
            vid_path = f"/media/thinkdiff/Seagate Hub/server_grow_up/video_mebau/{id_video-1}.mp4"
        else:
            vid_path = f"/media/thinkdiff/Seagate Hub/server_grow_up/video_mebau/{id_video}.mp4"
        src_path = image
        out_path = f"/var/www/build_futurelove/image/image_user/{id_user}/mebau/{folder}/{file_name}"
        link_vid = f"https://photo.gachmen.org/image/image_user/{id_user}/mebau/{folder}/{file_name}"
        print("VIDEO_____" + str(vid_path) + "___KET_QUA" + str(path_folder))
        start_time = time.time()
        try:
            core.runvid(src_path, vid_path, out_path)
            execution_time = time.time() - start_time

            dataReturn = save_video_to_mysql_swap_imagevideo_mebau(
                image, vid_path, link_vid, id_user, device, ip, "mebau"
            )
            print("_____LINKVIDEO____" + str(link_vid))
            return dataReturn

        except Exception as e:
            print(
                str(out_path)
                + "___________________________BI_EXPTION_KHI_SWAP_VIDEO___Error occurred during video generation:____"
                + str(e)
            )
            data = {
                "id_saved": "",
                "link_video_goc": vid_path,
                "link_image": image,
                "link_vid_da_swap": link_vid,
                "thoigian_sukien": "",
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": "",
                "message": "ket qua khong thanh cong, Bi Exeption: " + str(e),
            }
        return data
    else:
        print("ket qua khong thanh cong, khong tim thay image: " + str(image))
        data = {
            "id_saved": "",
            "link_video_goc": vid_path,
            "link_image": image,
            "link_vid_da_swap": link_vid,
            "thoigian_sukien": "",
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "loai_sk": "",
            "message": "ket qua khong thanh cong, khong tim thay image: " + str(image),
        }
        return data


def gen_video_fancy_mebau(id_user, id_video, linkimg, device, ip):
    print("ID_VIDEO " + str(id_video))
    print("_____________________linkimg____" + str(linkimg))
    data = swap_video_fancy_mebau(id_user, id_video, linkimg, device, ip)

    torch.cuda.empty_cache()
    return data
