import click, ktorrent, json

def colors():
  enums = dict(
    COUNT   = 'white',
    NAME    = 'yellow',
    SEED    = 'green',
    LEECH   = 'red',
    SIZE    = 'cyan',
    AGE     = 'blue'
  )
  return type('Enum', (), enums)

def cap(s, l):
    return s if len(s)<=l else s[0:l-3]+'...'

def print_data(raw_data):
    if raw_data == "Nothing found":
        click.secho("%s" % 'Nothing found!', fg='red', bold=True)
        return

    torrents = raw_data['torrent']

    click.secho("%-3s  %-60s    %-10s    %-10s    %s  " % ("#", "NAME", "AGE", "SIZE", "SEED   LEECH"), bold=True, fg="white", reverse=True)

    count = 0
    for torrent in torrents:
        count += 1
        name = torrent['name']
        age = torrent['age']
        size = torrent['size']
        seed = torrent['seed']
        leech = torrent['leech']

        click.secho("%-3s" % str(count), nl=False, fg=colors().COUNT, bold=True)
        click.secho("%s" % '»' if torrent['verified'] == '1' else ' ', nl=False)
        click.secho(' %-60s' % cap(name, 60), nl=False, fg=colors().NAME)
        click.secho('    %-10s' % age, nl=False, fg=colors().AGE)
        click.secho('    %-10s' % size, nl=False, fg=colors().SIZE)
        click.secho('    %-7s' % seed, nl=False, fg=colors().SEED)
        click.secho('%s' % leech, fg=colors().LEECH)

def get_params(**params):
    click.secho("%s" % 'Search type', fg='red', bold=True)
    strict = click.prompt(' -1: fuzzy\n  0: normal\n 1: strict\n')
    if strict.isdigit() and int(strict) in range(-1,2):
        params['strict'] = int(strict)

    click.secho("%s" % 'Safe search ON', fg='red', bold=True)
    safe = click.prompt('0 or 1')
    if safe.isdigit() and int(safe) in range(0,2):
        params['safe'] = int(safe)

    click.secho("%s" % 'Only verified torrent', fg='red', bold=True)
    verified = click.prompt('0 or 1')
    if verified.isdigit() and int(verified) in range(0,2):
        params['verified'] = int(verified)

    click.secho("%s" % 'Want to subtract some words from torrent name', fg='red', bold=True)
    yn_opt = click.prompt('y / n')
    if yn_opt == "y":
        subtract = click.prompt('Enter words to subtract')
        params['subtract'] = subtract

    click.secho("%s" % 'Uploads by certain user', fg='red', bold=True)
    yn_opt = click.prompt('y / n')
    if yn_opt == 'y':
        user = click.prompt('Enter username')
        params['user'] = user

    click.secho("%s" % 'Change torrents category', fg='red', bold=True)
    yn_opt = click.prompt('y / n')
    if yn_opt == 'y':
        category = click.prompt('Enter category')
        params['category'] = category

    click.secho("%s" % 'Sort result', fg='red', bold=True)
    yn_opt = click.prompt('y / n')
    if yn_opt == 'y':
        field = click.prompt('Enter field to sort')
        sorder = click.prompt('sorting order (asc/desc)')
        params['field'] = field
        params['sorder'] = sorder

    click.secho("%s" % 'Page Number', fg='red', bold=True)
    page = click.prompt('Enter page numer')
    if page.isdigit() and int(page) > 0:
        params['page'] = int(page)

    return params

def search_results(adv):

    search = click.prompt('Enter Search Query')

    params = {
        'search':   search,
        'strict':   0,
        'safe':     0,
        'verified': 0,
        'subtract': '',
        'user':     '',
        'category': 'all',
        'field':    'seed',
        'sorder':   'desc',
        'page':     1
    }

    if adv:
        params = get_params(**params)

    data = json.loads( ktorrent.search(**params) )
    print_data( data )

def top_results(adv):
   category = click.prompt('Enter Category')
   data = json.loads( ktorrent.top(category=category) )
   print_data( data )

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-s', '--search', is_flag=True, help='Search Torrent')
@click.option('-t', '--top', is_flag=True, help='Top Torrent')
@click.option('-a', '--adv', is_flag=True, help='Advance Options')
def main(search, top, adv):
    """katCLI"""
    if search and top:
        print("Choose only one function")
    elif search:
        search_results(adv)
    elif top:
        top_results(adv)
    else:
       print("Function argument missing")

if __name__ == "__main__": main()
