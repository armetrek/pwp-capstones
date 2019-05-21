class User(object):
	def __init__(self, name, email):
		self.name = name
		self.email = email
		self.books = {}

	def get_email(self):
		return "{name}'s email address is {email}".format(name=self.name,email=self.email)

	def change_email(self, address):
		self.email = address
		return "{}'s email address has been updated".format(self.name)

	def __repr__(self):
		b_ct = len(self.books)
		return "User: {name}, email: {email}, books read: {books}".format(name=self.name,email=self.email,books=b_ct) 

	def __eq__(self, other_user):
		if self.name == other_user.name and self.email == other_user.email:
			return True
		else:
			return False

	def read_book(self,book,rating=None):
		self.books.update({book:rating})
		
	def get_average_rating(self):
		a_rate = 0
		a_count = 0
		for rating in self.books.values():
			if type(rating) == int:
				a_rate += rating
				a_count += 1
		return a_rate/a_count
		
class Book():
	def __init__(self,title,isbn):
		self.title = title
		self.isbn = isbn
		self.ratings = []
		
	def __repr__(self):
		#I added this because the return was looking weird without it
		return "The book, {title}, has an isbn of {isbn}".format(title=self.title,isbn=self.isbn)
	
	def get_title(self):
		return "The title of the book is {}".format(self.title)
		
	def get_isbn(self):
		return "The ISBN of the book, {title}, is {isbn}".format(title=self.title,isbn=self.isbn)
		
	def set_isbn(self,new_isbn):
		self.isbn = new_isbn
		print("The ISBN of the book, {}, has been updated".format(self.title))

	def add_rating(self,rating):
		if type(rating) == int:
			if rating >= 0 and rating <= 4:
				self.ratings.append(rating)
			else:
				return "Invalid Rating"
		else:
			return "Invaild Rating"
	
	def __eq__(self, other_book):
		self.title == other_book.title and self.isbn == other_book.isbn
		
	def get_average_rating(self):
		a_rate = 0
		for rating in self.ratings:
			if type(rating) == int:
				a_rate += rating
		return a_rate/len(self.ratings)
		
	def __hash__(self):
		return hash((self.title, self.isbn))


class Fiction(Book):
	def __init__(self,title,author,isbn):
		super().__init__(title,isbn)
		self.author = author
		
	def get_author(self):
		return "The writer of {title} is {author}".format(title=self.title,author=self.author)
		
	def __repr__(self):
		return "The book, {title}, was written by {author}".format(title=self.title,author=self.author)

class Non_Fiction(Book):
	def __init__(self,title,subject,level,isbn):
		super().__init__(title,isbn)
		self.subject = subject
		self.level = level
		
	def get_subject(self):
		return "The subject of {title} is {subject}".format(title=self.title,subject=self.subject)
		
	def get_level(self):
		return "The level of {title} is {level}".format(title=self.title,level=self.level)
		
	def __repr__(self):
		return "{title}, a {level} manual on {subject}".format(title=self.title,subject=self.subject,level=self.level)

class TomeRater():
	def __init__(self):
		#self.users maps an email to a User object {email:User}
		self.users = {}
		#self.books maps a Book to the number of Users that have read it {Book:count}
		self.books = {}
		
	def create_book(self,title,isbn):
		#check whether a book exists with this isbn
		#n_book is True if the ISBN already exists
		n_book = False
		for book in self.books:
			if book.get_isbn() == isbn:
				n_book = True
		if n_book == True:
			print('A book with this ISBN already exists')
		else:
			return Book(title,isbn)
	def create_novel(self,title,author,isbn):
		return Fiction(title,author,isbn)
		
	def create_non_fiction(self,title,subject,level,isbn):
		return Non_Fiction(title,subject,level,isbn)
		
	def add_book_to_user(self,book,email,rating = None):
		if email in self.users:
			#add the book to the user's books
			self.users[email].read_book(book,rating)
			#add the rating to the book's ratings
			book.add_rating(rating)
			#check if the book is already in self.books
			if book in self.books:
				self.books[book] += 1
			else:
				self.books[book] = 1
		else:
			return "There is no user with email {email}!".format(email=email)

	def add_user(self,name,email,user_books = None):
		#check whether the email address includes an @ and a proper domain
		if '@' in email:
			if '.com' in email or '.edu' in email or '.org' in email:
				#check whether name already exists in the list of users
				if email in self.users:
					print ('A user with this email already exists.')
				else:
					new_user = User(name,email)
					#this part adds a key:value pair to self.users, though the instructions do not seem to require that I do so
					#this part should actually first check if self.users[name] already exists, I suppose
					self.users[email] = new_user
		else:
			print('Please enter a valid email address')
		if user_books != None:
			for book in user_books:
				#print(book)
				self.add_book_to_user(book,email)
		
	def print_catalog(self):
		#the instructions are to iterate through all of the keys in self.books, and print them
		for book in self.books:
			print(book)
			
	def print_users(self):
		#the instructions are to iterate through all of the values in self.users, and print them
		for name in self.users.values():
			print(name)
			
	def most_read_book(self):
		#the instructions are to iterate through all of the books in self.books, and return the book that been read the most
		b_count = 0
		most_read = ""
		for book,readers in self.books.items():
			if readers > b_count:
				b_count = readers
				most_read = book
		return 'The most read book is {book}, which has been read by {readers} Users!'.format(book=most_read,readers=b_count)

	def highest_rated_book(self):
		b_rate = 0
		best_book = ""
		for book in self.books:
			c_rate = book.get_average_rating()
			if c_rate > b_rate:
				b_rate = c_rate
				best_book = book
		return 'The best book is {best}, with an average rating of {rating}'.format(best=best_book,rating=b_rate)
		
	def most_positive_user(self):
		#b_rate is the higest average rating
		b_rate = 0
		#best_reader is the name of the person with the highest average rating
		best_reader = ""
		for user in self.users.values():
			c_rate = user.get_average_rating()
			if c_rate > b_rate:
				b_rate = c_rate
				best_reader = user
		return 'The best reader is {reader}, with an average rating of {rating}'.format(reader=best_reader,rating=b_rate)