import cv2
import os
import sys
import time
import msvcrt
import numpy as np
import random
import math
import threading
import logging
from flask import Flask, render_template_string, request

# Ocultar os logs do Flask no terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

latest_frame = None
latest_timestamp = 0
frame_lock = threading.Lock()

# HTML + JS com Pipeline Concorrente (até 3 pedidos em simultâneo)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Câmara Web ASCII HD 15 FPS</title>
    <style>
        body { background: #111; color: #0f0; font-family: monospace; text-align: center; margin: 0; padding: 20px; }
        video, canvas { display: none; }
        .status { margin-top: 20px; font-size: 1.2em; }
    </style>
</head>
<body>
    <h2>Transmissão Concorrente HD</h2>
    <div class="status" id="status">A solicitar acesso à câmara...</div>
    <video id="video" autoplay playsinline></video>
    <canvas id="canvas" width="480" height="360"></canvas>

    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const context = canvas.getContext('2d');
        const status = document.getElementById('status');
        let inflight = 0;
        const maxInflight = 3;

        navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: "environment", width: { ideal: 640 }, height: { ideal: 480 } } 
        })
        .then(stream => {
            video.srcObject = stream;
            status.innerText = "Câmara HD LIGADA! Transmissão 15 FPS ativa.";
            setInterval(sendFrame, 40);
        })
        .catch(err => {
            status.innerText = "Erro ao aceder à câmara: " + err;
        });

        function sendFrame() {
            if (video.readyState === video.HAVE_ENOUGH_DATA && inflight < maxInflight) {
                inflight++;
                context.drawImage(video, 0, 0, 480, 360);
                
                canvas.toBlob(blob => {
                    if (!blob) { inflight--; return; }
                    const ts = Date.now();
                    fetch('/upload?t=' + ts, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/octet-stream' },
                        body: blob
                    })
                    .then(() => { inflight--; })
                    .catch(() => { inflight--; });
                }, 'image/jpeg', 0.65);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/upload', methods=['POST'])
def upload():
    global latest_frame, latest_timestamp
    t_str = request.args.get('t', '0')
    try:
        ts = int(t_str)
    except ValueError:
        ts = 0

    img_bytes = request.data
    if img_bytes:
        with frame_lock:
            if ts >= latest_timestamp:
                np_arr = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                if img is not None:
                    latest_frame = img
                    latest_timestamp = ts
    return ('', 204)

def run_flask():
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False, use_reloader=False)

# Escala de 6 níveis
CHAR_ARRAY = np.array([" ", "º", "*", "a", "%", "#"])
VERDE_ANSI_BASE = np.array([14, 161, 19], dtype=np.float32)

def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    os.system("") 
    os.system('cls')

    fonte_camera = "WEB"  # "WEB" para o telemóvel, "LOCAL" para a câmara do PC
    cap_local = None

    largura_maxima_mono = 1000
    largura_maxima_cor = 350  
    
    limiar_contraste = 20 
    limiar_saturacao = 80     
    modo_cor = False          
    fator_zoom = 1.0  
    fator_aspecto_fonte = 0.43  
    TEMPO_POR_FRAME = 1.0 / 15.0  

    print("\n\033[36mAguardando conexão do telemóvel no porto 5000 (ou pressione 'T' para câmara local)...\033[0m\n")

    proximo_frame_tempo = time.perf_counter()

    glitch_ativo = False
    glitch_frames_restantes = 0
    glitch_frames_totais = 0
    g_centro_r, g_centro_c = 0, 0
    g_raio_base = 0.0

    try:
        while True:
            tempo_atual = time.perf_counter()
            if tempo_atual < proximo_frame_tempo:
                time.sleep(0.002)
                continue
                
            proximo_frame_tempo = tempo_atual + TEMPO_POR_FRAME

            frame = None
            if fonte_camera == "WEB":
                with frame_lock:
                    if latest_frame is not None:
                        frame = latest_frame.copy()
            else:
                if cap_local is not None and cap_local.isOpened():
                    ret_c, frame_c = cap_local.read()
                    if ret_c and frame_c is not None:
                        frame = cv2.flip(frame_c, 1)

            if frame is None:
                continue

            largura_maxima_alvo = largura_maxima_cor if modo_cor else largura_maxima_mono

            try:
                t_cols, t_rows = os.get_terminal_size()
                largura_alvo = t_cols - 1
                altura_maxima = t_rows - 3  
                if largura_alvo > largura_maxima_alvo: 
                    largura_alvo = largura_maxima_alvo
            except OSError:
                largura_alvo = 120
                altura_maxima = 35

            if fator_zoom > 1.0:
                h_orig, w_orig = frame.shape[:2]
                novo_h = int(h_orig / fator_zoom)
                novo_w = int(w_orig / fator_zoom)
                inicio_y = (h_orig - novo_h) // 2
                inicio_x = (w_orig - novo_w) // 2
                frame = frame[inicio_y:inicio_y + novo_h, inicio_x:inicio_x + novo_w]
            elif fator_zoom < 1.0:
                h_orig, w_orig = frame.shape[:2]
                pad_y = int((h_orig / fator_zoom - h_orig) / 2)
                pad_x = int((w_orig / fator_zoom - w_orig) / 2)
                frame = cv2.copyMakeBorder(frame, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_CONSTANT, value=[0, 0, 0])

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            gray_16 = gray.astype(np.int16)
            diff_x = np.abs(gray_16[:, 1:] - gray_16[:, :-1])
            diff_x = np.pad(diff_x, ((0,0), (0,1)), mode='constant')
            diff_y = np.abs(gray_16[1:, :] - gray_16[:-1, :])
            diff_y = np.pad(diff_y, ((0,1), (0,0)), mode='constant')
            
            contraste_puro = np.uint8(np.clip(diff_x + diff_y, 0, 255))
            contraste_puro = cv2.normalize(contraste_puro, None, 0, 255, cv2.NORM_MINMAX)
            
            kernel = np.ones((2,2), np.uint8)
            contraste_puro = cv2.dilate(contraste_puro, kernel, iterations=1)
            
            h, w = contraste_puro.shape
            aspect_ratio = h / w
            altura_alvo = int(largura_alvo * aspect_ratio * fator_aspecto_fonte)
            
            if altura_alvo > altura_maxima:
                altura_alvo = altura_maxima
                largura_alvo = int((altura_alvo / fator_aspecto_fonte) / aspect_ratio)

            if largura_alvo < 5 or altura_alvo < 5:
                continue
                
            resized = cv2.resize(contraste_puro, (largura_alvo, altura_alvo), interpolation=cv2.INTER_LINEAR)
            
            if not glitch_ativo:
                if random.random() < 0.05:
                    tam_bloco_c = random.randint(6, max(8, int(largura_alvo * 0.05)))
                    g_raio_base = tam_bloco_c / 2.0
                    zona_r = random.choice(['topo', 'centro', 'fundo'])
                    if zona_r == 'topo':
                        g_centro_r = random.randint(0, int(altura_alvo * 0.2))
                    elif zona_r == 'fundo':
                        g_centro_r = random.randint(int(altura_alvo * 0.8), altura_alvo - 1)
                    else:
                        g_centro_r = random.randint(0, altura_alvo - 1)
                        
                    if zona_r == 'centro' and random.random() < 0.8:
                        g_centro_c = random.choice([random.randint(0, int(largura_alvo * 0.2)), 
                                                    random.randint(int(largura_alvo * 0.8), largura_alvo - 1)])
                    else:
                        g_centro_c = random.randint(0, largura_alvo - 1)

                    glitch_ativo = True
                    glitch_frames_totais = random.randint(5, 9)
                    glitch_frames_restantes = glitch_frames_totais

            t1 = max(1, int(limiar_contraste * 0.4))
            t2 = max(2, int(limiar_contraste * 0.8))
            t3 = int(limiar_contraste * 1.2)
            t4 = int(limiar_contraste * 1.6)
            t5 = int(limiar_contraste * 2.0)
            
            frames_decorridos = glitch_frames_totais - glitch_frames_restantes

            indices = np.digitize(resized, [t1, t2, t3, t4, t5])
            ascii_matrix = CHAR_ARRAY[indices]

            if glitch_ativo:
                r_coords = np.arange(altura_alvo)[:, None]
                c_coords = np.arange(largura_alvo)[None, :]
                dc = c_coords - g_centro_c
                dr = (r_coords - g_centro_r) / fator_aspecto_fonte
                distancia_centro = np.sqrt(dc**2 + dr**2)
                angulo = np.arctan2(dr, dc)
                deformacao_ruido = np.sin(angulo * 6.0 + frames_decorridos) * (g_raio_base * 0.20)
                raio_irregular = g_raio_base + deformacao_ruido
                
                glitch_mask = distancia_centro <= raio_irregular
                glitch_chars = np.random.choice(["1", "0"], size=(altura_alvo, largura_alvo))
                ascii_matrix[glitch_mask] = glitch_chars[glitch_mask]

            if modo_cor:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                saturacao = hsv[:, :, 1].astype(np.float32)
                
                sat_diff = np.maximum(0.0, saturacao - limiar_saturacao)
                fator_sat = np.clip(sat_diff / 40.0, 0.0, 1.0) ** 0.4
                fator_sat = fator_sat[:, :, None]
                
                verde_matrix = np.tile(VERDE_ANSI_BASE, (frame.shape[0], frame.shape[1], 1))
                frame_misturado = ((1.0 - fator_sat) * verde_matrix + fator_sat * frame.astype(np.float32)).astype(np.uint8)
                
                frame_cor_resized = cv2.resize(frame_misturado, (largura_alvo, altura_alvo), interpolation=cv2.INTER_LINEAR)
                sat_resized = cv2.resize(saturacao, (largura_alvo, altura_alvo), interpolation=cv2.INTER_LINEAR)
                
                b_mat = frame_cor_resized[:, :, 0]
                g_mat = frame_cor_resized[:, :, 1]
                r_mat = frame_cor_resized[:, :, 2]
                
                rows = []
                for r in range(altura_alvo):
                    line_pieces = []
                    last_was_native = False
                    for red, green, blue, sat_val, ch in zip(r_mat[r], g_mat[r], b_mat[r], sat_resized[r], ascii_matrix[r]):
                        if sat_val <= limiar_saturacao:
                            if not last_was_native:
                                line_pieces.append(f"\033[32m{ch}")
                                last_was_native = True
                            else:
                                line_pieces.append(ch)
                        else:
                            line_pieces.append(f"\033[38;2;{red};{green};{blue}m{ch}")
                            last_was_native = False
                    rows.append("".join(line_pieces))
                ascii_frame = "\n".join(rows)
            else:
                ascii_frame = "\n".join("".join(row) for row in ascii_matrix)

            if glitch_ativo:
                glitch_frames_restantes -= 1
                if glitch_frames_restantes <= 0:
                    glitch_ativo = False
            
            if modo_cor:
                sys.stdout.write("\033[H" + ascii_frame)
            else:
                sys.stdout.write("\033[H\033[32m" + ascii_frame)

            label_fonte = "PHONE (WEB)" if fonte_camera == "WEB" else "PC WEBCAM"
            barra_status = (
                f"\n\033[J\033[36m███ CYBERPUNK HD 15 FPS ███ "
                f"\033[33m[ CAM: {label_fonte} ] "
                f"\033[32m[ COLS: {largura_alvo} ] "
                f"\033[34m[ CONTR: {limiar_contraste} ] "
                f"\033[31m[ ZOOM: {fator_zoom:.1f}x ] "
                f"\033[35m[ STRETCH: {fator_aspecto_fonte:.2f} ] "
                f"\033[36m[ COR: {'ON ' if modo_cor else 'OFF'} ] "
                f"\033[33m[ SAT_LIM: {limiar_saturacao} ]\033[0m"
            )
            sys.stdout.write(barra_status)
            sys.stdout.flush()

            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in (b'\x00', b'\xe0'):
                    key_ext = msvcrt.getch()
                    if key_ext == b'H':
                        fator_zoom = min(4.0, round(fator_zoom + 0.1, 1))
                    elif key_ext == b'P':
                        fator_zoom = max(0.5, round(fator_zoom - 0.1, 1))
                else:
                    if key in (b't', b'T'):  # Alternar fonte de câmara (PHONE <-> PC)
                        if fonte_camera == "WEB":
                            cap_test = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                            if cap_test.isOpened():
                                ret_t, _ = cap_test.read()
                                if ret_t:
                                    cap_local = cap_test
                                    cap_local.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                                    cap_local.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                                    fonte_camera = "LOCAL"
                                else:
                                    cap_test.release()
                            else:
                                cap_test.release()
                        else:
                            if cap_local is not None:
                                cap_local.release()
                                cap_local = None
                            fonte_camera = "WEB"
                    elif key in (b'c', b'C'):
                        modo_cor = not modo_cor
                    elif key in (b'f', b'F'):
                        limiar_saturacao = min(250, limiar_saturacao + 5)
                    elif key in (b'v', b'V'):
                        limiar_saturacao = max(0, limiar_saturacao - 5)
                    elif key in (b'w', b'W'):
                        limiar_contraste = max(2, limiar_contraste - 2)
                    elif key in (b's', b'S'):
                        limiar_contraste = min(100, limiar_contraste + 2)
                    elif key in (b'e', b'E'):
                        fator_aspecto_fonte = min(1.0, round(fator_aspecto_fonte + 0.02, 2))
                    elif key in (b'd', b'D'):
                        fator_aspecto_fonte = max(0.1, round(fator_aspecto_fonte - 0.02, 2))
                    elif key in (b'q', b'Q'):
                        break

    except KeyboardInterrupt:
        pass
    finally:
        if cap_local is not None:
            cap_local.release()
        print("\n\033[J\033[0mFluxo encerrado.")

if __name__ == "__main__":
    main()