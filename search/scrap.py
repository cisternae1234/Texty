from bs4 import BeautifulSoup
from . import models
import ksalib.ksalib.gaonnuri as gaonnuri
import ksalib.ksalib.lms as lms

gaonnuri_name = '가온누리'
gaonnuri_board_name = gaonnuri_name + ' {}'
lms_name = 'LMS'
lms_board_name = lms_name + ' {}'

# read id and pw from text file
def read_id_pw(path):
    f = open(path)
    text = f.readlines()
    return text[0], text[1]

# all links are saved in Page model
def all_links_saved(links):
    for i in range(len(links)):
        find = models.Page.objects.filter(link=links[i])
        if len(find) == 0:
            return False
    return True

def save_gaonnuri_page(auth, link):
    find = models.Page.objects.filter(link=link)
    if len(find) == 0:
        response = gaonnuri.get_gaonnuri_response(auth, link)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        page_model = models.Page(website=gaonnuri_name, link=link, title=title, content='')
        page_model.save()

def save_all_gaonnuri_page(auth):
    gaonnuri_links = [
        'https://gaonnuri.ksain.net/xe/',
        'https://gaonnuri.ksain.net/mentoring/',
    ]
    board_names = gaonnuri.get_board_names(auth)
    for board in board_names:
        gaonnuri_links.append(gaonnuri.board_url.format(board))
    special_links = gaonnuri.get_special_links(auth)
    gaonnuri_links.extend(special_links)
    for link in gaonnuri_links:
        save_gaonnuri_page(auth, link)
        print(link)

def save_gaonnuri_post(auth, link, board):
    find = models.Page.objects.filter(link=link)
    if len(find) == 0:
        post = gaonnuri.Post(auth, link)
        website = gaonnuri_board_name.format(board)
        comments = '\n'.join([f'{comment.author} {comment.content}' for comment in post.comments])
        content = f'{post.text()} {comments}'
        post_model = models.Page(website=website, link=link, title=post.title, content=content, author=post.author,
                                 time=post.time)
        post_model.save()

def save_gaonnuri_board(auth, board_name, board_names):
    print(board_names[board_name])
    board = gaonnuri.Board(auth, board_name)
    page_num = board.page_num()
    for page in range(1, page_num+1):
        print(f'Page: {page}/{page_num}')
        links = board.links_in_page(page)
        if all_links_saved(links):
            break
        for i in range(len(links)):
            print(f'{links[i]} {i+1}/{len(links)}')
            try:
                save_gaonnuri_post(auth, links[i], board_names[board_name])
            except:
                print('error')

def save_all_gaonnuri_post(auth):
    board_names = gaonnuri.get_board_names(auth)
    for board_name in board_names.keys():
        save_gaonnuri_board(auth, board_name, board_names)

def save_lms_post(auth, link, board):
    find = models.Page.objects.filter(link=link)
    if len(find) == 0:
        post = lms.Post(auth, link)
        website = lms_board_name.format(board)
        content = ''
        for file in post.files:
            content += f'{file}\n'
        content += f'{post.article}\n'
        for comment in post.comments:
            content += f'{comment.author} {comment.content}\n'
        post_model = models.Page(website=website, link=link, title=post.title, author=post.author, content=content, time=post.time)
        post_model.save()

def save_lms_board(auth, scBCate):
    board = lms.Board(auth, scBCate)
    print(str(board))
    for page in range(1, board.page_num+1):
        print(f'Page: {page}/{board.page_num}')
        links = board.get_links_page(page)
        if all_links_saved(links):
            break
        for i in range(len(links)):
            print(f'{links[i]} {i+1}/{len(links)}')
            try:
                save_lms_post(auth, links[i], str(board))
            except:
                print('error')

def save_all_lms_post(auth):
    boards = lms.get_all_boards(auth)
    for board in boards.keys():
        save_lms_board(auth, board)
