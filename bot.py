#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBot_V11_Adapter

# Fix import path problem in server
dir_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, dir_path)

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
nonebot.load_plugins("DicePP/plugins")
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(OneBot_V11_Adapter)

nonebot.load_from_toml("pyproject.toml")
# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...


if __name__ == "__main__":
    # nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
