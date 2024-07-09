import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PIL import Image
from datetime import datetime

def wrap_text(text, canvas, x, y, max_width, line_height, padding):
    words = text.split()
    lines = []
    line = ""
    
    for word in words:
        if canvas.stringWidth(line + " " + word, "Helvetica", 12) <= max_width:
            line += " " + word
        else:
            lines.append(line.strip())
            line = word

    if line:
        lines.append(line.strip())

    for line in lines:
        if y < padding + line_height:  # Check if we need to create a new page
            canvas.showPage()
            canvas.setFont("Helvetica", 12)
            y = letter[1] - padding

        canvas.drawString(x, y, line)
        y -= line_height

    return y

def gerar_pdf(data, nome_arquivo, imagem_caminho):
    field_labels = {
        'nome_cliente': 'Nome do Cliente',
        'previsao_entrega': 'Previsão de Entrega',
        'orcamento_valido_ate': 'Orçamento Válido Até',
        'formas_pagamento': 'Formas de Pagamento',
        'nome_vendedor': 'Nome do Vendedor',
        'nome_arquivo': 'Nome do Arquivo'
    }

    product_labels = {
        'nome_item': 'Nome do Item',
        'ambiente': 'Ambiente',
        'largura': 'Largura',
        'altura': 'Altura',
        'cor': 'Cor',
        'quantidade': 'Quantidade',
        'descricao': 'Descrição',
        'componentes': 'Componentes',
        'valor_total': 'Valor Total'
    }

    c = canvas.Canvas(f"{nome_arquivo}.pdf", pagesize=letter)
    c.setFont("Helvetica", 12)

    # Carregar a imagem usando PIL para obter suas dimensões
    img = Image.open(imagem_caminho)
    img_width, img_height = img.size

    # Definir o tamanho máximo da imagem no PDF
    max_width = 200
    max_height = 200

    # Calcular a escala para redimensionar a imagem mantendo a proporção
    scale = min(max_width / img_width, max_height / img_height)
    image_width = int(img_width * scale)
    image_height = int(img_height * scale)

    # Centralizar a imagem no topo
    page_width, page_height = letter
    image_x = 50
    image_y = page_height - image_height - 50  # 50 unidades de margem do topo

    c.drawImage(imagem_caminho, image_x, image_y, width=image_width, height=image_height)

    # Adicionar informações de contato no cabeçalho
    contact_info = [
        "ENDEREÇO: Rua São José, 26, Urca (Justinópolis), Ribeirão das Neves, 33933-490",
        "CNPJ: 27.182.292/0001-87",
        "EMAIL: brsvidross@gmail.com",
        "TELEFONE: (31) 98677-0422",
        "INSTAGRAM: @brsvidros"
    ]

    contact_x = image_x + image_width + 20
    contact_y = page_height - 70

    for info in contact_info:
        if "ENDEREÇO" in info:
            y_address = wrap_text(info, c, contact_x, contact_y, 250, 14, 0)
            contact_y = y_address
        else:
            c.drawString(contact_x, contact_y, info)
            contact_y -= 14  # Ajuste o espaçamento entre as linhas

    # Data do documento
    current_date = datetime.now().strftime("%d/%m/%Y")
    c.drawRightString(page_width - 50, page_height - 70, current_date)

    # Posicionar o texto abaixo da imagem com espaço
    padding = 30  # Ajusta a posição do texto para ficar abaixo da imagem com um espaçamento de 30 unidades
    y = image_y - padding - 50  # Ajustar para espaço extra devido ao cabeçalho

    c.drawString(100, y, "Orçamento Financeiro")
    y -= padding

    # Adicionar dados do cliente e orçamento
    for key, value in data.items():
        if key != 'produtos':
            label = field_labels.get(key, key)  # Obter o rótulo personalizado ou usar a chave se não estiver no dicionário
            c.drawString(100, y, f"{label}: {value}")
            y -= padding

    y -= padding  # Espaço extra antes da lista de produtos

    total_valor = 0  # Inicializa a soma dos valores dos produtos

    # Adicionar lista de produtos
    for product in data.get('produtos', []):
        if y < padding + 150:  # Check if we need to create a new page
            c.showPage()
            c.setFont("Helvetica", 12)
            y = letter[1] - padding

        y -= padding
        for key, value in product.items():
            label = product_labels.get(key, key)  # Obter o rótulo personalizado ou usar a chave se não estiver no dicionário
            if key == 'descricao':  # Descrição precisa ser tratada com wrap_text
                y = wrap_text(f"{label}: {value}", c, 100, y, 400, padding, padding)
            else:
                c.drawString(120, y, f"{label}: {value}")
                y -= padding
                if key == 'valor_total':
                    total_valor += float(value)  # Soma o valor total do produto
        y -= padding  # Espaço extra entre produtos

        # Adicionar uma linha horizontal para separar os produtos
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.line(90, y + 10, 520, y + 10)
        y -= padding  # Espaço para a linha

    # Adicionar o preço total ao final
    y -= padding  # Espaço extra antes do total
    c.drawString(100, y, f"Preço Total: {total_valor:.2f}")

    c.save()
    print("PDF gerado com sucesso!")

def main():
    # Caminho para o arquivo JSON
    json_file_path = 'data.json'
    # Caminho para a imagem
    imagem_caminho = 'logoVidros.jpg'  # Ajuste para o caminho correto da imagem

    # Leitura dos dados do arquivo JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

            nome_arquivo = data.get('nome_arquivo')
            gerar_pdf(data, nome_arquivo, imagem_caminho)

    except FileNotFoundError:
        print(f"Arquivo {json_file_path} não encontrado!")

if __name__ == "__main__":
    main()
