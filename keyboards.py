from aiogram.utils.keyboard import InlineKeyboardBuilder

from sql_handler import DatabaseManager

NBA_TEAMS = {
    'ATL': 'Atlanta Hawks',
    'BKN': 'Brooklyn Nets',
    'BOS': 'Boston Celtics',
    'CHA': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'LA Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHX': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SAS': 'San Antonio Spurs',
    'SAC': 'Sacramento Kings',
    'TOR': 'Toronto Raptors',
    'UTJ': 'Utah Jazz',
    'WSH': 'Washington Wizards',
}


def start_ikb(user_id):
    builder = InlineKeyboardBuilder()
    dbm = DatabaseManager()
    user_tags = dbm.get_user_tags(user_id)

    for k in NBA_TEAMS:
        if (k,) in user_tags:
            builder.button(text='💚 ' + k + ' 💚', callback_data=k)
        else:
            builder.button(text=k, callback_data=k)

    builder.adjust(3)
    dbm.close()
    return builder.as_markup()
