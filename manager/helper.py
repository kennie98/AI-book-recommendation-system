import ast

class Helper:

    @staticmethod
    def getListFromRecords(bookList, titleList):
        result = []
        bookTitleList = ast.literal_eval(titleList)

        for title in bookTitleList:
            for book in bookList:
                if book['Title'].lower() == title['title']:
                    del book['_id']
                    result.append(book)
                    break
        return result
