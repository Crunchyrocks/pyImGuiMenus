import imgui
import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer
import os
import json
import webbrowser
import numpy as np

def impl_glfw_init(window_name="Mod Menu Example 1", width=1280, height=720):
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)
    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)
    return window

class GUI(object):
    def __init__(self):
        super().__init__()
        self.backgroundColor = (0, 0, 0, 1)
        self.window = impl_glfw_init()
        gl.glClearColor(*self.backgroundColor)
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)
        self.num_settings_areas = 10
        self.rendering = True
        self.menu_collapsed = False 
        self.current_tab_index = 0  
        self.tabs = ["Main", "ESP" ,"Fun", "Zombies"]
        self.tab_settings = {
            "Main": {},
            "ESP": {},
            "Fun": {},
            "Zombies": {}
        }


        self.exit_requested = False
        
        self.loop()



    def loop(self):
        while not self.exit_requested:
            while self.rendering:
                glfw.poll_events()
                self.impl.process_inputs()
                imgui.new_frame()
                
                self.draw_menu()

                imgui.render()

                gl.glClearColor(*self.backgroundColor)
                gl.glClear(gl.GL_COLOR_BUFFER_BIT)

                self.impl.render(imgui.get_draw_data())
                glfw.swap_buffers(self.window)
                
        
                if imgui.is_key_pressed(imgui.KEY_RIGHT_ARROW):
                    self.current_tab_index = (self.current_tab_index + 1) % len(self.tabs)
                elif imgui.is_key_pressed(imgui.KEY_LEFT_ARROW):
                    self.current_tab_index = (self.current_tab_index - 1) % len(self.tabs)
                    
            pass

        self.impl.shutdown()
        glfw.terminate()


    def draw_menu(self):
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (0, 10))
        imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (25, 10))

        if imgui.begin("Menu - Demo 2"):
            for i, tab in enumerate(self.tabs):
                if i > 0:
                    imgui.same_line()
                if self.current_tab_index == i:
                    imgui.push_style_color(imgui.COLOR_BUTTON, 0.3, 0.4, 0.8, 1.0)  
                else:
                    imgui.push_style_color(imgui.COLOR_BUTTON, 0.10, 0.3, 0.5, 1)  

                if imgui.button(tab, width=150):
                    self.current_tab_index = i

                imgui.pop_style_color()  

    
            if self.current_tab_index == 0:
                self.draw_main_tab()
            elif self.current_tab_index == 1:
                self.draw_esp_tab()
            elif self.current_tab_index == 2:
                self.draw_fun_tab()
            elif self.current_tab_index == 3:
                self.draw_zombies_tab()

            imgui.end()

        imgui.pop_style_var(2)




    def draw_tab_content(self, tab_title):
        if tab_title == "Aim":
            self.draw_aim_tab()
        elif tab_title == "Visuals":
            self.draw_esp_tab()
        elif tab_title == "Misc":
            self.draw_misc_tab()
        elif tab_title == "Zombies": 
            self.draw_zombies_tab()
    

    def draw_main_tab(self):
        link_text = 'https://randomlink'
        imgui.text_colored(link_text, 0, 100, 255)
        imgui.separator()
         
        _, self.tab_settings["Main"]["Doyoulike"] = imgui.checkbox("Do you like it?", self.tab_settings["Main"].get("Doyoulike", False))
        _, self.tab_settings["Main"]["magicbullet"] = imgui.checkbox("Magic Bullet", self.tab_settings["Main"].get("magicbullet", False))
        _, self.tab_settings["Main"]["aimbot"] = imgui.checkbox("Aimbot", self.tab_settings["Main"].get("aimbot", False))    
        _, self.tab_settings["Main"]["antiaim"] = imgui.checkbox("Anti Aim", self.tab_settings["Main"].get("antiaim", False))
        _, self.tab_settings["Main"]["doubledamage"] = imgui.checkbox("Double Damage", self.tab_settings["Main"].get("doubledamage", False))
        _, self.tab_settings["Main"]["reverrelaod"] = imgui.checkbox("Never Reload", self.tab_settings["Main"].get("reverrelaod", False))
        _, self.tab_settings["Main"]["unlimtedammo"] = imgui.checkbox("Unlimted Ammo", self.tab_settings["Main"].get("unlimtedammo", False))
        _, self.tab_settings["Main"]["rapidfire"] = imgui.checkbox("Rapid Fire", self.tab_settings["Main"].get("rapidfire", False))

       
        
        
    def draw_esp_tab(self):
        link_text = 'https://randomlink'
        imgui.text_colored(link_text, 0, 100, 255)
        imgui.separator()
         
        _, self.tab_settings["ESP"]["showbox"] = imgui.checkbox("Show Player Box", self.tab_settings["ESP"].get("showbox", False))
        _, self.tab_settings["ESP"]["showbones"] = imgui.checkbox("Show Player Bones", self.tab_settings["ESP"].get("showbones", False))
        _, self.tab_settings["ESP"]["esp_range"] = imgui.slider_float("ESP Range", self.tab_settings["ESP"].get("esp_range", 100.0), min_value=1.0, max_value=1000.0, format="%.1f", power=1.0)
        _, self.tab_settings["ESP"]["showdist"] = imgui.checkbox("Show Player Distance", self.tab_settings["ESP"].get("showdist", False))
        _, self.tab_settings["ESP"]["showhealth"] = imgui.checkbox("Show Player Health", self.tab_settings["ESP"].get("showhealth", False))
        _, self.tab_settings["ESP"]["gunoutline"] = imgui.checkbox("Gun Outline", self.tab_settings["ESP"].get("gunoutline", False))



    def draw_fun_tab(self):
        link_text = 'https://randomlink'
        imgui.text_colored(link_text, 0, 100, 255)
        imgui.separator()
         
        _, self.tab_settings["Fun"]["superslide"] = imgui.checkbox("Super Slide", self.tab_settings["Fun"].get("superslide", False))
        _, self.tab_settings["Fun"]["unlockall"] = imgui.checkbox("Unlock All", self.tab_settings["Fun"].get("unlockall", False))
        _, self.tab_settings["Fun"]["unlimiteduav"] = imgui.checkbox("Unlimited UAV", self.tab_settings["Fun"].get("unlimiteduav", False))


        imgui.text("Give player gun:")
        gun_options = [ "Bowie-Knife" , "M4A1", "Scar-H", "1911", "RPK" ,"RPG",  "RayGun"]

        _, self.tab_settings["Fun"]["selected_gun"] = imgui.combo("", self.tab_settings["Fun"].get("selected_gun", 0), gun_options)
        imgui.spacing()
        imgui.same_line()
        if imgui.button("Confirm"):
            current_selection = gun_options[self.tab_settings["Fun"].get("selected_gun", 0)]
            print(f"Selected Gun: {current_selection}")

    def draw_zombies_tab(self):
        link_text = 'https://randomlink'
        imgui.text_colored(link_text, 0, 100, 255)
        imgui.separator()
         
        _, self.tab_settings["Main"]["godmode"] = imgui.checkbox("God Mode", self.tab_settings["Main"].get("godmode", False))
        _, self.tab_settings["Main"]["flying"] = imgui.checkbox("Flying", self.tab_settings["Main"].get("flying", False))

        imgui.separator()
        
        _, self.tab_settings["ESP"]["showzombox"] = imgui.checkbox("Show Zombie Box", self.tab_settings["ESP"].get("showzombox", False))
        _, self.tab_settings["ESP"]["showzombones"] = imgui.checkbox("Show Zombie Bones", self.tab_settings["ESP"].get("showzombones", False))
        _, self.tab_settings["ESP"]["showzomhealth"] = imgui.checkbox("Show Zombie Health", self.tab_settings["ESP"].get("showzomhealth", False))
        _, self.tab_settings["ESP"]["outlinembox"] = imgui.checkbox("Outline Mystery Box", self.tab_settings["ESP"].get("outlinembox", False))

        imgui.separator()
         
        _, self.tab_settings["Fun"]["lockbox"] = imgui.checkbox("Lock Box", self.tab_settings["Fun"].get("lockbox", False))
        _, self.tab_settings["Fun"]["spawnnuke"] = imgui.checkbox("Shoot Nukes", self.tab_settings["Fun"].get("spawnnuke", False))
        _, self.tab_settings["Fun"]["spawnmax"] = imgui.checkbox("Shoot Max Ammo", self.tab_settings["Fun"].get("spawnmax", False))
        _, self.tab_settings["Fun"]["spawninstakill"] = imgui.checkbox("Shoot Instant Kill", self.tab_settings["Fun"].get("spawninstakill", False))

    

if __name__ == "__main__":
    gui = GUI()
    gui.request_exit()
