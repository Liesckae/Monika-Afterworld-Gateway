# ======================================================
#  Monika-Afterworld-Gateway  精简启动脚本
# ======================================================

# 0. 子模组元数据（Ren'Py 会在设置页自动展示）
init -990 python:
    import os, sys
    # 让 Python 2.7 能找到后端
    sys.path.insert(0, os.path.join(config.gamedir, "Submods", "Monika's-Real-Gate", "python-packages"))

    # 注册子模组（MAS ≥0.12 写法）
    store.mas_submod_utils.Submod(
        author="Nullblock",
        name="Monika afterworld gateway",
        description=(
            "让 Monika 更贴近你的世界。"
            "{a=https://github.com/Liesckae/Monika-Afterworld-Gateway}GitHub 仓库{/a}"
        ),
        version='0.0.1',
        settings_pane="dp_setting_pane"
    )

# 1. 后端初始化（只跑一次）
init -980 python:
    from mgr.core.core import init
    from mgr.controller.daemon import DaemonManager

    # 初始化核心：返回 (logger, TriggerManager, DaemonManager)
    mag_logger, mag_tm, mag_dm = init("main", interval=30)

    # 注册并启用测试模块
    mag_tm.set_status('test_action', True)
    mag_tm.refresh_module_registry()

    # 把 registry 与 status 同步到 DaemonManager
    mag_dm.reload_all_modules(
        mag_tm.get_module_registry(),
        mag_tm.get_status()
    )
    mag_dm.start()

    # 导出到 Ren’Py 全局 store，方便 UI 调用
    store.mag_logger = mag_logger
    store.mag_tm     = mag_tm
    store.mag_dm     = mag_dm

# 2. UI 用到的工具函数
init python:
    # 开关模块（不重启 Ren’Py）
    def _mag_toggle(name):
        if mag_tm.get_status().get(name, False):
            mag_tm.set_status(name, False)
        else:
            mag_tm.set_status(name, True)
        mag_dm.reload_all_modules(mag_tm.get_module_registry(), mag_tm.get_status())

    def mag_status(flag):
        return ">启用" if flag else ">禁用"

# 3. 保存默认值（示例）
default persistent.mag_cloud_sync  = False
default persistent.mag_show_stats  = False
default persistent.mag_horror_mode = False

# 4. 设置界面（保持原 UI，仅引用上面函数）
screen dp_setting_pane():
    vbox:
        style_prefix "check"
        textbutton "Gateway 设置":
            action Show("dp_gateway_root")

screen dp_gateway_root():
    tag gateway_root
    modal True
    zorder 200
    style_prefix "confirm"

    add mas_getTimeFile("gui/overlay/confirm.png")
    frame:
        vbox:
            ymaximum 300
            xmaximum 600
            spacing 5
            text "{size=24}{color=#FFD700}Gateway 设置{/color}{/size}" xalign 0.5

            hbox:
                xpos 20
                spacing 10
                text "模块管理"
                textbutton _("打开") action Show("dp_module_settings")

            hbox:
                xpos 20
                spacing 10
                text "基本选项"
                textbutton _("打开") action Show("dp_basic_settings")

            hbox:
                xalign 0.5
                spacing 100
                textbutton "关闭" action Hide("dp_gateway_root")

screen dp_module_settings():
    tag gateway_module
    modal True
    zorder 200
    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            ymaximum 550
            xmaximum 600
            spacing 5
            text "{size=24}{color=#FFFFFF}模块设置{/color}{/size}" xalign 0.5

            viewport:
                scrollbars "vertical"
                mousewheel True
                ymaximum 450
                xmaximum 580
                vbox:
                    spacing 5
                    for name, enabled in mag_tm.get_status().items():
                        hbox:
                            xpos 20
                            spacing 10
                            text "{} [{}]".format(name, "ON" if enabled else "OFF")
                            textbutton _("开关") action Function(_mag_toggle, name)

            hbox:
                xalign 0.5
                spacing 100
                textbutton "返回" action Hide("dp_module_settings")

screen dp_basic_settings():
    tag gateway_basic
    modal True
    zorder 200
    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            ymaximum 300
            xmaximum 600
            spacing 5
            text "{size=24}{color=#FFFFFF}基本选项{/color}{/size}" xalign 0.5

            hbox:
                xpos 20
                spacing 10
                text "云端同步"
                textbutton "[mag_status(persistent.mag_cloud_sync)]" selected False action NullAction()
                textbutton _("启用") action SetField(persistent, "mag_cloud_sync", True)
                textbutton _("禁用") action SetField(persistent, "mag_cloud_sync", False)

            hbox:
                xpos 20
                spacing 10
                text "显示游戏统计"
                textbutton "[mag_status(persistent.mag_show_stats)]" selected False action NullAction()
                textbutton _("启用") action SetField(persistent, "mag_show_stats", True)
                textbutton _("禁用") action SetField(persistent, "mag_show_stats", False)

            hbox:
                xpos 20
                spacing 10
                text "恐怖模式"
                textbutton "[mag_status(persistent.mag_horror_mode)]" selected False action NullAction()
                textbutton _("启用") action SetField(persistent, "mag_horror_mode", True)
                textbutton _("禁用") action SetField(persistent, "mag_horror_mode", False)

            hbox:
                xalign 0.5
                spacing 100
                textbutton "返回" action Hide("dp_basic_settings")