from bs4 import element
import requests
try:
    from tkinter import *     
except:
    pass
try:
    from PIL import Image, ImageTk
except:
    pass
try:
    import os
except:
    pass
try:
    import subprocess
except:
    pass
try:
    from subprocess import check_output
except:
    pass
try:
    from subprocess import Popen, PIPE
except:
    pass
try:
    from threading import Thread
except:
    pass
try:
    from colorama import *
except:
    pass
try:
    from colorama import init
except:
    pass
try:
    from bs4 import BeautifulSoup
except:
    pass
try:
    from time import *
except:
    pass
try:
    import re
except:
    pass
init(autoreset=True)

os.system("cls")

class cape_list(object):
    def minecraft(self, username):
        try:
            image = requests.get(f"https://api.capes.dev/load/{username}/minecraft").json()

            view = image['frontImageUrl']
            with open('pic1.png', 'wb') as handle:
                response = requests.get(view + ".png", stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
            viewimageonscreen(username)
        except:
            print(f"no cape found on player {username}")

    def optifine(self, username):
        try:
            image = requests.get(f"https://api.capes.dev/load/{username}/optifine").json()

            view = image['frontImageUrl']
            with open('pic1.png', 'wb') as handle:
                response = requests.get(view + ".png", stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
            viewimageonscreen(username)
        except:
            print(f"no cape found on player {username}")

    def minecraftcapes_net(self, username):
        try:
            image = requests.get(f"https://api.capes.dev/load/{username}/minecraftcapes").json()

            view = image['frontImageUrl']
            with open('pic1.png', 'wb') as handle:
                response = requests.get(view + ".png", stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
            viewimageonscreen(username)
        except:
            print(f"no cape found on player {username}")
    
    def labymod(self, username):
        try:
            image = requests.get(f"https://api.capes.dev/load/{username}/labymod").json()

            view = image['frontImageUrl']
            with open('pic1.png', 'wb') as handle:
                response = requests.get(view + ".png", stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
            viewimageonscreen(username)
        except:
            print(f"no cape found on player {username}")
    
    def tlauncher(self, username):
        try:
            image = requests.get(f"https://api.capes.dev/load/{username}/tlauncher").json()

            view = image['frontImageUrl']
            with open('pic1.png', 'wb') as handle:
                response = requests.get(view + ".png", stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
            viewimageonscreen(username)
        except:
            print(f"no cape found on player {username}")
    
    def dowloadcape(username, file_pach: None):
        try:
            str(file_pach)
            str(username)
            if(file_pach == None):
                print("no file pach")
                exit()
            if("." in file_pach):
                print("file pach only. no files like /coolcape.png")
                exit()
            else:
                
                image = requests.get(f"https://api.capes.dev/load/{username}/minecraft").json()

                view = image['frontImageUrl']
                if(str(file_pach).endswith("/") == False):
                    file_pach = str(file_pach) + "/"
                with open(f'{file_pach}cape.png', 'wb') as handle:
                    response = requests.get(view + ".png", stream=True)

                    if not response.ok:
                        print(response)

                    for block in response.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)
            print(f"saved in '{file_pach}cape.png'")
        except:
            print(f"no cape found on player {username}")


    def dowloadfullcape(username, file_pach: None):
        try:
            str(file_pach)
            str(username)
            if(file_pach == None):
                print("no file pach")
                exit()
            if("." in file_pach):
                print("file pach only. no files like /coolcape.png")
                exit()
            else:
                
                image = requests.get(f"https://api.capes.dev/load/{username}/minecraft").json()

                view = image['imageUrl']
                if(str(file_pach).endswith("/") == False):
                    file_pach = str(file_pach) + "/"
                with open(f'{file_pach}full_cape.png', 'wb') as handle:
                    response = requests.get(view + ".png", stream=True)

                    if not response.ok:
                        print(response)

                    for block in response.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)
            print(f"saved in '{file_pach}full_cape.png'")
        except:
            print(f"no cape found on player {username}")



def findcapes(username):
    try:
        image = requests.get(f"https://api.capes.dev/load/{username}/minecraft").json()

        view = image['frontImageUrl']
        print(f"{Fore.GREEN}minecraft cape found on player {username}")
    except:
        print(f"{Fore.RED}no minecraft cape found on player {username}")
    try:
        uRL = f"https://api.capes.dev/load/{username}/minecraftcapes"
        page = requests.get(uRL)

        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find(id="col s6 m3 l2 cape")
        print(results.prettify())

        print(f"{Fore.GREEN}minecraftcapes.net cape found on player {username}")
    except:
        print(f"{Fore.RED}no minecraftcapes.net cape found on player {username}")
    try:
        image = requests.get(f"https://api.capes.dev/load/{username}/labymod").json()

        view = image['frontImageUrl']
        print(f"{Fore.GREEN}labymod cape found on player {username}")
    except:
        print(f"{Fore.RED}no labymod cape found on player {username}")
    try:
        image = requests.get(f"https://api.capes.dev/load/{username}/tlauncher").json()

        view = image['frontImageUrl']
        print(f"{Fore.GREEN}tlauncher cape found on player {username}")
    except:
        print(f"{Fore.RED}no tlauncher cape found on player {username}")

 

def findcapes_file(names_list: None, file_pach: None):
    with open(names_list, "r") as x:
        print("reading names in wurd list...")
        names_list2 = x.readlines()
        sleep(20)
        x.close()
        print("done!")
    for name in names_list2:
        print("starting...")
        username = name
        str(file_pach)
        if(file_pach == None):
            print("no file pach")
            exit()
        if(names_list == None):
            print("no name list")
            exit()
        else:
            print(username)
            with open(file_pach, "a") as f:
                try:
                    image = requests.get(f"https://api.capes.dev/load/{username}/minecraft").json()

                    view = image['frontImageUrl']
                    print(f"{Fore.GREEN}minecraft cape found on player {username}")
                    f.write(f"minecraft cape found on player {username}\n")
                except:
                    print("")
                # try:
                #     uRL = f"https://api.capes.dev/load/{username}/minecraftcapes"
                #     page = requests.get(uRL)

                #     soup = BeautifulSoup(page.content, "html.parser")

                #     results = soup.find(id="col s6 m3 l2 cape")
                #     print(results.prettify())

                #     print(f"{Fore.GREEN}minecraftcapes.net cape found on player {username}")
                #     f.write(f"minecraftcapes.net cape found on player {username}\n")
                # except:
                #     print("")
                # try:
                #     image = requests.get(f"https://api.capes.dev/load/{username}/labymod").json()

                #     view = image['frontImageUrl']
                #     print(f"{Fore.GREEN}labymod cape found on player {username}")
                #     f.write(f"labymod cape found on player {username}\n")
                # except:
                #     print("")
                # try:
                #     image = requests.get(f"https://api.capes.dev/load/{username}/tlauncher").json()

                #     view = image['frontImageUrl']
                #     print(f"{Fore.GREEN}tlauncher cape found on player {username}")
                #     f.write(f"tlauncher cape found on player {username}\n")
                # except:
                #     print("")
# # Opens a image in RGB mode
# im = Image.open("pic1.png")
 
# # Size of the image in pixels (size of original image)
# # (This is not mandatory)
# width, height = im.size
 
# # Setting the points for cropped image
# left = 5
# top = height / 4
# right = 164
# bottom = 3 * height / 4
 
# # Cropped image of above dimension
# # (It will not change original image)
# im1 = im.crop((left, top, right, bottom))




# #Import the required Libraries

# #Create an instance of tkinter frame
# win = Tk()

# #Set the geometry of tkinter frame
# win.geometry("194x290")

# #Create a canvas
# canvas= Canvas(win, width= 200, height= 279)
# canvas.pack()

# #Load an image in the script
# img= (Image.open("pic1.png"))

# #Resize the Image using resize method
# resized_image= img.resize((174,278), Image.ANTIALIAS)
# new_image= ImageTk.PhotoImage(resized_image)

# #Add image to the Canvas Items
# canvas.create_image(10,1, anchor=NW, image=new_image)

#win.mainloop()
def sing(username):
    try:
        # Opens a image in RGB mode
        im = Image.open("pic1.png")
        
        # Size of the image in pixels (size of original image)
        # (This is not mandatory)
        width, height = im.size
        
        # Setting the points for cropped image
        left = 5
        top = height / 4
        right = 164
        bottom = 3 * height / 4
        
        # Cropped image of above dimension
        # (It will not change original image)
        im1 = im.crop((left, top, right, bottom))




        #Import the required Libraries

        #Create an instance of tkinter frame
        win = Tk()

        #Set the geometry of tkinter frame
        win.geometry("194x291")

        #Create a canvas
        canvas= Canvas(win, width= 200, height= 279)
        canvas.pack()

        #Load an image in the script
        img= (Image.open("pic1.png"))

        #Resize the Image using resize method
        resized_image= img.resize((174,278), Image.ANTIALIAS)
        new_image= ImageTk.PhotoImage(resized_image)

        #Add image to the Canvas Items
        canvas.create_image(10,1, anchor=NW, image=new_image)
        win.title(username + "'s cape")
        win.wm_attributes('-toolwindow', 'True')
        win.mainloop()
        os.remove("pic1.png")
    except:
        print("you can only open 1 cape at the time!")


def viewimageonscreen(username):
    thread = Thread(target=sing, args=[str(username)])
    thread.start()




def cape():
    return cape_list()
    


# def check_names(names_list: None, file_pach: None):
#     with open(names_list, "r") as x:
#         print("reading names in wurd list...")
#         names_list2 = x.readlines()
#         sleep(5)
#         x.close()
#         print("done!")
#     for name in names_list2:
#         username = str(name)
#         username = username.replace("\n", "")
#         str(file_pach)
#         if(file_pach == None):
#             print("no file pach")
#             exit()
#         if(names_list == None):
#             print("no name list")
#             exit()
#         else:
#             print(username)
#             with open(file_pach, "a") as f:
#                 try:
#                     headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
#                     page = requests.get('https://api.capes.dev/load/{username}',headers=headers).json()
#                     try:
#                         error = page['error']
#                     except:
#                         pass
#                     if error in page:
#                         f.write(f"{username} in not claimed!\n")
#                         print(f"{username} in not claimed!")
#                     else:
#                         pass
                    
#                 except:
#                     pass


