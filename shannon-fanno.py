import math
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import operator

class ShanonFanno(object):

    def __init__(self):
        self.sum_logs_with_pis = 0
        self.size_after_compress = 0
        self.sorted_s = ""
        self.char_dict = dict()

    def devide_chars(self, x, itr, code):
        '''makes the tree recursively'''
        if len(x) == 2 : return [[x[0], itr + 1, code + "0"], [x[1], itr + 1, code + "1"]]
        if len(x) == 1 : return [[x, itr, code]]
        index = self.break_the_node(x)
        return [self.devide_chars(x[:index+1], itr + 1, code + "0"), self.devide_chars(x[index+1:], itr + 1, code + "1")]

    def make_count(self):
        '''returns a dict of chars with counts + string with sorted chars by appearence'''

        self.char_dict = dict(Counter(self.sentence))
        char_ls = sorted(self.char_dict.items(), key=operator.itemgetter(1),reverse=True)
        sorted_s = ""
        for i in char_ls :
            sorted_s += i[0]
        return self.char_dict, sorted_s

    def flatten_the_tree(self, tree):
            leaf = False
            flat_list = []
            if len(tree) == 1 : tree = tree[0]
            while(leaf == False):


                if type(tree[-1]) is not list: 
                    if len(tree) != 3 : break
                    #достижение листа и вычисление числа пи

                    leaf = True
                    pi = self.sentence.count(tree[0])/self.total
                    log_pi = math.log(1/pi, 2)
                    x = tree.copy()
                    x.append(pi)
                    self.sum_logs_with_pis += pi * log_pi
                    return [x]
                else:
                    # идет рекурсивно вправо и влево

                    flat_right = []
                    flat_left = []
                    flat_right.extend(self.flatten_the_tree(tree[0]))
                    flat_left.extend(self.flatten_the_tree(tree[1]))
                    flat_list.extend(flat_right)
                    flat_list.extend(flat_left)
                    return flat_list




    def break_the_node(self, node):
        total = 0
        for i in node :
            total += self.char_dict[i]
        length = len(node)
        count = 0
        last_char_index = 0
        for i in range(length//2):
            count += self.char_dict[self.sorted_s[i]]
            if (count - (total/2) >= 0):
                last_char_index = i +1
                break
        return last_char_index

    def plot_bar(self):
        x_labels = list(map(lambda x : x[0], self.final_flat))
        y = list(map(lambda x : x[1], self.final_flat))
        plt.bar(range(len(y)), y, align='center', alpha=0.5)
        plt.xticks(range(len(y)), x_labels)
        plt.ylabel('recurrence')
        plt.title('Chars in the sentence')
        plt.show()
        
    def plot_pie(self):
        x_labels = list(map(lambda x : x[0], self.final_flat))
        y = list(map(lambda x : x[1], self.final_flat))
        plt.pie(y, labels=x_labels, autopct='%1.1f%%',  startangle=90)
        plt.show()

    def display_compressed(self):
        np_final_flat = np.array(sh.final_flat)
        keys = np_final_flat[:,0]
        values = np_final_flat[:,2]
        chars_encoded_dict = dict(zip(keys, values))
        f=open("encoded.txt","a")
        for ch in self.sentence:
            print(chars_encoded_dict[ch], end=" ")
            f.write("{} ".format(chars_encoded_dict[ch]))
        f.write("= {}\n".format(self.sentence))
        f.close()
        print(self.sentence)
        
                                  
    def do_the_work(self,s):
        self.sentence = s
        self.total = len(s)
        self.char_dict, self.sorted_s = self.make_count()
        # сгенерируйте узлы, разделив исходный
        last_char_index = self.break_the_node(self.sorted_s)
        left = self.sorted_s[:last_char_index]
        right = self.sorted_s[last_char_index:]
        #делать дерево
        left_tree = self.devide_chars(left, 1, "0")
        right_tree = self.devide_chars(right, 1, "1")

        #вычисление числа Пи и сглаживание дерева, чтобы упростить вычисление

        left_flat = self.flatten_the_tree(left_tree)
        right_flat = self.flatten_the_tree(right_tree)
        self.final_flat = []
        self.final_flat.extend(left_flat)
        self.final_flat.extend(right_flat)
        self.write_final_logs(self.final_flat)

    def write_final_logs(self, final_flat):
        '''here is the final logs'''
        b1 = 0
        for i in final_flat :
                count = self.sentence.count(i[0])
                b1 += count*i[1]
                print("Symbol: {0} => [Pi: {1}], [Code: {2}], [Freq.: {3}], [No. of Bits: {4}]".format(i[0],i[-1],i[2],count,i[1]*count))
        b0 = len(self.sentence)*8



f = open("text.txt","r")
s2 = str(f.read())
f.close()
sh = ShanonFanno()
sh.do_the_work(s2)
sh.display_compressed()

