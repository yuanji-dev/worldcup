# -*- coding: utf-8 -*-
import sys
import json

import colorama
import arrow

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

from cn import get_chs

FUTURE = "future"
NOW = "now"
PAST = "past"
SCREEN_WIDTH = 68


def progress_bar(percentage, separator="o", character="-"):
    """
    Creates a progress bar by given percentage value
    """
    filled = colorama.Fore.GREEN + colorama.Style.BRIGHT
    empty = colorama.Fore.WHITE + colorama.Style.BRIGHT

    if percentage == 100:
        return filled + character * SCREEN_WIDTH

    if percentage == 0:
        return empty + character * SCREEN_WIDTH

    completed = int((SCREEN_WIDTH / 100.0) * percentage)

    return (filled + (character * (completed - 1)) +
            separator +
            empty + (character * (SCREEN_WIDTH - completed)))


def prettify(match):
    """
    Prettifies given match object
    """
    diff = (arrow.now() - arrow.get(match['datetime']).to('Asia/Shanghai'))

    seconds = diff.total_seconds()

    if seconds > 0:
        if seconds > 60 * 90:
            status = PAST
        else:
            status = NOW
    else:
        status = FUTURE

    if status in [PAST, NOW]:
        color = colorama.Style.BRIGHT + colorama.Fore.GREEN
    else:
        color = colorama.Style.NORMAL + colorama.Fore.WHITE

    home = match['home_team']
    away = match['away_team']

    if status == NOW:
        minute = int(seconds / 60)
        match_status = u"已经踢了: %s 分钟了。" % minute
    elif status == PAST:
        if match['winner'] == 'Draw':
            result = u'平手'
        else:
            result = u"%s 胜利！" % (get_chs(match['winner']))
        match_status = u"%s已经踢过。 %s" % (arrow.get(match['datetime']).humanize(locale='zh_CN'),
                                                  result)
    else:
        match_status = u"%s将会比赛。" % arrow.get(match['datetime']).humanize(locale='zh_CN')

    if status == NOW:
        match_percentage = int(seconds / 60 / 90 * 100)
    elif status == FUTURE:
        match_percentage = 0
    else:
        match_percentage = 100

    return u"""
    {} {:<30} {} - {} {:>30}
    {}
    \u26BD  {}
    """.format(
        color,
        get_chs(home['country']),
        home['goals'],
        away['goals'],
        get_chs(away['country']),
        progress_bar(match_percentage),
        colorama.Fore.WHITE + match_status
    )

def group_list(country):
    """
    Lists a group member
    """
    return """
    {:<5} \t\t| wins: {} | losses: {} | goals for: {} | goals against: {} | out? {}
    {}
    """.format(
        country['country'],
        country['wins'],
        country['losses'],
        country['goals_for'],
        country['goals_against'],
        country['knocked_out'],
        "-" * SCREEN_WIDTH
    )


def is_valid(match):
    """
    Validates the given match object
    """
    return (
        isinstance(match, dict) and
        isinstance(match.get('home_team'), dict) or
        isinstance(match.get('away_team'), dict) or
        isinstance(match.get('group_id'), int)
    )


def fetch(endpoint):
    """
    Fetches match results by given endpoint
    """
    url = "http://worldcup.sfg.io/matches/%(endpoint)s?by_date=ASC" % {
        "endpoint": endpoint
    }

    data = urlopen(url).read().decode('utf-8')
    matches = json.loads(data)

    for match in matches:
        if is_valid(match):
            yield match


def main():
    colorama.init()

    endpoint = ''.join(sys.argv[1:])

    # todo: use argument parser

    for match in fetch(endpoint):
        print(prettify(match).encode('utf-8'))

if __name__ == "__main__":
    main()