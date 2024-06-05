import tabulate

class Matches:
    leaderboard = []
    no_of_teams = 8
    matches_won = [0 for _ in range(no_of_teams)]

    def run(self):
        no_of_weeks = 5
        for week in range(1, no_of_weeks + 1):
            team1_set = range(int(self.no_of_teams / 2))
            opponents = range(int(self.no_of_teams / 2), self.no_of_teams)
            week_scores = []
            last_score = week # Using the week number as the seed for generating scores
            for team1, team2 in zip(team1_set, opponents):
                last_score = team1_score = self.linear(last_score)
                last_score = team2_score = self.linear(last_score)
                week_scores.append([f"Team {team1}: {team1_score}", f"Team {team2}: {team2_score}"])
                if team1_score > team2_score:
                    self.matches_won[team1] += 1
                elif team2_score > team1_score:
                    self.matches_won[team2] += 1
            self.print_current_leaderboard_and_scores(week, week_scores)
    
    def print_current_leaderboard_and_scores(self, week, week_scores):
        teams = [team for team in range(self.no_of_teams)]
        teams.sort(key=lambda team: -self.matches_won[team])
        print("Scores for week", week)
        print(tabulate.tabulate([*week_scores]))
        print("Leaderboard for week", week)
        print("Position | Team")
        for pos, team in enumerate(teams):
            print(f"{pos+1} | {team}")
        print()

    def linear(self, xi):
        m, a, c = 8, 17, 43
        return (a * xi + c) % m

x = 1

matches = Matches()
matches.run()
