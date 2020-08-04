from getVisited_Title_And_ISBN_And_ssSet import getPack_title_isbn_ssSet,get_douban_urls
# from getIIDFromISBN import get_iids_from_isbn
from getSSfromIID import get_ss_list_from_iid_list,isValid_ss

import os

book_dir=r"D:\AllDowns\newbooks"
reference_dir=r"D:\AllDowns\upload_results"
reference_text_path=r"D:\AllDowns\upload_results\Books And IDs.txt"

def get_abs_path(book_name_with_pdf):
    return book_dir+os.sep+book_name_with_pdf

def writeOne_reference_text(new_title):
    assert os.path.exists(reference_dir)

    isbn=new_title.rsplit("isbnisbn",maxsplit=1)[1]
    one_line="{}\t{}".format(new_title,isbn)
    with open(reference_text_path,"a",encoding="utf-8") as f:
        f.write(one_line)


def main():
    books=sorted(os.listdir(book_dir),key=lambda x: os.path.getmtime(os.path.join(book_dir, x)),reverse=True)
    # print(len(books))
    pickout_douban_urls=get_douban_urls(max_cnt=len(books)*3)
    # pickout_douban_urls=douban_urls[0:len(books)]
    packs=[]

    for each_pick_url in pickout_douban_urls:
        pack=getPack_title_isbn_ssSet(each_pick_url)
        packs.append(pack)



    for book in books:
        ss_title=book.strip(".pdf")
        if isValid_ss(ss_title):
            print("YesYesYes")
            for each_pack in packs:
                ss_set=each_pack[2]
                if ss_title in ss_set:
                    title=each_pack[0]
                    isbn=each_pack[1]
                    new_title="{}isbnisbn{}".format(title,isbn)
                    new_filename=new_title+".pdf"
                    old_abs=get_abs_path(book)
                    new_abs=get_abs_path(new_filename)
                    os.rename(old_abs,new_abs)
                    print("One Done.")

                    writeOne_reference_text(new_title)
                    print("One Written.")

    print("All Done.")
    print("All Written.")

if __name__ == '__main__':
    main()