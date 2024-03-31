import imgui
import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer
import os
import json

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
        self.tabs = ["Aim", "Visuals", "Misc", "Configs"]
        self.tab_settings = {
            "Aim": {
                "enable": False,
                "aim_accel_value": 90,
                "aim_key_index": 0,
                "aim_key_index2": 0,
                "silent_aim_enabled": False,
                "fov_aim_enabled": False,
                "slider_value": 90,
                "norecoil_aim_enabled": False,
                "nospread_aim_enabled": False,
                "aim_bone_index": 0,
                "aimallies_aim_enabled": False,
                "ignorebot_aim_enabled": False,
                "ignordowned_aim_enabled": False
            },
            "Visuals": {},
            "Misc": {},
            "Configs": {}
        }

        # Load settings for all configuration areas
        self.load_settings()

        # Initialize exit_requested attribute
        self.exit_requested = False
        
        self.loop()

    def save_settings(self, index):
        filename = f"Settings_{index + 1}.json"
        settings = self.tab_settings["Configs"].get(f"Settings {index + 1}", {})
        try:
            with open(filename, 'w') as file:
                # Iterate over each setting and include it in the settings dictionary
                for key, value in self.tab_settings.items():
                    if key == "Configs":
                        continue  # Skip the "Configs" key
                    settings[key] = value
                json.dump(settings, file, indent=4)
                print(f"Settings saved to {filename}: {settings}")
        except Exception as e:
            print(f"Error saving settings to {filename}: {e}")


    def load_settings(self):
        try:
            with open("Settings_1.json", "r") as file:
                settings = json.load(file)
                print("Settings loaded from Settings_1.json:", settings)
            
                # Update UI elements with loaded settings
                for key, value in settings.items():
                    if key in self.tab_settings:
                        for sub_key, sub_value in value.items():
                            if sub_key in self.tab_settings[key]:
                                self.tab_settings[key][sub_key] = sub_value
        except FileNotFoundError:
            print("No settings file found: Settings_1.json")
            # Handle the case when the settings file is not found


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
            pass

        self.impl.shutdown()
        glfw.terminate()


    def draw_menu(self):
        imgui.set_next_window_size(360, 508)

        
        if imgui.begin("Menu - Demo", not self.menu_collapsed):

          
            for i, tab in enumerate(self.tabs):
                if i > 0:
                    imgui.same_line()
                if imgui.button(tab, 80, 20):
                    print(f"{tab} button clicked")
                    self.current_tab_index = i  

           
            imgui.spacing()
            imgui.separator()

        
            self.draw_tab_content(self.tabs[self.current_tab_index])

        imgui.end()

    def draw_tab_content(self, tab_title):
        if tab_title == "Aim":
            self.draw_aim_tab()
        elif tab_title == "Visuals":
            self.draw_visuals_tab()
        elif tab_title == "Misc":
            self.draw_misc_tab()
        elif tab_title == "Configs":
            self.draw_configs_tab()

    def draw_aim_tab(self):
        imgui.text("AimBot:")
        _, self.tab_settings["Aim"]["enable"] = imgui.checkbox("Enable Aim", self.tab_settings["Aim"]["enable"])
        _, self.tab_settings["Aim"]["aim_accel_value"] = imgui.slider_int("Strength", self.tab_settings["Aim"]["aim_accel_value"], 1, 100)


        # Aim key 1
        aim_key_options = ["Right Click", "Left Click", "Shift", "Custom"]
        _, self.tab_settings["Aim"]["aim_key_index"] = imgui.combo("##aim_key_combo1", self.tab_settings["Aim"]["aim_key_index"], aim_key_options)
        imgui.same_line()
        imgui.text("Aim Key 1")

        # Aim key 2
        _, self.tab_settings["Aim"]["aim_key_index2"] = imgui.combo("##aim_key_combo2", self.tab_settings["Aim"]["aim_key_index2"], aim_key_options)
        imgui.same_line()
        imgui.text("Aim Key 2")

        imgui.spacing()
        imgui.separator()
        imgui.spacing()

        
        imgui.text("Aim Settings:")
        _, self.tab_settings["Aim"]["silent_aim_enabled"] = imgui.checkbox("Silent Aim", self.tab_settings["Aim"]["silent_aim_enabled"])
        _, self.tab_settings["Aim"]["fov_aim_enabled"] = imgui.checkbox("Show Fov", self.tab_settings["Aim"]["fov_aim_enabled"])
        _, self.tab_settings["Aim"]["slider_value"] = imgui.slider_int("Fov Slider", self.tab_settings["Aim"]["slider_value"], 1, 180)
        _, self.tab_settings["Aim"]["norecoil_aim_enabled"] = imgui.checkbox("No Recoil", self.tab_settings["Aim"]["norecoil_aim_enabled"])
        _, self.tab_settings["Aim"]["nospread_aim_enabled"] = imgui.checkbox("No Spread", self.tab_settings["Aim"]["nospread_aim_enabled"])

        imgui.separator()
        imgui.spacing()


        imgui.text("Target Options:")
        aimbone_key_options = ["Head", "Neck", "Chest", "Body", "Random"]
        _, self.tab_settings["Aim"]["aim_bone_index"] = imgui.combo("##aim_bone_combo", self.tab_settings["Aim"]["aim_bone_index"], aimbone_key_options)
        _, self.tab_settings["Aim"]["aimallies_aim_enabled"] = imgui.checkbox("Target Allies", self.tab_settings["Aim"]["aimallies_aim_enabled"])
        _, self.tab_settings["Aim"]["ignorebot_aim_enabled"] = imgui.checkbox("Ignore Bots", self.tab_settings["Aim"]["ignorebot_aim_enabled"])
        _, self.tab_settings["Aim"]["ignordowned_aim_enabled"] = imgui.checkbox("Ignore Downed Players", self.tab_settings["Aim"]["ignordowned_aim_enabled"])
        imgui.spacing()

    def draw_visuals_tab(self):
        _, self.tab_settings["Visuals"]["enable"] = imgui.checkbox("Enable ESP", self.tab_settings["Visuals"].get("enable", False))
        imgui.spacing()
        imgui.separator()
        imgui.text("Player ESP:")
        imgui.spacing()
        _, self.tab_settings["Visuals"]["espline_enabled"] = imgui.checkbox("Esp Line", self.tab_settings["Visuals"].get("espline_enabled", False))
        _, self.tab_settings["Visuals"]["espbox_enabled"] = imgui.checkbox("Esp Box", self.tab_settings["Visuals"].get("espbox_enabled", False))
        _, self.tab_settings["Visuals"]["showname_enabled"] = imgui.checkbox("Show Name", self.tab_settings["Visuals"].get("showname_enabled", False))
        _, self.tab_settings["Visuals"]["showgun_enabled"] = imgui.checkbox("Show Gun", self.tab_settings["Visuals"].get("showgun_enabled", False))
        _, self.tab_settings["Visuals"]["showhealth_enabled"] = imgui.checkbox("Show Health", self.tab_settings["Visuals"].get("showhealth_enabled", False))
        _, self.tab_settings["Visuals"]["showdist_enabled"] = imgui.checkbox("Show Distance", self.tab_settings["Visuals"].get("showdist_enabled", False))
        _, self.tab_settings["Visuals"]["playerwarn_enabled"] = imgui.checkbox("Player warnings", self.tab_settings["Visuals"].get("playerwarn_enabled", False))

        imgui.separator()
        imgui.spacing()

        imgui.text("Loot ESP:")
        imgui.spacing()
        
        _, self.tab_settings["Visuals"]["showcash_enabled"] = imgui.checkbox("Show Money", self.tab_settings["Visuals"].get("showcash_enabled", False))
        _, self.tab_settings["Visuals"]["showguns_enabled"] = imgui.checkbox("Show Guns", self.tab_settings["Visuals"].get("showguns_enabled", False))
        _, self.tab_settings["Visuals"]["showchest_enabled"] = imgui.checkbox("Show Chest", self.tab_settings["Visuals"].get("showchest_enabled", False))
        _, self.tab_settings["Visuals"]["showleth_enabled"] = imgui.checkbox("Show Lethals", self.tab_settings["Visuals"].get("showleth_enabled", False))
        _, self.tab_settings["Visuals"]["showlootdist_enabled"] = imgui.checkbox("Show Loot Distance", self.tab_settings["Visuals"].get("showlootdist_enabled", False))


        

    def draw_misc_tab(self):
        imgui.text("Misc:")
        imgui.spacing()
        _, self.tab_settings["Misc"]["super_speed_enabled"] = imgui.checkbox("Super Speed", self.tab_settings["Misc"].get("super_speed_enabled", False))
        _, self.tab_settings["Misc"]["unlockall_enabled"] = imgui.checkbox("Unlock All", self.tab_settings["Misc"].get("unlockall_enabled", False))
        _, self.tab_settings["Misc"]["superslide_enabled"] = imgui.checkbox("Super Slide", self.tab_settings["Misc"].get("superslide_enabled", False))


    def draw_configs_tab(self):
        for i in range(self.num_settings_areas):
            imgui.push_item_width(175)
            imgui.text(f"Settings {i + 1}")
            imgui.pop_item_width()
            imgui.same_line()
        
            if imgui.button(f"Save##{i + 1}"):
                self.save_settings(i)
        
            imgui.same_line()

            if imgui.button(f"Load##{i + 1}"):
                self.load_settings()


if __name__ == "__main__":
    gui = GUI()
    gui.request_exit()
