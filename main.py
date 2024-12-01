# BlenderAddonPackageTool - A framework for developing multiple blender addons in a single workspace
# Copyright (C) 2024 Xinyu Zhu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from configparser import ConfigParser

from common.class_loader.module_installer import default_blender_addon_path

# The name of current active addon to be created, tested or released
# 要创建、测试或发布的当前活动插件的名称
ACTIVE_ADDON = "expression_addon"

# The path of the blender executable. Blender2.93 is the minimum version required
# Blender可执行文件的路径，Blender2.93是所需的最低版本

BLENDER_EXE_PATH = "K:/Goo Engine V3.6.02/goo-engine-stable/blender.exe"

# You can override the default path by setting the path manually
# 您可以通过手动设置路径来覆盖默认插件安装路径 或者在config.ini中设置
# BLENDER_ADDON_PATH = "C:/software/general/Blender/Blender3.5/3.5/scripts/addons/"
BLENDER_ADDON_PATH = None
if os.path.exists(BLENDER_EXE_PATH):
    BLENDER_ADDON_PATH = default_blender_addon_path(BLENDER_EXE_PATH)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# 若存在config.ini则从其中中读取配置
CONFIG_FILEPATH = os.path.join(PROJECT_ROOT, 'config.ini')

# The default release dir. Must not within the current workspace
# 插件发布的默认目录，不能在当前工作空间内
DEFAULT_RELEASE_DIR = os.path.join(PROJECT_ROOT, "../addon_release/")

# The default test release dir. Must not within the current workspace
# 测试插件发布的默认目录，不能在当前工作空间内
TEST_RELEASE_DIR = os.path.join(PROJECT_ROOT, "../addon_test/")

if os.path.isfile(CONFIG_FILEPATH):
    configParser = ConfigParser()
    configParser.read(CONFIG_FILEPATH, encoding='utf-8')

    if configParser.has_option('blender', 'exe_path'):
        BLENDER_EXE_PATH = configParser.get('blender', 'exe_path')
        # The path of the blender addon folder
        # 同时更改Blender插件文件夹的路径
        BLENDER_ADDON_PATH = default_blender_addon_path(BLENDER_EXE_PATH)

    if configParser.has_option('blender', 'addon_path') and configParser.get('blender', 'addon_path'):
        BLENDER_ADDON_PATH = configParser.get('blender', 'addon_path')

    if configParser.has_option('default', 'addon') and configParser.get('default', 'addon'):
        ACTIVE_ADDON = configParser.get('default', 'addon')

    if configParser.has_option('default', 'release_dir') and configParser.get('default', 'release_dir'):
        DEFAULT_RELEASE_DIR = configParser.get('default', 'release_dir')

    if configParser.has_option('default', 'test_release_dir') and configParser.get('default', 'test_release_dir'):
        TEST_RELEASE_DIR = configParser.get('default', 'test_release_dir')

# Could not find the blender addon path, raise error. Please set BLENDER_ADDON_PATH manually.
# 未找到Blender插件路径，引发错误 请手动设置BLENDER_ADDON_PATH
if not BLENDER_ADDON_PATH or not os.path.exists(BLENDER_ADDON_PATH):
    raise ValueError("Blender addon path not found: " + BLENDER_ADDON_PATH, "Please set the correct path in config.ini")

# The framework use this pattern to find the import module within the workspace
