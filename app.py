from flask import Flask, render_template, send_from_directory, request

# Inicializa o aplicativo Flask
# Initialize the Flask application
app = Flask(__name__)

# Serve robots.txt e sitemap.xml da pasta static
# Serve robots.txt and sitemap.xml from the static folder
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

# Rota principal para a página inicial
# Main route for the home page
@app.route('/')
def index():
    """
    Renderiza o template da página inicial do site.
    Renders the home page template of the website.
    """
    return render_template('index.html')


# Rota da landing comercial do Oráculo CRM
# Route for the Oráculo CRM commercial landing page
@app.route('/oraculo')
@app.route('/oraculo/')
def oraculo():
    """
    Renderiza a landing page comercial do Oráculo CRM.
    Renders the Oráculo CRM commercial landing page.
    """
    return render_template('oraculo.html')

# Rota para a página de Sistema Sob Medida
# Route for the Custom System page
@app.route('/sistema-sob-medida')
def sistema_sob_medida():
    """
    Renderiza o template da página de Sistema Sob Medida.
    Renders the Custom System page template.
    """
    return render_template('sistema_sob_medida.html')

# Rota para a página de transformação de planilhas em sistemas
# Route for the spreadsheets to systems page
@app.route('/planilhas')
def planilhas():
    """
    Renderiza o template da página de Planilhas para Sistemas.
    Renders the Spreadsheets to Systems page template.
    """
    return render_template('planilhas.html')

# Rota para a página de desenvolvimento de sites
# Route for the website development page
@app.route('/sites')
def sites():
    """
    Renderiza o template da página de criação de sites.
    Renders the website creation page template.
    """
    return render_template('sites.html')


# Rota para o menu Nossos Serviços (Catálogo de 10 nichos de mercado)
# Route for Our Services menu (Catalog of 10 market niches)
@app.route('/nossos-servicos')
def nossos_servicos():
    """
    Renderiza o catálogo de 10 produtos e nichos com acesso às demonstrações ao vivo.
    """
    return render_template('nossos_servicos.html')


# Rota dinâmica para os sites demonstrativos dos 10 nichos
# Dynamic route for 10 niche demonstration websites
@app.route('/demo/<nicho>')
def demo(nicho):
    """
    Renderiza a demonstração navegável do nicho selecionado.
    """
    valid_demos = {
        'consultorio': 'Consultório (Site com Agendamento)',
        'barbearia': 'Barbearia (Site com Agendamento)',
        'restaurante': 'Restaurante (Site + Cardápio Online)',
        'academia': 'Academia (Planos e Matrícula)',
        'salao': 'Salão de Beleza (Serviços + Agendamento)',
        'clinica': 'Clínica Estética (Serviços + Agendamento)',
        'loja': 'Loja (Catálogo de Produtos)',
        'imobiliaria': 'Imobiliária (Imóveis e Contato)',
        'hotel': 'Hotel / Pousada (Quartos + Reservas)',
        'oficina': 'Oficina (Serviços + Agendamento)',
        'escola': 'Escola / Cursos Online',
        'planilha': 'Sistema Financeiro (Planilha → Sistema Web)'
    }
    if nicho in valid_demos:
        return render_template(f'demos/{nicho}.html', nicho=nicho, nicho_nome=valid_demos[nicho])
    return render_template('nossos_servicos.html'), 404



# Handler de erro 404 personalizado / Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    """
    Renderiza uma página 404 personalizada estilizada.
    Renders a custom styled 404 error page.
    """
    return render_template('nossos_servicos.html'), 404


# Inicia o servidor se o script for executado diretamente
# Start the server if the script is run directly
if __name__ == '__main__':
    # Estamos rodando em modo debug para facilitar o desenvolvimento
    # We are running in debug mode to ease development
    app.run(debug=True, port=5000)
