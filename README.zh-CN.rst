doujinshi-dl
==============

`English <README.rst>`_ | `中文 <README.zh-CN.rst>`_

あなたも変態。 いいね?

|pypi| |license|

通过站点插件搜索、下载和整理同人志的命令行工具，支持批量 ID、收藏夹、
HTML 阅读器，以及 CBZ、PDF 和 ZIP 导出。

**使用前需要安装站点插件，并按站点要求配置认证。** 本文以
``doujinshi-dl-nhentai`` 为例；其他插件的认证方式、搜索语法和镜像支持请参考其说明。
建议使用 Python 3.12，以下安装命令会让 uv 选择该版本。

.. contents:: 目录
   :local:
   :depth: 2

快速开始
----------

先按 `uv 官方安装指南 <https://docs.astral.sh/uv/getting-started/installation/>`_
安装 uv。macOS 也可以通过 Homebrew 安装：

.. code-block:: bash

   brew install uv

将主程序和插件安装在同一个隔离环境中：

.. code-block:: bash

   uv tool install --python 3.12 --with doujinshi-dl-nhentai doujinshi-dl
   uv tool update-shell

重新打开终端，然后检查命令是否可用：

.. code-block:: bash

   doujinshi-dl --help

从站点账户设置中获取 API token，将下面的 ``YOUR_API_TOKEN`` 替换为实际值。
保存 token 和下载应分两次执行，设置 token 后程序会退出：

.. code-block:: bash

   doujinshi-dl --token "YOUR_API_TOKEN"
   doujinshi-dl --id 123855 --output ./downloads

默认下载到当前工作目录，并生成 HTML 阅读器。使用 ``--output`` 指定保存位置。

安装与更新
------------

管理命令行工具
~~~~~~~~~~~~~~~~

``uv tool`` 为工具管理独立的 Python 环境。插件必须通过 ``--with`` 装进主程序环境，
单独安装到另一个环境中的插件无法被发现。当前程序自动加载第一个发现的站点插件，
建议每个环境只安装一个站点插件。

更新或卸载：

.. code-block:: bash

   uv tool upgrade doujinshi-dl
   uv tool uninstall doujinshi-dl

需要导出 PDF 时，额外安装 ``img2pdf``，同时保留站点插件：

.. code-block:: bash

   uv tool install --python 3.12 --with doujinshi-dl-nhentai --with img2pdf doujinshi-dl

从源码安装
~~~~~~~~~~~~

适合使用仓库中的最新代码或参与开发。以下命令在项目目录创建虚拟环境，
以可编辑模式安装主程序，同时安装站点插件：

.. code-block:: bash

   git clone https://github.com/RicterZ/doujinshi-dl.git
   cd doujinshi-dl
   uv venv --python 3.12
   uv pip install -e . doujinshi-dl-nhentai

激活环境后，即可使用本文其余的 ``doujinshi-dl`` 命令：

.. code-block:: bash

   # bash / zsh
   source .venv/bin/activate
   doujinshi-dl --help

fish 使用 ``source .venv/bin/activate.fish``；Windows PowerShell 使用
``.venv\Scripts\Activate.ps1``。也可以直接运行虚拟环境中的可执行文件，
例如 macOS / Linux 下的 ``.venv/bin/doujinshi-dl``。

源码环境需要 PDF 支持时运行 ``uv pip install img2pdf``。
项目使用 Poetry 构建后端，uv 会自动处理构建依赖，无需单独安装 Poetry。

常用操作
----------

按 ID 下载或查看信息
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 一次下载多个 ID
   doujinshi-dl --id 123855 123866 123877 --output ./downloads

   # 只显示信息
   doujinshi-dl --id 123855 --show

   # 从文件读取 ID
   doujinshi-dl --file doujinshi.txt --output ./downloads

``doujinshi.txt`` 每行放一个数字 ID：

.. code-block:: text

   123855
   123866
   123877

搜索和收藏夹
~~~~~~~~~~~~~~

搜索、作者和收藏夹查询需要加 ``--download`` 才会下载结果。
分页支持单页、范围和组合，例如 ``1``、``3-5``、``1,3-5,7``；
``--page-all`` 用于获取全部搜索结果。

.. code-block:: bash

   # 搜索并下载第一页
   doujinshi-dl --search "full color" --page 1 --download

   # 下载指定页范围的收藏，每部作品之间等待 1 秒
   doujinshi-dl --favorites --page 3-5,7 --download --delay 1

搜索语法由插件决定。``--artist`` 可以按作者查询；``--sorting`` 可选
``recent``、``popular``、``popular-today``、``popular-week`` 或 ``date``，
默认值为 ``popular``，实际支持情况取决于站点。

导出与阅读
~~~~~~~~~~~~

.. code-block:: bash

   # 导出带元数据的 CBZ
   doujinshi-dl --id 123855 --cbz --output ./downloads

   # 导出 PDF，需先安装 img2pdf
   doujinshi-dl --id 123855 --pdf --output ./downloads

   # 直接下载为 ZIP，并关闭 HTML 生成
   doujinshi-dl --id 123855 --zip --output ./downloads

   # 为已下载的目录生成 HTML 阅读器
   doujinshi-dl --html ./downloads

   # 下载后生成总览页
   doujinshi-dl --id 123855 --gen-main --output ./downloads

``--no-html`` 关闭下载后的 HTML 生成；``--meta`` 额外写入插件提供的元数据文件。
已有 CBZ / PDF 时可用 ``--regenerate`` 请求重新生成。

默认保留图片目录。``--rm-origin-dir`` 会删除原目录，仅应在确认导出成功后使用；
``--move-to-folder`` 会清理目录内原文件并将导出文件移入其中。
这两个选项不能同时使用。

文件夹命名
~~~~~~~~~~~~

默认格式为 ``[%i][%a][%t]``。例如只保留 ID 和标题：

.. code-block:: bash

   doujinshi-dl --id 123855 --format '[%i]%t'

以下占位符由示例站点插件支持：

.. list-table:: 文件夹名称占位符
   :header-rows: 1
   :widths: 20 80

   * - 占位符
     - 内容
   * - ``%i``
     - 作品 ID
   * - ``%t``
     - 标题
   * - ``%s``
     - 副标题或翻译标题
   * - ``%p``
     - 简化标题
   * - ``%a``
     - 作者
   * - ``%g``
     - 社团
   * - ``%ag``
     - 作者，缺少时使用社团
   * - ``%f``
     - 收藏数

Windows 的 ``.bat`` / ``.cmd`` 批处理文件中需要将 ``%`` 写成 ``%%``；
PowerShell 直接使用上面的单引号示例即可。

配置与下载参数
----------------

认证、语言和代理
~~~~~~~~~~~~~~~~~~

以下配置会保存供后续命令使用。设置 token、语言或代理后程序会退出，
应先配置，再单独执行下载命令。

.. code-block:: bash

   doujinshi-dl --token "YOUR_API_TOKEN"
   doujinshi-dl --language english
   doujinshi-dl --proxy "http://127.0.0.1:1080"

   # 清除语言过滤或代理
   doujinshi-dl --language ""
   doujinshi-dl --proxy ""

语言配置会在关键词或作者搜索中追加 ``language:`` 条件。
配置文件和历史记录位置由插件决定；示例插件通常使用 ``~/.doujinshi-dl/``，
已有 ``~/.nhentai/`` 时会沿用旧目录，Linux 还支持 ``XDG_DATA_HOME``。

使用兼容的镜像
~~~~~~~~~~~~~~~~

将示例地址替换为插件支持的镜像根地址：

.. code-block:: bash

   # bash / zsh
   DOUJINSHI_DL_URL=https://your-mirror.example.com doujinshi-dl --id 123855

镜像必须兼容插件使用的 API 和图片地址规则，仅设置环境变量不会自动适配任意站点。

下载参数速查
~~~~~~~~~~~~~~

.. list-table:: 常用下载参数
   :header-rows: 1
   :widths: 30 15 55

   * - 参数
     - 默认值
     - 作用
   * - ``--output``, ``-o``
     - ``.``
     - 保存目录
   * - ``--threads``, ``-t``
     - ``5``
     - 下载线程数，建议设置为 1–15
   * - ``--timeout``, ``-T``
     - ``30``
     - 请求超时秒数
   * - ``--delay``, ``-d``
     - ``0``
     - 每部作品之间的等待秒数
   * - ``--retry``
     - ``3``
     - 失败重试次数，由插件应用
   * - ``--exit-on-fail``
     - 关闭
     - 下载失败时退出
   * - ``--no-filename-padding``
     - 关闭
     - 不对图片文件名中的页码补零
   * - ``--save-download-history``
     - 关闭
     - 记录下载历史，并跳过已记录的 ID

下载历史需要在每次希望记录或跳过已下载作品时显式开启：

.. code-block:: bash

   doujinshi-dl --id 123855 123866 --save-download-history

完整参数以 ``doujinshi-dl --help`` 为准。

Docker
--------

仓库提供的 Dockerfile 会安装主程序和示例站点插件。
在仓库根目录构建，并持久化下载目录与配置目录：

.. code-block:: bash

   docker build -t doujinshi-dl:latest .
   docker volume create doujinshi-dl-config
   mkdir -p downloads
   docker run --rm -it -v doujinshi-dl-config:/root/.doujinshi-dl \
     doujinshi-dl:latest --token "YOUR_API_TOKEN"
   docker run --rm -it -v doujinshi-dl-config:/root/.doujinshi-dl \
     -v "$(pwd)/downloads:/output" doujinshi-dl:latest --id 123855

下载输出位于宿主机的 ``downloads`` 目录。自定义镜像地址时为 ``docker run``
添加 ``-e DOUJINSHI_DL_URL=https://your-mirror.example.com``。

常见问题
----------

安装后找不到 doujinshi-dl 命令
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用 ``uv tool install`` 安装后，运行 ``uv tool update-shell`` 并重新打开终端。
可以用 ``uv tool list`` 确认工具已安装。

``uv pip install --system`` 将包装入 uv 选中的 Python 环境，命令脚本位于该解释器的
脚本目录；它不会自动将这个目录加入 PATH，也不会自动刷新 pyenv 的命令 shim。
多版本 Python 环境中，安装时的解释器还可能与当前终端的解释器不同。
先检查 uv 选择的环境及安装位置：

.. code-block:: bash

   uv pip show --system doujinshi-dl doujinshi-dl-nhentai

对于作为命令行工具使用的场景，建议按“快速开始”改用 ``uv tool install``。
若继续使用 pyenv 管理的安装，请确认已选中安装这些包的 Python 版本，再执行
``pyenv rehash``，并确保 pyenv shims 目录在 PATH 中。

提示未安装插件
~~~~~~~~~~~~~~~~

即使运行 ``--help``，程序也会先加载插件。出现
``No doujinshi-dl plugin installed`` 时，重新执行包含 ``--with doujinshi-dl-nhentai``
的工具安装命令；源码安装则在同一个虚拟环境中执行 ``uv pip install doujinshi-dl-nhentai``。

认证失败、请求失败或下载不完整
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 认证失败：确认 token 属于当前站点，并用 ``--token`` 重新保存。
* 连接失败：检查镜像地址和代理；站点的 API 变化可能需要更新插件。
* 请求限流：降低 ``--threads``，增加 ``--delay``，并遵守站点的访问限制。
* PDF 未生成：按安装章节把 ``img2pdf`` 装入主程序所在环境。

许可证
--------

本项目使用 `MIT 许可证 <LICENSE>`_。

.. |pypi| image:: https://img.shields.io/pypi/v/doujinshi-dl.svg
   :target: https://pypi.org/project/doujinshi-dl/
   :alt: PyPI version

.. |license| image:: https://img.shields.io/github/license/RicterZ/nhentai.svg
   :target: LICENSE
   :alt: MIT license
