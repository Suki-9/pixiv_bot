# Pixiv Archiver Bot

## なにこれは
Pixiv上にアップロードされているイラストをDiscord Botを介してアーカイブすることができます<br>
コレがどういうソフトウェアなのかを理解したうえで、使い方は各々の良心に任されています(MITライセンス)<br>
パッケージマネージャとかそういうのは使用してないです(Python周りのエコシステムに対するヘイトスピーチ)

## 使い方
いい感じにModuleをインストールして各種設定を行ってよしなに起動してくださいな。
```sh
$ pip install -r requirements.txt
$ cp src/example.yaml src/config.yaml
$ python src/init.py
$ python src/main.py
```

前提としてsqlite3がインストール済であること<br>
私はv3.10で開発しています、動かないとかの不具合は適当にググって解決してください

## 駄文(読まなくていいです)
Pixivのイラストってなんか気づいたら消えてたりしますよね。<br>
私は結構消えたイラストを覚えていたりするのでかなり悲しい...

# License
MIT License

Copyright © 2024 Suki_music9

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.