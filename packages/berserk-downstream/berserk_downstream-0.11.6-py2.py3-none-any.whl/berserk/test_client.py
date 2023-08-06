import berserk


LICHESS_TOKEN = 'pq2djZpS9tI9QZZ4'  # OAuth token for Lichess API access
session = berserk.TokenSession(LICHESS_TOKEN)
lichess = berserk.Client(session=session)

games = list(lichess.games.export_by_player('ZCCZe', as_pgn=True, max=1, clocks=False))

print(games)


