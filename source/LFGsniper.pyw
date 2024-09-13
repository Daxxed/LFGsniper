import discord, os, threading, asyncio, datetime, logging
import tkinter as tk
from tkinter import ttk, messagebox

# Set up logging
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='')

# GUI Class
class CommanderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LFG Sniper")

# Handle closing of the GUI
        def on_closing():
            if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
                logging.info(f"{datetime.datetime.now()}: Stopping GUI by closing window")
                self.root.destroy()
                logging.info(f"{datetime.datetime.now()}: Stopping Sniper by closing GUI")
                os._exit(0)

        root.protocol("WM_DELETE_WINDOW", on_closing)

# GUI Setup
        self.client_items = {}
        self.initialize_variables()
        self.setup_gui()

    def initialize_variables(self):
        self.Cerusbutton_value = tk.BooleanVar(value=1)
        self.Europebutton_value = tk.BooleanVar(value=1)
        self.Muricabutton_value = tk.BooleanVar(value=1)
        self.CerusAlacHealbutton_value = tk.BooleanVar(value=1)
        self.CerusBoonDPSbutton_value = tk.BooleanVar(value=1)
        self.CerusBossDPSbutton_value = tk.BooleanVar(value=1)
        self.HTCMbutton_value = tk.BooleanVar(value=1)
        self.HTCMEuropebutton_value = tk.BooleanVar(value=1)
        self.HTCMMuricabutton_value = tk.BooleanVar(value=1)
        self.HTCMAlacHealbutton_value = tk.BooleanVar(value=1)
        self.HTCMBoonDPSbutton_value = tk.BooleanVar(value=1)
        self.HTCMBossDPSbutton_value = tk.BooleanVar(value=1)
        self.HTCMPortalbutton_value = tk.BooleanVar(value=1)
        self.HTCMVenticatorbutton_value = tk.BooleanVar(value=1)
        self.StartButtonVar = tk.BooleanVar(value=0)
        self.ReactDelayVar = tk.IntVar(value=30)

    def setup_gui(self):
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("one")
        self.tree.column("one", width=65)
        self.tree.heading("one", text="Discord ID")
        self.tree['show'] = 'headings'
        self.tree.pack(anchor='w', padx=5, pady=5)

        self.create_checkbuttons()
        self.create_start_button()
        self.create_delay_widgets()

    def create_checkbuttons(self):
        checkbuttons = [
            ("Cerus", self.Cerusbutton_value, 85, 5),
            ("EU", self.Europebutton_value, 85, 25),
            ("NA", self.Muricabutton_value, 85, 45),
            ("AHeal", self.CerusAlacHealbutton_value, 85, 65),
            ("Quick", self.CerusBoonDPSbutton_value, 85, 85),
            ("DPS", self.CerusBossDPSbutton_value, 85, 105),
            ("HTCM", self.HTCMbutton_value, 145, 5),
            ("EU", self.HTCMEuropebutton_value, 145, 25),
            ("NA", self.HTCMMuricabutton_value, 145, 45),
            ("AHeal", self.HTCMAlacHealbutton_value, 145, 65),
            ("Quick", self.HTCMBoonDPSbutton_value, 145, 85),
            ("DPS", self.HTCMBossDPSbutton_value, 145, 105),
            ("Portal", self.HTCMPortalbutton_value, 145, 125),
            ("Venti", self.HTCMVenticatorbutton_value, 145, 145)
        ]
        
        for text, var, x, y in checkbuttons:
            cb = ttk.Checkbutton(self.root, text=text, variable=var)
            cb.place(x=x, y=y)

    def create_start_button(self):
        start_button = tk.Button(self.root, text="Start", width=8, command=self.start_button_clicked)
        start_button.place(x=135, y=165)
        
    def create_delay_widgets(self):
        delay_label = ttk.Label(self.root, text="React Delay\n(in seconds)")
        delay_label.place(x=75, y=130)
        delay_text = ttk.Entry(self.root, width=5, textvariable=self.ReactDelayVar)
        delay_text.place(x=85, y=165)

# Start the discord bot from GUI start button
    def start_button_clicked(self):
        if not self.StartButtonVar.get():
            self.StartButtonVar.set(1)
            threading.Thread(target=self.start_discord_bot).start()

    def start_discord_bot(self):
        asyncio.run(discord_bot(self))
        if self.StartButtonVar.get():
            return

# Add dicord ID to the connections tab
    def update_clients(self, client_id):
        if client_id in self.client_items:
            self.tree.delete(self.client_items[client_id])

        item_id = self.tree.insert('', 'end', values=(client_id))
        self.client_items[client_id] = item_id
        if self.StartButtonVar.get():
            self.tree.heading("one", text="Listening")

# Update heading text: running/paused
    def update_heading(self, text):
        self.root.after(0, lambda: self.tree.heading("one", text=text))

# Discord Channel IDs
class ID:
    VL_Guild_ID = 1121166847266537562
    VL_EU_HTCM_CHANNEL_ID = 1121195413752520715
    VL_EU_CERUS_CHANNEL_ID = 1221395173137973318
    VL_NA_HTCM_CHANNEL_ID = 1122556847430307970
    VL_NA_CERUS_CHANNEL_ID = 1235348961003311155

# Keywords to listen for
VL_CERUS_KEYWORDS = ['@veteran febeheal', '@veteran febeboondps', '@veteran febedps']
VL_HTCM_KEYWORDS = ['@veteran healkiter alac', '@veteran quickdps', '@veteran portal', '@veteran venticator', '@veteran bossdps']

# Discord bot
async def discord_bot(gui):

# Retrieve Discord Token
    def retrieve_token():
        TOKEN = open("token.txt","r").read()
        if not TOKEN:
            TOKEN = os.environ.get("TOKEN")
        return TOKEN

    logging.info(f"{datetime.datetime.now()}: Starting Sniper")

    client = discord.Client()

# Successfully logged in
    @client.event
    async def on_ready():
        logging.info(f"{datetime.datetime.now()}: Logged in as {client.user}")
        gui.update_clients(client.user)

# Incoming messages
    @client.event
    async def on_message(message):
        if isinstance(message.channel, discord.DMChannel):
            return
        match message.channel.id:
            case ID.VL_EU_CERUS_CHANNEL_ID:
                type = 'EU Cerus'
            case ID.VL_NA_CERUS_CHANNEL_ID:
                type = 'NA Cerus'
            case ID.VL_EU_HTCM_CHANNEL_ID:
                type = 'EU HTCM'
            case ID.VL_NA_HTCM_CHANNEL_ID:
                type = 'NA HTCM'
            case _:
                return

        match message.guild.id:
            case ID.VL_Guild_ID:
                server = 'Void Lounge'
            case _:
                return
            
        logging.info(f"{datetime.datetime.now()}: Message found in server: {server} and channel: {type}")

        if type == 'NA Cerus' and gui.Muricabutton_value.get() == False:
                logging.info(f"{datetime.datetime.now()}: Ignoring NA Cerus because not selected")
                return
        elif type == 'EU Cerus' and gui.Europebutton_value.get() == False:
                logging.info(f"{datetime.datetime.now()}: Ignoring EU Cerus because not selected")
                return
        elif type == 'NA HTCM' and gui.HTCMMuricabutton_value.get() == False:
                logging.info(f"{datetime.datetime.now()}: Ignoring NA HTCM because not selected")
                return
        elif type == 'EU HTCM' and gui.HTCMEuropebutton_value.get() == False:
                logging.info(f"{datetime.datetime.now()}: Ignoring EU HTCM because not selected")
                return

        if client.user.mentioned_in(message):
            logging.info(f"{datetime.datetime.now()}: We have been tagged in server: {server} and channel: {type} by {message.author}")
            logging.info(f"{datetime.datetime.now()}: Stopping Sniper by mention:message")
            gui.StartButtonVar.set(0)
            gui.update_heading("Paused")
            messagebox.showerror("Success", "You have been tagged in LFG and the script has been paused.\nPress Start again to resume.")
            await client.close()

        if server == 'Void Lounge':
            if type == 'NA Cerus' or type == 'EU Cerus':
                if gui.Cerusbutton_value.get() == False:
                    logging.info(f"{datetime.datetime.now()}: Ignoring Cerus because not selected")
                    return
                if gui.ReactDelayVar.get() > 0:
                    logging.info(f"{datetime.datetime.now()}: Delaying reaction by {gui.ReactDelayVar.get()}s")
                    await asyncio.sleep(gui.ReactDelayVar.get())
                for keyword in VL_CERUS_KEYWORDS:
                    if keyword in message.content.lower():
                        logging.info(f"{datetime.datetime.now()}: {server} {type} with keyword '{keyword}' found")
                        VL_guild = discord.utils.get(client.guilds, id=ID.VL_Guild_ID)
                        match keyword:
                            case '@veteran febeheal':
                                if gui.CerusAlacHealbutton_value.get() == False:
                                    continue
                                VL_emoji = discord.utils.get(VL_guild.emojis, name='VLHealAlac')
                            case '@veteran febeboondps':
                                if gui.CerusBoonDPSbutton_value.get() == False:
                                    continue
                                VL_emoji = discord.utils.get(VL_guild.emojis, name='VLQuickDPS')
                            case '@veteran febedps':
                                if gui.CerusBossDPSbutton_value.get() == False:
                                    continue
                                VL_emoji = discord.utils.get(VL_guild.emojis, name='VLBossDPS')
                        await message.add_reaction(VL_emoji)
                        logging.info(f"{datetime.datetime.now()}: Reacted to {server} {type} with {VL_emoji}")
                        await asyncio.sleep(1)
            elif type == 'NA HTCM' or type == 'EU HTCM':
                if gui.HTCMbutton_value.get() == False:
                    logging.info(f"{datetime.datetime.now()}: Ignoring HTCM because not selected")
                    return
                if gui.ReactDelayVar.get() > 0:
                    logging.info(f"{datetime.datetime.now()}: Delaying reaction by {gui.ReactDelayVar.get()}s")
                    await asyncio.sleep(gui.ReactDelayVar.get())
                for keyword in VL_HTCM_KEYWORDS:
                    if keyword in message.content.lower():
                        logging.info(f"{datetime.datetime.now()}: {server} {type} with keyword '{keyword}' found")
                        VL_guild = discord.utils.get(client.guilds, id=ID.VL_Guild_ID)
                        match keyword:
                            case '@veteran healkiter alac':
                                if gui.HTCMAlacHealbutton_value.get() == False:
                                    continue
                                VL_emoji = discord.utils.get(VL_guild.emojis, name='VLHealAlac')
                            case '@veteran quickdps':
                                if gui.HTCMBoonDPSbutton_value.get() == False:
                                    continue
                                VL_emoji = discord.utils.get(VL_guild.emojis, name='VLQuickDPS')
                            case '@veteran portal':
                                if gui.HTCMPortalbutton_value.get() == False:
                                    continue
                                VL_emoji = discord.utils.get(VL_guild.emojis, name='VLPortal')
                            case '@veteran venticator':
                                if gui.HTCMVenticatorbutton_value.get() == False:
                                    continue
                                VL_emoji = discord.utils.get(VL_guild.emojis, name='VLVenticator')
                            case '@veteran bossdps':
                                if gui.HTCMBossDPSbutton_value.get() == False:
                                    continue
                                VL_emoji = discord.utils.get(VL_guild.emojis, name='VLBossDPS')
                        await message.add_reaction(VL_emoji)
                        logging.info(f"{datetime.datetime.now()}: Reacted to {server} {type} with {VL_emoji}")
                        await asyncio.sleep(1)

# Edited messages
    @client.event
    async def on_message_edit(message, message2):
        if isinstance(message.channel, discord.DMChannel):
            return
        match message.channel.id:
            case ID.VL_EU_CERUS_CHANNEL_ID:
                type = 'EU Cerus'
            case ID.VL_NA_CERUS_CHANNEL_ID:
                type = 'NA Cerus'
            case ID.VL_EU_HTCM_CHANNEL_ID:
                type = 'EU HTCM'
            case ID.VL_NA_HTCM_CHANNEL_ID:
                type = 'NA HTCM'
            case _:
                return

        match message.guild.id:
            case ID.VL_Guild_ID:
                server = 'Void Lounge'
            case _:
                return
        
        logging.info(f"{datetime.datetime.now()}: Edited message found in server: {server} and channel: {type}")

        if client.user.mentioned_in(message2):
            logging.info(f"{datetime.datetime.now()}: We have been tagged in server: {server} and channel: {type} by {message.author}")
            logging.info(f"{datetime.datetime.now()}: Stopping Sniper by mention:edit")
            gui.StartButtonVar.set(0)
            gui.update_heading("Paused")
            messagebox.showerror("Success", "You have been tagged in LFG and the script has been paused.\nPress Start again to resume.")
            await client.close()
        else:
            return

# Connect to discord and log exceptions
    try:
        TOKEN = retrieve_token()
        await client.start(TOKEN)
    except discord.LoginFailure:
        logging.info(f"{datetime.datetime.now()}: Discord bot log in Failure")
        gui.StartButtonVar.set(0)
        if messagebox.askretrycancel("Login failed", "Failure to log in, most likely your discord token is wrong/missing."):
            logging.info(f"{datetime.datetime.now()}: Retrying log in")
            gui.start_button_clicked()
        else:
            logging.info(f"{datetime.datetime.now()}: Aborted log in")
    except discord.ConnectionClosed:
        logging.info(f"{datetime.datetime.now()}: Discord bot connection Failure")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("210x200")
    gui = CommanderGUI(root)   
    logging.info(f"{datetime.datetime.now()}: Control Panel Booted")
    root.mainloop()
