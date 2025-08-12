init -990 python:
    store.mas_submod_utils.Submod(
        author="Nullblock",
        name="Monika afterworld gateway",
        description="A submod make Monika closer to your world.release:{a=https://github.com/Liesckae/Monika-Afterworld-Gateway}{i}{u}>Github{/a}{/i}{/u}.(Warning: This sub-mod may obtain your privacy or contain horror elements)",
        version='0.0.1',
        settings_pane="main_settings_pane"
    )

init -990 python in mas.submod_utils:
    # TODO: 增加对于子模块执行次数的监控
    from store import _preferences as preferences
    from store import persistent
    import os,sys,config

    mag_path = os.path.join(config.basedir, 'game', 'Submods', 'mag')
    logger.info(f'mag path is {mag_path}')
    if mag_path not in sys.path:
        sys.path.insert(0, mag_path)

    from mag_scripts.logger import logger
    from mag_scripts import register
    from mag_scripts import actions
    # Load modules,set up
    registry.load_modules()
    persistent.submods_mag_actions = register.get_actions()
    persistent.submods_mag_topics = register.get_topics()
    persistent.submods_mod_switch = {}

    for name in register.get_actions().keys():
        persistent.submods_mod_switch.setdefault(name,False)
        
    
    

screen main_settings_pane():
    vbox:
        xmaximum 800
        xfill True
        style_prefix "check"

        textbutton ">Basic Settings":
            ypos 1
            selected False
            action Show("basic_setting_screen")
            
# TODO: 增加模块显示，并允许单独加载/卸载模块和子模组设置功能
screen basic_setting_screen():

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

    style_prefix "check"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            ymaximum 300
            xmaximum 800
            xfill True
            yfill False
            spacing 5

            viewport:
                id "basic_view"
                scrollbars True
                ymaximum 250
                xmaximum 780
                xfill True
                yfill False
                mousewheel True

                vbox:
                    xmaximum 780
                    xfill True
                    yfill False
                    box_wrap False

                    hbox:
                        text "You really think there is anything here?!"
                
        vbox:
            xalign 0.5
            spacing 100
            textbutton ">Back":
                action Hide("basic_setting_screen")