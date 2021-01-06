
Arnold Packaging
==

1. 從官方 Release Note 確認該版本所對應的 Arnold Core 版號，並製作相應版本的 Core 封包
2. 下載安裝檔，用 7-zip 解壓縮(或直接跑安裝)後，放置 `.ico` 圖示，有必要的話清除一些像 Uninstall 的冗餘檔案 (MtoA)，或者直接忽略外層的 License 及其他冗餘檔案 (HtoA)
3. 打包成 `.zip`，並依照 Rez 封包名稱及其 variants 的層級放置於 `REZUTIL_ZIP_ROOT` 這個環境變數所指向的目錄中。


Notes:

Maya 2018 may pops up the following warning message on startup in Maya output window, if `MAYA_MODULE_PATH` is set to read `mtoa.mod` file that lives in package root.
```
sys:1: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
```
