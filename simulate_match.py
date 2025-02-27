import random
import time

# Define squads with substitutes
teams = {
    "Manchester United": [
        "Onana", "Dalot", "Varane", "Martinez", "Shaw", "Casemiro", "Eriksen", "Fernandes", "Antony", "Rashford", "Hojlund",
        "Heaton", "Maguire", "Lindelof", "Malacia", "McTominay", "Mount", "Sancho", "Pellistri", "Martial", "Garnacho"
    ],
    "Manchester City": [
        "Ederson", "Walker", "Dias", "Akanji", "Gvardiol", "Rodri", "De Bruyne", "Silva", "Foden", "Grealish", "Haaland",
        "Ortega", "Stones", "Laporte", "Cancelo", "Phillips", "Alvarez", "Mahrez", "Gomez", "Palmer", "Lewis"
    ]
}

max_subs = 5
substitutions = {"Manchester United": [], "Manchester City": []}
events_log = []

# Track yellow and red cards for players
yellow_cards = {"Manchester United": {}, "Manchester City": {}}
red_cards = {"Manchester United": [], "Manchester City": []}

def log_event(event, minute):
    events_log.append(f"{minute}' {event}")
    print(f"{minute}' {event}")

def issue_red_card(team, player, minute):
    if player not in red_cards[team]:  # Only issue red card if the player hasn't already received one
        red_cards[team].append(player)
        log_event(f"RED CARD! {player} is sent off!", minute)

def issue_yellow_card(team, player, minute):
    """ Issue a yellow card to a player. If it's their second yellow card, issue a red card. """
    if player not in yellow_cards[team]:
        yellow_cards[team][player] = 1
        log_event(f"YELLOW CARD! {player}", minute)
    elif yellow_cards[team][player] == 1:  # If it's the second yellow card, issue a red card
        yellow_cards[team][player] += 1
        issue_red_card(team, player, minute)
        log_event(f"SECOND YELLOW CARD! {player} is sent off!", minute)

def make_substitution(team, minute):
    if len(substitutions[team]) < max_subs:
        starters = teams[team][:11]
        bench = teams[team][11:]
        
        # If there are players on the bench
        if bench:
            out_player = random.choice(starters)
            in_player = random.choice(bench)
            
            # Ensure the out_player is fully substituted out (no way back)
            starters.remove(out_player)
            bench.remove(in_player)
            
            # Remove out_player from team completely, and add in_player to the team
            teams[team].remove(out_player)
            teams[team].append(in_player)
            
            # Log the substitution
            substitutions[team].append((minute, out_player, in_player))
            log_event(f"SUBSTITUTION: {out_player} off, {in_player} on", minute)

def simulate_half(start_minute, end_minute, added_time):
    for minute in range(start_minute, end_minute + added_time + 1):
        time.sleep(1)  # Increased wait time for more realistic pacing (1 second per minute)
        event_chance = random.random()
        
        if event_chance < 0.03:  # Goal scored (lower chance)
            team = random.choice(list(teams.keys()))
            scorer = random.choice(teams[team][:11])
            score[team] += 1
            log_event(f"GOAL! {scorer} scores for {team}! Score: {score['Manchester United']} - {score['Manchester City']}", minute)
        elif event_chance < 0.10:  # Yellow card
            team = random.choice(list(teams.keys()))
            player = random.choice(teams[team][:11])
            issue_yellow_card(team, player, minute)
        elif event_chance < 0.12:  # Red card (direct or from yellow cards)
            team = random.choice(list(teams.keys()))
            player = random.choice(teams[team][:11])
            issue_red_card(team, player, minute)
        elif event_chance < 0.18:  # Foul committed
            team = random.choice(list(teams.keys()))
            fouls[team] += 1
            log_event(f"FOUL! {team} commits a foul", minute)
        elif event_chance < 0.22:  # Substitutions at any time
            team = random.choice(list(teams.keys()))
            make_substitution(team, minute)

def simulate_match():
    global score, yellow_cards, red_cards, fouls, goal_scorers
    score = {"Manchester United": 0, "Manchester City": 0}
    yellow_cards = {"Manchester United": {}, "Manchester City": {}}
    red_cards = {"Manchester United": [], "Manchester City": []}
    fouls = {"Manchester United": 0, "Manchester City": 0}
    goal_scorers = {"Manchester United": [], "Manchester City": []}
    
    # First half
    first_half_added_time = random.randint(0, 3)
    log_event("KICKOFF: First half begins!", 0)
    simulate_half(1, 45, first_half_added_time)
    log_event(f"HALF-TIME: First half ends with {first_half_added_time} minutes added.", 45)
    
    # Realistic 15-minute half-time break simulation
    print("\n\nHALF-TIME BREAK\n=====================")
    log_event("15-MINUTE HALF-TIME BREAK", 45)
    time.sleep(2)  # Simulate break (longer wait time for break)
    log_event("Players warming up, discussing tactics...", 45)
    time.sleep(2)
    log_event("Second half preparations underway...", 45)
    time.sleep(2)
    
    # Second half
    second_half_added_time = random.randint(0, 5)
    log_event("SECOND HALF BEGINS!", 45)
    simulate_half(46, 90, second_half_added_time)
    log_event(f"FULL-TIME! Match ends with {second_half_added_time} minutes added.", 90)
    
    log_event(f"Final Score: Manchester United {score['Manchester United']} - {score['Manchester City']} Manchester City", 90)
    log_event(f"Goals: {goal_scorers}", 90)
    log_event(f"Yellow Cards: {yellow_cards}", 90)
    log_event(f"Red Cards: {red_cards}", 90)
    log_event(f"Fouls: {fouls}", 90)
    log_event(f"Substitutions: {substitutions}", 90)
    
    # Match report
    print("\nMATCH REPORT")
    print("======================")
    for event in events_log:
        print(event)

# Run the simulation
simulate_match()
