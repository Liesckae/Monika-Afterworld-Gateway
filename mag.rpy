init -990 python:
    store.mas_submod_utils.Submod(
        author="Nullblock",
        name="Monika afterworld gateway",
        description="A submod make Monika closer to your world.release:{a=https://github.com/Liesckae/Monika-Afterworld-Gateway}{i}{u}>Github{/a}{/i}{/u}.(Warning: This sub-mod may obtain your privacy or contain horror elements)",
        version='0.0.1',
        settings_pane="main_settings_pane"
    )

init -989 python in mas.submod_utils:
    # TODO: 增加对于子模块执行次数的监控
    from store import _preferences as preferences
    from store import persistent
    import renpy.store as store
    import renpy.config as config
    import os,sys

    mag_path = os.path.join(config.basedir, 'game', 'Submods', 'Monika-Afterworld-Gateway')
    if mag_path not in sys.path:
        sys.path.insert(0, mag_path)

    from mag_scripts.logger import logger
    from mag_scripts.registry import load_modules, get_actions,get_topics
    from mag_scripts import actions
    store._mag_actions = get_actions()
    # Load modules
    load_modules()
    # set up
    persistent.submods_mag_actions = get_actions()
    persistent.submods_mag_topics = get_topics()
    persistent.submods_mod_switch = {}

    for name in get_actions().keys():
        persistent.submods_mod_switch.setdefault(name,False)
        
screen main_settings_pane():
    vbox:
        xmaximum 800
        xfill True
        spacing 10
        style_prefix "check"

        textbutton "⚙ Basic Settings":
            style "check_button"
            ypos 1
            selected False
            action Show("basic_setting_screen")
            hover_sound "mod_assets/sfx/click.wav"
            
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

    
    
    frame:
        
        xmaximum 800
        ymaximum 500
        xalign 0.5
        yalign 0.5
        padding (20, 20)

        vbox:
            spacing 15
            xfill True
            yfill True

            text "{size=28}{color=#FFD700}Settings Panel{/color}{/size}" xalign 0.5 ypos 20
            
            null height 20
            
            hbox:
                xfill True
                spacing 20
                
                vbox:
                    xmaximum 380
                    spacing 10
                    
                    text "{size=20}{color=#FFFFFF}Modules{/color}{/size}" xalign 0.5
                    
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        ymaximum 300
                        xfill True
                        
                        vbox:
                            spacing 5
                            
                            for name, cls in store._mag_actions.items():
                                textbutton "[name]":
                                    style "check_button"
                                    action ToggleDict(persistent.submods_mod_switch, name)
                                    hover_sound "mod_assets/sfx/hover.wav"
                                    xfill True
                                    
            vbox:
                xmaximum 380
                spacing 10
                
                text "{size=20}{color=#FFFFFF}Options{/color}{/size}" xalign 0.5
                
                textbutton "Reset All Settings":
                    style "check_button"
                    action NullAction()
                    hover_sound "mod_assets/sfx/hover.wav"
                    xfill True
                    
        hbox:
            xalign 0.5
            ypos 450
            spacing 50
            
            textbutton "Back":
                style "check_button"
                action Hide("basic_setting_screen")
                hover_sound "mod_assets/sfx/click.wav"