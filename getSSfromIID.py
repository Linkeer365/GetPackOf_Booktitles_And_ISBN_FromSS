from getIIDFromISBN import get_iids_from_isbn

def get_ss_str(iid_str):
	least_signif_two=int(iid_str[-2:])
	# print("Last two:\t",least_signif_two)
	base_num=least_signif_two+30
	base_str=str(base_num)
	# print("Base num:\t",base_num)
	two_char_list=[]
	for start in range(0,20,2):
		end=start+2
		two_char=iid_str[start:end]
		two_char_list.append(two_char)
	# print("BF:\t",two_char_list)
	two_char_list=[str(int(each_val,16)-int(base_str,16)) for each_idx,each_val in enumerate(two_char_list) if each_idx!=2 and each_idx!=6]
	# print("AF:\t",two_char_list)
	# ss_list=map(lambda x:str(x-base_num),two_char_list)
	ss_list=two_char_list
	ss_str="".join(ss_list)
	# print("Final ss list:\t",ss_list)
	return ss_str

def isValid_ss(some_ss_str):
    return not some_ss_str[0]=='0'


def get_ss_list_from_iid_list(some_iid_list):
    # assert some_iid_list!="NIL"
    if some_iid_list=="NIL":
        ss_list=['']
        return ss_list
    ss_list = []
    for each_iid in some_iid_list:
        ss_str = get_ss_str(each_iid)
        if isValid_ss(ss_str):
            ss_list.append(ss_str)
    # print("SS List", ss_list)
    return ss_list


def main():
    broken_isbn="9787301167045"
    multi_isbn="9787509749296"
    onlyone_isbn="9787208060753"

    iid_list1=get_iids_from_isbn(broken_isbn)
    iid_list2=get_iids_from_isbn(multi_isbn)
    iid_list3=get_iids_from_isbn(onlyone_isbn)

    iid_lists=[iid_list1,iid_list2,iid_list3]

    for each_list in iid_lists:
        if each_list!="NIL":
            ss_list=get_ss_list_from_iid_list(each_list)


if __name__ == '__main__':
    main()



