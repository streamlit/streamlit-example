import pandas as pd
import itertools
from datetime import datetime, timedelta

def bin_packing_fair_seeding(teams, group_size):
    """
    Distribute teams into groups to minimize the average point difference between groups.
    
    This function sorts teams by their points and then assigns them to groups in a way that
    aims to balance the total points in each group. Teams are distributed alternatively to
    each group based on their ranking.

    Parameters:
    - teams (list of tuples): List where each tuple contains team information (name, points).
    - group_size (int): The number of teams in each group.

    Returns:
    - list: A list of groups, each group is a list of teams.
    """
    if len(teams) < group_size:
        return []

    teams.sort(key=lambda x: x[1], reverse=True)
    num_groups = len(teams) // group_size
    groups = [[] for _ in range(num_groups)]

    for i, team in enumerate(teams):
        index = i % num_groups if i // num_groups % 2 == 0 else num_groups - 1 - (i % num_groups)
        groups[index].append(team)

    return groups

def schedule_matches(groups, available_times, match_duration, num_courts):
    """
    Schedule matches for teams within each group, considering available times and courts.

    Ensures no player is double-booked and schedules matches according to the provided
    time slots and court availability.

    Parameters:
    - groups (list): List of groups, each group is a list of teams.
    - available_times (dict): Dictionary with available times for each day of matches.
    - match_duration (int): Duration of each match in minutes.
    - num_courts (int): Number of available courts.

    Returns:
    - list: A list of scheduled matches, each match includes time, match detail, and court.
    """
    matches = [match for group in groups for match in itertools.combinations([team for team, _ in group], 2)]
    all_players = set(player for group in groups for team, _ in group for player in team.split(' - '))

    time_slots = []
    for day, times in available_times.items():
        for start, end in times:
            current_time = start
            while current_time + timedelta(minutes=match_duration) <= end:
                for court in range(num_courts):
                    time_slots.append((current_time, court + 1))
                current_time += timedelta(minutes=match_duration)

    def is_player_free(player, time_slot, scheduled_matches):
        for scheduled_time, scheduled_match, _ in scheduled_matches:
            if scheduled_time == time_slot and player in scheduled_match.replace('Match_', '').replace('_', ' - '):
                return False
        return True

    scheduled_matches = []
    for time_slot, court in time_slots:
        for match in list(matches):
            players = match[0].split(' - ') + match[1].split(' - ')
            if all(is_player_free(player, time_slot, scheduled_matches) for player in players):
                scheduled_matches.append((time_slot, f'Match_{match[0]}_{match[1]}', f'Court {court}'))
                matches.remove(match)
                break

    return scheduled_matches

def schedule_to_dataframe(schedule):
    """
    Convert a schedule list to a pandas DataFrame.

    Parameters:
    - schedule (list): A list of tuples, each containing time, match, and court information.

    Returns:
    - DataFrame: A pandas DataFrame with columns for Date, Time, Team 1, Team 2, and Court.
    """
    
    # Prepare data for DataFrame
    data = []
    for entry in schedule:
        if len(entry) == 3:
            time, match_str, court = entry
            day = time.strftime('%Y-%m-%d')
            match_time = time.strftime('%H:%M')
            teams = match_str.replace('Match_', '').split('_')
            team1, team2 = teams[0], teams[1]

            row = {
                "Day": day,
                "Time": match_time,
                "Team 1": team1,
                "Team 2": team2,
                "Court": court
            }
            data.append(row)
        else:
            print(f"Invalid entry in schedule: {entry}")

    # Create DataFrame
    df = pd.DataFrame(data)
    return df
