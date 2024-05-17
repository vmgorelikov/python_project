import engine
import pygame
import json
import marshal

def swixtch(state,task_name):
    print("S")
    if state["progress"][task_name]["available"]:
        state["current_task"] = task_name
        state["SWITCH"] = task_name[:-1]
    return state

def slide_switch(state,slide_no,x=21):
    engine.global_offset[0] = 800*(slide_no-1)
    state["village"]["slide_no"] = slide_no
    state["village"]["scene"].pos = (engine.global_offset[0],0)
    state["village"]["scene"].current_sprite = "slide" + str(slide_no)
    state["village"]["entities"]["player"].pos = \
    ((slide_no-1)*800+x,\
    state["village"]["entities"]["player"].pos[1])
    return state

def trigger_name(state,text):
    print(text)
    return state

class House():
    def __init__(self,name,dweller,dialogues:list=[],task=""):
        self.name = name
        self.dweller = dweller
        self.dialogues = dialogues
        self.task = task
        self.dialogue_line = 0
        self.note = int(name[-1:])
        #self.dweller.pos = (self.trigger.pos[0]+self.trigger.size[0]-40,self.trigger.pos[1]+self.trigger.size[1])
    def sequence(self,state):
        state["village"]["triggers"][self.name].fired = False
        if not state["progress"][self.name]["visited"]:
            if not self.name in state["village"]["texts"]:
                state["village"]["texts"][self.name] = engine.Text(((state["village"]["slide_no"]-1)*800+300,300),width=300,colour="BLACK",box_colour=(208, 176, 132, 255))
            print(self.name)
            state["village"]["entities"]["player"].current_sprite = "back"
            state["village"]["entities"]["dweller"+str(self.note)] = self.dweller
            if self.dialogue_line < len(self.dialogues):
                state["village"]["halt_player"] = True
                state["village"]["texts"][self.name].text = self.dialogues[self.dialogue_line]
                self.dialogue_line += 1
            else:
                state["progress"][self.name]["visited"] = True
                state["progress"][self.task]["available"] = True
                state["village"]["halt_player"] = False
                del state["village"]["entities"]["dweller"+str(self.note)]
                del state["village"]["texts"][self.name]
        elif state["progress"][self.task]["completed"]:
            state["village"]["triggers"][self.name].fired = True
            state["progress"]["notes"][self.note] = True
            print(self.note)
            
        return state
    def render(self,screen):
        pass
    
def village(state):
    if not state["initialised"]:
        state["village"] = dict()
        state["hchchc"] = 0
        state["twetwet"] = 1
        state["village"]["entities"] = dict()
        state["village"]["triggers"] = dict()
        state["village"]["texts"] = dict()
        state["village"]["halt_player"] = False
        state["village"]["entities"]["player"] = engine.GameEntity((57,442),(32,120),
                                    {"default": "images/player_left.png",
                                    "left2": "images/player_left2.png",
                                    "right": "images/player_right.png",
                                    "right2": "images/player_right2.png",
                                    "front": "images/player_front.png",
                                    "back":"images/player_back.png"
                                    })
        state["village"]["scene"] = engine.Scene(size=(800,600),sprite_named_filenames=\
                                    {"slide1": "images/slide1.jpg",
                                     "slide2": "images/slide2.jpg",
                                     "slide3": "images/slide3.jpg",
                                     "slide4": "images/slide4.jpg",
                                     "slide5": "images/slide5.jpg",
                                     "slide6": "images/slide6.jpg",
                                     "slide7": "images/slide7.png",
                                     "slide8": "images/slide8.png",
                                     "slide9": "images/slide9.png",
                                     "slide10": "images/slide10.png",
                                     "slide11": "images/slide11.png",
                                     "slide12": "images/slide12.png",
                                     "slide13": "images/slide13.jpg",
                                     "slide14": "images/slide14.jpg",
                                     "slide15": "images/slide15.jpg",
                                     "swamp": "images/swamp.jpg",
                                     "izbushka": "images/izbushka.jpg",
                                     "ovrag": "images/ovrag.jpg"
                                     })

        coords_list = json.loads(open("coordinates.json","r",encoding="utf-8").read())
        for coords in coords_list:
            pos = (coords_list[coords][0],coords_list[coords][1])
            size = (coords_list[coords][2],coords_list[coords][3])
            if coords[:2] == "ho":
                state["village"]["entities"][coords] = House(coords,\
                    engine.GameEntity((pos[0]+size[0]-30,pos[1]+size[1]-90),\
                    (32,120),{"asdasd":"images/dweller" + coords[-1:] + ".png"}),
                    coords_list[coords][5],coords_list[coords][6])
                state["village"]["triggers"][coords] = engine.Trigger(pos, size,\
                func=state["village"]["entities"][coords].sequence,type={"collides","key"},\
                sprite_named_filenames={"default":"images/trigger.png"},cooldown=120)
            elif coords[:2] == "fo":
                state["village"]["triggers"][coords] = engine.Trigger(pos, size,\
                func=slide_switch,default_params=[int(coords[-1:])+6,400],type={"collides","key"},\
                sprite_named_filenames={"default":"images/trigger.png"})
            elif coords[:2] == "og" or coords[:2] == "hi":
                state["village"]["triggers"][coords] = engine.Trigger(pos, size,{"default":"images/trigger.png"},
                                type={"collides","key"}, func=swixtch,default_params=[coords_list[coords][6]],
                                once=False)
            elif coords[:2] == "we":
                state["village"]["triggers"][coords] = engine.Trigger(pos, size,{"default":"images/trigger.png"})
            elif coords[:2] == "za":
                state["village"]["triggers"][coords] = engine.Trigger(pos, size,{"default":"images/trigger.png"})
            #state["village"]["texts"][coords] = engine.Text(pos,text=coords)

                
        #print(state["village"]["triggers"]["house1"].pos,state["village"]["triggers"]["house1"].size)
        #state["village"]["triggers"][coords].func = swixtch
        #state["village"]["triggers"][coords].default_params = ["insects"]
        #state["village"]["triggers"]["hill"].func = swixtch
        #state["village"]["triggers"]["hill"].default_params = ["stars"]
        
        state["village"]["slide_no"] = 1
        state["initialised"] = True

    if not state["village"]["halt_player"]:
        if state["k"][pygame.K_RIGHT]:
            state["village"]["entities"]["player"].pos = state["village"]["entities"]["player"].pos[0] \
                                        + 3, state["village"]["entities"]["player"].pos[1]
            state["village"]["entities"]["player"].current_sprite = "right" if\
                            (pygame.time.get_ticks() % 1000 < 500) else "right2"
        elif state["k"][pygame.K_LEFT]:
            state["village"]["entities"]["player"].pos = state["village"]["entities"]["player"].pos[0] \
                                        - 3, state["village"]["entities"]["player"].pos[1]
            state["village"]["entities"]["player"].current_sprite = "default" if\
                            (pygame.time.get_ticks() % 1000 < 500) else "left2"
    #elif state["k"][pygame.K_DOWN]:
    #    state["entities"]["player"].current_sprite = "front"
    if state["village"]["entities"]["player"].pos[0] % 800 > 780:
        if state["village"]["slide_no"] in {6,15}:
            state["village"]["entities"]["player"].pos = (state["village"]["entities"]["player"].pos[0]-20,state["village"]["entities"]["player"].pos[1])
        else:
            state["village"]["slide_no"] += 1
            slide_switch(state,state["village"]["slide_no"])
    
    if state["village"]["entities"]["player"].pos[0] % 800 < 20:
        if state["village"]["slide_no"] in {1,7}:
            state["village"]["entities"]["player"].pos = (state["village"]["entities"]["player"].pos[0]+20,state["village"]["entities"]["player"].pos[1])
        else:
            state["village"]["slide_no"] -= 1
            slide_switch(state,state["village"]["slide_no"],x=779)
    
    #print(state["entities"]["player"].pos)
    #if state["triggers"]["house1"].collides(state["entities"]["player"]) and state["k"][pygame.K_UP]:
    #    state["entities"]["player"].current_sprite = "back"

    efiegjwiomo = pygame.mouse.get_pressed()
    if efiegjwiomo[0] and state["twetwet"] == 1:
        state["twetwet"] = 2
        state["fkwoefkmofk"]=pygame.mouse.get_pos()
        print("[{0},{1},".format(state["fkwoefkmofk"][0]+engine.global_offset[0],state["fkwoefkmofk"][1]))
        state["hchchc"] += 1
    elif efiegjwiomo[2] and state["twetwet"] == 2:
        state["twetwet"] = 1
        print("{0},{1},{2}]".format(pygame.mouse.get_pos()[0]-state["fkwoefkmofk"][0],\
            pygame.mouse.get_pos()[1]-state["fkwoefkmofk"][1],state["hchchc"]))


    state["village"]["scene"].render(engine.SCREEN)

    for trigger in state["village"]["triggers"].values():
        state = trigger.check(state,state["village"]["entities"]["player"])
        trigger.render(engine.SCREEN)

    for entity in state["village"]["entities"].values():
        entity.render(engine.SCREEN)
    state["village"]["entities"]["player"].render(engine.SCREEN) #поверх всех
    for text in state["village"]["texts"].values():
        text.render(engine.SCREEN)
    #print(state["village"]["slide_no"])
    return state