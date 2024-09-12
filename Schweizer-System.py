# Schweizer System Schachturnier
import json
from random import randrange


class Tournament:
    participants = []
    rounds = 0
    currentRound = -1
    pairings = []
    results = []

    def __init__(self):
        pass # assert?

    def sortParticipants(self):
        x = lambda a: (float(a[3]), float(a[2]))
        self.participants.sort(key=x)
        self.participants.reverse()

    def printParticipants(self):
        print("-----")
        for i in self.participants:
            print(i[0], i[1], i[2], i[3])
        print("-----")

    def printPairings(self):
        print("-----")
        for i in self.pairings[self.currentRound]:
            print(' '.join([i[0][0], i[0][1], "-", i[1][0], i[1][1]]))
        print("-----")

    def printResults(self):
        print("-----")
        print(' '.join(["Round:", str(self.currentRound + 1)]))
        j = 0
        for i in self.pairings[self.currentRound]:
            if i != []:
                print(' '.join([i[0][0], i[0][1], "-", i[1][0], i[1][1],
                                self.results[self.currentRound][j].split("-")[0], "-", self.results[self.currentRound][j].split("-")[1]]))
            j += 1
        print("-----")

    def printAll(self):
        x = self.currentRound
        if x >= 0:
            for i in range(x + 1):
                self.currentRound = i
                self.printResults()
        self.printParticipants()

    def setParticipants(self):
        participant = input("Add Player: Name Surname Elo | stop | undo: ")
        while (participant != "stop"):
            if participant == "undo":
                if len(self.participants) > 0:
                    self.participants = self.participants[:-1]
                    print(' '.join(["Removed:", str(self.participants[-1])]))
            else:
                temp = participant.split(' ')
                temp.append("0")
                self.participants.append(temp)
                self.participants[-1][2] = int(self.participants[-1][2])
                self.participants[-1][3] = int(self.participants[-1][3])
                print(' '.join(["Added:", str(self.participants[-1])]))
            participant = input("Add Player: Name Surname Elo | stop | undo: ")
        if len(self.participants) % 2 != 0:
            self.participants.append([" ", " ", 0, 0])

    def setRounds(self):
        self.rounds = int(input("Number of rounds: "))
        self.results = [["...-..." for _ in range(len(self.participants))] for _ in range(self.rounds)]
        self.pairings = [[] for _ in range(self.rounds)]

    def nextRound(self):
        if self.currentRound == -1:
            self.currentRound += 1
            slice1 = self.participants[:int(len(self.participants) / 2)]
            slice2 = self.participants[int(len(self.participants) / 2):]
            for i in range(len(slice1)):
                if randrange(2) == 0:
                    self.pairings[self.currentRound].append([slice1[i][:-1], slice2[i][:-1]])
                else:
                    self.pairings[self.currentRound].append([slice2[i][:-1], slice1[i][:-1]])
        elif self.currentRound > -1 and self.currentRound < self.rounds - 1:
            pass

    def enterResults(self):
        j = 0
        for i in self.pairings[self.currentRound]:
            temp = input(' '.join(["Result of", i[0][0], i[0][1], "-", i[1][0], i[1][1], "...-...: "]))
            self.results[self.currentRound][j] = temp
            res = temp.split("-")
            for h in self.participants:
                if h[0] == i[0][0] and h[1] == i[0][1]:
                    h[3] += float(res[0])
                if h[0] == i[1][0] and h[1] == i[1][1]:
                    h[3] += float(res[1])
            j += 1
        self.sortParticipants()

if __name__ == "__main__":
    tournament = Tournament()
    command = -1
    while command != 4:
        command = int(input("Choose: New Tournament [0] | Current Tournament [1] | Load Tournament [2] | Save Tournament [3] | Exit [4]: "))
        if command == 0:
            tournament.setParticipants()
            tournament.sortParticipants()
            tournament.printParticipants()
            tournament.setRounds()
        elif command == 1:
            action = -1
            while action != 3:
                action = int(input("Choose: Enter Results [0] | Next Round [1] | Show tournament [2] | Back [3]: "))
                if action == 0:
                    tournament.enterResults()
                elif action == 1:
                    tournament.nextRound()
                    tournament.printPairings()
                elif action == 2:
                    tournament.printAll()
                elif action == 3:
                    pass
        elif command == 2:
            with open('package.json', 'r') as f:
                loaded = json.load(f)
                tournament.participants = loaded['p']
                tournament.rounds = loaded['r']
                tournament.results = loaded['e']
                tournament.pairings = loaded['g']
                tournament.currentRound = loaded['c']
            print("-----Loaded tournament-----")
        elif command == 3:
            with open('package.json', 'w+') as f:
                data = {"p": tournament.participants, "r": tournament.rounds, "c": tournament.currentRound, "e": tournament.results, "g": tournament.pairings}
                json.dump(data, f, indent=4, sort_keys=True)
            print("-----Saved tournament-----")
        print(" ")