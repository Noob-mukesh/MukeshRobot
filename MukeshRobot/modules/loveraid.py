import random
from time import sleep

from MukeshRobot import dispatcher
from MukeshRobot.modules.disable import DisableAbleCommandHandler
from MukeshRobot.modules.helper_funcs.chat_status import user_admin

USERS_GROUP = 4

LOVEOP = (
    "JAANU I LOVE U NA🥺",
    "TU HI HAIN MERI JAAN KISI AUKAT NAI HAIN JO HUMARE BICH ME AAYE🥺😏",
    "SKY IS BLUE I GOT FLU I LOVE TOO🥺",
    "TU HI MERI JAAN HAIN JANUDI🥺",
    "KYU TUMHARE ANKHEN ITNI SUNDAR HAIN🥺",
    "MISS U BABY LOVE BABY I TRUST U BABY🥺",
    "BHAGWAN NE TUMHE MERE LIYE BANAYA HAIN SACHI 🥺",
    "BABY ANKHEN BAND KARO AUR DEKHO KYA DIKH RAHA JO DIKH RAHA HAIN VO MY LIFE WITHOUT 🥺",
    "PATA NAI MERE DOST TUMHE SUBAH SE BHABHI BOL RAHE HAIN SAYAD UNHE HUMARE BARE PATA CHAL GAYA😍",
    "JAAN SE JYADA TUM PYAARI HO BABY🥺",
    "KYA MATLAB TUM MERI HO GYI HO🥺",
    "MERE BACCHON KI MAA BANOGI 🥺",
    "TUNE MERI ZINGADI BANA DI🥺",
    "KYA MATLAB HUM SHADI KAR RAHE HAIN 😍",
    "BABY TUM NA MILI TOH ME FIRSE TRY KARUNGA 😏",
    "YUN TOH KISI CHEEJ KE MOHTAAJ NAI HUM BAS EK TERI AADAT SI HO GAYI HAIN 🥺",
    "KOI NAI THA AUR NA HOGA TERE JITNA TERE KREEB MERE DIL KE😍",
    "TU HI MERI SHAMO SUBAH",
    "TU HI MERI FIRST AND LAST CHOICE🥺😍",
    "TERA HAR ANDAZ PASAND HAI SIWAYE NARAZ ANDAZ KARNE KA🥺😍",
    "TU JAB NARAZ HOTI HAIN TAB MERE DIL KO KUCH KUCH HOTA HAIN🥺",
    "KYU MERE DIL MEIN TUMHARE KHAYAL AATE HAIN🥺",
    "TUNE MERI LIFE AUR DIL KO FIRSE KHUSH KAR DIYA😍",
    "EK DIN NA DEKHON TUJHE TOH MUJHE HURT HOTA HAIN🥺",
    "YE SPAM NAI MERE DIL KE BAATE HAIN TUMHARE LIYE🥺",
    "LIFE KA PATA NAI BUT TUMHARA AUR MERA DIL KA CONNECTION EK HAIN😍",
    "MERE LIYE SABKUCH TUM HO🥺",
    "AGAR TUM CHALI GAYI TOH MERA KYA HOGA🥺",
    "LOVE KARLO BAS EK BAAR FIR KABHI NAI CHHODUNGA🥺",
    "EK BAAR DIL KA CONNECTION EK KARLU FIR SURNAME EK HI HONE WALA HAIN",
    "DIMAAG KA PATA NAI LEKIN DIL TUMHARE PAS LE AAYA 🥺",
    "TU HI MERI JAAN SHAAN DIL KI ARMAAN 🥺❤️",
    "TERI DIL ME JAGAH BANAUNGA AAJ PLEASE MAAN JAO NA 🥺❤️",
    "ME TERA RAJA TU MERI RANI DO MILKE EK PREM KAHANI ❤️",
    "YE LOVE NAI TOH KYA HAIN 🥺❤️",
    "AAJ TAK ME KISIKE SAMNE NAI JHUKA BUT APNE PYAAR KE SAMNE ME HAAR GAYA🥺",
    "KYUN TUJHE ME ITNA CHAHANE LAGA ❤️🥺",
    "PYAAR TOH EK DIL KA PART HAIN AUR TU MERI HAIN",
    "DIMAAG KA PATA NAI LEKIN DIL TUMHARE PAS LE AAYA 🥺",
    "TU KYUN MERE SEEDHA DIL ME AATI HAIN ❤️🥺",
    "DIL AUR DIMAAG EK KAR DUNGA TERKO WIFE BANANE MEIN 🥺❤️",
    "MERI LIFE MEIN PEHLE BOHOT TENSION THI JABSE TUMKO DEKHA MERA PROBLEM SOLVE HO GAYA 🥺",
    "MERI MUMMY TUMHARA GHARPE INTZAAR KAR RAHI HAIN PLEASE AAJAO❤️🥺",
)


@user_admin
def loveraid(update, context):
    args = context.args
    if args:
        username = str(",".join(args))
    context.bot.sendChatAction(
        update.effective_chat.id, "typing"
    )  # Bot typing before send messages
    for i in range(30):
        lovemessage = random.choice(LOVEOP)
        update.effective_message.reply_text(lovemessage + username)
        sleep(0.2)


__help__ = """
*Admin only:*
- /loveraid *@username*: Spam user with loveraid wishes.
"""

__mod_name__ = "ʟᴏᴠᴇʀᴀɪᴅ💝"


LOVERAID_HANDLER = DisableAbleCommandHandler("loveraid", loveraid, pass_args=True)

dispatcher.add_handler(LOVERAID_HANDLER)
