# stats_processing.py
import openpyxl
from collections import defaultdict
import pandas as pd

def process_stats(sheet):
    # Słownik na statystyki graczy
    player_stats = defaultdict(lambda: defaultdict(int))
    
    # Znajdź wiersz z nazwami graczy
    player_row = None
    players = []
    for idx, row in enumerate(sheet.iter_rows(values_only=True)):
        if row[1] == 'Jonatan':  # Szukamy wiersza z nazwami graczy
            player_row = idx
            players = [name.lower() for name in row[1:7] if name]  # Konwertujemy na małe litery
            print(f"\nDEBUG - Znalezieni gracze: {players}")
            break
    
    if not player_row:
        print("\nDEBUG - Nie znaleziono wiersza z graczami!")
        return {}

    # Przetwarzanie statystyk
    for row in sheet.iter_rows(values_only=True):
        if not row[0]:  # Pomijamy puste wiersze
            continue
            
        action = row[0]
        if action and isinstance(action, str):
            action = action.lower()  # Konwertujemy nazwę akcji na małe litery
            
            # Dla wszystkich statystyk używamy tego samego wzorca
            for i, player in enumerate(players):
                value = row[i + 1]  # +1 bo pierwsza kolumna to nazwa akcji
                if isinstance(value, (int, float)):
                    player_stats[player][action] = value
                    if action in ['perfect set', 'good set', 'playable set', 'bad set', 'scored points', 'lost points']:
                        print(f"DEBUG - {action}: {player} = {value}")

    # Debug print - końcowe statystyki
    print("\nDEBUG - Końcowe statystyki:")
    for player, stats in player_stats.items():
        print(f"\n{player}:")
        for action, value in stats.items():
            print(f"  {action}: {value}")
    
    return player_stats

def merge_stats(all_stats):
    merged_stats = defaultdict(lambda: defaultdict(int))
    for stats in all_stats:
        for player, player_stats in stats.items():
            player = player.lower()  # Konwertujemy na małe litery
            for action, value in player_stats.items():
                if isinstance(value, (int, float)):  # Upewniamy się, że wartość jest liczbą
                    merged_stats[player][action] += value
    return merged_stats

def format_player_stats(player_stats, is_summary=False):
    if not player_stats:
        return "Nie znaleziono statystyk graczy\n"
    
    title = "\nPODSUMOWANIE WSZYSTKICH MECZÓW:\n" if is_summary else "\nStatystyki graczy:\n"
    output = title
    output += "-" * 50 + "\n"
    
    for player, stats in player_stats.items():
        output += f"\n{player.upper()}:\n"
        
        # Statystyki ataku
        attacks = stats.get('attack', 0)
        attack_errors = stats.get('error', 0) + stats.get('attack net', 0) + stats.get('out', 0)
        attack_points = attacks
        if attacks > 0:
            attack_efficiency = (attack_points - attack_errors) / (attack_points + attack_errors) * 100
        else:
            attack_efficiency = 0
            
        output += f"ATAK:\n"
        output += f"  Punkty: {attack_points}\n"
        output += f"  Błędy: {attack_errors}\n"
        output += f"  Skuteczność: {attack_efficiency:.1f}%\n"
        
        # Statystyki zagrywki
        aces = stats.get('ace', 0)
        serve_points = stats.get('serve point', 0)
        serve_errors = stats.get('serve out', 0) + stats.get('serve net', 0)
        total_serves = aces + serve_points + serve_errors
        if total_serves > 0:
            serve_efficiency = (aces + serve_points) / total_serves * 100
        else:
            serve_efficiency = 0
            
        output += f"\nZAGRYWKA:\n"
        output += f"  Asy: {aces}\n"
        output += f"  Punkty z zagrywki: {serve_points}\n"
        output += f"  Błędy: {serve_errors}\n"
        output += f"  Skuteczność: {serve_efficiency:.1f}%\n"
        
        # Statystyki przyjęcia
        good_receives = stats.get('good receive', 0)
        ok_receives = stats.get('ok receive', 0)
        bad_receives = stats.get('bad receive', 0)
        total_receives = good_receives + ok_receives + bad_receives
        
        if total_receives > 0:
            # Nowa formuła na skuteczność przyjęcia:
            # (dobre * 100% + średnie * 50% - złe * 50%) / całkowita liczba przyjęć
            receive_efficiency = ((good_receives * 1.0 + ok_receives * 0.5 - bad_receives * 0.5) / total_receives) * 100
        else:
            receive_efficiency = 0
        
        output += f"\nPRZYJĘCIE:\n"
        output += f"  Perfekcyjne: {good_receives} ({receive_efficiency:.1f}%)\n"
        output += f"  Dobre: {ok_receives}\n"
        output += f"  Złe: {bad_receives}\n"
        output += f"  Łącznie przyjęć: {total_receives}\n"
        output += f"  Skuteczność: {receive_efficiency:.1f}%\n"
        
        # Pozostałe statystyki
        blocks = stats.get('block', 0)
        free_balls = stats.get('free ball', 0)
        
        output += f"\nPOZOSTAŁE:\n"
        output += f"  Bloki: {blocks}\n"
        output += f"  Free ball: {free_balls}\n"
        output += "-" * 30 + "\n"
    
    return output

def create_player_summary_df(player_stats):
    """Tworzy DataFrame z podsumowaniem statystyk gracza"""
    data = []
    for player, stats in player_stats.items():
        # Atak - rozdzielone błędy
        attacks = stats.get('attack', 0)
        errors = stats.get('error', 0)
        attack_nets = stats.get('attack net', 0)
        outs = stats.get('out', 0)
        
        # Zagrywka
        aces = stats.get('ace', 0)
        serve_points = stats.get('serve point', 0)
        serve_errors = stats.get('serve out', 0) + stats.get('serve net', 0)
        
        # Przyjęcie
        good_receives = stats.get('good receive', 0)
        ok_receives = stats.get('ok receive', 0)
        bad_receives = stats.get('bad receive', 0)
        total_receives = good_receives + ok_receives + bad_receives
        receive_efficiency = ((good_receives * 1.0 + ok_receives * 0.5 - bad_receives * 0.5) / total_receives) * 100 if total_receives > 0 else 0
        
        # Dodajemy statystyki setów i punktów
        perfect_sets = stats.get('perfect set', 0)
        good_sets = stats.get('good set', 0)
        playable_sets = stats.get('playable set', 0)
        bad_sets = stats.get('bad set', 0)
        scored_points = stats.get('scored points', 0)
        lost_points = stats.get('lost points', 0)
        
        # Dodajemy nowe statystyki straconych punktów
        receive_outs = stats.get('receive out', 0)
        enemy_aces = stats.get('enemy ace', 0)
        enemy_blocks = stats.get('enemy block', 0)
        
        data.append({
            'Gracz': player,
            'Punkty z ataku': attacks,
            'Błędy': errors,
            'Atak w siatkę': attack_nets,
            'Aut': outs,
            'Asy': aces,
            'Punkty z zagrywki': serve_points,
            'Błędy zagrywki': serve_errors,
            'Dobre przyjęcia': good_receives,
            'Średnie przyjęcia': ok_receives,
            'Złe przyjęcia': bad_receives,
            'Skuteczność przyjęcia %': round(receive_efficiency, 1),
            'Bloki': stats.get('block', 0),
            'Free ball': stats.get('free ball', 0),
            'Perfect set': perfect_sets,
            'Good set': good_sets,
            'Playable set': playable_sets,
            'Bad set': bad_sets,
            'Zdobyte punkty': scored_points,
            'Stracone punkty': lost_points,
            'Receive out': receive_outs,
            'Enemy ace': enemy_aces,
            'Enemy block': enemy_blocks
        })
    
    return pd.DataFrame(data)
