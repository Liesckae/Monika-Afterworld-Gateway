init -990 python:
    store.mas_submod_utils.Submod(
        author="Nullblock",
        name="Monika afterworld gateway",
        description="A submod make Monika closer to your world.release:{a=https://github.com/Liesckae/Monika-Afterworld-Gateway}{i}{u}>Github{/a}{/i}{/u}.(Warning: This sub-mod may obtain your privacy or contain horror elements)",
        version='0.0.1',
        settings_pane="main_settings_pane"
    )

screen main_settings_pane():
    vbox:
        xmaximum 800
        xfill True
        style_prefix "check"

        textbutton ">Basic Settings":
            ypos 1
            selected False
            action Show("basic_setting_screen")

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