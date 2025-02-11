# plots.py
import plotly.graph_objects as go
import pandas as pd

def create_plots(df):
    """Tworzy wykresy dla statystyk"""
    # Wykres przyjęcia - zmieniony na stacked bar chart z procentami
    fig_receive = go.Figure()
    
    # Obliczanie procentowego udziału dla każdego typu przyjęcia
    for idx, row in df.iterrows():
        total = row['Dobre przyjęcia'] + row['Średnie przyjęcia'] + row['Złe przyjęcia']
        if total > 0:
            good_percent = (row['Dobre przyjęcia'] / total) * 100
            ok_percent = (row['Średnie przyjęcia'] / total) * 100
            bad_percent = (row['Złe przyjęcia'] / total) * 100
            
            # Dodawanie adnotacji z liczbą przyjęć - przesunięte wyżej
            fig_receive.add_annotation(
                x=row['Gracz'],
                y=115,  # Przesunięte wyżej
                text=f'Łącznie: {total}',
                showarrow=False,
                font=dict(size=10)
            )
            
            # Dodawanie słupków z procentami
            fig_receive.add_trace(go.Bar(
                name='Dobre przyjęcia',
                x=[row['Gracz']],
                y=[good_percent],
                marker_color='rgb(15, 142, 0)',
                text=[f'{int(row["Dobre przyjęcia"])}'],
                textposition='inside',
                legendgroup='good',
                showlegend=idx == 0
            ))
            fig_receive.add_trace(go.Bar(
                name='Średnie przyjęcia',
                x=[row['Gracz']],
                y=[ok_percent],
                marker_color='rgb(255, 191, 0)',
                text=[f'{int(row["Średnie przyjęcia"])}'],
                textposition='inside',
                legendgroup='ok',
                showlegend=idx == 0
            ))
            fig_receive.add_trace(go.Bar(
                name='Złe przyjęcia',
                x=[row['Gracz']],
                y=[bad_percent],
                marker_color='rgb(255, 0, 0)',
                text=[f'{int(row["Złe przyjęcia"])}'],
                textposition='inside',
                legendgroup='bad',
                showlegend=idx == 0
            ))
    
    fig_receive.update_layout(
        title='Statystyki przyjęcia (rozkład procentowy)',
        yaxis_title='Procent przyjęć (%)',
        barmode='stack',
        showlegend=True,
        yaxis_range=[0, 120],  # Zwiększony zakres osi Y
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        margin=dict(t=50, b=50),  # Dodatkowy margines
        uniformtext_minsize=10,
        uniformtext_mode='hide'
    )
    
    # Nowy wykres dla setów
    fig_sets = go.Figure()
    
    for idx, row in df.iterrows():
        total_sets = row['Perfect set'] + row['Good set'] + row['Playable set'] + row['Bad set']
        if total_sets > 0:
            perfect_percent = (row['Perfect set'] / total_sets) * 100
            good_percent = (row['Good set'] / total_sets) * 100
            playable_percent = (row['Playable set'] / total_sets) * 100
            bad_percent = (row['Bad set'] / total_sets) * 100
            
            # Dodawanie adnotacji z łączną liczbą setów
            fig_sets.add_annotation(
                x=row['Gracz'],
                y=115,
                text=f'Łącznie: {total_sets}',
                showarrow=False,
                font=dict(size=10)
            )
            
            # Dodawanie słupków z procentami
            fig_sets.add_trace(go.Bar(
                name='Perfect set',
                x=[row['Gracz']],
                y=[perfect_percent],
                marker_color='rgb(15, 142, 0)',  # Ciemny zielony
                text=[f'{int(row["Perfect set"])}'],
                textposition='inside',
                legendgroup='perfect',
                showlegend=idx == 0
            ))
            fig_sets.add_trace(go.Bar(
                name='Good set',
                x=[row['Gracz']],
                y=[good_percent],
                marker_color='rgb(76, 175, 80)',  # Jaśniejszy zielony
                text=[f'{int(row["Good set"])}'],
                textposition='inside',
                legendgroup='good',
                showlegend=idx == 0
            ))
            fig_sets.add_trace(go.Bar(
                name='Playable set',
                x=[row['Gracz']],
                y=[playable_percent],
                marker_color='rgb(255, 191, 0)',  # Żółty
                text=[f'{int(row["Playable set"])}'],
                textposition='inside',
                legendgroup='playable',
                showlegend=idx == 0
            ))
            fig_sets.add_trace(go.Bar(
                name='Bad set',
                x=[row['Gracz']],
                y=[bad_percent],
                marker_color='rgb(255, 0, 0)',  # Czerwony
                text=[f'{int(row["Bad set"])}'],
                textposition='inside',
                legendgroup='bad',
                showlegend=idx == 0
            ))
    
    fig_sets.update_layout(
        title='Statystyki setów (rozkład procentowy)',
        yaxis_title='Procent setów (%)',
        barmode='stack',
        showlegend=True,
        yaxis_range=[0, 120],  # Zwiększony zakres osi Y dla adnotacji
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        margin=dict(t=50, b=50)
    )
    
    # Wykres zdobytych punktów
    fig_scored = go.Figure()
    
    for idx, row in df.iterrows():
        attacks = row['Punkty z ataku']
        aces = row['Asy']
        serve_points = row['Punkty z zagrywki']
        total_points = attacks + aces + serve_points
        
        if total_points > 0:
            # Dodawanie adnotacji z łączną liczbą punktów
            fig_scored.add_annotation(
                x=row['Gracz'],
                y=total_points + 2,  # Trochę powyżej słupka
                text=f'Łącznie: {total_points}',
                showarrow=False,
                font=dict(size=10)
            )
            
            # Dodawanie słupków
            fig_scored.add_trace(go.Bar(
                name='Atak',
                x=[row['Gracz']],
                y=[attacks],
                marker_color='rgb(19, 102, 10)',  # Zielony
                text=[f'{int(attacks)}'],
                textposition='inside',
                legendgroup='attacks',
                showlegend=idx == 0
            ))
            fig_scored.add_trace(go.Bar(
                name='Asy',
                x=[row['Gracz']],
                y=[aces],
                marker_color='rgb(76, 175, 80)',  # Jaśniejszy zielony
                text=[f'{int(aces)}'],
                textposition='inside',
                legendgroup='aces',
                showlegend=idx == 0
            ))
            fig_scored.add_trace(go.Bar(
                name='Punkty z zagrywki',
                x=[row['Gracz']],
                y=[serve_points],
                marker_color='rgb(159, 201, 135)',  # Najjaśniejszy zielony
                text=[f'{int(serve_points)}'],
                textposition='inside',
                legendgroup='serve_points',
                showlegend=idx == 0
            ))
    
    fig_scored.update_layout(
        title='Zdobyte punkty',
        yaxis_title='Liczba punktów',
        barmode='stack',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        margin=dict(t=50, b=50)
    )
    
    # Zmodyfikowany wykres straconych punktów
    fig_lost = go.Figure()
    
    for idx, row in df.iterrows():
        net_attacks = row['Atak w siatkę']
        outs = row['Aut']
        serve_errors = row['Błędy zagrywki']
        receive_outs = row['Receive out']
        enemy_aces = row['Enemy ace']
        enemy_blocks = row['Enemy block']
        total_errors = net_attacks + outs + serve_errors + receive_outs + enemy_aces + enemy_blocks
        
        if total_errors > 0:
            # Dodawanie adnotacji z łączną liczbą błędów
            fig_lost.add_annotation(
                x=row['Gracz'],
                y=total_errors + 2,
                text=f'Łącznie: {total_errors}',
                showarrow=False,
                font=dict(size=10)
            )
            
            # Dodawanie słupków
            fig_lost.add_trace(go.Bar(
                name='Atak w siatkę',
                x=[row['Gracz']], y=[net_attacks],
                marker_color='rgb(255, 159, 34)',
                text=[f'{int(net_attacks)}'],
                textposition='inside',
                legendgroup='net_attacks',
                showlegend=idx == 0
            ))
            fig_lost.add_trace(go.Bar(
                name='Aut',
                x=[row['Gracz']], y=[outs],
                marker_color='rgb(223, 80, 69)',
                text=[f'{int(outs)}'],
                textposition='inside',
                legendgroup='outs',
                showlegend=idx == 0
            ))
            fig_lost.add_trace(go.Bar(
                name='Błędy zagrywki',
                x=[row['Gracz']], y=[serve_errors],
                marker_color='rgb(177, 17, 17)',
                text=[f'{int(serve_errors)}'],
                textposition='inside',
                legendgroup='serve_errors',
                showlegend=idx == 0
            ))
            fig_lost.add_trace(go.Bar(
                name='Receive out',
                x=[row['Gracz']], y=[receive_outs],
                marker_color='rgb(156, 39, 176)',
                text=[f'{int(receive_outs)}'],
                textposition='inside',
                legendgroup='receive_outs',
                showlegend=idx == 0
            ))
            fig_lost.add_trace(go.Bar(
                name='Enemy ace',
                x=[row['Gracz']], y=[enemy_aces],
                marker_color='rgb(63, 81, 181)',
                text=[f'{int(enemy_aces)}'],
                textposition='inside',
                legendgroup='enemy_aces',
                showlegend=idx == 0
            ))
            fig_lost.add_trace(go.Bar(
                name='Enemy block',
                x=[row['Gracz']], y=[enemy_blocks],
                marker_color='rgb(0, 150, 136)',
                text=[f'{int(enemy_blocks)}'],
                textposition='inside',
                legendgroup='enemy_blocks',
                showlegend=idx == 0
            ))
    
    fig_lost.update_layout(
        title='Stracone punkty',
        yaxis_title='Liczba punktów',
        barmode='stack',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        margin=dict(t=50, b=50)
    )
    
    # Return only the remaining plots
    return fig_receive, fig_sets, fig_scored, fig_lost

def create_trend_plot(selected_files, all_stats):
    """Tworzy wykres trendów z treningu na trening"""
    # Przygotuj daty i dane
    dates = [file.replace('.xlsx', '') for file in selected_files]
    
    # Przygotuj dane dla każdego treningu
    training_data = []
    for stats in all_stats:
        team_stats = {
            'perfect_sets': 0,
            'good_sets': 0,
            'bad_sets': 0,
            'good_receives': 0,
            'ok_receives': 0,
            'bad_receives': 0,
            'attacks': 0,
            'attack_errors': 0
        }
        
        # Sumuj statystyki wszystkich graczy
        for player_stats in stats.values():
            team_stats['perfect_sets'] += player_stats.get('perfect set', 0)
            team_stats['good_sets'] += player_stats.get('good set', 0)
            team_stats['bad_sets'] += player_stats.get('bad set', 0)
            team_stats['good_receives'] += player_stats.get('good receive', 0)
            team_stats['ok_receives'] += player_stats.get('ok receive', 0)
            team_stats['bad_receives'] += player_stats.get('bad receive', 0)
            team_stats['attacks'] += player_stats.get('attack', 0)
            team_stats['attack_errors'] += (player_stats.get('attack net', 0) + 
                                          player_stats.get('out', 0))
        
        # Oblicz skuteczności
        total_sets = team_stats['perfect_sets'] + team_stats['good_sets'] + team_stats['bad_sets']
        set_efficiency = ((team_stats['perfect_sets'] + team_stats['good_sets']) / total_sets * 100 
                         if total_sets > 0 else 0)
        
        total_receives = team_stats['good_receives'] + team_stats['ok_receives'] + team_stats['bad_receives']
        receive_efficiency = ((team_stats['good_receives'] + team_stats['ok_receives']) / total_receives * 100 
                            if total_receives > 0 else 0)
        
        total_attacks = team_stats['attacks'] + team_stats['attack_errors']
        attack_efficiency = (team_stats['attacks'] / total_attacks * 100 
                           if total_attacks > 0 else 0)
        
        training_data.append({
            'set_efficiency': set_efficiency,
            'receive_efficiency': receive_efficiency,
            'attack_efficiency': attack_efficiency
        })

    # Stwórz wykres
    fig_trend = go.Figure()

    # Dodaj linie dla każdego typu skuteczności
    fig_trend.add_trace(go.Scatter(
        x=dates,
        y=[data['set_efficiency'] for data in training_data],
        name='Skuteczność rozegrania',
        mode='lines+markers',
        line=dict(color='rgb(76, 175, 80)'),
        marker=dict(size=8)
    ))

    fig_trend.add_trace(go.Scatter(
        x=dates,
        y=[data['receive_efficiency'] for data in training_data],
        name='Skuteczność przyjęcia',
        mode='lines+markers',
        line=dict(color='rgb(33, 150, 243)'),
        marker=dict(size=8)
    ))

    fig_trend.add_trace(go.Scatter(
        x=dates,
        y=[data['attack_efficiency'] for data in training_data],
        name='Skuteczność ataku',
        mode='lines+markers',
        line=dict(color='rgb(255, 87, 34)'),
        marker=dict(size=8)
    ))

    fig_trend.update_layout(
        title='Trendy skuteczności drużyny',
        xaxis_title='Data treningu',
        yaxis_title='Skuteczność (%)',
        yaxis_range=[0, 100],
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        margin=dict(t=50, b=50)
    )

    return fig_trend

def create_player_trend_plots(player_name, selected_files, all_stats):
    """Tworzy wykresy trendów dla pojedynczego gracza, podzielone na kategorie"""
    dates = [file.replace('.xlsx', '') for file in selected_files]
    
    # Zdefiniuj własną paletę wyrazistych kolorów
    vibrant_colors = [
        '#FF0000',  # Czerwony
        '#00FF00',  # Zielony
        '#0000FF',  # Niebieski
        '#FF00FF',  # Magenta
        '#00FFFF',  # Cyan
        '#FFD700',  # Złoty
        '#FF8C00',  # Ciemnopomarańczowy
        '#4B0082',  # Indygo
        '#FF1493',  # Głęboki róż
        '#32CD32',  # Limonkowy
        '#4169E1',  # Królewski niebieski
        '#8B4513',  # Brązowy
        '#008080',  # Morski
        '#9400D3',  # Fioletowy
        '#FF4500'   # Pomarańczowo-czerwony
    ]
    
    # Zdefiniuj kategorie statystyk
    attack_stats = ['attack', 'attack net', 'out', 'block']
    serve_stats = ['ace', 'serve point', 'serve net', 'serve out']
    receive_stats = ['good receive', 'ok receive', 'bad receive', 'receive out', 'enemy ace']
    set_stats = ['perfect set', 'good set', 'playable set', 'bad set']
    other_stats = ['free ball', 'defence', 'enemy block', 'enemy fault']
    points_stats = ['scored points', 'lost points']
    
    categories = {
        'Atak': attack_stats,
        'Zagrywka': serve_stats,
        'Przyjęcie': receive_stats,
        'Rozegranie': set_stats,
        'Inne': other_stats,
        'Punkty': points_stats
    }
    
    figures = {}
    
    # Stwórz wykres dla każdej kategorii
    for category_name, stats_list in categories.items():
        fig = go.Figure()
        
        # Dodaj linię dla każdej statystyki w kategorii
        for i, stat_type in enumerate(stats_list):
            values = []
            for stats in all_stats:
                if player_name.lower() in stats:
                    values.append(stats[player_name.lower()].get(stat_type, 0))
                else:
                    values.append(0)
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=values,
                name=stat_type,
                mode='lines+markers',
                line=dict(
                    color=vibrant_colors[i % len(vibrant_colors)],
                    width=2
                ),
                marker=dict(
                    size=8,
                    line=dict(
                        color='white',
                        width=1
                    )
                )
            ))

        fig.update_layout(
            title=f'{category_name} - {player_name}',
            xaxis_title='Data treningu',
            yaxis_title='Wartość',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor='rgba(255, 255, 255, 0.8)'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=50, b=50)
        )
        
        # Dodaj siatkę
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='lightgrey'
        )
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='lightgrey'
        )
        
        figures[category_name] = fig
    
    return figures
