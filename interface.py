# interface.py
import os
import openpyxl
import gradio as gr
from stats_processing import process_stats
from analysis import analyze_stats

def create_interface():
    with gr.Blocks(title="Analiza Statystyk Siatkówki") as interface:
        gr.Markdown("# Analiza Statystyk Siatkówki")
        gr.Markdown("""
        ### Instrukcja:
        1. Wybierz pliki Excel do analizy
        2. Lub użyj przycisku 'Analizuj wszystkie' aby przeanalizować wszystkie pliki
        3. Kliknij przycisk 'Analizuj wybrane'
        4. Przeglądaj wyniki w formie tabeli i wykresów
        """)
        
        excel_folder = "excel"
        available_files = [f for f in os.listdir(excel_folder) if f.endswith(".xlsx")] if os.path.exists(excel_folder) else []
        
        with gr.Row():
            file_selector = gr.Dropdown(
                choices=available_files,
                label="Wybierz pliki do analizy",
                multiselect=True,
                value=[]
            )
        
        with gr.Row():
            analyze_selected_btn = gr.Button("Analizuj wybrane", variant="primary")
            analyze_all_btn = gr.Button("Analizuj wszystkie", variant="secondary")
            
        with gr.Row():
            summary_text = gr.Textbox(
                label="Podsumowanie",
                placeholder="Tu pojawi się podsumowanie...",
                lines=2
            )
            
        with gr.Row():
            stats_table = gr.DataFrame(
                label="Szczegółowe statystyki",
                headers=['Gracz', 'Punkty z ataku', 'Błędy', 'Atak w siatkę', 'Aut',
                         'Asy', 'Punkty z zagrywki', 'Błędy zagrywki',
                         'Dobre przyjęcia', 'Średnie przyjęcia', 'Złe przyjęcia', 
                         'Skuteczność przyjęcia %', 'Bloki', 'Free ball',
                         'Perfect set', 'Good set', 'Playable set', 'Bad set',
                         'Zdobyte punkty', 'Stracone punkty', 'Receive out', 'Enemy ace', 'Enemy block']
            )
        
        # Dodaj zakładki
        with gr.Tabs() as tabs:
            with gr.Tab("Drużyna"):
                with gr.Row():
                    plot_receive = gr.Plot(label="Statystyki przyjęcia")
                    plot_sets = gr.Plot(label="Statystyki setów")
                
                with gr.Row():
                    plot_scored = gr.Plot(label="Zdobyte punkty")
                    plot_lost = gr.Plot(label="Stracone punkty")
                    
                with gr.Row():
                    plot_trend = gr.Plot(label="Trendy drużyny")
                    
                with gr.Row():
                    gr.Markdown("""
                    ### Objaśnienie skuteczności:
                    
                    **Skuteczność rozegrania** = (perfect sets + good sets) / wszystkie sety * 100%
                    - Uwzględnia perfect sets i good sets jako udane
                    - Im wyższa wartość, tym lepsze rozegranie
                    
                    **Skuteczność przyjęcia** = (dobre przyjęcia + średnie przyjęcia) / wszystkie przyjęcia * 100%
                    - Uwzględnia zarówno dobre jak i średnie przyjęcia jako udane
                    - Im wyższa wartość, tym lepsze przyjęcie
                    
                    **Skuteczność ataku** = punkty z ataku / (punkty + błędy) * 100%
                    - Błędy obejmują tylko: attack net, out
                    - Im wyższa wartość, tym skuteczniejszy atak
                    """)
            
            # Stwórz słownik do przechowywania komponentów wykresów graczy
            player_plots = {}
            
            # Znajdź początkową listę graczy
            initial_players = set()
            if os.path.exists("excel"):
                for file in os.listdir("excel"):
                    if file.endswith(".xlsx"):
                        file_path = os.path.join("excel", file)
                        workbook = openpyxl.load_workbook(file_path, data_only=True)
                        if "suma" in workbook.sheetnames:
                            sheet = workbook["suma"]
                            stats = process_stats(sheet)
                            initial_players.update(stats.keys())
            
            # Stwórz zakładki dla każdego gracza
            for player in sorted(initial_players):
                with gr.Tab(player.title()):
                    player_plots[player] = {}
                    with gr.Row():
                        player_plots[player]['Atak'] = gr.Plot(label=f"Statystyki ataku")
                        player_plots[player]['Zagrywka'] = gr.Plot(label=f"Statystyki zagrywki")
                    with gr.Row():
                        player_plots[player]['Przyjęcie'] = gr.Plot(label=f"Statystyki przyjęcia")
                        player_plots[player]['Rozegranie'] = gr.Plot(label=f"Statystyki rozegrania")
                    with gr.Row():
                        player_plots[player]['Inne'] = gr.Plot(label=f"Pozostałe statystyki")
                        player_plots[player]['Punkty'] = gr.Plot(label=f"Zdobyte/stracone punkty")
        
        def analyze_all():
            files = [f for f in os.listdir("excel") if f.endswith(".xlsx")]
            files.sort()
            summary, fig_receive, fig_sets, fig_scored, fig_lost, df, fig_trend, player_figs = analyze_stats(files)
            outputs = [summary, fig_receive, fig_sets, fig_scored, fig_lost, df, fig_trend]
            # Dodaj wykresy graczy w tej samej kolejności co zakładki
            for player in sorted(player_plots.keys()):
                if player in player_figs:
                    for category in ['Atak', 'Zagrywka', 'Przyjęcie', 'Rozegranie', 'Inne', 'Punkty']:
                        outputs.append(player_figs[player].get(category, None))
                else:
                    outputs.extend([None] * 6)
            return outputs
        
        def analyze_selected(selected_files):
            if not selected_files:
                return [None] * (7 + len(player_plots) * 6)  # 6 wykresów na gracza
            selected_files.sort()
            summary, fig_receive, fig_sets, fig_scored, fig_lost, df, fig_trend, player_figs = analyze_stats(selected_files)
            outputs = [summary, fig_receive, fig_sets, fig_scored, fig_lost, df, fig_trend]
            
            # Dodaj wykresy graczy w odpowiedniej kolejności
            for player in sorted(player_plots.keys()):
                if player in player_figs:
                    for category in ['Atak', 'Zagrywka', 'Przyjęcie', 'Rozegranie', 'Inne', 'Punkty']:
                        outputs.append(player_figs[player].get(category, None))
                else:
                    outputs.extend([None] * 6)
            return outputs
        
        # Zaktualizuj handlery przycisków
        analyze_selected_btn.click(
            fn=analyze_selected,
            inputs=[file_selector],
            outputs=[summary_text, plot_receive, plot_sets, plot_scored, plot_lost, 
                     stats_table, plot_trend] + 
                     [plot for player_dict in player_plots.values() for plot in player_dict.values()]
        )
        
        analyze_all_btn.click(
            fn=analyze_all,
            outputs=[summary_text, plot_receive, plot_sets, plot_scored, plot_lost, 
                     stats_table, plot_trend] + 
                     [plot for player_dict in player_plots.values() for plot in player_dict.values()]
        )
    
    return interface
