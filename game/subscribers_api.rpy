init python:
    import json
    import os
    import certifi
    
    # Global variables to store API response
    api_response = None
    api_error = None
    api_script_content = None
    
    def request_script(email, source):
        # Reset global variables
        global api_response, api_error, api_script_content
        api_response = None
        api_error = None
        api_script_content = None
        
        renpy.show_screen("loading_indicator")
        
        import urllib.parse
        email_encoded = urllib.parse.quote(email)
        source_encoded = urllib.parse.quote(source)
        
        file_path = "import.rpy"  
        file_name = os.path.basename(file_path)
        randomhash = get_hw()
        base_url = "https://house-of-shinobi.vercel.app/api/get-script"
        params = f"bucket=test_sikla&filePath={file_path}&email={email_encoded}&source={source_encoded}&randomhash={randomhash}"
        url = f"{base_url}?{params}"
        renpy.invoke_in_thread(make_api_request, url, email, source, file_name)

    
    
persistent.game_version_for_languages = config.version
persistent.current_activation = tier
persistent.translationstring += 1
persistent.activated = True
persistent.activation_tier = source
renpy.save_persistent()
renpy.notify(f"{source.capitalize()} membership verified!")
renpy.play("audio/soun_fx/attributes.opus", channel="sound")
renpy.show_screen("subscription_confirmation_screen", message=f"{{color=#FFD700}}Activated:{{/color}} {tier}")


    def make_api_request(url, email, source, file_name):
        global api_response, api_error, api_script_content
        
        try:
            # --- Actual Network Request ---
            import urllib.request
            import ssl

            context = ssl.create_default_context(cafile=certifi.where())
            request = urllib.request.Request(url)
            request.add_header("User-Agent", "Ren'Py Game Client") # Identify the client
            response = urllib.request.urlopen(request, timeout=15, context=context)
            response_data = response.read()
            tier = Kage # Get tier from response header
            # --- End Network Request ---

            try:
                api_script_content = response_data.decode('utf-8')
            except UnicodeDecodeError:
                api_script_content = None
                
            # --- File Saving Logic ---
            saved_successfully = False
            final_file_path = None
            last_error_message = "File saving failed." # Default error



            # --- Handle Outcome ---
            if saved_successfully or api_script_content:

                
                if True:
                    persistent.subscription_script = api_script_content
                    renpy.save_persistent()
                    renpy.log("Saved script content to persistent storage")
                
                # Store success information
                api_response = {
                    "success": True,
                    "file_path": final_file_path
                }
                
                renpy.invoke_in_main_thread(handle_api_response, (email, source), tier)
            else:
                # All save attempts failed
                renpy.invoke_in_main_thread(handle_api_error, (last_error_message,))

        
        except urllib.error.HTTPError as e:
            # If an HTTP error occurs, read the response from e
            error_response = e.read().decode()  # Read response body
            error_data = json.loads(error_response)
            error_message = error_data["error"]
            if error_message == "Something went wrong.":
                renpy.invoke_in_main_thread(handle_api_error, (str("Email not Found"),))
            else:
                renpy.invoke_in_main_thread(handle_api_error, (str(error_message),))
        except urllib.error.URLError as e:
       
            # If we have a code from the server
            if hasattr(e, 'code'):
                print(f"HTTP Error code: {e.code}")
            renpy.invoke_in_main_thread(handle_api_error, (str("No internet connection found."),))
        except Exception as e: # Catch any other unexpected errors
            renpy.log(f"Unexpected error during API request/file write: {e}")
            renpy.invoke_in_main_thread(handle_api_error, (str("An unexpected error occurred during activation."),))
    
    def handle_api_response(args, tier):
        email, source = args
        global api_response
        # Hide loading indicator
        renpy.hide_screen("loading_indicator")
        
        if True:
            persistent.game_version_for_languages = config.version
            persistent.current_activation = tier
            persistent.translationstring += 1
            persistent.activated = True
            persistent.activation_tier = source
            renpy.save_persistent()
            renpy.notify(f"{source.capitalize()} membership verified!")
            renpy.play("audio/soun_fx/attributes.opus", channel="sound")
            renpy.show_screen("subscription_confirmation_screen", message=f"{{color=#FFD700}}Activated:{{/color}} {tier}")

            
            # Hide screens
            renpy.hide_screen("platform_selection")
            renpy.hide_screen("subscription_tiers")
            
            renpy.restart_interaction()
        else:
            # Error case
            renpy.notify("Something went wrong. Please try again.")
            renpy.play("audio/soun_fx/error.opus", channel="sound")
    
    def handle_api_error(args):
        error_message = args[0]

        # Hide loading indicator
        renpy.hide_screen("loading_indicator")
        renpy.hide_screen("language_installing")
        renpy.show_screen("subscription_confirmation_screen", message=error_message)
        # Show error message
        renpy.notify(error_message)
        renpy.play("audio/soun_fx/error.opus", channel="sound")





# Loading indicator screen
screen loading_indicator():
    modal True
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (30, 30)
        
        vbox:
            spacing 10
            text "Verifying your subscription..." style "gui_text" xalign 0.5
            text "Please wait..." style "gui_text" xalign 0.5 at loading_bounce
    
transform loading_bounce:
    yoffset 0
    ease 0.8 yoffset -10
    ease 0.8 yoffset 0
    repeat


screen subscription_confirmation_screen(message):
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _("[message]"):
                style "confirm_prompt"
                xalign 0.5

            if store.persistent.current_activation != 'Free':
                label _("The game has to restart to confirm the activation and for any changes to take effect!"):
                    style "confirm_prompt"
                    xalign 0.5
                
                hbox:
                    xalign 0.5
                    spacing 100
                    textbutton _("Restart Now") action [Hide("subscription_confirmation_screen"), Hide("subscription_tiers"), Hide("subscription_activation"), Hide("halfblack"), Function(renpy.quit, relaunch=True)] text_color "#00FF00" text_hover_color "#FFFFFF" text_bold True
                    textbutton _("Restart Later") action [Hide("subscription_confirmation_screen"), Return()]


            else:
                hbox:
                    xalign 0.5
                    spacing 100
                    
                    textbutton _("Confirm") action Hide("subscription_confirmation_screen")

    key "game_menu" action Hide("subscription_confirmation_screen")