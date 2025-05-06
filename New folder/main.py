import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

staff_channel_id = 1369282767908507710

questions_all = {
    "anpc": [
        "Nume + Prenume",
        "Gradul detinut in politie + callsign?",
        "Cu ce se ocupa A.N.P.C?",
        "Ce înseamnă prescurtarea A.N.P.C.?",
        "Ce drepturi are un consumator în România?",
        "Care sunt domeniile în care A.N.P.C. intervine cel mai des?",
        "A.N.P.C. este o instituție publică sau privată?",
        "Descrie-te in 30 de cuvinte",
        "Esti de acord ca nu mai poti schimba departamentul pentru 7 zile?"
    ],
    "dcco": [
        "Nume + Prenume",
        "CNP + Call Sign",
        "Gradul dumneavoastră",
        "Data intrării în departament",
        "Cu ce crezi că se ocupă Direcția de Combatere a Criminalității Organizate?",
        "De ce ai ales acest subdepartament?",
        "Spune-ne 3 calități care te recomandă pentru acest post",
        "Spune-ne 3 defecte care te-ar dezavantaja",
        "Care crezi că sunt calitățile unui detectiv bun?",
        "Cum ai gestiona o investigație asupra unei grupări suspecte?",
        "Cum ai reacționa dacă un coleg este luat ostatic?",
        "Dacă ai descoperi că un coleg colaborează cu o organizație criminală, ce ai face?",
        "Un suspect îți cere să comiți o infracțiune pentru încredere. Cum procedezi?",
        "Un informator îți oferă o informație fără dovezi. Ce faci?",
        "Ai un suspect care nu cooperează. Cum îl convingi?",
        "Ce echipamente ai voie în recunoaștere?",
        "Ce vehicule ai voie în recunoaștere?"
    ],
    "sas": [
        "Nume + Prenume",
        "CNP + Call Sign",
        "Gradul dumneavoastră",
        "Data intrării în departament",
        "Cu ce crezi că se ocupă Serviciul de Acțiuni Speciale?",
        "De ce ai ales acest subdepartament?",
        "Spune-ne 3 calități",
        "Spune-ne 3 defecte",
        "În cazul unui cod 0, cine primește primul trusă?",
        "Ești singur și vezi persoane înarmate. Cum procedezi?",
        "Sunt 2 jafuri, ai voie să patrulezi în S.A.S?",
        "Dacă este cod 0, ai voie să te echipezi în S.A.S?",
        "Ai voie să procesezi oameni în S.A.S?",
        "Când ai voie să dai jos masca în S.A.S?",
        "Ești de acord să păstrezi confidențialitatea răspunsurilor?"
    ],
    "rar": [
        "Nume + Prenume",
        "Gradul detinut in politie + callsign?",
        "Ce înseamnă prescurtarea R.A.R.?",
        "R.A.R. se ocupă cu verificarea kilometrajului?",
        "Descrie-te in 30 de cuvinte",
        "Esti de acord ca nu mai poti schimba departamentul pentru 7 zile?"
    ]
}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

@bot.tree.command(name="formular", description="Deschide meniul de alegere a formularului")
async def formular(interaction: discord.Interaction):
    class DepartmentView(View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="ANPC", style=discord.ButtonStyle.blurple)
        async def anpc_button(self, interaction_button: discord.Interaction, button: Button):
            await start_form(interaction_button.user, "anpc", interaction_button)

        @discord.ui.button(label="DCCO", style=discord.ButtonStyle.blurple)
        async def dcco_button(self, interaction_button: discord.Interaction, button: Button):
            await start_form(interaction_button.user, "dcco", interaction_button)

        @discord.ui.button(label="SAS", style=discord.ButtonStyle.blurple)
        async def sas_button(self, interaction_button: discord.Interaction, button: Button):
            await start_form(interaction_button.user, "sas", interaction_button)

        @discord.ui.button(label="RAR", style=discord.ButtonStyle.blurple)
        async def rar_button(self, interaction_button: discord.Interaction, button: Button):
            await start_form(interaction_button.user, "rar", interaction_button)

    await interaction.response.send_message(
        "**Formulare disponibile:**\nAlege subdepartamentul pentru care dorești să completezi formularul.",
        view=DepartmentView(), ephemeral=True
    )

async def start_form(user: discord.User, departament: str, interaction_button: discord.Interaction):
    dm = await user.create_dm()
    responses = {}
    for question in questions_all[departament]:
        await dm.send(f"**Întrebare:** {question}")
        try:
            msg = await bot.wait_for("message", timeout=300, check=lambda m: m.author == user and m.channel == dm)
            responses[question] = msg.content
        except:
            await dm.send("Timpul a expirat pentru această întrebare.")
            return

    embed = discord.Embed(title=f"Formular {departament.upper()}", description=f"Trimis de: {user.mention}", color=discord.Color.blue())
    for q, a in responses.items():
        embed.add_field(name=f"🔹 {q}", value=a, inline=False)

    class ApproveView(View):
        @discord.ui.button(label="✅ Aproba", style=discord.ButtonStyle.green)
        async def approve(self, interaction_staff: discord.Interaction, button: Button):
            await user.send("✅ Felicitări! Cererea ta a fost **aprobată**.")
            await interaction_staff.response.send_message("Cererea aprobată!", ephemeral=True)
            self.stop()

        @discord.ui.button(label="❌ Respinge", style=discord.ButtonStyle.red)
        async def reject(self, interaction_staff: discord.Interaction, button: Button):
            await user.send("❌ Ne pare rău! Cererea ta a fost **respinsă**.")
            await interaction_staff.response.send_message("Cererea respinsă.", ephemeral=True)
            self.stop()

    staff_channel = bot.get_channel(staff_channel_id)
    if staff_channel:
        await staff_channel.send(embed=embed, view=ApproveView())
    await dm.send("✅ Formularul tău a fost trimis spre evaluare. Vei primi un răspuns cât de curând!")

bot.run(os.getenv("TOKEN"))
