# Gourmet Quest Dashboard

## Visão Geral
O **Gourmet Quest Dashboard** é um aplicativo web baseado em Streamlit projetado para analisar dados de restaurantes a partir do dataset da Zomato. Este painel interativo oferece insights sobre a quantidade de restaurantes registrados, cidades, médias de avaliações e custos médios para duas pessoas em vários países. Os dados são visualizados por meio de gráficos Plotly, com filtros para personalizar a visualização por país. 

## Funcionalidades
- **Filtros por País**: Selecione países específicos para análise por meio de um widget multiseleção na barra lateral.
- **Visualização de Dados em Tempo Real**:
  - Gráficos com métricas para análise dos dados.
- **Download de Dados**: Exporte o dataset filtrado como um arquivo CSV.

## Requisitos
- **Python 3.8+**
- **Bibliotecas**:
  - `pandas`
  - `streamlit`
  - `pillow`
  - `plotly`

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/gabrielnasatto/gourmet-quest-dashboard.git
   cd gourmet-quest-dashboard
   ```
2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Coloque o arquivo `zomato.csv` na pasta `dataset/` (disponível no repositório ou fornecido separadamente).
5. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```

## Estrutura do Projeto
- `Home.py`: Script principal do Streamlit com o dashboard.
- `dataset/zomato.csv`: Dataset de entrada com dados de restaurantes.
- `logo.png`: Logotipo exibido na barra lateral (opcional, ajuste o caminho no código se necessário).
- `requirements.txt`: Lista de dependências do projeto.
- `pages/`: Páginas indivuiduais.

## Uso
- Acesse o aplicativo no navegador: https://gourmet-quest.streamlit.app
- Use a barra lateral para filtrar países e baixar os dados tratados.
- Explore os gráficos para analisar as métricas por país.

## Contribuições
Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request com suas sugestões ou melhorias. Certifique-se de seguir as boas práticas de código e adicionar testes se aplicável.

- Última atualização: 30 de agosto de 2025, 14:47 (horário de Brasília).
