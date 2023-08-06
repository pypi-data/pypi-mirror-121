import binascii
import getpass
import gzip
import hashlib
import http.cookiejar
import json
import os
import pathlib
import shutil
import subprocess
import time
import urllib
from typing import Any, TypeVar, Union


def openWindowsFolder(folder: str):
    os.system(f"start explorer {folder}")


def getPath(basePath: str, *parList: str) -> str:
    return os.path.abspath(os.path.join(basePath, *parList))


def getDesktopPath(*parList: Any):
    return getPath(os.path.expanduser("~"), "Desktop", *parList)


def writeFile(file: str, data: str, encoding: str = 'utf8', newline: str = '\n'):
    makeFolder(os.path.dirname(file))
    with open(file, 'w', encoding=encoding, newline=newline) as f:
        f.write(data)
        f.flush()
        f.close()
    return file


def writeBinFile(file: str, data: bytes):
    makeFolder(os.path.dirname(file))
    with open(file, 'wb') as f:
        f.write(data)
        f.flush()
        f.close()
    return file


def readFile(file: str, encoding: str = 'utf8', newline: str = '\n'):
    with open(file, 'r', encoding=encoding, newline=newline) as f:
        data = f.read()
        f.close()
    return data


def readBinFile(file: str):
    with open(file, 'rb') as f:
        data = f.read()
        f.close()
    return data


def jsonDumps(value: Any):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def remove(fileOrFolder: str):
    if os.path.isfile(fileOrFolder):
        os.remove(fileOrFolder)
    elif os.path.isdir(fileOrFolder):
        shutil.rmtree(fileOrFolder)


def makeFolder(folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)


def clearFolder(*folderAry: str):
    for folder in folderAry:
        if os.path.isdir(folder):
            for target in getFileAndFolderList(folder):
                remove(target)


def copy(fromFileOrFolder: str, toFileOrFolder: str):
    if os.path.isfile(fromFileOrFolder):
        fromFile = fromFileOrFolder
        toFile = toFileOrFolder
        makeFolder(getParentFolder(toFile))
        shutil.copyfile(fromFile, toFile)
    elif os.path.isdir(fromFileOrFolder):
        fromFolder = fromFileOrFolder
        toFolder = toFileOrFolder
        makeFolder(getParentFolder(toFolder))
        shutil.copytree(fromFolder, toFolder)


def getParentFolder(fileOrFolder: str, level: int = 1):
    result = fileOrFolder
    while level > 0:
        level -= 1
        result = os.path.dirname(result)
    return result


def getFileExtName(file: str):
    return file[file.rfind('.') + 1:].lower()


def getFileBaseName(file: str):
    fileName = os.path.basename(file)
    return fileName[:fileName.rfind(".")]


def getFileList(folder: str):
    ary: list[str] = []
    for targetName in os.listdir(folder):
        target = os.path.join(folder, targetName)
        if os.path.isfile(target):
            ary.append(target)
    return ary


def getFolderList(folder: str):
    ary: list[str] = []
    for targetName in os.listdir(folder):
        target = os.path.join(folder, targetName)
        if os.path.isdir(target):
            ary.append(target)
    return ary


def getFileAndFolderList(folder: str):
    ary: list[str] = []
    for targetName in os.listdir(folder):
        target = os.path.join(folder, targetName)
        ary.append(target)
    return ary


def getAllFileList(folder: str):
    ary: list[str] = []
    for targetName in getFileAndFolderList(folder):
        target = os.path.join(folder, targetName)
        if os.path.isfile(target):
            ary.append(target)
        elif os.path.isdir(target):
            ary.extend(getAllFileList(target))
    return ary


def getAllFolderList(folder: str):
    ary: list[str] = []
    for targetName in getFileAndFolderList(folder):
        target = os.path.join(folder, targetName)
        if os.path.isdir(target):
            ary.append(target)
            ary.extend(getAllFolderList(target))
    return ary


def getAllFileAndFolderList(folder: str):
    ary: list[str] = []
    for targetName in getFileAndFolderList(folder):
        target = os.path.join(folder, targetName)
        if os.path.isfile(target):
            ary.append(target)
        elif os.path.isdir(target):
            ary.append(target)
            ary.extend(getAllFileAndFolderList(target))
    return ary


def getFileMD5(file: str):
    data = readBinFile(file)
    return hashlib.md5(data).hexdigest()


def getFileCRC(file: str):
    return getDataCRC(readBinFile(file))


def getContentCRC(content: str):
    return getDataCRC(content.encode())


def getDataCRC(data: bytes):
    return hex(binascii.crc32(data))[2:].zfill(8)


def getClassFullName(classItem: Any):
    return getattr(classItem, '__module__') + '.' + getattr(classItem, '__name__')


def makeTempWorkspace(clearOneDayBefore: bool = True):
    baseWorkspaceFoler = getPath(os.path.expanduser("~"), "beniutils.workspace")
    makeFolder(baseWorkspaceFoler)
    nowTime = int(time.time() * 10000000)
    if clearOneDayBefore:
        oneDayBeforeTime = nowTime - 24 * 60 * 60 * 10000000
        for folderName in os.listdir(baseWorkspaceFoler):
            if int(folderName) < oneDayBeforeTime:
                remove(getPath(baseWorkspaceFoler, folderName))
    for i in range(100):
        nowTime += i
        workspaceFolder = getPath(baseWorkspaceFoler, str(nowTime))
        if not os.path.exists(workspaceFolder):
            makeFolder(workspaceFolder)
            return workspaceFolder
    raise Exception("创建tempWorkspace目录失败")


def execute(*pars: str, showCmd: bool = True, showOutput: bool = False, ignoreError: bool = False):
    from . import log
    cmd = ' '.join(pars)
    if showCmd:
        log.info(cmd)
    p = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    outBytes, errBytes = p.communicate()
    p.kill()
    if showOutput:
        from .byte import decode
        outStr = decode(outBytes).replace("\r\n", "\n")
        errStr = decode(errBytes).replace("\r\n", "\n")
        if outStr:
            log.info(f"output:\n{outStr}")
        if errStr:
            log.info(f"error:\n{errStr}")
    if not ignoreError and p.returncode != 0:
        raise Exception("执行命令出错")
    return p.returncode, outBytes, errBytes


def executeWinScp(winscpExe: str, keyFile: str, server: str, commandAry: list[str], showCmd: bool = True):
    logFile = getPath(str(pathlib.Path.home()), "executeWinScp.log")
    remove(logFile)
    ary = [
        'option batch abort',
        'option transfer binary',
        f'open sftp://{server} -privatekey={keyFile} -hostkey=*',
    ]
    ary += commandAry
    ary += [
        'close',
        'exit',
    ]
    # /console
    cmd = f'{winscpExe} /log={logFile} /loglevel=0 /command ' + ' '.join('"%s"' % x for x in ary)
    return execute(cmd, showCmd=showCmd)


def executeTry(*parList: str, output: str = "", error: str = ""):
    _, outputBytes, errorBytes = execute(*parList, showCmd=False, ignoreError=True)
    if type(output) == str:
        output = output.encode()
    if output and output not in outputBytes:
        raise Exception(f"命令执行失败：{' '.join(parList)}")
    if type(error) == str:
        error = error.encode()
    if error and error not in errorBytes:
        raise Exception(f"命令执行失败：{' '.join(parList)}")


def syncFolder(fromFolder: str, toFolder: str):
    # 删除多余目录
    toSubFolderList = sorted(getAllFolderList(toFolder), reverse=True)
    for toSubFolder in toSubFolderList:
        fromSubFolder = os.path.join(fromFolder, toSubFolder[len(toFolder + os.path.sep):])
        if not os.path.isdir(fromSubFolder):
            remove(toSubFolder)
    # 删除多余文件
    toFileList = getAllFileList(toFolder)
    for toFile in toFileList:
        fromFile = os.path.join(fromFolder, toFile[len(toFolder + os.path.sep):])
        if not os.path.isfile(fromFile):
            remove(toFile)
    # 同步文件
    fromFileList = getAllFileList(fromFolder)
    for fromFile in fromFileList:
        toFile = os.path.join(toFolder, fromFile[len(fromFolder + os.path.sep):])
        if os.path.isfile(toFile):
            fromData = readBinFile(fromFile)
            toData = readBinFile(toFile)
            if fromData != toData:
                writeBinFile(toFile, fromData)
        else:
            remove(toFile)
            copy(fromFile, toFile)
    # 添加新增目录
    fromSubFolderList = sorted(getAllFolderList(fromFolder), reverse=True)
    for fromSubFolder in fromSubFolderList:
        toSubFolder = os.path.join(toFolder, fromSubFolder[len(fromFolder + os.path.sep):])
        if not os.path.isdir(toSubFolder):
            makeFolder(toSubFolder)


_DEFAULT_FMT = '%Y-%m-%d %H:%M:%S'


def timestampByStr(value: str, fmt: str = _DEFAULT_FMT):
    return int(time.mktime(time.strptime(value, fmt)))


def strByTimestamp(timestamp: float = time.time(), fmt: str = _DEFAULT_FMT):
    ary = time.localtime(timestamp)
    return time.strftime(fmt, ary)


def hold(msg: str = "", showInput: bool = True, *exitValueList: str):
    msg = msg or "测试暂停，输入exit可以退出"
    exitValueList = exitValueList or ("exit",)
    inputFunc = showInput and input or getpass.getpass
    while True:
        inputValue = inputFunc(f"{msg}：")
        if inputValue in exitValueList:
            return inputValue

# ---- http


_defaultHeader = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}


# Cookie
_cookie = http.cookiejar.CookieJar()
_cookieProc = urllib.request.HTTPCookieProcessor(_cookie)
_opener = urllib.request.build_opener(_cookieProc)
urllib.request.install_opener(_opener)


def _getHeaderByDefault(headers: dict[str, str]):
    result = dict(_defaultHeader)
    if headers:
        for key, value in headers.items():
            result[key] = value
    return result


def httpGet(url: str, headers: dict[str, str] = {}, timeout: int = 30, retry: int = 3):
    method = 'GET'
    headers = _getHeaderByDefault(headers)
    result = None
    response = None
    currentTry = 0
    while currentTry < retry:
        currentTry += 1
        try:
            request = urllib.request.Request(url=url, headers=headers, method=method)
            response = urllib.request.urlopen(request, timeout=timeout)
            result = response.read()
            response.close()
            break
        except Exception:
            pass
    contentEncoding = response.headers.get('Content-Encoding')
    if contentEncoding == 'gzip':
        result = gzip.decompress(result)
    return result, response


def httpPost(url: str, data=None, headers: dict[str, str] = {}, timeout: int = 30, retry: int = 3):
    method = 'POST'
    headers = _getHeaderByDefault(headers)
    postData = data
    if type(data) == dict:
        postData = urllib.parse.urlencode(data).encode()
    result = None
    response = None
    currentTry = 0
    while currentTry < retry:
        currentTry += 1
        try:
            request = urllib.request.Request(url=url, data=postData, headers=headers, method=method)
            response = urllib.request.urlopen(request, timeout=timeout)
            result = response.read()
            response.close()
            break
        except Exception:
            pass
    return result, response


IntFloatStr = Union[int, float, str]
IntFloat = Union[int, float]


def toFloat(value: IntFloatStr, default: float):
    result = default
    try:
        result = float(value)
    except:
        pass
    return result


def toInt(value: IntFloatStr, default: int):
    result = default
    try:
        result = int(value)
    except:
        pass
    return result


def getLimitedValue(value: IntFloat, minValue: IntFloat, maxValue: IntFloat):
    value = min(value, maxValue)
    value = max(value, minValue)
    return value


_xPar = "0123456789abcdefghijklmnopqrstuvwxyz"


def intToX(value: int) -> str:
    n = len(_xPar)
    return ((value == 0) and "0") or (intToX(value // n).lstrip("0") + _xPar[value % n])


def xToInt(value: str):
    return int(value, len(_xPar))


# def scrapy(urlList, parseFun, extendSettings=None):

#     from scrapy.crawler import CrawlerProcess
#     from scrapy.utils.log import get_scrapy_root_handler
#     import scrapy.http

#     resultList = []
#     resultUrlList = urlList[:]

#     class TempSpider(scrapy.Spider):

#         name = str(random.random())
#         start_urls = urlList

#         def parse(self, response):
#             itemList, urlList = parseFun(response)
#             if itemList:
#                 resultList.extend(itemList)
#             if urlList:
#                 for url in urlList:
#                     resultUrlList.append(url)
#                     yield scrapy.http.Request(url)

#     settings = {
#         'LOG_LEVEL': logging.INFO,
#         'LOG_FORMAT': '%(asctime)s %(levelname)-1s %(message)s',
#         'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S',
#         'DOWNLOAD_TIMEOUT': 5,
#         'CONCURRENT_REQUESTS': 50,
#         'RETRY_HTTP_CODES': [514],
#         'RETRY_TIMES': 5,
#         # 'ITEM_PIPELINES': {
#         #    ptGetClassFullName( TempPipeline ): 300,
#         # },
#     }
#     if extendSettings:
#         for k, v in extendSettings.items():
#             settings[k] = v

#     process = CrawlerProcess(settings)
#     process.crawl(TempSpider)
#     process.start()

#     rootHandler = get_scrapy_root_handler()
#     if rootHandler:
#         rootHandler.close()

#     # 函数执行后再调用logging都会有2次显示在控制台
#     logging.getLogger().handlers = []

#     return resultList, resultUrlList
