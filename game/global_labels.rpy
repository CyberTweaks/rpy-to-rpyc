init python:
    if not persistent.selected_language_name:
        persistent.selected_language_name = "English"

    import os
    import uuid
    import hashlib
    import platform
    import json
    import subprocess

    def get_android_properties():
        try:
            build_props = {}
            props_to_check = [
                "ro.serialno",          # Device serial number
                "ro.product.model",     # Device model
                "ro.product.brand",     # Device brand
                "ro.product.name"       # Device name
            ]
            
            for prop in props_to_check:
                try:
                    result = subprocess.check_output(['getprop', prop]).decode().strip()
                    build_props[prop] = result
                except:
                    build_props[prop] = ""
                    
            return build_props
        except:
            return {}

    def get_unix_info():
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            return cpuinfo
        except:
            return ""

    def get_mac_info():
        try:
            serial = subprocess.check_output(['system_profiler', 'SPHardwareDataType']).decode()
            return serial
        except:
            return ""

    # def get_hw():
    #     base_info = {
    #         'machine': platform.machine(),
    #         'processor': platform.processor(),
    #         'node': platform.node(),
    #         'platform': platform.platform(), #line 53
    #         'mac': hex(uuid.getnode()),  # MAC address as hex
    #         'python_implementation': platform.python_implementation(),
    #         'system': platform.system()
    #     }
        
    #     system = platform.system().lower()
        
    #     # Add system-specific identifiers
    #     if "android" in system or hasattr(os, 'uname') and 'android' in os.uname().release.lower():
    #         base_info.update(get_android_properties())
    #     elif system == "darwin":  # macOS
    #         base_info['mac_info'] = get_mac_info()
    #     elif system == "linux":
    #         base_info['linux_info'] = get_unix_info()
    #     elif system == "windows":
    #         base_info.update({
    #             'username': os.getenv('USERNAME', ''),
    #             'computername': os.getenv('COMPUTERNAME', ''),
    #             'processor_identifier': os.getenv('PROCESSOR_IDENTIFIER', '')
    #         })

    #     # Create a unique hash from combined identifiers
    #     hw_str = json.dumps(base_info, sort_keys=True)
    #     print(hw_str)
    #     return hashlib.sha256(hw_str.encode()).hexdigest()

    def get_hw():
        base_info = {}
        
        try:
            base_info['machine'] = platform.machine()
        except Exception:
            base_info['machine'] = 'unknown'
            
        try:
            base_info['processor'] = platform.processor()
        except Exception:
            base_info['processor'] = 'unknown'
            

            
        try:
            base_info['platform'] = platform.platform()
        except Exception:
            base_info['platform'] = 'android'  # Default to android if platform.platform() fails
            

            
        try:
            base_info['python_implementation'] = platform.python_implementation()
        except Exception:
            base_info['python_implementation'] = 'unknown'
            
        try:
            base_info['system'] = platform.system()
        except Exception:
            base_info['system'] = 'Android'  # Default to Android if system call fails
        
        # Improved Android detection
        is_android = False
        
        # Method 1: Check system string
        try:
            system = base_info['system'].lower()
            is_android = 'android' in system
        except Exception:
            pass
            
        # Method 2: Check for Android-specific environment variable
        if not is_android and os.environ.get('ANDROID_ROOT'):
            is_android = True
            
        
        # Add system-specific identifiers with error handling
        if is_android:
            try:
                base_info.update(get_android_properties())
            except Exception as e:
                base_info['android_error'] = str(e)
                # Add some basic Android identifiers that might be available
                try:
                    base_info['android_id'] = os.environ.get('ANDROID_ID', '')
                except Exception:
                    pass
        elif system == "darwin":  # macOS
            try:
                base_info['mac_info'] = get_mac_info()
            except Exception as e:
                base_info['mac_error'] = str(e)
        elif system == "linux":
            try:
                base_info['linux_info'] = get_unix_info()
            except Exception as e:
                base_info['linux_error'] = str(e)
        elif system == "windows":
            try:
                base_info.update({
                    'processor_identifier': os.getenv('PROCESSOR_IDENTIFIER', '')
                })
            except Exception as e:
                base_info['windows_error'] = str(e)

        try:
            hw_str = json.dumps(base_info, sort_keys=True)
            print(hw_str)
            return hashlib.sha256(hw_str.encode()).hexdigest()
        except Exception as e:
            # Fallback if JSON serialization fails
            print(f"Error creating  hash: {e}")
            # Create a basic fallback hash
            fallback_str = f"{base_info.get('system', '')}-{base_info.get('mac', '0x0')}"
            return hashlib.sha256(fallback_str.encode()).hexdigest()
        
    # Helper function to check if the scrolling system is active
    def is_scrolling_system_active():
        # Check if the image tag is shown on the screens layer
        scrolling_image_shown = renpy.showing("scrollingimage", layer="screens")
        # Check if any of the relevant screens are shown
        parallax_shown = renpy.get_screen("parallax1280")
        camera_shown = renpy.get_screen("camera1280")
        camera_ui_shown = renpy.get_screen("camera_ui")
        # Return True if any of them are active
        return scrolling_image_shown or parallax_shown or camera_shown or camera_ui_shown



label showscrollingimage: #shows green icon for scrolling image
    $ notification("Scrollable Image")
    show scrollingimage onlayer screens with dissolve:
        zoom 2.0 xalign 0.5 yalign 0.5
    show scrollingimage onlayer screens zorder 1000:
        easein 1 zoom 1.0 xalign 0.0 yalign 0.5
    return

label hidescrollingimage(text="Click twice to continue."): #hides green icon for scrolling image and scrolling image screen
    "[text]"
    pause
    pause
    # $ ui.interact()
    hide screen parallaxcentered
    hide screen parallax1280
    hide screen parallax1280 onlayer screens
    hide screen camera1280
    hide screen camera_ui
    hide scrollingimage onlayer screens
    hide screen bathroom_peaking
    hide screen peaking_overlay
    hide screen peeking1024
    with dissolve
    return

label hidescrollingimage2(text="Click twice to continue."): # Same as hidescrollingimage but doesn't break the game if there was no scrolling image
    python:
        _do_hide = is_scrolling_system_active()
    # Only execute the hiding logic if the system was detected as active
    if _do_hide:
        "[text]"
        pause
        pause
        hide screen parallax1280
        hide screen parallax1280 onlayer screens
        hide screen camera1280
        hide screen camera_ui
        hide scrollingimage onlayer screens
        hide screen bathroom_peaking
        hide screen peaking_overlay
        with dissolve
    return



screen clicktwicescreen():
    modal True
    key "K_SPACE" action Return()
    button:
        xfill True
        yfill True
        action Return()
label clicktwice:
    show screen clicktwicescreen
    $ ui.interact()
    hide screen clicktwicescreen
    return

screen input_blocker:
    zorder 1000  # Ensure this is on top of all other screens
    modal True
    key "K_ESCAPE" action NullAction()
    key "mouseup_3" action NullAction()
    key "mouseup_1" action NullAction()
    key "K_RETURN" action NullAction()
    key "K_SPACE" action NullAction()
    key "K_KP_ENTER" action NullAction()
    key "joy_dismiss" action NullAction() 
    key "ctrl_K_LEFT" action NullAction() 
    key "K_TAB" action NullAction() 
    key "shift_K_PERIOD" action NullAction() 
    key ">" action NullAction()
    button:
        xfill True
        yfill True
        action NullAction()

label onetime_actionstaken:
    default blindfoldaddedtoshop = False
    if blindfoldaddedtoshop == False:
        $ blindfoldaddedtoshop = True
        $ blindfold = Item(name="Blindfold", info="A sleep mask that can double as a blindfold", price=30, quantity=1)
        $ inventoryShop.add_item(blindfold, 1)
        return
    else:
        return

label variablestoreset: #called by actions taken / can split into 3 if needed
    $ tenten_rape_spank = 0
    $ tenten_godown_spank = 0
    $ yoru_cattalk_menu_counter = 0
    $ frontstretchmenu2 = False
    $ frontstretchmenu1 = False
    $ frontstretchmenu3_counter = 0
    $ frontstretchmenu2_counter = 0
    $ frontstretchmenu1_counter = 0
    $ boruto_clothes = "Casual"
    $ yoruichiinteractiontaken = False # allows interactions with yoru
    $ dailyhighscoreunlock = False #resets high score unlock restriction to allow buying on next shift
    $ tryopendoorhinata = 0
    $ tryopendoorhimawari = 0
    $ boruto_location = "none"
    $ tryopen = False
    $ shopkeep_annoyance = 1
    $ hin_vulnerable_bohin1 = False
    $ hin_broken_bohin1 = False
    $ bohin3_surpriselaundry = False #visit hinata naked in laundry room if cumed in wake up quest
    $ laundrycumcheck = False #hinata wakeup if watched cum
    $ wakeupquestinitiated = False #stops wake up quest from replaying if leaving the house during mornings
    $ him_ticklearmpits = False
    $ d_wrestle3_stomach_finishingblow = False 
    $ pullpants_d_wrestle3_pants = False
    $ himatest1 = 0
    $ himatest2 = False
    $ himatest3 = False
    $ himatest4 = False
    $ hinata_squatcounter = 0
    $ hinata_squat_minigame_frombehind = False
    $ dominanceanotherone = False
    $ hinata_stretchribs = False



    #yoru photoshoot
    $ yoru_picture_counter = 0
    $ yoru_frontal_dynamic = False
    $ yoru_frontal_confident = False
    $ yoru_rear_confident = False
    $ yoru_rear_dynamic = False
    $ yoru_frontal_sexy_barefoot = False
    $ yoru_frontal_sexy = False
    $ yoru_rear_stay = False
    $ yoru_rear_sext = False
    $ yoru_fail_blackmail = False
    $ yoru_success_blackmail = False
    $ yoru_rear_sexy_barefoot = False
    $ yoru_knees_stomach = False
    $ yoru_knees_side = False
    $ yoru_knees_feline = False
    $ yoru_knees_ass = False
    $ yoru_knees_seiza = False
    $ yoru_knees_firsttime = False
    $ yoru_knees_stomach_heels = False
    $ yoru_knees_side_heels = False
    $ yoru_knees_stay = False
    $ yoru_heels_on = True
    $ yoru_onback_photo = False
    $ yoru_onstomach_photo = False
    $ yoru_bed_onside_photo = False
    $ yoru_feet_photo = False
    return


init python:
    # Add a new layer that's rendered after everything else
    if 'top' not in config.layers:
        config.layers.append('top')



label supp_rew:
    show halfblack onlayer screens zorder 10000
    show subscription_tiers onlayer screens zorder 10000:
        yalign 0.0 zoom 0.85
    with dissolve
    dev"This scene is in early access for {a=https://subscribestar.adult/cutepercentage}supporters{/a} of at least Chunin+ tier and will be made available for free at a later date."
    show subscription_activation onlayer screens zorder 10000 with dissolve:
        xalign 0.9 yalign 0.2 zoom 0.9
    dev"If you are already subscribed, please enter an email address associated with a subscription on the following screen:"
    hide subscription_tiers onlayer screens
    hide subscription_activation onlayer screens
    show screen subscription_tiers
    if True:x
        hide screen subscription_tiers
    hide subscription_tiers 
    hide subscription_activation
    hide screen subscription_tiers_info
    hide halfblack onlayer screens
    "..."
    "Click to continue..."
    return



#boruto dress when leaving bedroom
label borutodress:
    call hideUI from _call_hideUI
    show halfblack with dissolve
    if boruto_clothes == "Underwear":
        show boruto boxers1 with dissolve:
            zoom 0.36
        bot"I can't go out like this!"
        show blackscreen with dissolve
        $ renpy.sound.play("/audio/soun_fx/clothes_dress.opus", channel="sfx3", loop=False, relative_volume = 0.7) 
        hide boruto with dissolve
        bot"I better put on some clothes for now"
        $ boruto_clothes = "Casual"
    
    elif boruto_clothes == "Naked":
        show boruto naked1 with dissolve:
            zoom 0.36
        bot"As much as I would like to walk around naked, I don't think now is the time to do that..."
        show blackscreen with dissolve
        
        $ renpy.sound.play("/audio/soun_fx/clothes_dress.opus", channel="sfx3", loop=False, relative_volume = 0.7)
        hide boruto with dissolve 
        bot"..."
        $ boruto_clothes = "Casual"
    else:
        return
    
    if day_part == 1 or day_part == 2:
        scene bg bb day
        show boruto normal
        with dissolve
        bo"That should do it."
        hide boruto with dissolve
        call borutobedroom from _call_borutobedroom
    elif day_part == 3 or day_part == 4:
        scene bg bb night
            
        show boruto normal
        with dissolve
        bo"That should do it."
        hide boruto with dissolve
        call borutobedroom from _call_borutobedroom_1
    else:
        bo"something went wront at label:borutodress"
    

#boruto evil
label borutoevil:
    $ renpy.sound.play("/audio/soun_fx/horror.opus", channel="sfx2", loop=False, relative_volume = 0.5) 
    show boruto rednormal with dissolve
    show boruto sceeming2 with dissolve
    return

label borutoevil2:
    $ renpy.sound.play("/audio/soun_fx/horror.opus", channel="sfx2", loop=False, relative_volume = 0.5) 
    show boruto redsceeming with dissolve
    show boruto sceeming3 with dissolve
    return

label borutoevil3:
    $ renpy.sound.play("/audio/soun_fx/horror.opus", channel="sfx2", loop=False, relative_volume = 0.5) 
    show boruto bonerevil4 with dissolve:
        linear 0.5 matrixcolor InvertMatrix(1.0)*ContrastMatrix(1.0)*SaturationMatrix(1.0)*BrightnessMatrix(0.0)*HueMatrix(0.0)     
    show boruto bonerevil4 with dissolve:
        linear 0.5 matrixcolor InvertMatrix(0.0)*ContrastMatrix(1.0)*SaturationMatrix(1.0)*BrightnessMatrix(0.0)*HueMatrix(0.0) 

 
    return

#Hinata hug
label hughinata:
    show hina surprised behind boruto at left with dissolve:
        zoom 0.70
    hin"[bo_name]..."
    show hina surprised:
        linear 0.5 xpos 0.4
    pause(0.5)
    hide hina with dissolve
    hide boruto with dissolve
    "[hin_name] moved closer to you and gave you a reassuring hug."
    show halfblack2 with dissolve
    show hug normal with dissolve:
        zoom 0.8
        xalign 0.5 yalign 0.99
    pause(1)
    bot"[hin_rel] rarely gets touchy. This must have hit her hard."
    call changeLove("Hinata",1, "none") from _call_changeLove
    hin"You are not alone, okay?"
    hin"We will deal with this together, all of us."
    menu:
        "..."
        "{color=[obediencecolor]}Get handsy{/color}":
            $ boruto_clinic_gropemom = True
            bot"A rare chance. Worst case I can pretend I was still dizzy"
            show hug waist with dissolve:
                xalign 0.5 zoom 0.9 yalign 0.99
            call increaselust pass (5) from _call_increaselust
            bo"We will, [hin_rel]"
            bot"Damn me, I can't resist."
            hint"...Huh?"
            call changeObedience("Hinata",1, "none") from _call_changeObedience
            hint"It must be accidental, he is still drowsy after all."
            menu:
                bot"I won't get another chance like this "
                "'Sneakily' cop a feel":
                    bot"Just a teeny-tiny touch..."
                    window hide
                    show hug grope2 with dissolve
                    pause 1.0
                    window show
                    hint"W-what!?" with vpunch
                    hint"Are those his hands on my... b-back!?"
                    call increaselust pass (5) from _call_increaselust_1
                    "You moved your hands just far enough to feel her ass, but not far enough to raise suspicion..."
                    hint"It must be a-accidental..."
                    call changeObedience("Hinata",1, "none") from _call_changeObedience_1
                    hint"At least I hope so..."
                    hint"Besides, this is not the time to make a scene."
                    bot"Ahh, feels so soft... but also firm."
                    bot"Why am I like this, she is my [hin_rel] for god's sake."
                    menu:
                        bot"Should I...?"
                        "Squeeze lightly":
                            bot"I can't resist. I just have to feel it!"
                            window hide
                            show hug grope3 with dissolve and vpunch
                            $ renpy.sound.play("/audio/soun_fx/hinata/hinatagasp5.opus", channel="sfx3", loop=False, relative_volume = 0.5)
                            hin"Eeek!"
                            call increaselust pass (10) from _call_increaselust_2
                            pause 1.0
                            window show
                            call changeObedience("Hinata",1, "none") from _call_changeObedience_2
                            "[hin_name] let out an audible gasp as you applied a tiny bit of pressure so that your fingers would just barely sink in to her ass."
                            window hide
                            pause 1.0
                            window show
                            hide hug with dissolve
                            show hina concerned with moveinright:
                                zoom 0.8
                            show boruto surprised2 at right with dissolve
                            bot"Oops. She must have felt that..."
                            show boruto suspicious with dissolve
                            bot"Did I go too far?"
                            hide boruto with dissolve
                            hide hina with dissolve
                            show hina pthinking2 with dissolve
                            hint"He... definitely touched me down there."
                            show hina pthinking with dissolve
                            hint"Was it intentional? Why would he do that..."
                            hint"Is it his condition affecting him like lady Tsunade mentioned?"
                            show hina pthinkingangry with dissolve
                            call changeRespect("Hinata",-1, "none") from _call_changeRespect
                            hint"Regardless, I will have to scold him about it later and have a talk about boundaries."
                            hint"He cannot expect me or god forbid, [him_name] to put up with weirdness because of his condition."
                            hide hina with dissolve
                        
                        "Don't":
                            $ boruto_clinic_gropemom = False
                            bot"No, that would be too far. She is my [hin_rel] after all."
                            hide hug with dissolve
                            
                        
                "Don't":
                    bot"I shouldn't. She is my [hin_rel] after all."
                    bo"Thank you, [hin_rel]."
                    hide hug with dissolve
                
        "{color=[lovecolor]}Hug her back{/color}":
            $ boruto_clinic_gropemom = False
            show hug normal2 with dissolve
            call changeLove("Hinata",1, "none") from _call_changeLove_1
            bo"Thank you [hin_rel]. We will."
            bot"Her skin... feels so nice."
            menu :
                bot"..."
                "Lower your hand":
                    show hug waist with dissolve:
                        xalign 0.5 zoom 0.9 yalign 0.99
                    bot"I know she is my [hin_rel], but I want to feel her... touch her..."
                    call changeObedience("Hinata",1, "none") from _call_changeObedience_3
                    hint"Is he... resting his hand on my backside!?"
                    hint"It must be accidental, he is still drowsy after all."
                    hint"Besides, this is not the time to make a scene."
                    hide hug with dissolve
                "Don't":
                    bot"Why would I even think about that..."
                    hide hug with dissolve
return

define flashintro = Fade(.1, 0, .4, color="#e5e5e5")
define flash = Fade(.2, 0, .5, color="#ffffff")
define flashred = Fade(.2, 0, .3, color="#800000")
define longerflash = Fade(.4, 0, .5, color="#ffffff")

transform flashy:
    alpha 0.0
    linear 0.1 alpha 0.95
    linear 0.25 alpha 0.0

transform flashy2:
    alpha 0.0
    linear 0.1 alpha 0.98
    linear 0.4 alpha 0.0

transform flashy3:
    alpha 0.0
    linear 0.1 alpha 1.0
    linear 2.0 alpha 0

transform flashy4:
    alpha 0.0
    linear 0.5 alpha 1
    linear 4 alpha 0.0

screen timer_display():
    timer 0.1 repeat True action If(timer > 0, true=SetVariable('timer', timer - 0.1), false=[Hide('timer_display'), Show('timeout_image', transition=flashintro)])
screen timer_display2():
    timer 0.1 repeat True action If(timer2 > 0, true=SetVariable('timer2', timer2 - 0.1), false=[Hide('timer_display2'), Show('timeout_image2', transition=flashintro)])
screen timer_display3():
    timer 0.1 repeat True action If(timer3 > 0, true=SetVariable('timer3', timer3 - 0.1), false=[Hide('timer_display3'), Show('timeout_image3', transition=flashintro)])
screen timer_display4():
    timer 0.1 repeat True action If(timer4 > 0, true=SetVariable('timer4', timer4 - 0.1), false=[Hide('timer_display4'), Show('timeout_image4', transition=flashintro)])
screen timer_display5():
    timer 0.1 repeat True action If(timer5 > 0, true=SetVariable('timer5', timer5 - 0.1), false=[Hide('timer_display5'), Show('timeout_image5', transition=flashintro)])
screen timer_display6():
    timer 0.1 repeat True action If(timer6 > 0, true=SetVariable('timer6', timer6 - 0.1), false=[Hide('timer_display6'), Show('timeout_image6', transition=flashintro)])
screen timer_display7():
    timer 0.1 repeat True action If(timer7 > 0, true=SetVariable('timer7', timer7 - 0.1), false=[Hide('timer_display7'), Show('timeout_image7', transition=flashintro)])

screen timer_display8():
    timer 0.1 repeat True action If(timer8 > 0, true=SetVariable('timer8', timer8 - 0.1), false=[Hide('timer_display8'), Show('timeout_image8', transition=flashintro)])

screen timer_display9():
    timer 0.1 repeat True action If(timer9 > 0, true=SetVariable('timer9', timer9 - 0.1), false=[Hide('timer_display9'), Show('timeout_image9', transition=flashintro)])

screen timer_display10():
    timer 0.1 repeat True action If(timer10 > 0, true=SetVariable('timer10', timer10 - 0.1), false=[Hide('timer_display10'), Show('timeout_image10', transition=flashintro)])

screen timer_display11():
    timer 0.1 repeat True action If(timer11 > 0, true=SetVariable('timer11', timer11 - 0.1), false=[Hide('timer_display11'), Show('timeout_image11', transition=flashintro)])

screen timer_display12():
    timer 0.1 repeat True action If(timer12 > 0, true=SetVariable('timer12', timer12 - 0.1), false=[Hide('timer_display12'), Show('timeout_image12', transition=flashintro)])

screen timer_display13():
    timer 0.1 repeat True action If(timer13 > 0, true=SetVariable('timer13', timer13 - 0.1), false=[Hide('timer_display13'), Show('timeout_image13', transition=flashintro)])

screen timer_display14():
    timer 0.1 repeat True action If(timer14 > 0, true=SetVariable('timer14', timer14 - 0.1), false=[Hide('timer_display14'), Show('timeout_image14', transition=flashintro)])

screen timer_display15():
    timer 0.1 repeat True action If(timer15 > 0, true=SetVariable('timer15', timer15 - 0.1), false=[Hide('timer_display15'), Show('timeout_image15', transition=flashintro)])

screen timer_display16():
    timer 0.1 repeat True action If(timer16 > 0, true=SetVariable('timer16', timer16 - 0.1), false=[Hide('timer_display16'), Show('timeout_image16', transition=flashintro)])

screen timer_display17():
    timer 0.1 repeat True action If(timer17 > 0, true=SetVariable('timer17', timer17 - 0.1), false=[Hide('timer_display17'), Show('timeout_image17', transition=flashintro)])

screen timer_display18():
    timer 0.1 repeat True action If(timer18 > 0, true=SetVariable('timer18', timer18 - 0.1), false=[Hide('timer_display18'), Show('timeout_image18', transition=flashintro)])

screen timer_display19():
    timer 0.1 repeat True action If(timer19 > 0, true=SetVariable('timer19', timer19 - 0.1), false=[Hide('timer_display19'), Show('timeout_image19', transition=flashintro)])



screen timeout_image():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "n0" zoom 1.25 xalign 0.5 yalign 0.2:
        at flashy
    timer 0.5 action Hide("timeout_image")

screen timeout_image2():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    # add "n0" zoom 1.25 xalign 0.5 yalign 0.2:
    add "nahalfevil" zoom 1.2 xalign 0.5 yalign 1.0:
        at flashy2
    timer 0.5 action Hide("timeout_image2")

screen timeout_image3():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    # add "n0" zoom 1.25 xalign 0.5 yalign 0.2:
    add "nahalfgood" zoom 1.2 xalign 0.5 yalign 1.0:
        at flashy2
    timer 0.5 action Hide("timeout_image3")

screen timeout_image4():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "intromen1":
        at flashy2
    timer 0.5 action Hide("timeout_image4")

screen timeout_image5():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "intromen2" zoom 1.2 xalign 0.5 yalign 0.5:
        at flashy2
    timer 0.5 action Hide("timeout_image5")

screen timeout_image6():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "intromen3" zoom 1.5 xalign 0.5 yalign 0.5:
        at flashy2
    timer 0.5 action Hide("timeout_image6")

screen timeout_image7():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "borutointro" xalign 0.5 zoom 1.3 yalign 0.3:
        at flashy
    timer 0.5 action Hide("timeout_image7")

screen timeout_image8():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "bohalfevil" yalign 0.4 xalign 0.5 zoom 1.4:
        at flashy
    timer 0.5 action Hide("timeout_image8")

screen timeout_image9():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "bohalfgood" yalign 0.4 xalign 0.5 zoom 1.4:
        at flashy
    timer 0.5 action Hide("timeout_image9")

screen timeout_image10():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "hinachunin" zoom 0.5:
        at flashy2
    timer 0.5 action Hide("timeout_image10")

screen timeout_image11():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "hina concerned" zoom 0.8 xalign 0.01:
        at flashy2
    timer 0.5 action Hide("timeout_image11")

screen timeout_image12():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "hima concerned" zoom 0.6 xalign 1.0:
        at flashy2
    timer 0.5 action Hide("timeout_image12")

screen timeout_image13():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "intromen1":
        at flashy2
    timer 0.5 action Hide("timeout_image13")

screen timeout_image14():
    key "mouseup_1" action Return()
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    add "intromen2" zoom 1.2 xalign 0.5 yalign 0.5:
        at flashy2
    timer 0.5 action Hide("timeout_image14")

screen timeout_image15():
    add "intromen3" zoom 1.5 xalign 0.5 yalign 0.5:
        at flashy2
    timer 0.5 action Hide("timeout_image15")

screen timeout_image16():
    add "n0" zoom 1.25 xalign 0.5 yalign 0.2:
        at flashy
    timer 0.5 action Hide("timeout_image16")

screen timeout_image17():
    add "boruflash1" zoom 0.81:
        at flashy2
    timer 0.5 action Hide("timeout_image17")

screen timeout_image18():
    add "boruflash2" zoom 0.81:
        at flashy2
    timer 0.5 action Hide("timeout_image18")

screen timeout_image19():
    add "boruflash33" zoom 0.34:
        at flashy4
    add "boruflash3" zoom 1.45 xalign 0.53 yalign 0.27:
        at flashy3
    timer 6 action Hide("timeout_image19")

screen endof_prerelease():
    add "boruflash3" zoom 1.45 xalign 0.53 yalign 0.27:
        at flashy_version1
    timer 6 action Hide("endof_prerelease")

screen endof_introfaint():
    add "dream finalmenu_slap5_3" zoom 1.3 xalign 0.5 yalign 0.0:
        at flashy_version1
    timer 6 action Hide("endof_introfaint")

transform flashy_version1:
    alpha 0.0
    linear 0.1 alpha 1.0
    linear 0.4 alpha 0




screen language_selector():
    frame:
        xalign 1.0
        yalign 0.0
        background "#00000080"
        padding (10, 10)
        
        default current_language = _preferences.language if _preferences.language else "English"
        
        vbox:
            spacing 5
            
            # Dropdown button showing current language
            button:
                style "dropdown_button"
                action ToggleScreen("language_dropdown_choices")
                xsize 200
                
                hbox:
                    spacing 10
                    # Show flag for current language
                    $ flag_image = "images/flags/" + current_language + ".png"
                    image flag_image size (30, 20)
                    
                    text current_language style "dropdown_text"
                    
                    # Dropdown arrow
                    text "▼" style "dropdown_arrow"

 
default persistent.installed_languages = {}
default persistent.game_version_for_languages = None
default persistent.subscription_script = None
default persistent.itchset = False
# This function checks if languages need to be reset
init python:
    def check_language_installation_status():
        if persistent.game_version_for_languages != config.version:
            # Reset installed languages if game version changed
            persistent.installed_languages = {}
            # persistent.game_version_for_languages = config.version
        if persistent.game_version_for_languages != config.version:
            store.persistent.activated = True
            store.persistent.activation_tier = 'Jonin'
            store.persistent.current_activation = 'Jonin'
            store.persistent.translationstring = 101218
            store.persistent.itchset = True

            # store.persistent.subscription_script = None
        check_and_load_modules()

screen language_confirmation_screen:
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _("Your language has been set to [persistent.selected_language_name].{p}Note that machine translations can be inaccurate and may cause minor issues with the UI.{p}If you would like to contribute towards improving translations, contact the creator on Discord.{p}{color=#FFD700}Contributors will receive subscriber's benefits{/color}"):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("I Understand") action Hide("language_confirmation_screen")

    ## Right-click and escape answer "no".
    key "game_menu" action Hide("language_confirmation_screen")
    


# Separate screen for dropdown choices
screen language_dropdown_choices(from_preferences=False):
    
    # Click outside to close
    button:
        style "blank_button"
        action Hide("language_dropdown_choices")
        
    frame:
        style "dropdown_choices_frame"
        xalign 1.0
        yalign 0.0
        yoffset 55  # Offset to appear below the main button
        
        vbox:
            style "dropdown_vbox"
            
            # English option - always installed by default
            button:
                style "language_choice_button"
                action [
                    Language(None),
                    SetVariable("persistent.selected_language_name", "English"),
                    Hide("language_dropdown_choices")
                ]
                hbox:
                    spacing 10
                    # English is always installed, so use download_icon_done
                    image "download_icon_done" size (24, 24)
                    image "images/flags/English.png" size (30, 20)
                    text "English" style "dropdown_text"
            
            # Russian option
            button:
                style "language_choice_button"
                action [
                    # Check if installed
                    If (tl_folder_exists("Russian"),
                        # If installed, change language
                        [Language("Russian"),
                        SetVariable("persistent.selected_language_name", "Русский"),
                        Hide("language_dropdown_choices")],
                        # If not installed, show confirmation
                        [Hide("language_dropdown_choices"),
                        Show("language_confirm_download", language="Russian", display_name="Русский")]
                    )
                ]
                hbox:
                    spacing 10
                    # Show appropriate icon based on installation status
                    if tl_folder_exists("Russian"):
                        image "download_icon_done" size (24, 24)
                    else:
                        image "download_icon" size (24, 24)
                    image "images/flags/Russian.png" size (30, 20)
                    text "Русский" style "dropdown_text"
            
            # Chinese option
            button:
                style "language_choice_button"
                action [
                    If (tl_folder_exists("Chinese"),
                        [Language("Chinese"),
                        SetVariable("persistent.selected_language_name", "中文"),
                        Hide("language_dropdown_choices")],
                        [Hide("language_dropdown_choices"),
                        Show("language_confirm_download", language="Chinese", display_name="中文")]
                    )
                ]
                hbox:
                    spacing 10
                    # Show appropriate icon based on installation status
                    if tl_folder_exists("Chinese"):
                        image "download_icon_done" size (24, 24)
                    else:
                        image "download_icon" size (24, 24)
                    image "images/flags/Chinese.png" size (30, 20)
                    text "中文" style "dropdown_text"
            
            # Portuguese option
            button:
                style "language_choice_button"
                action [
                    If (tl_folder_exists("BR_Portuguese"),
                        [Language("BR_Portuguese"),
                        SetVariable("persistent.selected_language_name", "Português"),
                        Hide("language_dropdown_choices")],
                        [Hide("language_dropdown_choices"),
                        Show("language_confirm_download", language="BR_Portuguese", display_name="Português")]
                    )
                ]
                hbox:
                    spacing 10
                    # Show appropriate icon based on installation status
                    if tl_folder_exists("BR_Portuguese"):
                        image "download_icon_done" size (24, 24)
                    else:
                        image "download_icon" size (24, 24)
                    image "images/flags/BR_Portuguese.png" size (30, 20)
                    text "Português" style "dropdown_text"

            # Spanish option
            button:
                style "language_choice_button"
                action [
                    If (tl_folder_exists("Spanish"),
                        [Language("Spanish"),
                        SetVariable("persistent.selected_language_name", "Español"),
                        Hide("language_dropdown_choices")],
                        [Hide("language_dropdown_choices"),
                        Show("language_confirm_download", language="Spanish", display_name="Español")]
                    )
                ]
                hbox:
                    spacing 10
                    # Show appropriate icon based on installation status
                    if tl_folder_exists("Spanish"):
                        image "download_icon_done" size (24, 24)
                    else:
                        image "download_icon" size (24, 24)
                    image "images/flags/Spanish.png" size (30, 20)
                    text "Español" style "dropdown_text"
            
            # Italian
            button:
                style "language_choice_button"
                action [
                    If (tl_folder_exists("Italian"),
                        [Language("Italian"),
                        SetVariable("persistent.selected_language_name", "Italiano"),
                        Hide("language_dropdown_choices")],
                        [Hide("language_dropdown_choices"),
                        Show("language_confirm_download", language="Italian", display_name="Italiano")]
                    )
                ]
                hbox:
                    spacing 10
                    # Show appropriate icon based on installation status
                    if tl_folder_exists("Italian"):
                        image "download_icon_done" size (24, 24)
                    else:
                        image "download_icon" size (24, 24)
                    image "images/flags/Italian.png" size (30, 20)
                    text "Italiano" style "dropdown_text"

           

            # French
            button:
                style "language_choice_button"
                action [
                    If (tl_folder_exists("French"),
                        [Language("French"),
                        SetVariable("persistent.selected_language_name", "Français"),
                        Hide("language_dropdown_choices")],
                        [Hide("language_dropdown_choices"),
                        Show("language_confirm_download", language="French", display_name="Français")]
                    )
                ]
                hbox:
                    spacing 10
                    # Show appropriate icon based on installation status
                    if tl_folder_exists("French"):
                        image "download_icon_done" size (24, 24)
                    else:
                        image "download_icon" size (24, 24)
                    image "images/flags/French.png" size (30, 20)
                    text "Français" style "dropdown_text"

            # Turkish
            button:

                style "language_choice_button"
                action [
                    If (tl_folder_exists("Turkish"),
                    
                        [Language("Turkish"),
                        SetVariable("persistent.selected_language_name", "Türkiye"),
                        Hide("language_dropdown_choices")],
                        [Hide("language_dropdown_choices"),
                        Show("language_confirm_download", language="Turkish", display_name="Türkiye")]
                    )
                ]
                hbox:
                    spacing 10
                    # Show appropriate icon based on installation status
                    if tl_folder_exists("Turkish"):
                        image "download_icon_done" size (24, 24)
                    else:
                        image "download_icon" size (24, 24)
                    image "images/flags/Turkish.png" size (30, 20)
                    text "Türkiye" style "dropdown_text"
        
            # Greek
            button:
                style "language_choice_button"
                action [
                    If (tl_folder_exists("Greek"),
                        [Language("Greek"),
                        SetVariable("persistent.selected_language_name", "Ελληνικά"),
                        Hide("language_dropdown_choices")],
                        [Hide("language_dropdown_choices"),
                        Show("language_confirm_download", language="Greek", display_name="Ελληνικά")]
                    )
                ]
                hbox:
                    spacing 10
                    # Show appropriate icon based on installation status
                    if tl_folder_exists("Greek"):
                        image "download_icon_done" size (24, 24)
                    else:
                        image "download_icon" size (24, 24)
                    image "images/flags/Greek.png" size (30, 20)
                    text "Ελληνικά" style "dropdown_text"


screen language_confirm_download(language, display_name):
    modal True
    
    frame:
        style "confirm_frame"
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            
            text _("Do you want to install [display_name]?"):
                style "confirm_prompt"
                xalign 0.5
            
            text _("The game will restart once the download is complete."):
                style "confirm_prompt"
                xalign 0.5

            text _("Note: Machine translations can be inaccurate and may cause minor issues with the UI"):
                style "confirm_prompt"
                xalign 0.5
            
            hbox:
                spacing 100
                xalign 0.5
                
                textbutton _("Yes") style "confirm_button" text_style "confirm_button_text" action [
                    Function(download_language, language),
                    Hide("language_confirm_download")
                ]
                
                textbutton _("No") style "confirm_button" text_style "confirm_button_text" action Hide("language_confirm_download")


# Screen to show while language is installing
screen language_installing():
    modal True
    sensitive True 
    
    frame:
        style "confirm_frame"
        xalign 0.5
        yalign 0.5
        xsize 400
        
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            
            text _("Installing [current_language]..."):
                style "confirm_prompt"
                xalign 0.5
            
            # Progress bar
            bar value download_progress range 1.0 xsize 350 ysize 30
            
            text _("{0:.0%} complete".format(download_progress)):
                xalign 0.5
            
            # Animated "downloading" image
            image "download_icon_done" xalign 0.5 at downloading_animation
            
# Define an animation for the downloading icon
transform downloading_animation:
    xalign 0.5
    zoom 1.0
    linear 0.5 zoom 1.2
    linear 0.5 zoom 1.0
    repeat

# Updated styles
style dropdown_button:
    background "#171717"
    hover_background "#444444"
    padding (10, 5)

style dropdown_text:
    color "#ffffff"
    size 18

style dropdown_arrow:
    color "#ffffff"
    size 18
    xalign 1.0

style dropdown_choices_frame:  # New style name
    background "#000000CC"
    padding (5, 5)

style dropdown_vbox:
    spacing 2

style language_choice_button:  # New style for language choice buttons
    background None
    hover_background "#ffffff33"  # Semi-transparent white on hover
    padding (10, 5)
    xsize 220
style blank_button:
    background None

