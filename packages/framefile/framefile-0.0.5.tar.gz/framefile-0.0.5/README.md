[![PyPI version shields.io](https://img.shields.io/pypi/v/framefile.svg)](https://pypi.python.org/pypi/framefile/)
[![Generic badge](https://img.shields.io/badge/Python-3.7+-blue.svg)](#)
[![Generic badge](https://img.shields.io/badge/Tested_on-Windows%20|%20Linux-blue.svg)](#)
[![Downloads](https://pepy.tech/badge/framefile/month)](https://pepy.tech/project/framefile)

# [framefile](https://github.com/rtmigo/framefile_py#readme)

Python library for parsing and matching file name patterns like `IMG_####.JPG` or 
`IMG_%04d.JPG`.

Such patterns are used, for example, for the file names of individual video
frames in  [ffmpeg](https://www.ffmpeg.org/)
and [Blender](https://www.blender.org/).

# Install

```
pip3 install framefile
```

<details>
<summary>other options</summary>

#### Install pre-release from GitHub:
```
pip3 install git+https://github.com/rtmigo/framefile_py@staging#egg=framefile
```

</details>

# Use

## Guess pattern from file name

```python
import framefile

print(framefile.filename_to_hash_pattern("IMG_4567.JPG"))  # IMG_####.JPG
print(framefile.filename_to_pct_pattern("IMG_4567.JPG"))  # IMG_%04d.JPG
```



## Find files by pattern

```python
import glob
import framefile

file_mask = framefile.hash_pattern_to_glob('/path/to/img####.jpg')

print(glob.glob(file_mask))

# prints all files matching /path/to/img####.jpg
```

For percent patterns `pct_pattern_to_glob` can be used instead of `hash_pattern_to_glob`.

## Match file names as strings

```python
import re
import framefile

regex = framefile.hash_pattern_to_regex('img####.jpg')

a = re.match(regex, 'img0023.jpg')
print(a.group(0))  # img0023.jpg
print(a.group(1))  # 0023

b = re.match(regex, 'anything.txt')
print(b)  # None
```

For percent patterns `pct_pattern_to_regex` can be used instead of `hash_pattern_to_regex`.

## Extract number from file name

```python
import framefile

x: int = framefile.hash_extract_number("img####.jpg", "img0023.jpg")

print(x)  # 23

try:
    y = framefile.hash_extract_number("img####.jpg", "thumbs.db")
except framefile.PatternMismatchError:
    print("Oops!")
```

For percent patterns `pct_extract_number` can be used instead of `hash_extract_number`.

