#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import pefile
from pefile import PEFormatError
import hashlib
from ctypes import cdll, string_at
from collections import Counter
import sys
sys.path.append("/polyhawk/mds/analysis/sandbox")
from lib.cuckoo.common.config import Config
from lib.cuckoo.common.abstracts import StaticScan
from lib.cuckoo.common.constants import CONTENT_ROOT, LIB_ROOT

import logging.handlers
log = logging.getLogger()
formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")

ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

log.setLevel(logging.INFO)

cfg = Config("staticscan").get("peAnalyzer")

so_path = cfg.so_path
cfg_path = cfg.cfg_path
HAVE_PEFILE = False
try:
    libpefile = cdll.LoadLibrary(os.path.join(LIB_ROOT, so_path))
    ret = libpefile.pecker_gmcla_init(os.path.join(CONTENT_ROOT, cfg_path))
    if not ret:
        log.debug("load %s successfully", so_path)
        HAVE_PEFILE = True
    else:
        log.error("load %s failed, ret: %s" % (so_path, ret))
except:
    log.exception("load %s failed", so_path)

# DLL_API_FEATURES = [" slc.dll", " api-ms-win-core-errorhandling-l1-1-0.dll",
#                     " api-ms-win-core-libraryloader-l1-1-0.dll", " winsta.dll", " msvbvm60.dll", " secur32.dll",
#                     " mfc42u.dll", " userenv.dll", " setupapi.dll", " uxtheme.dll",
#                     " api-ms-win-security-base-l1-1-0.dll", " api-ms-win-core-processthreads-l1-1-0.dll",
#                     " powrprof.dll", " mfc42.dll", " api-ms-win-core-misc-l1-1-0.dll",
#                     " api-ms-win-core-profile-l1-1-0.dll", " api-ms-win-core-localregistry-l1-1-0.dll", " wbemcomn.dll",
#                     " oledlg.dll", " api-ms-win-core-sysinfo-l1-1-0.dll", " mswsock.dll", " ntdll.dll", "iswalpha",
#                     "SetClassLongA", "SetThreadUILanguage", "ConvertSidToStringSidW", "RegisterTraceGuidsW",
#                     "NtQueryValueKey", "CheckTokenMembership", "_wsetlocale", "UnregisterTraceGuids", "wcscat_s",
#                     "VerSetConditionMask", "RtlLengthSid", "memmove_s", "?what@exception@@UBEPBDXZ",
#                     "RtlCaptureContext", "ShellExecuteA", "RtlFreeHeap", "swprintf_s", "_ftol2", "AppendMenuA",
#                     "GetTraceEnableLevel", "wcscpy_s", "_CItan", "__wgetmainargs", "RevertToSelf",
#                     "ConvertStringSecurityDescriptorToSecurityDescriptorW", "RtlLookupFunctionEntry",
#                     "GetTraceLoggerHandle", "TraceMessage", "GetTraceEnableFlags", "RtlVirtualUnwind",
#                     "GetConsoleScreenBufferInfo", "SHBrowseForFolderA", "__C_specific_handler", "_fmode", "wcstol",
#                     "LookupAccountNameW", "NtDeviceIoControlFile", "_callnewh", "NtOpenFile", "vfwprintf", "__winitenv",
#                     "SHGetFileInfoA", "_commode", "wprintf", "RtlNtStatusToDosError"]
DLL_API_FEATURES = [' msi.dll', ' libgcc_s_dw2-1.dll', ' mscoree.dll', ' libstdc++-6.dll', ' qt5core.dll', ' olepro32.dll', '_Znwj', 'GdipSetInterpolationMode', 'SetAbortProc', 'CreateStatusWindowW', 'DrawStateW', 'GdipGetImagePixelFormat', 'MonitorFromWindow', '_CorExeMain', 'GdipBitmapUnlockBits', 'memchr', 'DragQueryFileW', 'SystemTimeToTzSpecificLocalTime', 'GdipGetImageWidth', 'GetDiskFreeSpaceW', 'InitializeSListHead', 'GdipDrawImageI', 'InternetCrackUrlW', 'CreateICA', 'localeconv', 'GdipDeleteGraphics', 'SignalObjectAndWait', 'CloseWindow', '__register_frame_info', 'VerSetConditionMask', 'GdipGetImageHeight', 'GetNearestPaletteIndex', 'VariantTimeToSystemTime', 'RtlCaptureContext', 'PathIsDirectoryW', 'CharUpperBuffW', 'GdipCreateBitmapFromScan0', 'GdipBitmapLockBits', 'EnumDisplayMonitors', 'VarBstrFromDate', '_ZdlPv', 'SubtractRect', '_ZTVN10__cxxabiv120__si_class_type_infoE', 'HttpOpenRequestW', 'AppendMenuW', '_CorDllMain', 'GdipDrawImageRectI', 'RtlUnwindEx', 'GdipCreateFromHDC', 'strerror', '_ZTVN10__cxxabiv117__class_type_infoE', 'SetLayeredWindowAttributes', 'RtlLookupFunctionEntry', 'MethCallEngine', '__deregister_frame_info', 'GradientFill', 'Shell_NotifyIconW', 'RtlVirtualUnwind', 'Ord(187)', 'CreateHatchBrush', 'HttpSendRequestW', 'TranslateAcceleratorW', 'GdipGetImageGraphicsContext', 'Ord(253)', '__C_specific_handler', 'RtlPcToFileHeader', '_fmode', '__mb_cur_max', 'LookupPrivilegeValueW', 'ExcludeUpdateRgn', 'EnumCalendarInfoW', 'MessageBoxIndirectW', 'GetMenuStringW', 'FreeConsole', 'modf', '_ZTVN10__cxxabiv121__vmi_class_type_infoE', 'InternetConnectW', 'DoDragDrop', '__vbaI4ErrVar', 'GetTextExtentPoint32W', 'ProcCallEngine', '__vbaGet3', 'WritePrivateProfileStringW', 'GetObjectType', 'OleDuplicateData']
strip_dll_api = map(str.strip, DLL_API_FEATURES)
SECTION_NAMES = ['rt_code', 'rt_data', 'nep', 'rsrc', 'bss', 'consent', 'rt_bss', 'reloc', 'pagelk', 'orpc', 'idata', 'rdata', 'fe_text', 'data', 'pdata', 'text', 'tls', 'other']
# SECTION_NAMES = [u'RT_CODE', u'RT_DATA', u'.nep', u'.rsrc', u'.bss', u'consent', u'RT_BSS', u'.reloc', u'PAGELK',
#                  u'.orpc', u'.idata', u'.rdata', u'FE_TEXT', u'.data', u'.pdata', u'.text', u'.tls', u'other']
# SECTION_NAMES = map(lambda x: x.strip('.').lower(), SECTION_NAMES)


def get_pe_info(target):
    row = [0] * (len(DLL_API_FEATURES) + len(SECTION_NAMES))
    try:
        pe = pefile.PE(target)
    except PEFormatError:
        # log.exception("%s, not valid PE File" % target)
        return None

    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            dll = entry.dll.lower()
            if dll in DLL_API_FEATURES:
                index = DLL_API_FEATURES.index(dll)
                row[index] = 1

            for imp in entry.imports:
                if imp.name in DLL_API_FEATURES:
                    index = DLL_API_FEATURES.index(imp.name)
                    row[index] = 1
    else:
        return None

    for section in pe.sections:
        se = section.Name.strip('.').strip("\x00").lower()
        if se in SECTION_NAMES:
            index = SECTION_NAMES.index(se)
            row[index + len(DLL_API_FEATURES)] = 1
        else:
            row[-1] += 1

    # change list to string
    return ",".join(map(str, row))


def mcla_match(target):
    pe_info = get_pe_info(target)
    if not pe_info:
        return "no_pe_info"

    p_category = libpefile.pecker_gmcla_group_predict_vec_data(pe_info, len(DLL_API_FEATURES) + len(SECTION_NAMES))
    if p_category:
        return string_at(p_category)
    else:
        return None


def mcla_match_count(target):
    pe_info = get_pe_info(target)
    if not pe_info:
        return -1
    category_count = libpefile.pecker_gmcla_group_checkall_vec_data(pe_info, len(DLL_API_FEATURES) + len(SECTION_NAMES))
    return category_count


def mcla_check(path):
    results = Counter()
    if os.path.isfile(path):
        results.update([mcla_match(path)])
    elif os.path.isdir(path):
        for target in os.listdir(path):
            target = os.path.join(path, target)
            results.update([mcla_match(target)])
    return results


def mcla_check_count(path):
    results = Counter()
    if os.path.isfile(path):
        results.update([mcla_match_count(path)])
    elif os.path.isdir(path):
        for target in os.listdir(path):
            target = os.path.join(path, target)
            results.update([mcla_match_count(target)])
    return results


def GetFileSha256(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.sha256()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


if __name__ == "__main__":
    if not HAVE_PEFILE:
        print("no PEFILE")

    csv_count = libpefile.pecker_gmcla_group_model_num()
    print "csv count: ", csv_count

    # dir_paths = ["/root/winexe/win7_32", "/root/winexe/win7_64", "/root/winexe/xpsp3", "/polydata/samples/worm"]
    dir_paths = ["/polydata/samples/worm"]
    # for dir_path in dir_paths:
    #     results = dict(mcla_check(dir_path))
    #     count_samples = len(os.listdir(dir_path))
    #     count_no_pe_info = results["no_pe_info"] if "no_pe_info" in results else 0
    #     print dir_path, count_samples, results
    #     print "white detection ratio:", results[None] * 1.0 / (count_samples - count_no_pe_info)
    count_mcla = Counter()
    for target in os.listdir(dir_paths[0]):
        target = os.path.join(dir_paths[0], target)
        count = mcla_match_count(target)
        # print target, count
        count_mcla.update([count])
    print dict(count_mcla)
    # Sha256 = GetFileSha256(target)
    # print Sha256
