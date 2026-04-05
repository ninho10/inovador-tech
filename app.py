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

# Rota para a página de dados e insights
# Route for the data and insights page
@app.route('/dados')
def dados():
    """
    Renderiza o template da página de dados e gráficos.
    Renders the data and graphics page template.
    """
    return render_template('dados.html')

# Rota para a página de inteligência artificial e agentes
# Route for the AI and agents page
@app.route('/ai')
def ai():
    """
    Renderiza o template da página de IA e automação.
    Renders the AI and automation page template.
    """
    return render_template('ai.html')

# Rota para a página de desenvolvimento de sites
# Route for the website development page
@app.route('/sites')
def sites():
    """
    Renderiza o template da página de criação de sites.
    Renders the website creation page template.
    """
    return render_template('sites.html')


# Inicia o servidor se o script for executado diretamente
# Start the server if the script is run directly
if __name__ == '__main__':
    # Estamos rodando em modo debug para facilitar o desenvolvimento
    # We are running in debug mode to ease development
    app.run(debug=True, port=5000)
