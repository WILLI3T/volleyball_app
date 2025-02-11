# analysis.py
import os
import openpyxl
from stats_processing import process_stats, merge_stats, create_player_summary_df
from plots import create_plots, create_trend_plot, create_player_trend_plots

def analyze_stats(selected_files):
    excel_folder = "excel"
    if not os.path.exists(excel_folder):
        return "Błąd: Folder 'excel' nie istnieje!", None, None, None, None, None, None, {}
    
    if selected_files is None or len(selected_files) == 0:
        return "Błąd: Nie wybrano żadnych plików!", None, None, None, None, None, None, {}
    
    # Sortuj pliki po dacie
    selected_files.sort()
    
    all_stats = []
    for file in selected_files:
        file_path = os.path.join(excel_folder, file)
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        
        if "suma" in workbook.sheetnames:
            sheet = workbook["suma"]
            player_stats = process_stats(sheet)
            all_stats.append(player_stats)
    
    merged_stats = merge_stats(all_stats)
    df = create_player_summary_df(merged_stats)
    fig_receive, fig_sets, fig_scored, fig_lost = create_plots(df)
    fig_trend = create_trend_plot(selected_files, all_stats)
    
    # Przygotuj wykresy dla każdego gracza
    player_figs = {}
    players = sorted(set(df['Gracz']))
    for player in players:
        player_figs[player] = create_player_trend_plots(player, selected_files, all_stats)
    
    summary = f"Przeanalizowano {len(selected_files)} plików:\n"
    summary += ", ".join(selected_files)
    
    return summary, fig_receive, fig_sets, fig_scored, fig_lost, df, fig_trend, player_figs
