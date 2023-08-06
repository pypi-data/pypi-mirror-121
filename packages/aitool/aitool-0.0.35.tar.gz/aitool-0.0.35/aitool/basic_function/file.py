# -*- coding: UTF-8 -*-
# @Time    : 2020/10/29
# @Author  : xiangyuejia@qq.com
import os
import json
import fileinput
import warnings
import pickle
import pandas as pd
import inspect
import requests
from tqdm import tqdm
import math
import functools
import zipfile
from typing import Any, List, Union, NoReturn
from aitool import split_dict


def file_exist(file: str) -> bool:
    return os.path.exists(file)


def make_dir(file: str, is_dir=False) -> NoReturn:
    if is_dir:
        path = file
    else:
        path, _ = os.path.split(file)
    if path and not os.path.exists(path):
        os.makedirs(path)


def dump_json(
        obj: Any,
        file: str,
        formatting: bool = False,
        ensure_ascii: bool = False,
        **kwargs,
) -> NoReturn:
    make_dir(file)
    kwargs['ensure_ascii'] = ensure_ascii
    if formatting:
        kwargs['sort_keys'] = True
        kwargs['indent'] = 4
        kwargs['separators'] = (',', ':')
    with open(file, 'w', encoding='utf-8') as fw:
        json.dump(obj, fw, **kwargs)


def load_json(file: str, **kwargs,) -> Any:
    if not os.path.isfile(file):
        print('incorrect file path')
        raise FileExistsError
    with open(file, 'r', encoding='utf-8') as fr:
        return json.load(fr, **kwargs,)


def dump_pickle(obj: Any, file: str, **kwargs) -> NoReturn:
    make_dir(file)
    with open(file, 'wb') as fw:
        pickle.dump(obj, fw, **kwargs)


def load_pickle(file: str, **kwargs) -> Any:
    if not os.path.isfile(file):
        print('incorrect file path')
        raise Exception
    with open(file, 'rb') as fr:
        return pickle.load(fr, **kwargs)


def dump_lines(data: List[Any], file: str) -> NoReturn:
    make_dir(file)
    with open(file, 'w', encoding='utf8') as fout:
        for d in data:
            print(d, file=fout)


def load_line(
        file: str,
        separator: Union[None, str] = None,
        separator_time: int = -1,
        form: str = None,
) -> List[Any]:
    with open(file, 'r', encoding='utf8') as fin:
        for line in fin:
            item = line.rstrip('\n\r')
            if separator:
                if separator_time == -1:
                    item = item.split(separator)
                else:
                    item = item.split(separator, separator_time)
            if form == 'set':
                item = set(item)
            yield item


def load_big_data(
        file: str,
        separator: Union[None, str] = None,
        separator_time: int = -1,
        form: str = None,
) -> List[Any]:
    warnings.warn("load_big_data 和 load_line 的功能一样，但内部实现不同，推荐优先使用load_line ", DeprecationWarning)
    for line in fileinput.input([file]):
        item = line.rstrip('\n\r')
        if separator:
            if separator_time == -1:
                item = item.split(separator)
            else:
                item = item.split(separator, separator_time)
        yield item


def load_lines(
        file: str,
        separator: Union[None, str] = None,
        separator_time: int = -1,
        form: str = None,
) -> List[Any]:
    data = []
    with open(file, 'r', encoding='utf8') as fin:
        for d in fin.readlines():
            item = d.rstrip('\n\r')
            if separator:
                if separator_time == -1:
                    item = item.split(separator)
                else:
                    item = item.split(separator, separator_time)
            data.append(item)
    if form == 'set':
        data = set(data)
    if form == 'dict':
        print('dict格式用每行的第一个元素作为key, 其后的元素的列表作为value。'
              '如果一行中不包含多个元素会报错。'
              '如果有相同的第一个元素会发生覆盖。')
        data = {item[0]: item[1:] for item in data}
    return data


MAX_LENGTH_XLSX = 1048576


def dump_panda(
        data: List[Any],
        file: str,
        file_format: str,
        dump_index: bool = False,
        **kwargs,
) -> NoReturn:
    make_dir(file)
    if 'index' in kwargs and isinstance(kwargs['index'], bool):
        raise ValueError('The parameter `index` is for pd.DataFrame. '
                         'If want to set the `index` for panda.to_csv/excel please use `dump_index`')
    if file_format == 'excel':
        if len(data) < MAX_LENGTH_XLSX - 100:
            selected_kwargs, _ = split_dict(kwargs, inspect.getfullargspec(pd.DataFrame).args)
            df = pd.DataFrame(data, **selected_kwargs)
            selected_kwargs, _ = split_dict(kwargs, inspect.getfullargspec(df.to_csv).args)
            selected_kwargs['index'] = dump_index
            df.to_excel(file, **selected_kwargs)
        else:
            piece_num = 0
            while data:
                piece_data = data[:MAX_LENGTH_XLSX - 100]
                piece_file = file + '_piece_' + str(piece_num) + '.xlsx'
                data = data[MAX_LENGTH_XLSX - 100:]
                selected_kwargs, _ = split_dict(kwargs, inspect.getfullargspec(pd.DataFrame).args)
                df = pd.DataFrame(piece_data, **selected_kwargs)
                selected_kwargs, _ = split_dict(kwargs, inspect.getfullargspec(df.to_csv).args)
                selected_kwargs['index'] = dump_index
                df.to_excel(piece_file, **selected_kwargs)
                piece_num += 1
    if file_format == 'csv':
        selected_kwargs, _ = split_dict(kwargs, inspect.getfullargspec(pd.DataFrame).args)
        df = pd.DataFrame(data, **selected_kwargs)
        selected_kwargs, _ = split_dict(kwargs, inspect.getfullargspec(df.to_csv).args)
        selected_kwargs['index'] = dump_index
        df.to_csv(file, **selected_kwargs)


dump_csv = functools.partial(dump_panda, file_format='csv')
dump_excel = functools.partial(dump_panda, file_format='excel')


def load_excel(*args, **kwargs) -> List:
    df = pd.read_excel(*args, **kwargs)
    data = df.values
    return data


def load_csv(*args, **kwargs) -> List:
    df = pd.read_csv(*args, **kwargs)
    data = df.values
    return data


def download_file(url: str, directory: str) -> str:
    """
    download a file from url
    :param url: url
    :param directory: save file in the directory
    :return: the path of the file has been downloaded.
    """
    chunk_size = 1024
    make_dir(directory, is_dir=True)
    _, name = os.path.split(url)
    resp = requests.get(url, stream=True)
    content_size = math.ceil(int(resp.headers['Content-Length']) / chunk_size)
    path = os.path.join(directory, name)
    with open(path, "wb") as file:
        for data in tqdm(iterable=resp.iter_content(1024), total=content_size, unit='k', desc=name):
            file.write(data)
    return path


def zip(src: str, tgt: str = '') -> NoReturn:
    """
    zip a file or a director.
    :param src: a file or a director
    :param tgt: Optional, the output file
    :return: NoReturn
    """
    # if tgt is Empty, then name the zipped file with a suffix .zip and save in the same director of src file/dir
    if not tgt:
        src_path, src_name = os.path.split(os.path.normpath(src))
        tgt_file = os.path.join(src_path, src_name+'.zip')
    # if tgt is a director, then name the zipped file with a suffix .zip and save in the director tgt
    _, tgt_name = os.path.split(tgt)
    if '.' not in tgt_name:
        src_path, src_name = os.path.split(os.path.normpath(src))
        tgt = os.path.join(tgt, src_name+'.zip')
    make_dir(tgt)
    z = zipfile.ZipFile(tgt, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(src):
        f_path = dir_path.replace(src, '')
        f_path = f_path and f_path + os.sep or ''
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), f_path+filename)
    z.close()


def unzip(src: str, tgt: str = '') -> NoReturn:
    if not tgt:
        tgt, _ = os.path.split(os.path.normpath(src))
    make_dir(tgt)
    r = zipfile.is_zipfile(src)
    if r:
        fz = zipfile.ZipFile(src, 'r')
        for file in fz.namelist():
            fz.extract(file, tgt)
    else:
        print('This is not a zip file')


def prepare_data(url: str, directory: str = '', packed: bool = False, pack_way: str = '', tmp_dir: str = '') -> NoReturn:
    if not packed:
        download_file(url, directory)
    else:
        if not tmp_dir:
            from aitool.datasets import PATH as DATA_PATH
            tmp_dir = os.path.join(DATA_PATH, 'tmp')
        packed_file = download_file(url, tmp_dir)
        unzip(packed_file, directory)


if __name__ == '__main__':
    test_data = [[i] for i in range(26)]
    test_file = 'test.xlsx'
    dump_excel(test_data, test_file)
