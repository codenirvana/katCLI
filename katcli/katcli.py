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


@click.command()
@click.option('-c', '--cat', 'category', default='all', help='Torrent Category')
@click.option('-f', '--field', 'field', default='seed', help='Select field to sort')
@click.option('-s', '--sort', 'sorder', default='desc', help='Select Sorting Order')
@click.option('-p', '--page', 'page', default='1', help='Page')
def main(category, field, sorder, page):
    click.secho("Search For: ", nl=False, fg='white', bold=True)
    search = input()
    #try:
    data = ktorrent.search(search=search, category=category, field=field, sorder=sorder, page=int(page))
    print(data)
    #except:
        #print("Couldn't retrieve data")

if __name__ == "__main__": main()
