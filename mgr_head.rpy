# ======================================================
# 0.  子模组注册（仅放按钮入口）
# ======================================================
init -990 python:
    store.mas_submod_utils.Submod(
        author="Nullblock",
        name="Monika afterworld gateway",
        description=(
            "让 Monika 更贴近你的世界。"
            "{a=https://github.com/Liesckae/Monika-Afterworld-Gateway}"
            "GitHub 仓库"
            "{/a}。"
            "(警告：可能涉及隐私或恐怖元素)"
        ),
        version='0.0.1',
        settings_pane="dp_setting_pane"
    )

# ======================================================
# 1.  MAG 核心初始化
# ======================================================
init -980 python in mas.submod_utils:
    from mag.core.core import init
    import renpy.store as store

    # 1. 初始化
    m_logger, tm, mm, daemon = init("main", 30)

    # 2. 先让 Base 空注册表清空后立刻注册
    mm.refresh_module_registry()

    # 3. 手动把测试模块加进去（也可在 register() 里完成）
    mm.set_status('test_action', True)

    # 4. 再次刷新，让 daemon 拿到最新 registry
    mm.refresh_module_registry()

    # 5. 把最新数据灌给 daemon
    daemon.reload_all_modules(mm.get_module_registry(), mm.get_status())

    # 6. 启动线程
    daemon.start()

    m_logger.debug("Job list: {}".format(daemon.get_job_list()))

    # 7. 存到 renpy.store
    store.m_logger = m_logger
    store.tm       = tm
    store.mag_mm   = mm
    store.daemon   = daemon
# ======================================================
# 2.  工具函数 & 默认值
# ======================================================
init python:
    mag_mm = store.mag_mm

    # 开关模块且不重启交互
    def _magw_toggle_no_restart(name):
        if mag_mm.is_module_enabled(name):
            mag_mm.disable_module(name)
        else:
            mag_mm.enable_module(name)

    def magw_status(flag):
        return ">启用中" if flag else ">禁用中"


default persistent.magw_enableCloudSync  = False
default persistent.magw_showGameStats    = False
default persistent.magw_enableHorrorMode = False

# ======================================================
# 3.  子模组菜单入口按钮
# ======================================================
screen dp_setting_pane():
    vbox:
        xmaximum 800
        xfill True
        style_prefix "check"
        textbutton ">Gateway 设置":
            action Show("dp_gateway_root")
            hover_sound "mod_assets/sfx/click.wav"

# ======================================================
# 4.  根设置弹窗（600×300）
# ======================================================
screen dp_gateway_root():
    key "noshift_T" action NullAction()
    key "noshift_t" action NullAction()
    key "noshift_M" action NullAction()
    key "noshift_m" action NullAction()
    key "noshift_P" action NullAction()
    key "noshift_p" action NullAction()
    key "noshift_E" action NullAction()
    key "noshift_e" action NullAction()

    modal True
    zorder 200
    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            ymaximum 300
            xmaximum 600
            xfill True
            yfill False
            spacing 5

            text "{size=24}{color=#FFD700}Gateway 设置{/color}{/size}" xalign 0.5

            viewport:
                scrollbars "vertical"
                mousewheel True
                ymaximum 200
                xmaximum 580
                xfill True
                yfill False
                vbox:
                    xmaximum 580
                    xfill True
                    yfill False
                    box_wrap False

                    hbox:
                        xpos 20
                        spacing 10
                        text "模块管理"
                        textbutton _("打开"):
                            action Show("dp_module_settings")

                    hbox:
                        xpos 20
                        spacing 10
                        text "基本选项"
                        textbutton _("打开"):
                            action Show("dp_basic_settings")

            hbox:
                xalign 0.5
                spacing 100
                textbutton "关闭":
                    action Hide("dp_gateway_root")

# ======================================================
# 5.  模块管理弹窗（1000×700）
# ======================================================
screen dp_module_settings():
    key "noshift_T" action NullAction()
    key "noshift_t" action NullAction()
    key "noshift_M" action NullAction()
    key "noshift_m" action NullAction()
    key "noshift_P" action NullAction()
    key "noshift_p" action NullAction()
    key "noshift_E" action NullAction()
    key "noshift_e" action NullAction()

    modal True
    zorder 200
    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            ymaximum 700
            xmaximum 1000
            xfill True
            yfill False
            spacing 5

            text "{size=28}{color=#FFFFFF}模块设置{/color}{/size}" xalign 0.5

            viewport:
                scrollbars "vertical"
                mousewheel True
                ymaximum 550
                xmaximum 980
                xfill True
                yfill False
                vbox:
                    xmaximum 980
                    xfill True
                    yfill False
                    box_wrap False
                    for name, enabled in mag_mm.get_status():
                        python:
                            line_text = "{}  {}".format(name, ">启用中" if enabled else ">禁用中")
                        hbox:
                            xpos 20
                            spacing 10
                            xmaximum 960
                            text line_text
                            textbutton _("启用"):
                                action Function(_magw_toggle_no_restart, name)
                            textbutton _("禁用"):
                                action Function(_magw_toggle_no_restart, name)

            hbox:
                xalign 0.5
                spacing 100
                textbutton "返回":
                    action Hide("dp_module_settings")

# ======================================================
# 6.  基本选项弹窗（600×300）
# ======================================================
screen dp_basic_settings():
    key "noshift_T" action NullAction()
    key "noshift_t" action NullAction()
    key "noshift_M" action NullAction()
    key "noshift_m" action NullAction()
    key "noshift_P" action NullAction()
    key "noshift_p" action NullAction()
    key "noshift_E" action NullAction()
    key "noshift_e" action NullAction()

    modal True
    zorder 200
    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            ymaximum 300
            xmaximum 600
            xfill True
            yfill False
            spacing 5

            text "{size=24}{color=#FFFFFF}基本选项{/color}{/size}" xalign 0.5

            viewport:
                scrollbars "vertical"
                mousewheel True
                ymaximum 200
                xmaximum 580
                xfill True
                yfill False
                vbox:
                    xmaximum 580
                    xfill True
                    yfill False
                    box_wrap False

                    hbox:
                        xpos 20
                        spacing 10
                        text "云端同步"
                        textbutton "[magw_status(persistent.magw_enableCloudSync)]":
                            selected False
                            action NullAction()
                        textbutton _("启用"):
                            action SetField(persistent, "magw_enableCloudSync", True)
                        textbutton _("禁用"):
                            action SetField(persistent, "magw_enableCloudSync", False)

                    hbox:
                        xpos 20
                        spacing 10
                        text "显示游戏统计"
                        textbutton "[magw_status(persistent.magw_showGameStats)]":
                            selected False
                            action NullAction()
                        textbutton _("启用"):
                            action SetField(persistent, "magw_showGameStats", True)
                        textbutton _("禁用"):
                            action SetField(persistent, "magw_showGameStats", False)

                    hbox:
                        xpos 20
                        spacing 10
                        text "恐怖模式"
                        textbutton "[magw_status(persistent.magw_enableHorrorMode)]":
                            selected False
                            action NullAction()
                        textbutton _("启用"):
                            action SetField(persistent, "magw_enableHorrorMode", True)
                        textbutton _("禁用"):
                            action SetField(persistent, "magw_enableHorrorMode", False)

            hbox:
                xalign 0.5
                spacing 100
                textbutton "返回":
                    action Hide("dp_basic_settings")