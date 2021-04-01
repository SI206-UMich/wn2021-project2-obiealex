from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    book_lst = []
    name_lst = []
    lst = []
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, filename)
    file = open(full_path,'r', encoding='utf-8')
    soup = BeautifulSoup(file, 'html.parser')
    file.close()
    table = soup.find('table', class_= "tableList")
    titles = table.find_all('a', class_= 'bookTitle')
    authors = table.find_all('span', itemtype= "http://schema.org/Person")
    for title in titles:
        url = title.text
        book_lst.append(url.strip())
    for author in authors:
        url = author.text
        end = url.find(',')
        url = url[:end]
        #url = url_list[0]

        name_lst.append(url.strip())
    for i in range(len(book_lst)):
        lst.append((book_lst[i], name_lst[i]))
    return lst

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    base = "https://www.goodreads.com"
    lst = []
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table')
    urls = table.find_all('a', class_= 'bookTitle')
    for i in range(10):
        lst.append(base+urls[i].get('href'))
    return lst

def get_book_summary(book_urls):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    lst = []
    for book_url in book_urls:
        r = requests.get(book_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        info = soup.find('div', class_= "leftContainer")
        title_tag = info.find('h1', id = "bookTitle")
        title = title_tag.text.strip()

        author_tag = info.find('a', class_="authorName")
        author = author_tag.contents[0].text.strip()

        page_tag = info.find('span', itemprop = "numberOfPages")
        page_str = page_tag.text
        page = re.findall('\d+',page_str)
        page_num = int(page[0][:])
        tup = (title,author,page_num)
        lst.append(tup)

    return lst
   
def summarize_best_books(filename):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, filename)
    lst =[]
    with open(full_path,'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        info = soup.find_all('div', class_= "category clearFix")
        for item in info:
            category = item.find('h4',class_="category__copy").text.strip()
            title_tag = item.find('img', class_= "category__winnerImage")
            title = title_tag.get("alt")
            url_tag = item.find('a')
            url = url_tag.get("href")
            tup = (category,title,url)
            lst.append(tup)

    return lst


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, filename)
    with open(full_path, 'w', newline ='') as outcsv:
        file = csv.writer(outcsv)
        file.writerow(["Book Title","Author Name"])
        for i in data:
            file.writerow([i[0], i[1]])
            
            
 


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    #call get_search_links() and save it to a static variable: search_urls\

    def setUp(self):
        self.search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        self.titles = get_titles_from_search_results("search_results.htm")

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(self.titles), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(self.titles), type([]))
        # check that each item in the list is a tuple
        for title in self.titles:
            self.assertEqual(type(title),type((2,2)))
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(self.titles[0],("Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(self.titles[-1],("Harry Potter: The Prequel (Harry Potter, #0.5)","J.K. Rowling"))

    def test_get_search_links(self):
        var = self.search_urls
        # check that TestCases.search_urls is a list
        self.assertEqual(type(var), type([]))
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(var), 10)

        # check that each URL in the TestCases.search_urls is a string
        for url in var:
            self.assertEqual(type(url), type('hello'))
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            found = re.findall('www.goodreads.com/book/show/', url)
            self.assertTrue(len(found) != 0)

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = get_book_summary(self.search_urls)

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries),10)
            # check that each item in the list is a tuple
        for summary in summaries:
            self.assertEqual(type(summary), type((2,2)))
            # check that each tuple has 3 elements
            self.assertEqual(len(summary), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(summary[0]+summary[1]), type("hello"))
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(summary[2]), type(9))
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)
        

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(best), 20)

        for book in best:
            # assert each item in the list of best books is a tuple
            self.assertEqual(type(book),type((2,2)))
            # check that each tuple has a length of 3
            self.assertEqual(len(book),3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020')) 

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        data = get_titles_from_search_results("search_results.htm")
        print(data)
        filename = "test.csv"
        write_csv(data,filename)
        # call write csv on the variable you saved and 'test.csv'
        csv_lines = []

             
        with open(filename, 'r', newline ='') as csvread:
            file = csv.reader(csvread)
            
            for row in file:
                csv_lines.append(row)
             

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ["Book Title", "Author Name"])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1],['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])
        


if __name__ == '__main__':
#     print(extra_credit("extra_credit.htm"))
     unittest.main(verbosity=2)



