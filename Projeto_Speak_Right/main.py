import os
import scipy.io.wavfile as wav
import sounddevice as sd
import speech_recognition as sr
from googletrans import Translator

# Inicialização dos serviços
translator = Translator()
recognizer = sr.Recognizer()

# Interface inicial
print("==========================================")
print(" 🎮 JOGO DE TRADUÇÃO POR VOZ 🎙️")
print("==========================================")

# Escolha do nível de dificuldade
print("\n📊 Escolha a dificuldade:")
print("1 - Fácil (gato, casa, carro)")
print("2 - Difícil (computador, conhecimento, desenvolvimento)")
opcao = input("👉 Digite 1 ou 2: ")

if opcao == "2":
    palavras = ["computador", "conhecimento", "desenvolvimento"]
else:
    palavras = ["gato", "casa", "carro"]

pontos = 0
taxa_amostragem = 44100
duracao_gravacao = 4  # segundos

print("\n🚀 O jogo começou! Fale a tradução em INGLÊS de cada palavra.\n")

# Loop principal do jogo
for palavra in palavras:
    print("-" * 40)
    print(f"🇧🇷 Traduza a palavra: {palavra.upper()}")
    input("Pressione [ENTER] quando estiver pronto para falar...")

    # Tradução da palavra via googletrans
    traducao_correta = translator.translate(
        palavra, src="pt", dest="en"
    ).text.lower()

    # Gravação do áudio com sounddevice e scipy
    print(f"🔴 GRAVANDO ({duracao_gravacao}s)... Fale agora!")
    audio_dados = sd.rec(
        int(duracao_gravacao * taxa_amostragem),
        samplerate=taxa_amostragem,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    wav.write("temp.wav", taxa_amostragem, audio_dados)

    # Reconhecimento do áudio salvo com speech_recognition
    print("⏳ Processando voz...")
    resposta_usuario = ""

    try:
        with sr.AudioFile("temp.wav") as source:
            audio_file = recognizer.record(source)
            resposta_usuario = recognizer.recognize_google(
                audio_file, language="en-US"
            ).lower()
        print(f"🗣️ Você disse: \"{resposta_usuario}\"")
    except:
        print("🤖 Não entendi o que você falou.")

    # Verificação do acerto e pontuação
    if resposta_usuario == traducao_correta:
        print("✨ CORRETO! Pronúncia perfeita! (+10 pontos)")
        pontos += 10
    else:
        print(f"❌ INCORRETO! A resposta certa era: \"{traducao_correta}\"")

# Limpeza do arquivo temporário
if os.path.exists("temp.wav"):
    os.remove("temp.wav")

# Tela de Fim de Jogo
print("\n==========================================")
print(" 🏁 FIM DE JOGO! 🏁")
print(f"🏆 Pontuação Final: {pontos} de {len(palavras) * 10} pontos")
print("==========================================")