import os
import sys
import cv2
import numpy as np

# =============================================================================
# 1. PARÂMETROS E CONFIGURAÇÕES DO ALGORITMO
# =============================================================================

# Caminho da imagem de entrada
CAMINHO_IMAGEM = "/home/rafa/Imagens/Eu/WhatsApp Image 2026-11-11 at 19.29.30.jpeg"

VALOR_LIMIAR = 120

# Valor atribuído aos pixels que superam o limiar (255 = Branco máximo)
VALOR_MAXIMO = 255

# Tamanho do Kernel da Suavização Gaussiana (deve ser ímpar, ex: (3,3), (5,5), (7,7))
KERNEL_GAUSSIANO = (5, 5)

# Fator de escala para redimensionar a imagem na tela e caber no monitor (original é 1600x900)
FATOR_ESCALA = 0.5


def main():
    print("=" * 70)
    print("   PIPELINE DE VISÃO COMPUTACIONAL: BINARIZAÇÃO DE IMAGEM")
    print("=" * 70)

    print(f"\n[Etapa 1] Carregando a imagem em:\n -> {CAMINHO_IMAGEM}")
    
    caminho_final = CAMINHO_IMAGEM
    if not os.path.exists(caminho_final):
        # Fallback para execucao em outros ambientes ou clone do repositorio
        caminho_fallback = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "entrada.jpeg")
        if os.path.exists(caminho_fallback):
            print(f"[AVISO] Caminho original nao encontrado. Utilizando imagem local de assets:\n -> {caminho_fallback}")
            caminho_final = caminho_fallback
        else:
            print(f"[ERRO] O arquivo nao existe no caminho especificado: {CAMINHO_IMAGEM}")
            sys.exit(1)

    imagem_colorida = cv2.imread(caminho_final)

    # Verificação simples caso a imagem não tenha sido carregada (arquivo corrompido ou sem permissão)
    if imagem_colorida is None:
        print("[ERRO] Falha ao carregar a imagem. Verifique o formato ou permissões do arquivo.")
        sys.exit(1)

    altura_orig, largura_orig, canais = imagem_colorida.shape
    print(f"[OK] Imagem carregada com sucesso! Resolução: {largura_orig}x{altura_orig} | Canais: {canais}")

   
    # variando de 0 (preto absoluto) a 255 (branco absoluto).
    print("\n[Etapa 2] Convertendo para escala de cinza (cv2.COLOR_BGR2GRAY)...")
    imagem_cinza = cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2GRAY)
    print(f"[OK] Conversão concluída. Matriz de intensidade: {imagem_cinza.shape}")

  
    print(f"\n[Etapa 3] Aplicando suavização Gaussiana (cv2.GaussianBlur, Kernel: {KERNEL_GAUSSIANO})...")
    imagem_suavizada = cv2.GaussianBlur(imagem_cinza, KERNEL_GAUSSIANO, 0)
    print("[OK] Suavização concluída com sucesso.")

    
    print(f"\n[Etapa 4] Aplicando limiarização (Threshold = {VALOR_LIMIAR}, Máximo = {VALOR_MAXIMO})...")
    _, binarizada = cv2.threshold(imagem_suavizada, VALOR_LIMIAR, VALOR_MAXIMO, cv2.THRESH_BINARY)
    _, binarizada_inv = cv2.threshold(imagem_suavizada, VALOR_LIMIAR, VALOR_MAXIMO, cv2.THRESH_BINARY_INV)
    print("[OK] Imagens binarizada (direta) e binarizada_inv (invertida) geradas.")

    print("\n[Etapa 5] Criando composição visual comparativa com np.hstack e np.vstack...")

    cinza_bgr = cv2.cvtColor(imagem_cinza, cv2.COLOR_GRAY2BGR)
    suavizada_bgr = cv2.cvtColor(imagem_suavizada, cv2.COLOR_GRAY2BGR)
    binarizada_bgr = cv2.cvtColor(binarizada, cv2.COLOR_GRAY2BGR)
    binarizada_inv_bgr = cv2.cvtColor(binarizada_inv, cv2.COLOR_GRAY2BGR)

    # Função auxiliar para desenhar uma barra de título legível no topo de cada quadrante
    def rotular(img, rotulo, cor_texto=(0, 255, 0)):
        canvas = img.copy()
        cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 80), (15, 15, 15), -1)
        cv2.putText(canvas, rotulo, (20, 52), cv2.FONT_HERSHEY_SIMPLEX, 1.05, cor_texto, 2, cv2.LINE_AA)
        return canvas

    q1_orig = rotular(imagem_colorida, "1. Imagem Original (Colorida)", (255, 255, 255))
    q2_suav = rotular(suavizada_bgr, f"2. Cinza Suavizada (Gauss {KERNEL_GAUSSIANO})", (200, 200, 200))
    q3_bin = rotular(binarizada_bgr, f"3. Binarizada (THRESH_BINARY = {VALOR_LIMIAR})", (0, 255, 255))
    q4_inv = rotular(binarizada_inv_bgr, f"4. Binarizada (THRESH_BINARY_INV = {VALOR_LIMIAR})", (0, 200, 255))

    # Composição: Linha 1 (Superior) com np.hstack
    linha_superior = np.hstack([q1_orig, q2_suav])

    # Composição: Linha 2 (Inferior) com np.hstack
    linha_inferior = np.hstack([q3_bin, q4_inv])

    # Painel completo 2x2 com np.vstack
    painel_2x2 = np.vstack([linha_superior, linha_inferior])

    # Redimensiona o painel para caber perfeitamente no monitor sem cortes
    largura_display = int(painel_2x2.shape[1] * FATOR_ESCALA)
    altura_display = int(painel_2x2.shape[0] * FATOR_ESCALA)
    painel_final = cv2.resize(painel_2x2, (largura_display, altura_display), interpolation=cv2.INTER_AREA)

    # Salva o resultado em disco
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_salvo = os.path.join(diretorio_atual, "resultado_comparativo.png")
    cv2.imwrite(caminho_salvo, painel_final)
    print(f"[OK] Painel comparativo salvo com sucesso em:\n -> {caminho_salvo}")

  
    titulo_janela = "Visao Computacional - Binarizacao de Imagem (OpenCV)"
    print(f"\n[Etapa 6] Exibindo janela de resultados: '{titulo_janela}'...")

    # Se estiver em ambiente gráfico (desktop ativo), exibe a janela normalmente
    if os.environ.get("DISPLAY"):
        try:
            cv2.namedWindow(titulo_janela, cv2.WINDOW_AUTOSIZE)
            cv2.imshow(titulo_janela, painel_final)

            print("\n>>> Pressione QUALQUER TECLA na janela para fechar o programa...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("[OK] Janelas finalizadas com sucesso.")
        except cv2.error as erro:
            print(f"[AVISO] Interface gráfica não disponível no momento: {erro}")
    else:
        print("[INFO] Variável DISPLAY não configurada (ambiente de terminal headless).")
        print("       Execute o script diretamente no terminal do seu sistema operacional para abrir a janela gráfica.")
        print(f"       A imagem processada pode ser visualizada no arquivo salvo: {caminho_salvo}")

    print("\n" + "=" * 70)
    print("   PIPELINE FINALIZADO COM SUCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    main()
