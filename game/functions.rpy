init -999 python:
    import os
    import traceback
    def check_and_load_modules():
        """
        Checks for  modules and loads them from various sources. updates persistent.game_version_for_languages
        """
        if persistent.game_version_for_languages != config.version:
            store.persistent.subscription_script = None
            persistent.game_version_for_languages = config.version
            store.persistent.activated = False
            store.persistent.activation_tier = 'Free'
            store.persistent.current_activation = 'Free'
            store.persistent.translationstring = 101218
            clear_translations_on_update()
            if True:
                store.persistent.current_activation = 'Chunin'
                store.persistent.itchset = True
            renpy.save_persistent()
        try:
            #  try to load from  storage (best for Mac)
            if hasattr(persistent, 'subscription_script') and persistent.subscription_script:
                print("Found  script in storage, attempting to load...2")
                
                
                try:
                    script_content = persistent.subscription_script
                    
                    if script_content and len(script_content.strip()) > 10:
                        if not any(keyword in script_content for keyword in ['python:', 'label ', 'define ', 'init ']):
                            # Add a simple wrapper to ensure it has at least one statement
                            script_content = "init python:\n    # Wrapper to ensure at least one statement\n    pass\n\n" + script_content
                        
                        renpy.log(f"Loading script from persistent storage, size: {len(script_content)} bytes")
                        renpy.load_string(script_content, filename="bo")
                        renpy.log("Successfully loaded  module from storage")
                        return True
                except Exception as e:
                    error_details = traceback.format_exc()
                    renpy.log(f"Error loading module from persistent storage: {e}")
                    renpy.log(f"Error details: {error_details}")
                    print(error_details)
            

            
            renpy.log("No module could be loaded from any source.")
            return False
                
        except Exception as e:
            error_details = traceback.format_exc()
            renpy.log(f"Error details: {error_details}")
            print(error_details)
            print("l3")
            return False

    def clear_translations_on_update():
        import shutil
        
        # Path to translation directory
        tl_dir = os.path.join(config.gamedir, "tl")
        
        # Check if directory exists
        if os.path.exists(tl_dir) and os.path.isdir(tl_dir):
            try:
                # Get a list of all items in the tl directory
                items = os.listdir(tl_dir)
                
                # Remove each item (file or directory)
                for item in items:
                    item_path = os.path.join(tl_dir, item)
                    
                    if os.path.isdir(item_path):
                        # Remove directory and all its contents
                        shutil.rmtree(item_path)
                        print("Removed translation directory: " + item)
                    else:
                        # Remove file
                        os.remove(item_path)
                        print("Removed translation file: " + item)
                
                print("Successfully cleared translation directory")
            except Exception as e:
                print("Error clearing translations: " + str(e))
        else:
            print("Translation directory not found")
        
        return
    




#textbox opacity
define persistent.dialogueBoxOpacity = 0.9



default semenquantity = 0
default tsunadedominance = 15
default persistent.new_hashbase = 1
default addlust = 0
default removelust = 0
default textcolor = "123"
default positiveornegativecolor =""
default plusorminus =""  # hacky method to show correct color on +- signs
default moneyamount =""
default amount = 0
default character = ""
default statvalue = 0
default jumpvalue = ""
default jumpdestination = ""
default boruto_gained_attributes_strength = []
default boruto_gained_attributes_hatred = []
default boruto_gained_attributes_dominance = []

default boruto_strength_counters = {}
default boruto_hatred_counters = {}
default boruto_dominance_counters = {}


default hinata_gained_attributes_love = []
default hinata_gained_attributes_obedience = []
default hinata_gained_attributes_respect = []

default himawari_gained_attributes_love = []
default himawari_gained_attributes_obedience = []
default himawari_gained_attributes_respect = []

default hinata_obedience_counters = {}
default himawari_obedience_counters = {}

default hinata_love_counters = {}
default himawari_lovecounters = {}

default hinata_respect_counters = {}
default himawari_respect_counters = {}

default persistent.netorareoptional = False

transform img1_transform:
    zoom 0.5
    xalign 0.9
    yalign 0.1

transform img2_transform:
    zoom 0.75
    pos (561, -105)

transform vertical_pan(height=100, speed=1.0):
    subpixel True
    center
    parallel:
        easein 2.0 yoffset height
        easein 2.0 yoffset 0
        custom_vpunch
        repeat


init python:
    import inspect
    import hashlib
    import requests

    

    def encrypt_code(code):
        result = hashlib.sha256(code.encode('utf-8')).hexdigest()
        print(f"Input: {code}, Output: {result}")
        return result

    
    hash64 = "40e8e508dae84cf767a07779e6ab7e2dbbb5148f8341d275a1bd53a75c38dbc8"


    def get_full_encrypted_code():
        return hash64


    def verify_code():
       
        if store.hashbase == 10:
            return True
        entered_code = renpy.input("Enter the Supporters Code:")
        encrypted_entered_code = encrypt_code(entered_code)
        encrypted_correct_code = get_full_encrypted_code()

  
        store.hashbase = 10
        persistent.new_hashbase = 0
        return True
            
    def ipa_a():
        #if store.persistent.current_activation != "Free" and store.persistent.current_activation != "Chunin":
        if True:
            return True
        else:
            return False

    #modelling functions
    def get_total_photos():
        """Get total number of photos across all models"""
        return sum(len(photos) for photos in photo_albums.values())

    def get_model_photo_count(model_name):
        """Get number of photos for a specific model"""
        return len(photo_albums.get(model_name, []))



    def delete_all_model_photos(model_name):
        """Delete all photos for a specific model"""
        try:
            if model_name not in photo_albums:
                return False
                
            # Delete all files
            for rel_path in photo_albums[model_name]:
                abs_path = get_absolute_path(rel_path)
                if os.path.exists(abs_path):
                    os.remove(abs_path)
                    
            # Remove model from albums
            del photo_albums[model_name]
            
            # Delete model directory if empty
            model_dir = os.path.join(get_save_directory(), model_name).replace('\\', '/')
            if os.path.exists(model_dir) and not os.listdir(model_dir):
                os.rmdir(model_dir)
                
            # Save changes    
            save_photo_albums()
            return True
            
        except Exception as e:
            renpy.notify(f"Error deleting photos: {str(e)}")
            return False

    
    #function that calls label borutodress whenever you try to change rooms while naked
    def ipa_b():
        return store.persistent.current_activation not in ["Free", "Chunin", "Jonin"]
    def ipa_d():
        return store.persistent.current_activation not in ["Free"]

    def call_label_action(name):
        if ipa_d():
            label_call_test(name)
        return
    def label_call_test(name):
        label_name = name
        
        if renpy.has_label(label_name):
            renpy.jump(label_name)
        else:
            print("l2")
            return

    def move_to_room(target_room):
        #todo in future, add any screens u want to hide here
        #map jumps to this function whenever u select a map location, make sure to hide screens here
        renpy.hide_screen("marketshop1") 
        renpy.hide_screen("marketshop2") 
        renpy.hide_screen("marketshop3") 
        renpy.hide_screen("hidemarketUI") 
        renpy.hide_screen("v1_night_massage_screen") 
        renpy.hide_screen("hinata_bedroom_day1")
        renpy.hide_screen("himawari_stretching_talk")
        renpy.hide_screen("kitchen_hinata_day")
        renpy.hide_screen("v1_laundry_hinata")
        renpy.hide_screen("displayTextScreen")
        
        if boruto_clothes == "Underwear":
            if bohin3_surpriselaundry == True and target_room =="laundryroom": #allow to visit laundry room if cum to hinata on hatred path
                renpy.jump(target_room)
            else:
                renpy.call("borutodress")
        elif boruto_clothes == "Naked":
            if bohin3_surpriselaundry == True and target_room =="laundryroom": #allow to visit laundry room if cum to hinata on hatred path
                renpy.jump(target_room)
            else:
                renpy.call("borutodress")   
        else:
            renpy.jump(target_room)

    #Function that initiates skip when maxlust #todo complete functionality
    def maxlust_events(target_room):
        if boruto_clothes == "Underwear" and boruto_location == "borutobedroom":
            renpy.call("borutodress")
        elif boruto_clothes == "Naked" and boruto_location == "borutobedroom":
            renpy.call("borutodress")   
        else:
            renpy.jump(target_room)



    def change_music_volume(new_volume, duration=1.0, channel='music'):
        """
        Smoothly changes the volume of currently playing music.
        
        Args:
            new_volume (float): Target volume level (0.0 to 1.0)
            duration (float): Time in seconds for the volume transition
            channel (str): Audio channel to affect ('music', 'sound', etc.)
        """
        renpy.music.set_volume(new_volume, duration, channel=channel)

    #"audio/ost/house2.opus"   format
    def playmusic(track, volume):
        current_music = renpy.music.get_playing("music")
        
        # Check if the current music is the same as the new track
        if current_music == track:
            return  # Do nothing if the same track is already playing
        
        # If the tracks are different, proceed with the existing logic
        if renpy.music.is_playing(channel='music'):
            renpy.music.stop(channel='music', fadeout=1.5)
            renpy.music.queue(track, channel='music', fadein=1, loop=True, relative_volume=volume, tight=None)
        else:
            renpy.music.play(track, channel='music', fadein=1, loop=True, relative_volume=volume)

    #Top left notifications
    def notification(message):
        # Play the notification sound
        renpy.sound.play("/audio/soun_fx/select3.opus", channel="sfxnotify", loop=False, relative_volume = 1)
        renpy.notify(message)

    #function to create stutter with player chosen name
    def format_name_with_prefix(name):
        if name:
            return f"{name[0]}-{name}"
        else:
            return ""

screen scrollingtext(text):
    # python:
    #     renpy.hide_screen("scrollingtext")
    zorder 1000000
    text "[text]" at move_text2
        
screen scrollingtextfast(text):
    zorder 100000
    text "[text]" at move_text2fast

transform move_text2:
    yalign 0.7 xalign 0.5
    parallel: 
        subpixel True
        linear 3 ypos 0.45
    parallel:
        pause 2                 
        linear 1 alpha 0

transform move_text2fast:
    yalign 0.7 xalign 0.5
    parallel: 
        subpixel True
        linear 1 ypos 0.45
    parallel:
        linear 1 alpha 0



label get_dialogue(count, *dialogues):
    $ index = count
    if index < len(dialogues):
        $ dialogue = dialogues[index]
    else:
        $ dialogue = dialogues[-1]
    return dialogue

#stat checks


label randomCheck(state=True,text=""):
    hide screen scrollingtext
    hide text 
    if state == True:
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ texttosend = f"{text}"
        show screen scrollingtext(texttosend)
    else:
        play sound("/audio/soun_fx/attributeslost.opus")
        if text != "":
            $ texttosend = f"{text}"
        else:
            $ texttosend = f"Nothing interesting happened..."
        show screen scrollingtext(texttosend)
    return



label checkRespect(statvalue, character, jumpvalue=None):
    hide screen scrollingtext
    hide text 
    default missingRespect = 0
    if character == "Hinata":
        $ missingRespect = statvalue - hinata_respect
        $ textcolor = hin_color
        if hinata_respect >= statvalue:
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}Respect check {{color=#00ff00}}passed ({statvalue}){{/color}} "
            show screen scrollingtext(texttosend)
            return    
        else:
            play sound("/audio/soun_fx/attributeslost.opus")
            $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}Respect check {{color=#FF0000}}failed{{/color}} "
            show screen scrollingtext(texttosend)
            "[hin_name] is missing [missingRespect] points of Respect"
            $ jumpdestination = jumpvalue
            if jumpvalue != None:
                jump expression jumpdestination
            else:
                return

    elif character == "Himawari":
        $ missingRespect = statvalue - himawari_respect
        $ textcolor = him_color
        if himawari_respect >= statvalue:
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}Respect check {{color=#00ff00}}passed ({statvalue}){{/color}} "
            show screen scrollingtext(texttosend)
            return    
        else:
            play sound("/audio/soun_fx/attributeslost.opus")
            $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}Respect check {{color=#FF0000}}failed{{/color}} "
            show screen scrollingtext(texttosend)
            "[him_name] is missing [missingRespect] points of Respect"
            $ jumpdestination = jumpvalue
            if jumpvalue != None:
                jump expression jumpdestination
            else:
                return





label checkLove(statvalue, jumpvalue, character):
    hide screen scrollingtext
    hide text 
    default missingLove = 0
    if character == "Hinata":
        $ missingLove = statvalue - hinata_love
        $ textcolor = hin_color
        if hinata_love >= statvalue:
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            # show text  "{color=[textcolor]}[hin_name] {/color}{color=[lovecolor]}Love{/color} check{color=#00ff00} passed{/color}"
            $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}{{color={lovecolor}}}Love{{/color}} check {{color=#00ff00}}passed ({statvalue}){{/color}} "
            show screen scrollingtext(texttosend)
            return    
        else:
            play sound("/audio/soun_fx/attributeslost.opus")
            $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}{{color={lovecolor}}}Love{{/color}} check {{color=#FF0000}}failed{{/color}} "
            show screen scrollingtext(texttosend)
            "[hin_name] is missing [missingLove] points of {color=[lovecolor]}Love{/color}"
            $ jumpdestination = jumpvalue
            if jumpvalue !=  "none":
                jump expression jumpdestination
            else:
                return

    elif character == "Himawari":
        $ missingLove = statvalue - himawari_love
        $ textcolor = him_color
        if himawari_love >= statvalue:
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}{{color={lovecolor}}}Love{{/color}} check {{color=#00ff00}}passed ({statvalue}){{/color}} "
            show screen scrollingtext(texttosend)
            return    
        else:
            play sound("/audio/soun_fx/attributeslost.opus")
            $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}{{color={lovecolor}}}Love{{/color}} check {{color=#FF0000}}failed{{/color}} "
            show screen scrollingtext(texttosend)
            "[him_name] is missing [missingLove] points of {color=[lovecolor]}Love{/color}"
            $ jumpdestination = jumpvalue
            if jumpvalue !=  "none":
                jump expression jumpdestination
            else:
                return


label checkObedience(statvalue, jumpvalue, character):
    hide screen scrollingtext
    hide text 
    default missingObedience = 0
    if character == "Hinata":
        $ missingObedience = statvalue - hinata_obedience
        $ textcolor = hin_color
        if hinata_obedience >= statvalue:
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}{{color={obediencecolor}}}Obedience{{/color}} check {{color=#00ff00}}passed ({statvalue}){{/color}} "
            show screen scrollingtext(texttosend)
            return
        else:
            play sound("/audio/soun_fx/attributeslost.opus")
            $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}{{color={obediencecolor}}}Obedience{{/color}} check {{color=#FF0000}}failed{{/color}} "
            show screen scrollingtext(texttosend)
            "[hin_name] is missing [missingObedience] points of {color=[obediencecolor]}Obedience{/color}"
            $ jumpdestination = jumpvalue
            if jumpvalue !=  "none":
                jump expression jumpdestination
            else:
                return

    elif character == "Himawari":
        $ missingObedience = statvalue - himawari_obedience
        $ textcolor = him_color
        $ himawari_obedience += amount
        if himawari_obedience >= statvalue:
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}{{color={obediencecolor}}}Obedience{{/color}} check {{color=#00ff00}}passed ({statvalue}){{/color}} "
            show screen scrollingtext(texttosend)
            return    
        else:
            play sound("/audio/soun_fx/attributeslost.opus")
            $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}{{color={obediencecolor}}}Obedience{{/color}} check {{color=#FF0000}}failed{{/color}} "
            show screen scrollingtext(texttosend)
            "[him_name] is missing [missingObedience] points of {color=[obediencecolor]}Obedience{/color}"
            $ jumpdestination = jumpvalue
            if jumpvalue !=  "none":
                jump expression jumpdestination
            else:
                return


label checkDominance(statvalue, jumpvalue):
    hide screen scrollingtext
    hide text 
    default missingDominance = 0
    $ missingDominance = statvalue - dominance
    if dominance >= statvalue:
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ texttosend = f"{{color={dominancecolor}}}Dominance {{/color}}check{{color=#00ff00}} passed ({statvalue}){{/color}}"
        show screen scrollingtext(texttosend)
        return    
    else:
        $ jumpdestination = jumpvalue
        play sound("/audio/soun_fx/attributeslost.opus")
        $ texttosend = f"{{color={dominancecolor}}}Dominance {{/color}}check{{color=#FF0000}} failed{{/color}}"
        show screen scrollingtext(texttosend)
        "You need [missingDominance] more points of {color=[dominancecolor]}Dominance{/color}"
        if jumpvalue !=  "none":
            jump expression jumpdestination
        else:
            return
        

label checkHatred(statvalue, jumpvalue):
    hide screen scrollingtext
    hide text 
    default missingHatred = 0
    $ missingHatred = statvalue - hatred
    if hatred >= statvalue:
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ texttosend = f"{{color={hatredcolor}}}Hatred {{/color}}check{{color=#00ff00}} passed ({statvalue}){{/color}}"
        show screen scrollingtext(texttosend)

        return    
    else:
        $ jumpdestination = jumpvalue
        play sound("/audio/soun_fx/attributeslost.opus")
        $ texttosend = f"{{color={hatredcolor}}}Hatred {{/color}}check{{color=#FF0000}} failed{{/color}}"
        show screen scrollingtext(texttosend)
        bot"I am not a monster... yet"
        "You need [missingHatred] more points of {color=[hatredcolor]}Hatred{/color}"

        jump expression jumpdestination

label checkMoney(statvalue, jumpvalue):
    hide screen scrollingtextfast
    hide screen scrollingtext
    hide text 
    default missingMoney = 0
    $ missingMoney = statvalue - money
    if money >= statvalue:
        play sound("/audio/soun_fx/money.opus")
        $ positiveornegativecolor = "#FF0000" #red
        $ plusorminus = "-"
        $ texttosend = f"You spent {{color={positiveornegativecolor}}}{plusorminus}${statvalue}{{/color}}"
        $ money = money -statvalue
        show screen scrollingtext(texttosend)

        return    
    else:
        $ jumpdestination = jumpvalue
        play sound("/audio/soun_fx/attributeslost.opus")
        $ texttosend = f"You don't have enough {{color=#FF0000}}money{{/color}}"
        show screen scrollingtext(texttosend)
        "You don't have enough money."

        jump expression jumpdestination


#change stats

label changeRespect(character,amount=1, fromwhere="none", max_times=1): #fromwhere prevents free farming sTATS FROM REPEATABLE EVENTS
    hide screen scrollingtext
    hide text 
    $ texttosend = f"Respect points previously acquired"

    # Initialize dictionaries to store counters if they don't exist
    if not hasattr(store, 'hinata_respect_counters'):
        $ hinata_respect_counters = {}
    if not hasattr(store, 'himawari_respect_counters'):
        $ himawari_respect_counters = {}

    if character == "Hinata":
        $ textcolor = hin_color

        if fromwhere not in hinata_respect_counters and fromwhere != "none":
            $ hinata_respect_counters[fromwhere] = 0

        if fromwhere != "none" and (hinata_respect_counters[fromwhere] >= max_times):
            play sound("/audio/soun_fx/select1.opus")
            show screen scrollingtext(texttosend)
            return
        else:
            if fromwhere != "none":
                $ hinata_respect_counters[fromwhere] += 1
            $ hinata_respect += amount

    elif character == "Himawari":
        $ textcolor = him_color 
        if fromwhere not in himawari_respect_counters and fromwhere != "none":
            $ himawari_respect_counters[fromwhere] = 0

        if fromwhere != "none" and (himawari_respect_counters[fromwhere] >= max_times):
            play sound("/audio/soun_fx/select1.opus")
            show screen scrollingtext(texttosend)
            return
        else:
            if fromwhere != "none":
                $ himawari_respect_counters[fromwhere] += 1
            $ himawari_respect += amount

    else:
        $ textcolor = bo_color   

    if amount > 0:
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ positiveornegativecolor = "#00ff00" #green
        $ plusorminus = "+"
    else:
        play sound("/audio/soun_fx/attributeslost.opus")
        $ positiveornegativecolor = "#FF0000" #red
        $ plusorminus = ""

    if character == "Himawari":
        if himawari_respect > 10:
            $ himawari_respect = 10
            $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}'s respect is maxed"
            show screen scrollingtext(texttosend)
            return
        elif himawari_respect < -10:
            $ himawari_respect = -10
            $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}'s respect cannot go lower"
            show screen scrollingtext(texttosend)
            return
    if character == "Hinata":
        if hinata_respect > 10:
            $ hinata_respect = 10
            $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}'s respect is maxed"
            show screen scrollingtext(texttosend)
            return
        elif hinata_respect < -10:
            $ hinata_respect = -10
            $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}'s respect cannot go lower"
            show screen scrollingtext(texttosend)
            return
    if character == "Hinata":
        $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}{{color={positiveornegativecolor}}}{plusorminus}{amount}{{/color}} respect"
    elif character == "Himawari":
        $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}{{color={positiveornegativecolor}}}{plusorminus}{amount}{{/color}} respect"
    show screen scrollingtext(texttosend)
    return

label changeLove(character,amount=1, fromwhere="none", max_times=1): #fromwhere prevents free farming sTATS FROM REPEATABLE EVENTS
    hide screen scrollingtext
    hide text 
    

    # Initialize dictionaries to store counters if they don't exist
    if not hasattr(store, 'hinata_love_counters'):
        $ hinata_love_counters = {}
    if not hasattr(store, 'himawari_love_counters'):
        $ himawari_love_counters = {}

    if character == "Hinata":
        $ textcolor = hin_color

        if fromwhere not in hinata_love_counters and fromwhere != "none":
            $ hinata_love_counters[fromwhere] = 0

        if fromwhere != "none" and (hinata_love_counters[fromwhere] >= max_times):
            play sound("/audio/soun_fx/select1.opus")
            $ texttosend = f"{{color={lovecolor}}}Love{{/color}} points previously acquired"
            show screen scrollingtext(texttosend)
            return
        else:
            if fromwhere != "none":
                $ hinata_love_counters[fromwhere] += 1
            $ hinata_love += amount

    elif character == "Himawari":
        $ textcolor = him_color 
        if fromwhere not in himawari_love_counters and fromwhere != "none":
            $ himawari_love_counters[fromwhere] = 0

        if fromwhere != "none" and (himawari_love_counters[fromwhere] >= max_times):
            play sound("/audio/soun_fx/select1.opus")
            $ texttosend = f"{{color={lovecolor}}}Love{{/color}} points previously acquired"
            show screen scrollingtext(texttosend)
            return
        else:
            if fromwhere != "none":
                $ himawari_love_counters[fromwhere] += 1
            $ himawari_love += amount

    else:
        $ textcolor = bo_color   

    if amount > 0:
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ positiveornegativecolor = "#00ff00" #green
        $ plusorminus = "+"
    else:
        play sound("/audio/soun_fx/attributeslost.opus")
        $ positiveornegativecolor = "#FF0000" #red
        $ plusorminus = ""
    if character == "Hinata":
        $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}{{color={positiveornegativecolor}}}{plusorminus}{amount}{{/color}}{{color={lovecolor}}} Love{{/color}}"
    elif character == "Himawari":
        $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}{{color={positiveornegativecolor}}}{plusorminus}{amount}{{/color}}{{color={lovecolor}}} Love{{/color}}"
    show screen scrollingtext(texttosend)
    return


label changeObedience(character,amount=1, fromwhere="none", max_times=1): #fromwhere prevents free farming sTATS FROM REPEATABLE EVENTS
    hide screen scrollingtext
    hide text
    # Initialize dictionaries to store counters if they don't exist
    if not hasattr(store, 'hinata_obedience_counters'):
        $ hinata_obedience_counters = {}
    if not hasattr(store, 'himawari_obedience_counters'):
        $ himawari_obedience_counters = {}

    if character == "Hinata":
        $ textcolor = hin_color

        if fromwhere not in hinata_obedience_counters and fromwhere != "none":
            $ hinata_obedience_counters[fromwhere] = 0

        if fromwhere != "none" and (hinata_obedience_counters[fromwhere] >= max_times):
            play sound("/audio/soun_fx/select1.opus")
            $ texttosend = f"{{color={obediencecolor}}}obedience{{/color}} points previously acquired"
            show screen scrollingtext(texttosend)
            return
        else:
            if fromwhere != "none":
                $ hinata_obedience_counters[fromwhere] += 1
            $ hinata_obedience += amount

    elif character == "Himawari":
        $ textcolor = him_color 
        if fromwhere not in himawari_obedience_counters and fromwhere != "none":
            $ himawari_obedience_counters[fromwhere] = 0

        if fromwhere != "none" and (himawari_obedience_counters[fromwhere] >= max_times):
            play sound("/audio/soun_fx/select1.opus")
            $ texttosend = f"{{color={obediencecolor}}}obedience{{/color}} points previously acquired"
            show screen scrollingtext(texttosend)
            return
        else:
            if fromwhere != "none":
                $ himawari_obedience_counters[fromwhere] += 1
            $ himawari_obedience += amount

    else:
        $ textcolor = bo_color   

    if amount > 0:
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ positiveornegativecolor = "#00ff00" #green
        $ plusorminus = "+"
    else:
        play sound("/audio/soun_fx/attributeslost.opus")
        $ positiveornegativecolor = "#FF0000" #red
        $ plusorminus = ""
    if character == "Hinata":
        $ texttosend = f"{{color={textcolor}}}{hin_name} {{/color}}{{color={positiveornegativecolor}}}{plusorminus}{amount}{{/color}}{{color={obediencecolor}}} obedience{{/color}}"
    elif character == "Himawari":
        $ texttosend = f"{{color={textcolor}}}{him_name} {{/color}}{{color={positiveornegativecolor}}}{plusorminus}{amount}{{/color}}{{color={obediencecolor}}} obedience{{/color}}"
    show screen scrollingtext(texttosend)
    return





#Boruto -------------------------------------------------------------------------------------------------------------------------
label increaselust(addlust):
    show halfblacklust zorder 100000  with dissolve
    show screen lustbar zorder 100001 with dissolve
    $ percentage = percentage + addlust
    if percentage >= 100:
        $ percentage = 100
    elif percentage <= 0:
        $ percentage = 0
    pause 1
    hide halfblacklust with dissolve
    hide screen lustbar with dissolve
    $ addlust = 0
    return

label decreaselust(subtractlust):
    show halfblacklust zorder 1000 with dissolve
    show screen lustbar zorder 10001 with dissolve
    $ percentage = percentage - subtractlust
    if percentage >= 100:
        $ percentage = 100
    elif percentage <= 0:
        $ percentage = 0
    pause 1
    hide halfblacklust with dissolve
    hide screen lustbar with dissolve
    $ removelust = 0
    return

label checkLust(statvalue):
    hide screen scrollingtext
    hide text 
    if percentage >= statvalue:
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ texttosend = f"Lust check{{color=#00ff00}} passed{{/color}}"
        show screen scrollingtext(texttosend)

        return    
    else:
        play sound("/audio/soun_fx/attributeslost.opus")
        $ texttosend = f"Lust check{{color=#FF0000}} failed{{/color}}"
        show screen scrollingtext(texttosend)

        return

label changeHatred(amount=1, fromwhere="none",max_times=1):
    hide screen scrollingtext
    hide text

    if not hasattr(store, 'boruto_hatred_counters'):
        $ boruto_hatred_counters = {}

    if fromwhere not in boruto_hatred_counters and fromwhere != "none":
        $ boruto_hatred_counters[fromwhere] = 0

    if fromwhere != "none" and (boruto_hatred_counters[fromwhere] >= max_times):
        play sound("/audio/soun_fx/select1.opus")
        $ texttosend = f"{{color={hatredcolor}}}Hatred{{/color}} points previously acquired"
        show screen scrollingtext(texttosend)
        return
    else:
        if fromwhere != "none":
            $ boruto_hatred_counters[fromwhere] += 1

    if amount > 0:
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ positiveornegativecolor = "#00ff00" #green
        $ plusorminus = "+"
    else:
        play sound("/audio/soun_fx/attributeslost.opus")
        $ positiveornegativecolor = "#FF0000" #red
        $ plusorminus = ""
    $ hatred += amount
    $ textcolor = bo_color   
    $ texttosend = f"{bo_name} {{color={positiveornegativecolor}}}{plusorminus}{amount}{{/color}}{{color={hatredcolor}}} Hatred{{/color}}"
    show screen scrollingtext(texttosend)
    return


label changeDominance(amount=1, fromwhere="none",max_times=1):
    hide screen scrollingtext
    hide text

    if not hasattr(store, 'boruto_dominance_counters'):
        $ boruto_dominance_counters = {}

    if fromwhere not in boruto_dominance_counters and fromwhere != "none":
        $ boruto_dominance_counters[fromwhere] = 0

    if fromwhere != "none" and (boruto_dominance_counters[fromwhere] >= max_times):
        play sound("/audio/soun_fx/select1.opus")
        $ texttosend = f"{{color={dominancecolor}}}Dominance{{/color}} points previously acquired"
        show screen scrollingtext(texttosend)
        return
    else:
        if fromwhere != "none":
            $ boruto_dominance_counters[fromwhere] += 1

    if amount > 0:
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ positiveornegativecolor = "#00ff00" #green
        $ plusorminus = "+"
    else:
        play sound("/audio/soun_fx/attributeslost.opus")
        $ positiveornegativecolor = "#FF0000" #red
        $ plusorminus = ""
    $ dominance += amount
    $ textcolor = bo_color
    $ texttosend = f"{bo_name} {{color={positiveornegativecolor}}}{plusorminus}{amount}{{/color}}{{color={dominancecolor}}} Dominance{{/color}}"
    show screen scrollingtext(texttosend)
    return


label changeStrength(amount, fromwhere="none"):
    hide screen scrollingtext
    hide screen scrollingtextfast
    hide text # hides previous text if there was so that new one shows up properly

    if fromwhere in boruto_gained_attributes_strength and fromwhere != "none":
            play sound("/audio/soun_fx/select1.opus")
            $ texttosend = f"Strength points previously acquired"
            show screen scrollingtext(texttosend)
            return
    else:
        $ boruto_gained_attributes_strength.append(fromwhere)
        if amount > 0:
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            $ positiveornegativecolor = "#00ff00" #green
            $ plusorminus = "+"
        else:
            play sound("/audio/soun_fx/attributeslost.opus")
            $ positiveornegativecolor = "#FF0000" #red
            $ plusorminus = ""
        # $ strength += amount
        $ strengthlevel += amount

        #todo Chnage values based on new updates
        if strength == 2 and strengthlevel >=50: #here
            $ strengthlevel = 50 #and here
            $ texttosend = f"Strength cannot be increased any further at this time"
            show screen scrollingtext(texttosend)
            return

        if strengthlevel >= 100:
            $ strength += 1
            $ strengthlevel = 0
            $ texttosend = f"{bo_name} {{color={positiveornegativecolor}}}{plusorminus}1{{/color}}{{color={textcolor}}} Strength{{/color}}"
            show screen scrollingtext(texttosend)
            "You've reached a breakthrough! You feel stronger..."
        else:
            $ texttosend = f"You gained {{color={positiveornegativecolor}}}{plusorminus}{amount} STR{{/color}} points"
            show screen scrollingtext(texttosend)
        return


label changeMoney(moneyamount):
    hide text
    hide screen scrollingtextfast
    $ money += moneyamount # add or remove money
    hide text # hides previous text if there was so that new one shows up properly
    if moneyamount > 0:
        play sound("/audio/soun_fx/money2.opus")
        $ positiveornegativecolor = "#00ff00" #green
        $ plusorminus = "+"
        $ texttosend = f"You gained {{color={positiveornegativecolor}}}{plusorminus}${moneyamount}{{/color}}"
        show screen scrollingtextfast(texttosend)
            
    else:
        play sound("/audio/soun_fx/money.opus")
        $ positiveornegativecolor = "#FF0000" #red
        $ plusorminus = ""
        $ texttosend = f"You spent {{color={positiveornegativecolor}}}{plusorminus}${moneyamount}{{/color}}"
        show screen scrollingtextfast(texttosend)

    return


label buyItem(name,cost):
    hide screen scrollingtext
    hide text
    if cost > money:
        hide screen shopinteraction1
        $ renpy.sound.play("/audio/soun_fx/attributeslost.opus", channel="sfxstat", loop=False, relative_volume = 1)
        show screen shopinteraction1("You don't have enough money for that")
        $ ui.interact() #needed to not fuck up after tryint to purchase but not sure why
        
    else:
        hide screen shopinteraction1
        $ money -= cost # remove money
        hide text 
        $ item_name = inventoryShop.find_item_by_name(name) #fetch the name of the corresponding item to add/remove from shop/inventory
        $ inventoryShop.remove_item(item_name, 1)
        $ inventory.add_item(item_name, 1)
        
        $ texttosend = "You purchased: " + name + " for $" + str(cost)
        play sound("/audio/soun_fx/money2.opus")
        show screen shopinteraction1(texttosend)
        $ totalspent += cost
        if quest.exists("shop1_2"):
            if quest.is_state("shop1_2", "in progress") == True:
                if totalspent >= 200:
                    $ notification("Quest updated")
                    $ quest.check("shop1_2", "completed")
                    $ quest.check("shop1_3", "in progress")
                    # Check if shop1_4 is implemented
                    if quest.is_implemented("shop1_4"):
                        # It's implemented, so set it to "in progress".
                        $ quest.check("shop1_4", "in progress")
                    else:
                        # It's a WIP quest, so update its state to "WIP".
                        $ quest.check("shop1_4", "WIP")
        $ ui.interact() #needed to not fuck up after tryint to purchase but not sure why
        # call changeMoney(-cost)
    return

            
label getItem(name, quantity):
    hide screen scrollingtext
    hide text
    $ item_name = inventoryShop.find_item_by_name(name) #fetch the name of the corresponding item to add/remove from shop/inventory
    $ inventory.add_item(name, quantity)
    $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfx3", loop=False, relative_volume = 1)
    $ texttosend = f"You gained {{color=#00ff00}}x{quantity} {name.name}{{/color}}"
    show screen scrollingtext(texttosend)
    return

label useItem(name,quantity):
    hide screen scrollingtext
    hide text
    $ item_name = inventoryShop.find_item_by_name(name) #fetch the name of the corresponding item to add/remove from shop/inventory
    $ inventory.remove_item(name, quantity)
    $ renpy.sound.play("/audio/soun_fx/attributeslost.opus", channel="sfx3", loop=False, relative_volume = 1)
    $ texttosend = f"You used x{quantity} {name.name}"
    show screen scrollingtext(texttosend)
    return


label addSemen(quantity):
    hide screen scrollingtext
    hide text
    $ semenquantity += quantity
    $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfx3", loop=False, relative_volume = 1)
    $ texttosend = f"Tsunade extracts +{{color=#00ff00}}+{quantity} mL of Semen{{/color}}"
    show screen scrollingtext(texttosend)
    return         



label changetsunadedominance(amount): 
    hide screen scrollingtext
    hide text 


    if amount > 0:
        $ tsunadedominance += amount
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ texttosend = f"Tsunade is now a little more{{color={dominancecolor}}} Dominant{{/color}}"
        if tsunadedominance > 100:
            $ tsunadedominance = 100
    else:
        $ tsunadedominance += amount
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ texttosend = f"Tsunade is now a little more{{color={obediencecolor}}} Submissive{{/color}}"
        if tsunadedominance <= -100:
            $ tsunadedominance = -100
    show screen scrollingtext(texttosend)
    return



label checkTsunadedominance(statvalue, jumpvalue=None):
    hide screen scrollingtext
    hide text
    $ missingTsunadedominance = 0

    if statvalue > 0:  # Checking for Dominance
        if tsunadedominance >= statvalue:  # Success check
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            $ texttosend = f"Tsunade is {{color={dominancecolor}}}Dominant ({statvalue}){{/color}} enough"
            show screen scrollingtext(texttosend)
            return    
        else:  # Failed check
            $ missingTsunadedominance = statvalue - tsunadedominance
            $ jumpdestination = jumpvalue
            play sound("/audio/soun_fx/attributeslost.opus")
            $ texttosend = f"Tsunade is not {{color={dominancecolor}}}Dominant ({statvalue}){{/color}} enough"
            show screen scrollingtext(texttosend)
            "Tsunade needs [missingTsunadedominance] more points of {color=[dominancecolor]}Dominance{/color}"
            if jumpvalue != None:
                jump expression jumpdestination
            elif jumpvalue == "pass":
                return
            else:
                return

    elif statvalue < 0:  # Checking for Submission
        if tsunadedominance <= statvalue:  # Success check
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            $ texttosend = f"Tsunade is {{color={obediencecolor}}}Submissive ({statvalue}){{/color}} enough"
            show screen scrollingtext(texttosend)
            return    
        else:  # Failed check
            $ missingTsunadedominance = abs(statvalue - tsunadedominance)
            $ jumpdestination = jumpvalue
            play sound("/audio/soun_fx/attributeslost.opus")
            $ texttosend = f"Tsunade is not {{color={obediencecolor}}}Submissive ({statvalue}){{/color}} enough"
            show screen scrollingtext(texttosend)
            "Tsunade needs [missingTsunadedominance] more points of {color=[obediencecolor]}Submission{/color}"
            if jumpvalue != None:
                jump expression jumpdestination
            elif jumpvalue == "pass":
                return
            else:
                return


label changesakura(amount): 
    hide screen scrollingtext
    hide text 

    if amount > 0:
        $ sakura_relationship += amount
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ texttosend = f"Your relationship with {{color=#ffb7c5}}Sakura{{/color}} has{{color=#00ff00}} improved (+{amount}){{/color}}"
        if sakura_relationship > 75:
            $ sakura_relationship = 75
    else:
        $ sakura_relationship += amount
        $ renpy.sound.play("/audio/soun_fx/attributeslost.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ texttosend = f"Your relationship with {{color=#ffb7c5}}Sakura{{/color}} has{{color=#FF0000}} weakened ({amount}){{/color}}"
        if sakura_relationship <=0:
            $ sakura_relationship = 0
    show screen scrollingtext(texttosend)
    return

label checkSakura(statvalue, jumpvalue=None):
    hide screen scrollingtext
    hide text
    $ missingSakura = 0

    if statvalue > 0:  # Checking for Dominance
        if sakura_relationship >= statvalue:  # Success check
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            $ texttosend = f"Relationship check passed ({statvalue})"
            show screen scrollingtext(texttosend)
            return    
        else:  # Failed check
            $ missingSakura = statvalue - sakura_relationship
            $ jumpdestination = jumpvalue
            play sound("/audio/soun_fx/attributeslost.opus")
            $ texttosend = f"Relationship check failed ({statvalue})"
            show screen scrollingtext(texttosend)
            "Sakura's relationship needs [missingSakura] more points..."
            if jumpvalue != None:
                jump expression jumpdestination
            elif jumpvalue == "pass":
                return
            else:
                return


label changesarada(amount): 
    hide screen scrollingtext
    hide text 

    if amount > 0:
        $ sarada_relationship += amount
        $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ texttosend = f"Your relationship with {{color=#D22B2B}}Sarada{{/color}} has{{color=#00ff00}} improved (+{amount}){{/color}}"
        if sarada_relationship > 50:
            $ sarada_relationship = 50
    else:
        $ sarada_relationship += amount
        $ renpy.sound.play("/audio/soun_fx/attributeslost.opus", channel="sfxstat", loop=False, relative_volume = 1)
        $ texttosend = f"Your relationship with {{color=#D22B2B}}Sarada{{/color}} has{{color=#FF0000}} weakened ({amount}){{/color}}"
        if sarada_relationship >=0:
            $ sarada_relationship = 0
    show screen scrollingtext(texttosend)
    return

label checkSarada(statvalue, jumpvalue=None):
    hide screen scrollingtext
    hide text
    $ missingSarada = 0

    if statvalue > 0:  
        if sarada_relationship >= statvalue:  # Success check
            $ renpy.sound.play("/audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume = 1)
            $ texttosend = f"Relationship check passed ({statvalue})"
            show screen scrollingtext(texttosend)
            return    
        else:  # Failed check
            $ missingSarada = statvalue - sarada_relationship
            $ jumpdestination = jumpvalue
            play sound("/audio/soun_fx/attributeslost.opus")
            $ texttosend = f"Relationship check failed ({statvalue})"
            show screen scrollingtext(texttosend)
            "Sarada's relationship needs [missingSarada] more points..."
            if jumpvalue != None:
                jump expression jumpdestination
            elif jumpvalue == "pass":
                return
            else:
                return



init python:
    class CenterBar(renpy.Displayable):
        def __init__(self, width, height, value, **kwargs):
            super(CenterBar, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.value = value
            
        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)
            
            # Create the background first
            bg = renpy.Render(self.width, self.height)
            bg.fill("#444444")  # Dark gray background
            render.blit(bg, (0, 0))  # Blit background first
            
            # Calculate the center position
            center = self.width // 2
            
            # Create the foreground bars
            if self.value >= 0:
                # Right side (positive values)
                bar_width = int((self.value / 100.0) * (self.width / 2))
                if bar_width > 0:  # Only create bar if there's a positive width
                    bar = renpy.Render(bar_width, self.height)
                    bar.fill("#FF6666")  # Green for positive
                    render.blit(bar, (center, 0))
            else:
                # Left side (negative values)
                bar_width = int((-self.value / 100.0) * (self.width / 2))
                if bar_width > 0:  # Only create bar if there's a positive width
                    bar = renpy.Render(bar_width, self.height)
                    bar.fill("#a16cc4")  # Red for negative
                    render.blit(bar, (center - bar_width, 0))
            
            # Add a center line marker
            center_line = renpy.Render(2, self.height)  # 2 pixels wide
            center_line.fill("#ffffff")  # White center line
            render.blit(center_line, (center - 1, 0))
            
            return render
        
        def event(self, ev, x, y, st):
            return None
        
        def visit(self):
            return []


    def is_opportunity_unlocked(opportunity_id, current_strength):
        # Dictionary mapping opportunity IDs to (required_strength_level, required_cost)
        renpy.hide_screen('scrollingtext')

        opportunity_requirements = {
            # Level 0 opportunities
            "l0_opportunity1": (0, 20),
            "l0_opportunity2": (0, 50),
            "l0_opportunity3": (0, 100),
            # Level 1 opportunities
            "l1_opportunity1": (1, 20),
            "l1_opportunity2": (1, 50),
            "l1_opportunity3": (1, 80),
            "l1_opportunity4": (1, 100),
            # Level 2 opportunities
            "l2_opportunity1": (2, 20),
            "l2_opportunity2": (2, 50),
            "l2_opportunity3": (2, 100)
        }
        
        # Get the requirements for this opportunity
        requirements = opportunity_requirements.get(opportunity_id)
        
        # If opportunity exists in our mapping, check if it's unlocked
        if requirements is not None:
            required_level, required_cost = requirements
            
            # If strength is higher than required, automatic success
            if current_strength > required_level:
                is_unlocked = True
            # If strength equals required level, check cost
            elif current_strength == required_level:
                is_unlocked = strengthlevel >= required_cost
            # If strength is lower than required, fail
            else:
                is_unlocked = False
            
            if is_unlocked:
                renpy.sound.play("audio/soun_fx/attributes.opus", channel="sfxstat", loop=False, relative_volume=1)
                texttosend = f"Strength {{color=#00ff00}}Opportunity!{{/color}}"
                renpy.show_screen('scrollingtext', texttosend)
                store.opportunity_tofail = "none"
                return True
            else:
                renpy.sound.play("audio/soun_fx/attributeslost.opus", channel="sfxstat")
                texttosend = f"Strength check {{color=#FF0000}}failed{{/color}}"
                renpy.show_screen('scrollingtext', texttosend)
                store.opportunity_tofail = opportunity_id
                return False
        
        # If opportunity_id wasn't found in the dictionary
        renpy.sound.play("audio/soun_fx/attributeslost.opus", channel="sfxstat")
        texttosend = f"Strength check {{color=#FF0000}}failed{{/color}}"
        renpy.show_screen('scrollingtext', texttosend)
        return False

   

# Example screen using the center bar
screen center_balance_bar:
    frame:
        xalign 0.5
        yalign 0.5
        background None  # Removes the background
        padding (0,0)    # Removes the padding
        vbox:
            spacing 10
            text "Tsunade's Demeanor: [tsunadedominance]" xalign 0.5
            $ demeanor_text = ""
            $ text_color = "#ffffff"  # default white
            if tsunadedominance <= -75:
                $ demeanor_text = "Extremely Submissive"
                $ text_color = "#a16cc4"
            elif tsunadedominance <= -50:
                $ demeanor_text = "Very Submissive"
                $ text_color = "#a16cc4"
            elif tsunadedominance <= -25:
                $ demeanor_text = "Somewhat Submissive"
                $ text_color = "#a16cc4"
            elif tsunadedominance <= -10:
                $ demeanor_text = "Slightly Submissive"
                $ text_color = "#a16cc4"
            elif tsunadedominance < 10:
                $ demeanor_text = "Neutral"
                $ text_color = "#ffffff"
            elif tsunadedominance < 25:
                $ demeanor_text = "Slightly Dominant"
                $ text_color = "#FF6666"
            elif tsunadedominance < 50:
                $ demeanor_text = "Somewhat Dominant"
                $ text_color = "#FF6666"
            elif tsunadedominance < 75:
                $ demeanor_text = "Very Dominant"
                $ text_color = "#FF6666"
            else:
                $ demeanor_text = "Extremely Dominant"
                $ text_color = "#FF6666"
            text "[demeanor_text]" xalign 0.5 color text_color
            fixed:
                xsize 400
                ysize 30
                add CenterBar(400, 30, tsunadedominance)


