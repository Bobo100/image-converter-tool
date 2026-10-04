# Change-Image-Type-And-Size

用 Python(tkinter + Pillow)寫的小工具：一次選多張圖片，裁成指定比例並縮放，輸出成 PNG。

## 狀態

2023 年為自己的工作流程寫的工具，已不再加新功能。

## 使用方式

```bash
pip install -r requirements.txt
python image.py
```

1. 按「Add Files」選圖片(jpg、png、tiff、jfif、bmp、gif)
2. 在清單裡選要處理的檔案
3. 從下拉選單選尺寸，按「Resize Images」

圖片會先裁成目標比例再縮放，輸出到原圖所在的資料夾，檔名以原圖「上兩層資料夾」的名稱開頭:

| 選項 | 尺寸 | 輸出檔名 |
|---|---|---|
| `2560x1440xBig` | 2560×1440 | `<資料夾>_big_image.png` |
| `2560x1440xSlide` | 2560×1440 | `<資料夾>_slides_image_01.png`(已存在就往後編號) |
| `960x540xTitle` | 960×540 | `<資料夾>_title_image.png` |
| `600x900` | 600×900 | `<資料夾>_small_image.png` |

`image/`、`image2/` 是範例圖與輸出結果,`test/` 是開發時的實驗腳本。
