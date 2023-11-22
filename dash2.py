from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_draggable

df = pd.read_csv('C:/Users/Я/Documents/Pandas/Krabota/movies_emotions.csv')

app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1(children='Фильмы: анализ рейтингов, эмоций и жанров', style={'textAlign':'center'}),

    html.Label('Выберите эмоцию:'),
    dcc.Dropdown(
        options=[
            {'label': 'Все', 'value': 'Все'}
        ] + [{'label': emotion, 'value': emotion} for emotion in df['emotion'].unique()],
        value='Все',
        id='emotion-selector',
    ),

    html.Label('Выберите жанр:'),
    dcc.Dropdown(
        options=[
            {'label': 'Все', 'value': 'Все'}
        ] + [{'label': genre, 'value': genre} for genre in df['genres'].unique()],
        value='Все',
        id='genre-selector',
    ),

    dash_draggable.ResponsiveGridLayout([
        dcc.Graph(id='top-10-bar-chart'),
        dcc.Graph(id='pie-chart'),
        dcc.Graph(id='emotion-frequency-line-chart'),
        dcc.Graph(id='rating-emotion-scatter-plot'),
    ]),
])


@app.callback(
    Output('top-10-bar-chart', 'figure'),
    Input('emotion-selector', 'value'),
    Input('genre-selector', 'value')
)
def update_top_10_bar_chart(selected_emotion, selected_genre):
    filtered_df = df.copy()
    
    if selected_emotion != 'Все':
        filtered_df = filtered_df[filtered_df['emotion'] == selected_emotion]
        
    if selected_genre != 'Все':
        filtered_df = filtered_df[filtered_df['genres'] == selected_genre]
    
    top_10_movies = filtered_df.groupby('title').max().sort_values('rating', ascending=False).head(10)
    
    figure = px.bar(top_10_movies, x=top_10_movies.index, y='rating', color='emotion',
                    labels={'rating': 'Рейтинг', 'x': 'Название фильма'},
                    title=f'Топ-10 фильмов по рейтингу для жанра "{selected_genre}" и эмоции "{selected_emotion}"')
    
    figure.update_layout(xaxis_title='Название фильма', yaxis_title='Рейтинг')
    
    return figure


@app.callback(
    Output('pie-chart', 'figure'),
    Input('emotion-selector', 'value'),
    Input('genre-selector', 'value')
)
def update_pie_chart(selected_emotion, selected_genre):
    filtered_df = df.copy()
    
    if selected_emotion != 'Все':
        filtered_df = filtered_df[filtered_df['emotion'] == selected_emotion]
        
    if selected_genre != 'Все':
        filtered_df = filtered_df[filtered_df['genres'] == selected_genre]
    
    total_movies = df.shape[0]
    matching_movies = filtered_df.shape[0]
    non_matching_movies = total_movies - matching_movies
    
    labels = ['Подходит', 'Не подходит']
    values = [matching_movies, non_matching_movies]
    
    figure = px.pie(names=labels, values=values, title='Соотношение количества фильмов')
    
    return figure


@app.callback(
    Output('emotion-frequency-line-chart', 'figure'),
    Input('genre-selector', 'value')
)
def update_emotion_frequency_line_chart(selected_genre):
    filtered_df = df.copy()
    
    if selected_genre != 'Все':
        filtered_df = filtered_df[filtered_df['genres'] == selected_genre]
    
    emotion_frequency = filtered_df['emotion'].value_counts().sort_index()
    
    figure = px.line(x=emotion_frequency.index, y=emotion_frequency.values,
                     labels={'x': 'Эмоция', 'y': 'Частота'},
                     title='Частота эмоций по фильтру жанра')
    
    return figure

@app.callback(
    Output('rating-emotion-scatter-plot', 'figure'),
    Input('emotion-selector', 'value'),
    Input('genre-selector', 'value')
)
def update_rating_emotion_scatter_plot(selected_emotion, selected_genre):
    filtered_df = df.copy()
    
    if selected_emotion != 'Все':
        filtered_df = filtered_df[filtered_df['emotion'] == selected_emotion]
    
    if selected_genre != 'Все':
        filtered_df = filtered_df[filtered_df['genres'] == selected_genre]
    
    figure = px.scatter(filtered_df, x='rating', y='rating_emotion', color='genres',
                       labels={'rating': 'Общий рейтинг', 'rating_emotion': 'Рейтинг эмоции'},
                       title=f'Зависимость рейтинга от рейтинга эмоции для жанра "{selected_genre}" и эмоции "{selected_emotion}"')
    
    return figure
if __name__ == '__main__':
    app.run(debug=True)
