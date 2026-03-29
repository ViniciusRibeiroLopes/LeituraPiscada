import cv2
import mediapipe as mp
import pyautogui
import time
import math

# Inicializar o MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Constantes para a lógica de piscada
EAR_THRESHOLD = 0.22 # Limiar de proporção para definir se o olho está fechado (ajuste se necessário)
CLOSED_TIME_THRESHOLD = 1.5 # Tempo em segundos com os olhos fechados para ativar o comando

# Indices dos pontos de referência (landmarks) do MediaPipe para os olhos
# Baseado na topologia do Face Mesh (468 landmarks)
# Olho esquerdo (visto pela câmera)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
# Olho direito (visto pela câmera)
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def euclidean_distance(point1, point2):
    """Calcula a distância euclidiana entre dois pontos 2D."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_ear(eye_landmarks, all_landmarks, frame_width, frame_height):
    """Calcula o Eye Aspect Ratio (EAR) de um olho específico para detectar fechamento."""
    # Extrair as coordenadas 2D dos pontos do olho
    points = []
    for idx in eye_landmarks:
        landmark = all_landmarks.landmark[idx]
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        points.append((x, y))
    
    # O EAR é calculado comparando as distâncias verticais do olho com a distância horizontal.
    # A ordem dos landmarks na lista é contínua em volta do olho:
    # 0 = canto interno, 3 = canto externo
    # 1, 2 = pontos superiores
    # 4, 5 = pontos inferiores (no caso invertidos, mas de forma geral as relativas estão corretas)
    
    v1 = euclidean_distance(points[1], points[5])
    v2 = euclidean_distance(points[2], points[4])
    h = euclidean_distance(points[0], points[3])
    
    if h == 0:
        return 0
    
    # A fórmula do EAR
    ear = (v1 + v2) / (2.0 * h)
    return ear

def main():
    # Inicializar a captura de vídeo da webcam
    # (O ID 0 costuma ser a webcam principal em notebooks)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erro ao abrir a webcam. Verifique se ela está conectada ou sendo usada por outro app.")
        return

    print("Iniciando LeituraPisca... Pressione 'q' na janela de vídeo para encerrar.")
    print(f"Limiar de tempo para ativação: {CLOSED_TIME_THRESHOLD} segundos.")

    eyes_closed_start_time = None
    command_executed = False

    while True:
        success, frame = cap.read()
        if not success:
            print("Falha ao ler o frame da webcam.")
            break

        # Espelhar a imagem horizontalmente para visualização intuitiva (opcional)
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        
        # O MediaPipe requer que a imagem esteja no formato de cor RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Processar a imagem para detectar as malhas faciais
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Calcular o EAR (aspect ratio) para os olhos esquerdo e direito
                left_ear = calculate_ear(LEFT_EYE, face_landmarks, frame_width, frame_height)
                right_ear = calculate_ear(RIGHT_EYE, face_landmarks, frame_width, frame_height)
                
                # Fazer uma média para estabilizar, já que ambos devem fechar simultaneamente
                avg_ear = (left_ear + right_ear) / 2.0
                
                # Exibir EAR na tela para calibração e debug
                cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Lógica principal de tempo
                if avg_ear < EAR_THRESHOLD:
                    # Se os olhos acabaram de fechar, marca o tempo de início
                    if eyes_closed_start_time is None:
                        eyes_closed_start_time = time.time()
                        command_executed = False
                    
                    elapsed_time = time.time() - eyes_closed_start_time
                    cv2.putText(frame, f"Olhos fechados: {elapsed_time:.1f}s", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    # Se o tempo passou do limiar e o comando ainda não foi rodado
                    if elapsed_time >= CLOSED_TIME_THRESHOLD and not command_executed:
                        print("Piscada longa (2s) confirmada! Simulando 'Page Down'...")
                        
                        # Simula a tecla pressionada no sistema (funciona pro app em foco)
                        pyautogui.press('pagedown')
                        command_executed = True
                        
                        # Reseta o timer para que, se o usuário continuar de olhos fechados, 
                        # não fique ativando em loop alucinante. Ele precisará abrir e fechar novamente
                        # ou esperar mais 2 segundos se preferirmos continuar passando a página.
                        eyes_closed_start_time = time.time() 

                else:
                    # Olhos estão abertos ou voltaram a abrir
                    eyes_closed_start_time = None
                    command_executed = False
                    cv2.putText(frame, "Olhos Abertos", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    
        else:
            # Nenhum rosto foi detectado no frame
            eyes_closed_start_time = None
            command_executed = False
            cv2.putText(frame, "Nenhum rosto detectado", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Mostrar o feed de vídeo em uma janela do OpenCV
        cv2.imshow('LeituraPisca - Webcam', frame)

        # Verifica se o usuário pressionou 'q' para sair do stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fechar graciosamente e liberar a câmera e janelas
    cap.release()
    cv2.destroyAllWindows()
    face_mesh.close()

if __name__ == "__main__":
    # Opcional: remover o fail-safe apenas se causar problemas acidentais 
    # (pyautogui fecha no failsafe se o mouse for bruscamente pro canto da tela)
    pyautogui.FAILSAFE = False
    
    print("---------------------------------------------------------")
    print("O script iniciará a captura de vídeo.")
    print("Mantenha o leitor de PDF em primeiro plano (foco atual).")
    print("O botão 'Page Down' será simulado quando você passar 2")
    print("segundos ininterruptos de olhos fechados.")
    print("---------------------------------------------------------")
    
    # Inicia as operações principais
    main()
