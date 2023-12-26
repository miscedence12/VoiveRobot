#!/bin/bash

# 设置要关闭的终端窗口的标题
WINDOW_TITLE="ui_window"

# 获取终端窗口的ID
WINDOW_ID=$(wmctrl -l | grep "$WINDOW_TITLE" | awk '{print $1}')

# 如果找到了窗口ID，则关闭该窗口
if [ -n "$WINDOW_ID" ]; then
    wmctrl -i -c "$WINDOW_ID"
else
    echo "未找到匹配的终端窗口"
fi

