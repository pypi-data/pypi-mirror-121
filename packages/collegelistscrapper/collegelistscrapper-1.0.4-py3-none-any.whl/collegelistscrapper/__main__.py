from .nichescrapper import NicheScrapper 

if __name__ == "__main__":
    # Take Input from User
    url = input("Enter the url :")
    filename = input("Enter filename to save :")
    obj = NicheScrapper(url=url, filename=filename)
    obj.run()