import click, ktorrent, json, webbrowser

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

def check_status(status):
    if status == 200:
        return True
    elif status == 400:
        msg = 'Invalid arguments passed!'
    elif status == 404:
        msg = 'Nothing Found!'
    elif status == 408:
        msg = 'Connection error!'

    click.secho("%s" % msg, fg='red', bold=True)
    return False

def print_data(torrents):

    click.secho(" %-3s  %-60s  %-9s  %-10s  %s " % ("#", "NAME", "AGE", "SIZE", "SEED   LEECH"), bold=True, fg="white", reverse=True)

    count = 0
    for torrent in torrents:
        count += 1
        name = torrent['name']
        age = torrent['age']
        size = torrent['size']
        seed = torrent['seed']
        leech = torrent['leech']

        click.secho(" %-3s" % str(count), nl=False, fg=colors().COUNT, bold=True)
        click.secho("%s" % '»' if torrent['verified'] == '1' else ' ', nl=False)
        click.secho(' %-60s' % cap(name, 60), nl=False, fg=colors().NAME)
        click.secho('  %-9s' % age, nl=False, fg=colors().AGE)
        click.secho('  %-10s' % size, nl=False, fg=colors().SIZE)
        click.secho('  %-7s' % seed, nl=False, fg=colors().SEED)
        click.secho('%s' % leech, fg=colors().LEECH)

    while 1:
        opt = result_options(torrents)
        if opt == 0:
            break

def result_options(torrents):
    click.secho("\n%s" % '1 : Open in browser\t 2 : Download Torrent\t 0 : Exit', fg='red', bold=True)
    opt = click.prompt('> ')
    if opt == '1':
        tID = click.prompt('Torrent ID')
        if tID.isdigit() and int(tID) in range(1,len(torrents)+1):
            tID = int(tID) - 1
        else:
            click.secho("%s" % "Invalid ID!", fg='red', bold=True)
            return 0

        url = torrents[tID]['web']
        webbrowser.open_new_tab(url)
    elif opt == '2':
        pass
    else:
        return 0

    return 1

def get_params(**params):
    click.secho("%s" % 'Search type', fg='blue')
    strict = click.prompt(' -1: fuzzy\n  0: normal\n 1: strict\n')
    if strict.isdigit() and int(strict) in range(-1,2):
        params['strict'] = int(strict)

    click.secho("%s" % 'Safe search ON', fg='blue')
    safe = click.prompt('0 or 1')
    if safe.isdigit() and int(safe) in range(0,2):
        params['safe'] = int(safe)

    click.secho("%s" % 'Only verified torrent', fg='blue')
    verified = click.prompt('0 or 1')
    if verified.isdigit() and int(verified) in range(0,2):
        params['verified'] = int(verified)

    click.secho("%s" % 'Want to subtract some words from torrent name', fg='blue')
    yn_opt = click.prompt('y / n')
    if yn_opt == "y":
        subtract = click.prompt('Enter words to subtract')
        params['subtract'] = subtract

    click.secho("%s" % 'Uploads by certain user', fg='blue')
    yn_opt = click.prompt('y / n')
    if yn_opt == 'y':
        user = click.prompt('Enter username')
        params['user'] = user

    click.secho("%s" % 'Change torrents category', fg='blue')
    yn_opt = click.prompt('y / n')
    if yn_opt == 'y':
        category = click.prompt('Enter category')
        params['category'] = category

    click.secho("%s" % 'Sort result', fg='blue')
    yn_opt = click.prompt('y / n')
    if yn_opt == 'y':
        field = click.prompt('Enter field to sort')
        sorder = click.prompt('sorting order (asc/desc)')
        params['field'] = field
        params['sorder'] = sorder

    click.secho("%s" % 'Page Number', fg='blue')
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

    if check_status( data['status'] ):
        print_data( data['torrent'] )

def top_results(adv):
   category = click.prompt('Enter Category')

   page = 1
   if adv:
       page = click.prompt('Enter Page')
       if page.isdigit() and int(page) > 0:
            page = int(page)

   data = json.loads( ktorrent.top(category=category, page=page) )

   if check_status( data['status'] ):
       print_data( data['torrent'] )

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-s', '--search', is_flag=True, help='Search Torrent')
@click.option('-t', '--top', is_flag=True, help='Top Torrent')
@click.option('-a', '--adv', is_flag=True, help='Advance Options')
def main(search, top, adv):
    """katCLI"""
    if search and top:
        click.secho("%s" % "Choose only one function", fg='red', bold=True)
    elif search:
        search_results(adv)
    elif top:
        top_results(adv)
    else:
        click.secho("%s" % "Function argument missing", fg='red', bold=True)

if __name__ == "__main__": main()
