import tkinter as tk
from tkinter import simpledialog, messagebox
#from graphviz import Digraph
from animais import rede_semantica
from perguntas import mapeamento_palavras_chave

#g = Digraph('Ontologia', filename='ontologia', format='pdf')
#g.attr(rankdir='LR', size='15')

##########################################################################################################################################################################

def inferencia(animal, propriedade):
    # Buscar diretamente na rede semântica
    if propriedade in rede_semantica[animal]:
        return rede_semantica[animal][propriedade]
    
    # Se não encontrarmos diretamente, vamos tentar encontrar através de relações
    if "é_um" in rede_semantica[animal]:
        return inferencia(rede_semantica[animal]["é_um"], propriedade)

    return None

def responder_pergunta(pergunta):
    pergunta = pergunta.lower()
    animal_escolhido = None
    propriedade_escolhida = None

    # Encontra um animal específico na pergunta
    for animal in rede_semantica.keys():
        if animal.lower() in pergunta:
            animal_escolhido = animal
            print("Animal: "+ animal_escolhido)
            break

    # Encontra uma propriedade específica na pergunta
    for palavra_chave, propriedade in mapeamento_palavras_chave.items():
        if palavra_chave in pergunta:
            propriedade_escolhida = propriedade
            print("Propriedade: "+ propriedade_escolhida)
            break

    # Animal não encontrado ou não fornecida
    if animal_escolhido is None:
        return "Não possuo informações sobre o animal especificado"
    
    # Propriedade não encontrada ou não fornecida
    if propriedade is None:
        return f"Não tenho informações específicas sobre o {animal}."

    # Responde a perguntas sobre um animal específico
    return responder_pergunta_especifica(animal_escolhido, propriedade_escolhida)

def responder_pergunta_especifica(animal, propriedade): # Responde a perguntas específicas sobre um animal
    criar_ontologia_pergunta(animal, propriedade)
    resposta_especifica = inferencia(animal, propriedade)

    if resposta_especifica:
        return f"O {animal} {propriedade} {resposta_especifica}."
    else:
        return f"Não tenho informações sobre {propriedade} do {animal}."
    
def gui_perguntar_textbox():
    # Obtendo o conteúdo da textbox
    global resposta_label
    pergunta = pergunta_entry.get()
    if pergunta:
        resposta = responder_pergunta(pergunta)
        resposta_label.config(text=resposta)

##########################################################################################################################################################################

def find_animals_by_property(termo, value):
    # Verifica no mapeamento de propriedades
    propriedade = mapeamento_palavras_chave.get(termo, termo) # Verifica se tem a propriedade x tem um correspondete y, se não tiver y usa x para a busca

    matching_animals = []
    for animal, properties in rede_semantica.items():
        if propriedade in properties:
            if isinstance(properties[propriedade], list):
                if value in properties[propriedade]:
                    matching_animals.append(animal)
            else:
                if properties[propriedade] == value:
                    matching_animals.append(animal)
    return matching_animals

def gui_find_animals_by_property():
    propriedade = simpledialog.askstring("Buscar Animais", "Digite a propriedade:")
    valor = simpledialog.askstring("Buscar Animais", "Digite o valor da propriedade:")
    propriedade = propriedade.lower()
    valor = valor.lower()

    if propriedade and valor:
        animais_encontrados = find_animals_by_property(propriedade, valor)
        messagebox.showinfo("Animais Encontrados", '\n'.join(animais_encontrados) if animais_encontrados else "Nenhum animal encontrado.")

##########################################################################################################################################################################

def comparar_animais(animal1, animal2):
    if animal1 not in rede_semantica or animal2 not in rede_semantica:
        return "Um ou ambos os animais não estão na base de dados."

    propriedades_animal1 = rede_semantica.get(animal1, {})
    propriedades_animal2 = rede_semantica.get(animal2, {})
    diferenças = []

    for prop, valor in propriedades_animal1.items():
        if prop in propriedades_animal2:
            if propriedades_animal2[prop] != valor:
                diferenças.append(f"{animal1} {prop} {valor}, enquanto {animal2} {prop} {propriedades_animal2[prop]}.")
        else:
            diferenças.append(f"{animal1} tem {prop} como {valor}, enquanto {animal2} não tem informação sobre '{prop}'.")

    for prop, valor in propriedades_animal2.items():
        if prop not in propriedades_animal1:
            diferenças.append(f"{animal2} tem {prop} como {valor}, enquanto {animal1} não tem informação sobre '{prop}'.")

    return "\n".join(diferenças)

def gui_comparar_animais():
    animal1 = simpledialog.askstring("Comparar", "Digite o nome do primeiro animal:").lower()
    animal2 = simpledialog.askstring("Comparar", "Digite o nome do segundo animal:").lower()
    if animal1 and animal2:
        resultado = comparar_animais(animal1, animal2)
        messagebox.showinfo("Comparação", resultado)

##########################################################################################################################################################################

def criar_ontologia(rede_semantica):
    g = Digraph('G', filename='ontologia.gv')
    g.attr(rankdir='LR', size='15')

    # Adicionando os nós
    for animal in rede_semantica:
        g.node(animal)

    # Adicionando as arestas
    for animal, propriedades in rede_semantica.items():
        for propriedade, valor in propriedades.items():
            # Verificando se o valor é uma lista
            if isinstance(valor, list):
                for v in valor:
                    g.edge(animal, v, label=propriedade)
            else:
                g.edge(animal, valor, label=propriedade)

    g.attr(ranksep='5')
    g.view()

def gui_visualizar_rede():
    criar_ontologia(rede_semantica)
    messagebox.showinfo("Info", "Ontologia visualizada em um arquivo externo.")

def criar_ontologia_pergunta(animal, propriedade):
    global g  # Declare que estamos usando o grafo global

    g.node(animal, color='blue')  # Colorir o nó do animal de azul

    if propriedade in rede_semantica[animal]:
        valor = rede_semantica[animal][propriedade]
        # Verifica se o valor é uma lista
        if isinstance(valor, list):
            for v in valor:
                g.node(v, color='green')  # Colorir os nós dos valores de verde
                g.edge(animal, v, label=propriedade)
        else:
            g.node(valor, color='green')  # Colorir o nó do valor de verde
            g.edge(animal, valor, label=propriedade)
    
    g.view()

##########################################################################################################################################################################

def listar_animais():
    nomes_animais = [item for item in rede_semantica.keys()]
    messagebox.showinfo("Animais", '\n'.join(nomes_animais))

def listar_propriedades():
    # Inverter o dicionário para agrupar por tipo
    tipo_para_termos = {}
    for termo, tipo in mapeamento_palavras_chave.items():
        if tipo not in tipo_para_termos:
            tipo_para_termos[tipo] = []
        tipo_para_termos[tipo].append(termo)

    # Formatar a string para exibição
    formatted_terms = ""
    for tipo, termos in tipo_para_termos.items():
        formatted_terms += f"{tipo}:\n" + ', '.join(termos) + "\n\n"

    messagebox.showinfo("Termos aceitos:", formatted_terms)

##########################################################################################################################################################################

def on_focus_in(event):
    """Função para lidar quando o campo de entrada recebe foco."""
    if pergunta_entry.get() == "insira sua pergunta aqui":
        pergunta_entry.delete(0, "end")  # Deleta todo o texto no campo
        pergunta_entry.config(fg="#006400")  # Muda a cor do texto para verde escuro

def on_focus_out(event):
    """Função para lidar quando o campo de entrada perde o foco."""
    if not pergunta_entry.get():
        pergunta_entry.insert(0, "insira sua pergunta aqui")  # Insere o texto do placeholder
        pergunta_entry.config(fg="gray")  # Muda a cor do texto para cinza

def main_gui():
    global resposta_label
    window = tk.Tk()
    window.title("Interface Gráfica para Análise de Animais")
    window.geometry('500x370')
    window.configure(bg="#808080")  # Definindo a cor de fundo da janela para cinza

    lbl = tk.Label(window, text="Analisador de Animais", bg="#808080")  # Cor de fundo do label correspondente à da janela
    lbl.pack(pady=10)

    # Frame para agrupar a textbox e o botão
    frame = tk.Frame(window, bg="#808080")  # Cor de fundo do frame correspondente à da janela
    frame.pack(pady=10)

    # Adicionando a textbox com largura ajustada
    global pergunta_entry
    pergunta_entry = tk.Entry(frame, width=25, fg="gray")  # Definindo a cor inicial do texto para cinza
    pergunta_entry.insert(0, "insira sua pergunta aqui")  # Adicionando texto padrão
    pergunta_entry.bind("<FocusIn>", on_focus_in)  # Bind do evento de foco
    pergunta_entry.bind("<FocusOut>", on_focus_out)  # Bind do evento de perder foco
    pergunta_entry.grid(row=0, column=0, padx=5)  # posicionado na primeira linha, primeira coluna

    # Botão de "Perguntar" à direita da textbox
    btn_perguntar_textbox = tk.Button(frame, text="Perguntar", command=gui_perguntar_textbox)
    btn_perguntar_textbox.grid(row=0, column=1)  # Posicionado na primeira linha, segunda coluna

    # Adicionando o label para exibir a resposta
    resposta_label = tk.Label(window, text="", wraplength=350, width=60, height=2, bd=1, relief="solid", fg="black")  # Wraplength para quebrar a linha se o texto for muito longo
    resposta_label.pack(pady=10)
    resposta_label.config(fg="blue", bg="white")

    btn_comparar = tk.Button(window, text="Comparar dois animais", command=gui_comparar_animais)
    btn_comparar.pack(fill=tk.X, padx=50, pady=10)

    # Botão para ver toda a ontologia
    btn2 = tk.Button(window, text="Visualizar rede semântica completa", command=gui_visualizar_rede)
    btn2.pack(fill=tk.X, padx=50, pady=10)

    # Colocando os botões de 
    buttons_frame = tk.Frame(window)
    buttons_frame.pack(fill=tk.X, padx=50, pady=(0, 10))

    # Botão de "Animais"
    btn_animais_textbox = tk.Button(buttons_frame, text="Ver os Animais", command=listar_animais)
    btn_animais_textbox.pack(side=tk.LEFT, expand=True, fill=tk.X)

    # Botão de "Ver Termos"
    btn_ver_prop = tk.Button(buttons_frame, text="Ver as propriedades", command=listar_propriedades)
    btn_ver_prop.pack(side=tk.LEFT, expand=True, fill=tk.X)

    # Botão de buscar o animal pela propriedade
    btn_buscar_animais = tk.Button(window, text="Buscar Animais por Propriedade", command=gui_find_animals_by_property)
    btn_buscar_animais.pack(fill=tk.X, padx=50, pady=10)

    btn3 = tk.Button(window, text="Sair", command=window.quit)
    btn3.pack(fill=tk.X, padx=50)
   
    window.mainloop()

if __name__ == '__main__':
    main_gui()
    