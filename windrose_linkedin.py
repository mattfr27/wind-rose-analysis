import os
import subprocess
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from windrose import WindroseAxes

# ==================================================
# CONFIGURAÇÕES
# ==================================================

ARQUIVOS = [
    '/home/mateusfernandes/Pictures/gifiguape/generatedBy_react-csv (3).csv',
    '/home/mateusfernandes/Pictures/gifiguape/generatedBy_react-csv (4).csv',
    '/home/mateusfernandes/Pictures/gifiguape/generatedBy_react-csv (5).csv',
    '/home/mateusfernandes/Pictures/gifiguape/generatedBy_react-csv (6).csv',
    '/home/mateusfernandes/Pictures/gifiguape/generatedBy_react-csv (7).csv',
    '/home/mateusfernandes/Pictures/gifiguape/generatedBy_react-csv (8).csv',
    '/home/mateusfernandes/Pictures/gifiguape/generatedBy_react-csv (9).csv',
    '/home/mateusfernandes/Pictures/gifiguape/generatedBy_react-csv (10).csv',
    '/home/mateusfernandes/Pictures/gifiguape/generatedBy_react-csv (11).csv'
]

INICIO = '2024-10-01'
FIM = '2024-12-01'

FPS = 2
PASTA_FRAMES = "frames_windrose"
VIDEO_SAIDA = "windrose_iguape_linkedin.mp4"


def direcao_cardeal(graus):
    setores = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    idx = int((graus + 22.5) // 45) % 8
    return setores[idx]


# ==================================================
# LEITURA DOS DADOS
# ==================================================

dfs = []

for arquivo in ARQUIVOS:
    print(f"Lendo: {arquivo}")
    dfs.append(pd.read_csv(arquivo, sep=';', decimal=','))

dff = pd.concat(dfs, ignore_index=True)

dff = dff[[
    'Data',
    'Hora (UTC)',
    'Vel. Vento (m/s)',
    'Dir. Vento (m/s)',
    'Raj. Vento (m/s)'
]].dropna()

dff['Hora (UTC)'] = (
    dff['Hora (UTC)']
    .astype(int)
    .astype(str)
    .str.zfill(4)
)

dff['datetime'] = pd.to_datetime(
    dff['Data'] + ' ' + dff['Hora (UTC)'],
    format='%d/%m/%Y %H%M'
)

dff = dff.sort_values('datetime')

dados = dff[
    (dff['datetime'] >= INICIO) &
    (dff['datetime'] < FIM)
].copy()

if len(dados) == 0:
    raise ValueError("Nenhum dado encontrado para o período selecionado.")

dados['dia'] = dados['datetime'].dt.date
dias = sorted(dados['dia'].unique())

print(f"Registros: {len(dados)}")
print(f"Dias: {len(dias)}")

# ==================================================
# PREPARAÇÃO DOS FRAMES
# ==================================================

os.makedirs(PASTA_FRAMES, exist_ok=True)

for f in os.listdir(PASTA_FRAMES):
    if f.endswith(".png"):
        os.remove(os.path.join(PASTA_FRAMES, f))

# ==================================================
# GERAÇÃO DOS FRAMES
# ==================================================

contador = 0

for dia in dias:

    dados_dia = dados[dados['dia'] == dia]

    if len(dados_dia) < 3:
        continue

    vel_media = dados_dia['Vel. Vento (m/s)'].mean()
    rajada_max = dados_dia['Raj. Vento (m/s)'].max()
    direcao_media = dados_dia['Dir. Vento (m/s)'].mean()
    dir_card = direcao_cardeal(direcao_media)

    fig = plt.figure(figsize=(8, 10), facecolor='white')

    ax = fig.add_subplot(
        111,
        projection='windrose'
    )

    ax.bar(
        dados_dia['Dir. Vento (m/s)'],
        dados_dia['Vel. Vento (m/s)'],
        normed=True,
        opening=0.90,
        edgecolor='white',
        linewidth=0.5,
        bins=[0, 1, 2, 3, 4, 5, 6, 8],
        cmap=plt.cm.turbo
    )

    ax.set_title(
        (
            "Dinâmica dos Ventos\n"
            "Iguape - SP\n"
            f"{dia.strftime('%d/%m/%Y')}"
        ),
        fontsize=22,
        fontweight='bold',
        pad=30
    )

    ax.set_legend(
        title='Velocidade do vento (m/s)',
        fontsize=9
    )

    fig.text(
        0.72,
        0.80,
        (
            f"Vel. média\n"
            f"{vel_media:.1f} m/s\n\n"
            f"Rajada máxima\n"
            f"{rajada_max:.1f} m/s\n\n"
            f"Direção\n"
            f"{dir_card}"
        ),
        fontsize=11,
        bbox=dict(
            facecolor='white',
            edgecolor='gray',
            alpha=0.95,
            boxstyle='round'
        )
    )

    progresso = (contador + 1) / len(dias)

    fig.text(0.14, 0.06, dias[0].strftime('%d/%m'), fontsize=10)
    fig.text(0.78, 0.06, dias[-1].strftime('%d/%m'), fontsize=10)

    ax_prog = fig.add_axes([0.23, 0.055, 0.48, 0.02])
    ax_prog.barh([0], [progresso], height=1)
    ax_prog.set_xlim(0, 1)
    ax_prog.axis('off')

    fig.text(
        0.5,
        0.02,
        'Visualização de Dados Meteorológicos • Python',
        ha='center',
        fontsize=9,
        color='gray'
    )

    arquivo_frame = os.path.join(
        PASTA_FRAMES,
        f'frame_{contador:04d}.png'
    )

    fig.savefig(
        arquivo_frame,
        dpi=250,
        facecolor='white',
        bbox_inches='tight'
    )

    plt.close(fig)

    contador += 1

    print(f"Frame {contador}/{len(dias)}")

print(f"Frames gerados: {contador}")

# ==================================================
# CRIAÇÃO DO MP4
# ==================================================

subprocess.run([
    "ffmpeg",
    "-y",
    "-framerate", str(FPS),
    "-i", f"{PASTA_FRAMES}/frame_%04d.png",
    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-crf", "18",
    VIDEO_SAIDA
], check=True)

print()
print("Vídeo criado com sucesso:")
print(VIDEO_SAIDA)
