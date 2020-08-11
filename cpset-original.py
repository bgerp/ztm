
#!/usr/bin/env python3

import usb.core
import usb.control
import subprocess
import time
import shutil

#--
usb_id_vendor = 0x0930
usb_id_product = 0x6544
target_folder = "/home/zdravko/testing"
excluded = ["media_extern", "mmcblk02p2", "mmcblk0p2", "sb1", "sda1", "sda2",
        "sda3"]
#--

def get_mountedlist():

    # dev = usb.core.find(idVendor=usb_id_vendor, idProduct=usb_id_product)
    # if dev is not None:
    #     print(dev.get_active_configuration())
    #     return dev
    # return None

    return [(item.split()[0].replace("├─", "").replace("└─", "")) for item in subprocess.check_output([
            "lsblk"]).decode("utf-8").split("\n") if "└─" in item]

def identify(disk):
    command = "find /dev/disk -ls | grep /"+disk
    output = subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8")
    if "usb" in output:
        return True
    else:
        return False

done = []
while True:
    mounted = get_mountedlist()

    new_paths = [dev for dev in get_mountedlist() if not dev in done and not dev[1] == "/"]
    valid = [dev for dev in new_paths if (identify(dev[0]), dev[1].split("/")[-1]  in excluded) == (True, False)]
    if valid:
        subprocess.call(["mkdir","/media/updateUsb"])
        for item in valid:
            print(item)

            #target = target_folder+"/"+item[1].split("/")[-1]
            try:
                subprocess.call(["mount", "/dev/" + item, "/media/updateUsb"]);
                shutil.rmtree(target_folder)
            except FileNotFoundError:
                pass
            shutil.copytree("/media/updateUsb/", target_folder)
        done = mounted
    time.sleep(4)

