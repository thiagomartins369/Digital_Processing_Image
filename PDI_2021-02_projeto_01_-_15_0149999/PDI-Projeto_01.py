# PROCESSAMENTO DIGITAL DE IMAGEM - Prof. Marcus Chaffim | UnB - FGA
# Projeto 01 - Adaptação ao brilho e discriminação

# Importando as bibliotecas principais que serão utilizadas no projeto
import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

# Geração das imagens para os procedimentos do experimento
x, y = (1024, 1024) # Criando as variáveis espaciais com as dimensões (1024x1024) da imagem
img = np.zeros((x,y),np.uint8) # Criando uma matrix (1024x1024) com tipos inteiros de 8 bits
borda_quadrados = 8 # Atribuindo o valor do tamanho da borda dos quadrados gerados
intensidade_inc = 1 # Variável da incrementação da intensidade do brilho
delta_I = np.array([], dtype=np.uint8) # Variação da incrementação do brilho
intensidade_detect = np.array([0], dtype=np.uint8) # O nível de intesidade de brilho detectado na iteração
count = 0 # Variavel para medição incremental nos quadrados formados

# O experimento - Iteração
for i in range(255): # início da iteração
    for largura in range(borda_quadrados*intensidade_inc, x-intensidade_inc*borda_quadrados): 
        for altura in range(borda_quadrados*intensidade_inc, y-intensidade_inc*borda_quadrados):
            img[largura, altura] = i # Imagem atual vai receber o valor i de itensidade

    # Apresenta a imagem    
    cv2.imshow('imagem',img)
    print("Valor de intensidade do pixel: "+str(i+1))
    decision = cv2.waitKey(0) # Aguarda com que a tecla 1 seja pressionada passando para próximo quadrado
    if chr(decision & 255) == '1':
        delta_I = np.append(delta_I, i-count) 
        intensidade_detect = np.append(intensidade_detect, i)
        intensidade_inc = intensidade_inc + 1
        count = i
# Apresentação da imagem de iteração
cv2.destroyAllWindows()
file_name = input("Nome do arquivo para salvar a imagem de teste: ")
cv2.imwrite(file_name + '.jpg',img)
cv2.destroyAllWindows()

# Interpolação dos coeficientes obtidos
interpol_coeff_delta_I = np.polyfit(np.arange(delta_I.shape[-1]),delta_I, 3) #interpolação com polinomio de ordem 3
interpol_coeff_intensity = np.polyfit(np.arange(intensidade_detect.shape[-1]),intensidade_detect, 3) #interpolação com polinomio de ordem 3
interpolation_delta_I = np.polyval(interpol_coeff_delta_I,np.arange(delta_I.shape[-1]))
interpolation_intensity = np.polyval(interpol_coeff_intensity, np.arange(intensidade_detect.shape[-1]))


# Plotagem dos Gráficos 
fig, (ax1, ax2) = plt.subplots(1, 2)
# Gráfico da variação do delta da intencidade 
ax1.plot(np.arange(delta_I.shape[-1]), interpolation_delta_I)
ax1.set_xlim(0, delta_I.shape[-1])
ax1.set_title(r'$\Delta I$')
#Gráfico da variação de intensidade detectada
ax2.plot(np.arange(intensidade_detect.shape[-1]), interpolation_intensity)
ax2.set_title('Variação de Intensidade' r'$I$')
ax2.set_xlim(0, intensidade_detect.shape[-1])
  
fig.savefig(file_name + '.png')
plt.show()
        