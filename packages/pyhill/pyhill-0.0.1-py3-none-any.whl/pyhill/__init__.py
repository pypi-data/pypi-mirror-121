from pymem import *
from pymem.process import *
import sys

#POINTERS: ----------------------------------------------------------
#x (FLOAT)
#0x004452F4
#0x0, 0x80, 0x0, 0x0, 0x104, 0x4, 0x514
#
#y (FLOAT)
#0x00286A4C
#0x4, 0x1AC, 0x0, 0x104, 0x4, 0x564
#
#z (FLOAT)
#0x004452F8
#0x78, 0x0, 0x0, 0x104, 0x4, 0x53C
#
#fov
#0x004452F8
#0x78, 0x0, 0x0, 0x104, 0x4, 0x970
#
#zoom
#0x004452F8
#0x78, 0x0, 0x0, 0x104, 0x4, 0x998
#
#rotation
#0x0027C5A8
#0x354, 0x74, 0x54, 0x28, 0x34, 0x34, 0xB78
#
#jump strength
#0x002863DC
#0x28, 0x34, 0x34, 0x948

def errorprint(text):
    print("\033[31m" + text + "\033[0m")
    sys.exit()

def getpointeraddress(base, offsets):
    addr = pymem.Pymem("Player.exe").read_int(base)
    for i in offsets:
        if i != offsets[-1]:
            addr = pymem.Pymem("Player.exe").read_int(addr + i)
    return addr + offsets[-1]

class get:
    fps = 0
    x = 0
    y = 0
    z = 0
    rotation = 0
    fov = 0
    zoom = 0
    jump = 0

def attach():
    try:
        pm = pymem.Pymem("Player.exe")
        client = process.module_from_name(pm.process_handle, "Player.exe").lpBaseOfDll
    except:
        errorprint("PyHill: Brick hill is not open! Could not attach.\n")

def modify(variable, value):
    pointerbase = ""
    pointeroffsets = ""

    if variable == "x":
        pointerbase = "0x004452F4"
        pointeroffsets = "0x0, 0x80, 0x0, 0x0, 0x104, 0x4, 0x514"
    if variable == "y":
        pointerbase = "0x00286A4C"
        pointeroffsets = "0x4, 0x1AC, 0x0, 0x104, 0x4, 0x564"
    if variable == "z":
        pointerbase = "0x004452F8"
        pointeroffsets = "0x78, 0x0, 0x0, 0x104, 0x4, 0x53C"
    if variable == "rotation":
        pointerbase = "0x0027C5A8"
        pointeroffsets = "0x354, 0x74, 0x54, 0x28, 0x34, 0x34, 0xB78"
    if variable == "fov":
        pointerbase = "0x004452F8"
        pointeroffsets = "0x78, 0x0, 0x0, 0x104, 0x4, 0x970"
    if variable == "zoom":
        pointerbase = "0x004452F8"
        pointeroffsets = "0x78, 0x0, 0x0, 0x104, 0x4, 0x998"
    if variable == "jump":
        pointerbase = "0x002863DC"
        pointeroffsets = "0x28, 0x34, 0x34, 0x948"

    exec("pymem.Pymem(\"Player.exe\").write_float(getpointeraddress(process.module_from_name(pymem.Pymem(\"Player.exe\").process_handle, \"Player.exe\").lpBaseOfDll + " + pointerbase + ", [" + pointeroffsets + "]), float(" + str(value) + "))")

def updateGet(only = ""):
    if only == "":
        try:
            get.fps = pymem.Pymem("Player.exe").read_int(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x0017270C, [0x0]))
            get.x = pymem.Pymem("Player.exe").read_float(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x004452F4, [0x0, 0x80, 0x0, 0x0, 0x104, 0x4, 0x514]))
            get.y = pymem.Pymem("Player.exe").read_float(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x00286A4C, [0x4, 0x1AC, 0x0, 0x104, 0x4, 0x564]))
            get.z = pymem.Pymem("Player.exe").read_float(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x004452F8, [0x78, 0x0, 0x0, 0x104, 0x4, 0x53C]))
            get.rotation = pymem.Pymem("Player.exe").read_double(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x0027C5A8, [0x354, 0x74, 0x54, 0x28, 0x34, 0x34, 0xB78]))
            get.fov = pymem.Pymem("Player.exe").read_double(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x004452F8, [0x78, 0x0, 0x0, 0x104, 0x4, 0x970]))
            get.zoom = pymem.Pymem("Player.exe").read_double(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x004452F8, [0x78, 0x0, 0x0, 0x104, 0x4, 0x998]))
            get.jump = pymem.Pymem("Player.exe").read_double(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x0027CFCC, [0x54, 0x4, 0x0, 0x28, 0x34, 0x34, 0x948]))
        except:
            errorprint("PyHill: Something went wrong! (updateGet())")
    if only == "fps":
        try:
            get.fps = pymem.Pymem("Player.exe").read_int(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x0017270C, [0x0]))
        except:
            errorprint("PyHill: Something went wrong! (updateGet('fps'))")
    if only == "x":
        try:
            get.x = pymem.Pymem("Player.exe").read_float(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x004452F4, [0x0, 0x80, 0x0, 0x0, 0x104, 0x4, 0x514]))
        except:
            errorprint("PyHill: Something went wrong! (updateGet('x'))")
    if only == "y":
        try:
            get.y = pymem.Pymem("Player.exe").read_float(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x00286A4C, [0x4, 0x1AC, 0x0, 0x104, 0x4, 0x564]))
        except:
            errorprint("PyHill: Something went wrong! (updateGet('y'))")
    if only == "z":
        try:
            get.z = pymem.Pymem("Player.exe").read_float(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x004452F8, [0x78, 0x0, 0x0, 0x104, 0x4, 0x53C]))
        except:
            errorprint("PyHill: Something went wrong! (updateGet('z'))")
    if only == "rotation":
        try:
            get.rotation = pymem.Pymem("Player.exe").read_double(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x0027C5A8, [0x354, 0x74, 0x54, 0x28, 0x34, 0x34, 0xB78]))
        except:
            errorprint("PyHill: Something went wrong! (updateGet('rotation'))")
    if only == "fov":
        try:
            get.fov = pymem.Pymem("Player.exe").read_double(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x004452F8, [0x78, 0x0, 0x0, 0x104, 0x4, 0x970]))
        except:
            errorprint("PyHill: Something went wrong! (updateGet('fov'))")
    if only == "zoom":
        try:
            get.zoom = pymem.Pymem("Player.exe").read_double(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x004452F8, [0x78, 0x0, 0x0, 0x104, 0x4, 0x998]))
        except:
            errorprint("PyHill: Something went wrong! (updateGet('zoom'))")
    if only == "jump":
        try:
            get.jump = pymem.Pymem("Player.exe").read_double(getpointeraddress(process.module_from_name(pymem.Pymem("Player.exe").process_handle, "Player.exe").lpBaseOfDll + 0x0027CFCC, [0x54, 0x4, 0x0, 0x28, 0x34, 0x34, 0x948]))
        except:
            errorprint("PyHill: Something went wrong! (updateGet('jump'))")

def modifyCustom(base, offsets, datatype, value):
    datatype2 = datatype
    if datatype == "double":
        datatype = "float"
        datatype2 = "double"
    if datatype == "string" or "str":
        datatype = "str"
        datatype2 = "string"
    if datatype == "integer" or "int":
        datatype = "int"
        datatype2 = "int"
    
    exec("pymem.Pymem(\"Player.exe\").write_" + datatype2 + "(getpointeraddress(process.module_from_name(pymem.Pymem(\"Player.exe\").process_handle, \"Player.exe\").lpBaseOfDll + " + base + ", [" + offsets + "]), " + datatype + "(" + str(value) + "))")