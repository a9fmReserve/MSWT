# install requirements
import pip
try:
    import psutil
    import cpuinfo
    from pyrogram import Client, filters
except:
    pip.main(["install", "psutil", "py-cpuinfo", "pyrogram", "--upgrade"])
    import psutil
    import cpuinfo
    from pyrogram import Client, filters
# ------------------------------------------------------------
import os
import sys
import os
import re
import subprocess
import random
import platform
import asyncio
from time import perf_counter
# ------------------------------------------------------------
owner = [1084116847, 5631980944, 5104909433, 5466899247]  # Write you Telegram id
version = "1.2.4"
# ------------------------------------------------------------
api_id = 2860432
api_hash = "2fde6ca0f8ae7bb58844457a239c7214"
app = Client("my_account", api_id=api_id, api_hash=api_hash)
# ------------------------------------------------------------


@app.on_message(filters.command(["start", "help"]) & filters.user(owner))
def help_menu(client, message):
    msg = f'''
AdminPanel by A9FM
Version: {version}
==========
1. RAM/CPU/ROM → /info
2. Bash Terminal → /sh (Команда)
3. Start Bots → /bots
4. Restart systemctl → /restart
5. Restart server (**WARNING**) → /stop
==========
'''
    app.send_message(message.chat.id, msg)


@app.on_message(filters.command("info") & filters.user(owner))
def disk(client, message):
    info = app.send_message(message.chat.id, "Loading...")

    try:
        diskTotal = int(psutil.disk_usage('/').total / (1024 * 1024 * 1024))
        diskUsed = int(psutil.disk_usage('/').used / (1024 * 1024 * 1024))
        diskPercent = psutil.disk_usage('/').percent
        disk = f"{diskUsed}GB / {diskTotal}GB ({diskPercent}%)"
    except:
        disk = "Unknown"

    info.edit("Get RAM and ROM info...")

    try:
        ramTotal = int(psutil.virtual_memory().total / (1024 * 1024))
        ramUsage = int(psutil.virtual_memory().used / (1024 * 1024))
        ramUsagePercent = psutil.virtual_memory().percent
        ram = f"{ramUsage}MB / {ramTotal} MB ({ramUsagePercent}%)"
    except:
        ram = "Unknown"

    info.edit("Test CPU...")

    try:
        cpuInfo = cpuinfo.get_cpu_info()['brand_raw']
        cpuUsage = psutil.cpu_percent(interval=1)
        cpu = f"{cpuInfo} ({cpuUsage}%)"
    except:
        cpu = "Unknown"

    info.edit("Get OS version...")

    try:
        os = f"{platform.system()} - {platform.release()} ({platform.machine()})"
    except:
        os = "Unknown"

    info.edit("Get Battery info...")

    try:
        battery = f"{int(psutil.sensors_battery().percent)}%"
    except:
        battery = f"Unknown"

    msg = f'''
Disk: **{disk}**
CPU: **{cpu}**
RAM: **{ram}**
OS: **{os}**
Battery: **{battery}**
Version: **{version}**
'''
    info.edit(msg)


@app.on_message(filters.command("sh") & filters.user(owner))
async def sh(client, message):
    splitested = message.text.split(maxsplit=1)[1]

    cmd_text = (
        splitested
        if message.reply_to_message is None
        else message.reply_to_message.text
    )
    message = await app.send_message(message.chat.id, "0")
    if not message.reply_to_message and len(splitested) == 1:
        return await message.edit(
            "<b>Specify the command in message text or in reply</b>"
        )
    cmd_obj = subprocess.Popen(cmd_text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    await message.edit("<b>Running...</b>")
    text = f"$ <code>{cmd_text}</code>\n\n"
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        text += "<b>Timeout expired (60 seconds)</b>"
    else:
        stop_time = perf_counter()
        if stdout:
            stdout_output = f"{stdout}"
            text += "<b>Output:</b>\n" f"<code>{stdout}</code>\n"
        else:
            stdout_output = ""

        if stderr:
            stderr_output = f"{stderr}"
            text += "<b>Error:</b>\n" f"<code>{stderr}</code>\n"
        else:
            stderr_output = ""

        time = round(stop_time - start_time, 3) * 1000
        text += f"<b>Completed in {time} miliseconds with code {cmd_obj.returncode}</b> "

    try:
        await message.edit(text)
    except:
        output = f"{stdout_output}\n\n{stderr_output}"
        command = f"{cmd_text}"

        await message.edit("Result too much, send with document...")

        i = random.randint(1, 9999)
        with open(f"result{i}.txt", "w") as file:
            file.write(f"{output}")

        try:
            await app.send_document(message.chat.id, f"result{i}.txt", caption=f"<code>{command}</code>")
            await message.delete()
        except:
            await app.send_document(message.chat.id, f"result{i}.txt", caption="Result")
            await message.edit(f"<code>{command}</code>")

        os.remove(f"result{i}.txt")

    cmd_obj.kill()


@app.on_message(filters.command("bots") & filters.user(owner))
def botes(client, message):
    bots(client, message)


@app.on_message(filters.command("restart") & filters.user(owner))
async def restart(client, message):
    for i in owner:
        try:
            await app.send_message(i, f"""{message.from_user.mention} send command to server (restart with "restart_daemon.sh" script)""")
        except:
            pass
    os.system(f"sh restart_daemon.sh")


@app.on_message(filters.command("stop") & filters.user(owner))
async def st_bots(client, message):
    for i in owner:
        try:
            await app.send_message(i, f"{message.from_user.mention} restarting server...")
        except:
            pass
    os.system("sudo reboot")


def prestart(api_id, api_hash):
    app = Client("my_account", api_id=api_id, api_hash=api_hash)
    with app:
        for i in owner:
            try:
                app.send_message(i, f"Server started!\nVersion: **{version}**")
            except:
                pass
        bots(app, "0")


def bots(app, message):
    text = ""

    for i in os.listdir("."):
        if re.compile("(-start.sh)").search(i):
            try:
                start_botes = subprocess.Popen([f"sh {i}"], stdout=subprocess.PIPE, shell=True)
                start_botes.daemon = True
                text += f"✅ File autostart {i} started!\n"
            except:
                text += f"❌ File autostart {i} not started!\n"
        if re.compile("(-start.bat)").search(i):
            try:
                start_botes = subprocess.Popen([f"{i}"], stdout=subprocess.PIPE, shell=True)
                start_botes.daemon = True
                text += f"✅ File autostart {i} started!\n"
            except:
                text += f"❌ File autostart {i} not started!\n"

    if text == "":
        text = "File autostart not found..."

    try:
        usernames = message.from_user.mention
    except:
        usernames = "ROOT"

    text = f"{usernames} trying to running autostart tasks\n{text}"
    for i in owner:
        try:
            app.send_message(i, text)
        except:
            pass


while True:
    prestart(api_id, api_hash)
    app.run()
