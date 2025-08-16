init -990 python:
    store.mas_submod_utils.Submod(
        author="Nullblock",
        name="Monika afterworld gateway",
        description="A submod make Monika closer to your world.release:{a=https://github.com/Liesckae/Monika-Afterworld-Gateway}{i}{u}>Github{/a}{/i}{/u}.(Warning: This submod may obtain your privacy or contain horror elements)",
        version='0.0.1',
        settings_pane="dp_settings_pane"
    )

init -980 python in mas.submod_utils:
    from mag.core.core import init
    import renpy.store as store
    m_logger, tm, mm, daemon = init("main", 30)
    mm.refresh_module_registry()
    store.mag_mm = mm

init python:
    class ToggleModule(Action):
        def __init__(self, name):
            self.name = name
        def __call__(self):
            if mag_mm.is_module_enabled(self.name):
                mag_mm.disable_module(self.name)
            else:
                mag_mm.enable_module(self.name)
            return True

screen dp_settings_pane():
    vbox:
        xmaximum 800
        xfill True
        spacing 10
        style_prefix "check"

        textbutton "⚙ 模块设置":
            style "check_button"
            ypos 1
            selected False
            action Show("dp_modules")
            hover_sound "mod_assets/sfx/click.wav"
            
screen dp_modules():
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
        xmaximum 1000
        ymaximum 700
        xalign 0.5
        yalign 0.5
        padding (20, 20)

        vbox:
            spacing 15
            xfill True
            yfill True

            # 标题
            text "{size=28}{color=#FFD700}Settings Panel{/color}{/size}" xalign 0.5

            # 主内容
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
                            for name, enabled in mag_mm.get_status():
                                textbutton "[name]":
                                    style "check_button"
                                    selected enabled
                                    action ToggleModule(name)
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
                spacing 50
                textbutton "Back":
                    style "check_button"
                    action Hide("dp_modules")
                    hover_sound "mod_assets/sfx/click.wav"

    
    