import json
import os
import posixpath
import uuid
from json import JSONDecodeError
from urllib.parse import unquote, urlsplit

import requests


def get_extension(filename):
    """
    returns extension of filename

    Args:
        filename (str): filename
    Returns:
        extension (str): returns extension in lowercase
    """
    return filename.rsplit('.', 1)[1].lower()


def is_allowed_extension(filename, formats):
    """
    checks whether filename extension is in formats

    Args:
        filename (str): filename
        formats (list): list of extensions in lowercase

    Returns:
        bool: True if filename extension is in formats, False otherwise

    Examples:
        >>> is_allowed_extension('video.mp4', ['mp4', '3gp', 'mkv'])
        True
        >>> is_allowed_extension('video.mp4', ['zip', 'tar'])
        False
    """
    return '.' in filename and get_extension(filename) in formats


def get_filename_from_url(url):
    """
    Args:
        url(str) : file url
    Returns:
        basename(str): file basename from url
    """
    url_path = urlsplit(url).path
    basename = posixpath.basename(unquote(url_path))
    # if (os.path.basename(basename) != basename or
    #     unquote(posixpath.basename(urlpath)) != basename):
    #     raise ValueError  # reject '%2f' or 'dir%5Cbasename.ext' on Windows
    return basename


def download_file(url, dirname, add_prefix=True):
    """
    downloads files from url

    Args:
        url (str): url
        dirname (str): directory name in which file will be downloading
        add_prefix (bool): adds uuid as prefix to filename if True, nothing otherwise

    Returns:
        bool: True if success, False otherwise
        str: file path if success, error message otherwise
    """
    try:
        if add_prefix:
            filename = os.path.join(dirname, uuid.uuid1().hex + get_filename_from_url(url))
        else:
            filename = os.path.join(dirname, get_filename_from_url(url))
        res = requests.get(url, allow_redirects=True, stream=True)
        print(res)
        if not res.ok:
            return False, 'url doest not exist: {}'.format(url)
        if len(res.content) <= 0:
            return False, 'no data exist in the url. {}'.format(url)
        with open(filename, "wb") as f:
            for chunk in res.iter_content(chunk_size=512 * 1024):
                if chunk:
                    f.write(chunk)
        return True, filename
    except requests.exceptions.ConnectionError as e:
        print(e)
        return False, 'url doest not exist: {}'.format(url)
    except Exception as e:
        print(e)
        return False, 'error in url: {}'.format(url)


def is_json(string=None, path=None):
    try:
        if string:
            json.loads(string)
            return True
        if path:
            json.load(open(path, "r"))
            return True
    except JSONDecodeError:
        return False
    except Exception:
        return False


def get_file_size(file_path, unit='MB'):
    file_size = os.path.getsize(file_path)  # v /1000/1000, ".2f"))
    return format(float({
                            'byte': file_size,
                            'kb': file_size / 1000,
                            'mb': file_size / 1000 / 1000,
                            'gb': file_size / 1000 / 1000 / 1000,
                            'tb': file_size / 1000 / 1000 / 1000 / 1000
                        }[unit.lower()]), ".2f")
