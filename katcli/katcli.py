import click, ktorrent

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

def print_data(data):
    count = 0

    click.secho("%-3s  %-60s    %-20s    %-20s    %s  " % ("#", "NAME", "AGE", "SIZE", "SEED / LEECH"), bold=True, fg="white", reverse=True)

    for torrent in data:
        count += 1
        name = torrent['name']
        age = torrent['age']
        size = torrent['size']
        seed = torrent['seed']
        leech = torrent['leech']

        click.secho("%-3s" % str(count), nl=False, fg=colors().COUNT, bold=True)
        click.secho('  %-60s' % cap(name, 60), nl=False, fg=colors().NAME)
        click.secho('    %-20s' % age, nl=False, fg=colors().AGE)
        click.secho('    %-20s' % size, nl=False, fg=colors().SIZE)
        click.secho('     %-7s' % seed, nl=False, fg=colors().SEED)
        click.secho('%s' % leech, fg=colors().LEECH)

def search_basic():
    pass

def search_adv():
    pass

def top_basic():
    pass

def top_adv():
    pass

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
        search_basic if adv else search_adv
    elif top:
        top_basic if adv else top_adv
    else:
       print("Function argument missing")

if __name__ == "__main__": main()
