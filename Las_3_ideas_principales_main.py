import discord
from discord.ext import commands
import unicodedata
import random

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

descripcion = "Un bot de conciencia ecológica"

bot = commands.Bot(command_prefix="!", intents=intents, description=descripcion)

# Lista de materiales de cada país con su respectiva información de reciclaje (IDEA 1)
reciclaje = {
    "plastico": {
        "Chile": "El plástico PET va al contenedor amarillo. Otros tipos deben llevarse a puntos limpios.",
        "Argentina": "Plásticos reciclables al contenedor verde. Algunos municipios tienen puntos especiales.",
        "Japón": "Se separa por tipo y debe lavarse antes de desecharse.",
        "Brasil": "Va al contenedor verde en muchas ciudades, pero varía según la región.",
        "EE.UU.": "Depende del estado; algunos aceptan solo plásticos 1 y 2 en el contenedor azul."
    },
    "vidrio": {
        "Chile": "Va al contenedor verde, limpio y sin tapas.",
        "Alemania": "Se separa por colores (verde, marrón y transparente).",
        "Japón": "Debe clasificarse en reciclable/no reciclable y lavarse antes.",
        "Brasil": "En muchas ciudades va al contenedor verde.",
        "España": "Se deposita en el iglú verde, pero no espejos ni cerámica."
    }
}
 
def normalizar(texto: str) -> str:
    texto = texto.lower()
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

    texto = texto.replace(".", "")
    return texto

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="🌱 Bot EcoInfo",
        description="¡Bienvenido! Este bot te ayuda a aprender sobre reciclaje",
        color=discord.Color.green()
)

    embed.add_field(name="📌 Comandos disponibles",
                    value="`!reciclar <material> <país>` ---> Guía de reciclaje\n"
                          "`!info` ---> Mostrar este menú",
                    inline=False)

    embed.add_field(name="♻️ Materiales disponibles",
                    value="\n".join(f"• {m.capitalize()}" for m in reciclaje.keys()),
                    inline=False)

    embed.add_field(name="🌍 Países disponibles por material",
                    value="\n".join(
                        f"• {m.capitalize()}: " + ", ".join(reciclaje[m]) for m in reciclaje.keys()
                    ),
                    inline=False)

    embed.set_footer(text="Cuidemos nuestro planeta 🌎")

    await ctx.send(embed=embed)

@bot.command()
async def reciclar(ctx, material: str, pais: str):
    material = material.lower().strip()
    pais_usuario = normalizar(pais.strip())
    pais_correcto = None

    if material not in reciclaje:
        await ctx.send(f"❌ Material '{material}' no reconocido. Usa `!info` para ver los materiales disponibles.")
        return
    
    for p in reciclaje[material]:
        if normalizar(p) == pais_usuario:
            pais_correcto = p
            break
        
    if not pais_correcto:
        await ctx.send(f"❌ País '{pais}' no reconocido para el material '{material}'. Usa `!info` para ver los países disponibles.")
        return
    
    info = reciclaje[material][pais_correcto]

    embed = discord.Embed(
        title=f"♻️ Guía de reciclaje para {material.capitalize()} en {pais_correcto}",
        description=info,
        color=discord.Color.blue()
    )
    embed.set_footer(text="¡Gracias por ayudar al planeta!")

    await ctx.send(embed=embed)

# Trivia ecológica para fomentar el aprendizaje (IDEA 2)
preguntas = [
    {"pregunta": "¿Cuál es el gas principal responsable del efecto invernadero?", "respuesta": "Dióxido de carbono"},
    {"pregunta": "¿Qué es más biodegradable: el plástico o el papel?", "respuesta": "El papel"},
    {"pregunta": "¿Cuál es la energía revobable más utilizada en el mundo?", "respuesta": "Energía hidroélectrica"},
    {"pregunta": "¿Cuál es el principal beneficio de plantar árboles?", "respuesta": "Absorber dióxido de carbono"},
    {"pregunta": "¿Cuáles son los 3 ciclos principales para la regulación del clima y el equilibrio ecológico?", "respuesta": "Ciclo del agua, ciclo del carbono y ciclo del nitrógeno"}
]

@bot.command()
async def trivia(ctx):
    pregunta = random.choice(preguntas)
    await ctx.send(f"❓ **Pregunta:** {pregunta['pregunta']}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        respuesta = await bot.wait_for("message", check=check, timeout=15)
    except:
        await ctx.send("⏰ Tiempo agotado!")
        return
    
    if normalizar(respuesta.content) == normalizar(pregunta["respuesta"]):
        await ctx.send("✅ ¡Correcto! 🎉")
    else:
        await ctx.send(f"❌ Incorrecto. La respuesta correcta es: {pregunta['respuesta']}")
    
# Consejos ecológicos para el público objetivo y estos lo tengan en consideración (IDEA 3)
consejos = [
    "Reduce el uso de plásticos de un solo uso.",
    "Utiliza bombillas LED para ahorrar energía.",
    "Separa tu basura correctamente para facilitar el reciclaje.",
    "Prefiere transporte público o bicicleta.",
    "Evita desperdiciar agua."
] 

@bot.command()
async def consejo(ctx):
    consejo_random = random.choice(consejos)
    await ctx.send(f"💡 **Consejo ecológico:** {consejo_random}")

bot.run(TU-TOKEN-AQUÍ)
