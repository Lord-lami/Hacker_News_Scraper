import requests
from bs4 import BeautifulSoup
import pprint
from sys import argv

def page_selector(list_of_pages):
	for page_number in list_of_pages:
		resp = requests.get(f'https://news.ycombinator.com/?p={int(page_number)}')
		egusi = BeautifulSoup(resp.text, 'html.parser')
		story_links = egusi.select('.titleline')
		story_votes = egusi.select('.subtext')
		yield {'link':story_links, 'vote': story_votes}

def sorted_by_votes(hnlist):
	return sorted(hnlist, key = lambda hnlink: hnlink['points'], reverse = True)


def create_custom_hn(links, votes):
	hn = []
	for i, tag in enumerate(links):
		title = tag.getText()
		link = tag.select('a')[0].get('href')
		if len(tag.select('a')) > 1:
			from_link = tag.select('a')[1].get('href')  
		else: 
			from_link = ''
			link = 'https://news.ycombinator.com/' + link
		
		if len(votes[i].select('.score')):
			vote = int(votes[i].select('.score')[0].getText().split(" ")[0])
		else:
			vote = 0

		if vote > 99:
			hn.append({'title': title, 'link': link, 'from_link': from_link, 'points': vote})
	return sorted_by_votes(hn)

def main():
	pg_list = []
	if len(argv) == 2:
		pg_list.append(int(argv[1]))
		print('tTWO')
	elif len(argv) > 2:
		pg_list = list(range(int(argv[1]), int(argv[2]) + 1))
		print('tTWO')
	elif len(argv) < 2:
		print('You need to pass a [age number or a range of page numbers as an argument]')
		raise ValueError
	page_gen = page_selector(pg_list)
	for i, page in enumerate(page_gen):
		print()
		print(f'CUSTOMIZED HACKER NEWS PAGE {pg_list[i]}')
		custom_page = create_custom_hn(page['link'], page['vote'])
		pprint.pprint(custom_page)
		print()


if __name__ == '__main__':
	main()
