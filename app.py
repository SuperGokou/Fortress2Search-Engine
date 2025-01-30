from flask import Flask, render_template, request, redirect, url_for
import searchEngine
import autoComplete
import re
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)


def fliterList(Lists):
    # tuple list to list
    lists = [item for items in Lists for item in items]
    newlist = []
    for list in lists:
        list = re.sub(r'\\', '', list)
        newlist.append(list)
    return newlist


def newList(list, offset=0, per_page=10):
    return list[offset: offset + per_page]


def wordsCheck(inputlist):
    if 'bm25' or 'tfidf' or 'view' or 'rel' in inputlist:
        if "bm25" in inputlist:
            searchE = 0
        elif "tfidf" in inputlist:
            searchE = 1
        elif "view" in inputlist:
            searchE = 2
        else:
            searchE = 5

    return searchE


@app.route('/', methods=['POST', 'GET'])
def homePage():  # put application's code here
    if request.method == 'POST':
        query = request.form.get(r'inputWords')
        ad1 = request.form.get(r'class')
        if ad1:
            query = query + " " + ad1
        else:
            query = query + " " + 'None'
        ad2 = request.form.get(r'quality')
        if ad2:
            query = query + " " + ad2
        else:
            query = query + " " + 'None'
        ad3 = request.form.get(r'grade')
        if ad3:
            query = query + " " + ad3
        else:
            query = query + " " + 'None'
        return redirect(url_for("dataPage", query=query))

    elif request.method == 'GET':
        auto = autoComplete.autoComplete()
        auto = fliterList(auto)
        return render_template('Index.html', languages=auto)
    else:
        return render_template('Index.html')


@app.route('/dataPage/<query>')
def dataPage(query):
    list = query.split()
    relativeList = ['bm25', 'tfidf', 'view', 'rel']
    newlist = [False for i in relativeList if i not in list]

    if 4 > len(newlist) > 0:
        query = " ".join(list[:-1])
        ad1 = 'None'
        ad2 = 'None'
        ad3 = 'None'
    else:
        query = " ".join(list[:-3])
        ad3 = list[-1]
        ad2 = list[-2]
        ad1 = list[-3]

    searchE = wordsCheck(list)

    adFlag = 0
    if ad1 != 'None':
        if len(ad1) > 0:
            adFlag = 1
    if ad2 != 'None':
        if len(ad2) > 0:
            adFlag += 2
    if ad3 != 'None':
        if len(ad3) > 0:
            adFlag += 4
    if not query:
        return render_template('Index.html')
    else:
        if searchE == 0:
            rel, costtime = searchEngine.queryBM25Search(query)
        elif searchE == 1:
            rel, costtime = searchEngine.queryWikiIdSearch(query)
        elif searchE == 2:
            rel, costtime = searchEngine.queryFrqsearch(query)
        else:
            rel, costtime = searchEngine.querySearch(query)
        if not rel:
            return render_template('404.html')
        else:
            groups = []
            for i in range(0, len(rel)):
                flag = 0
                for j in range(0, len(groups)):
                    if (rel[i][0] in groups[j][0][0]):
                        groups[j].append(rel[i])
                        flag = 1
                # Only ran if the item is not in a group already
                if not flag:
                    if adFlag == 0:
                        groups.append([rel[i]])
                    # Class
                    elif adFlag == 1:
                        if ad1 in rel[i][5]:
                            groups.append([rel[i]])
                    # Quality
                    elif adFlag == 2:
                        if ad2 in rel[i][2]:
                            groups.append([rel[i]])
                    # Quality & Class
                    elif adFlag == 3:
                        if ad1 in rel[i][5]:
                            if ad2 in rel[i][2]:
                                groups.append([rel[i]])
                    # Grade
                    elif adFlag == 4:
                        if rel[i][3] != None:
                            if ad3 in rel[i][3]:
                                groups.append([rel[i]])
                    # Class & Grade
                    elif adFlag == 5:
                        if rel[i][3] != None:
                            if ad1 in rel[i][5]:
                                if ad3 in rel[i][3]:
                                    groups.append([rel[i]])
                    # Quality & Grade
                    elif adFlag == 6:
                        if rel[i][3] != None:
                            if ad2 in rel[i][2]:
                                if ad3 in rel[i][3]:
                                    groups.append([rel[i]])
                    # Class & Quality & Grade
                    elif adFlag == 7:
                        if rel[i][3] != None:
                            if ad1 in rel[i][5]:
                                if ad2 in rel[i][2]:
                                    if ad3 in rel[i][3]:
                                        groups.append([rel[i]])

            page, per_page, offset = get_page_args(page_parameter='page',
                                                   per_page_parameter='per_page')
            total = len(groups)
            groups = newList(groups, offset=offset, per_page=per_page)
            pagination = Pagination(page=page,
                                    per_page=per_page,
                                    offset=offset,
                                    total=total,
                                    css_framework='foundation',
                                    record_name='groups')

            datas = groups[:3]
            print(datas)
            relist = []
            for data in datas:
                biglist = []
                for items in data:
                    tuplelist = []
                    for item in items:
                        item = str(item)
                        string = item.replace('<b>', '')
                        string = string.replace('</b>', '')
                        tuplelist.append(string)
                    tuplelist = tuple(tuplelist)
                    biglist.append(tuplelist)
                relist.append(biglist)
            print(relist)

            return render_template('Result.html', results=groups, searchquery=query, costTime=round(costtime, 5),
                                   number=total, similar_query1=query, newresults=relist,
                                   pagination=pagination, page=page, per_page=per_page)

@app.route('/groupPage')
def groupPage():
    group = request.args.get('group')

    group = group.translate({ ord('['): None })
    group = group.translate({ ord('('): None })
    group = group.translate({ ord(')'): None })
    group = group.translate({ ord(']'): None })
    group = group.translate({ ord('}'): None })
    group = group.translate({ ord('{'): None })
    group = group.translate({ ord('\''): None })
    group = group.translate({ ord('"'): None })
    #Rebuild the Groups
    print(group)
    items = group.split(',')
    print(items)
    group = []
    i = 0
    while i < len(items):
        j = 0
        temp = []
        while j <= 9:
            print(i)
            print(j)
            if(i+j > len(items)-1):
                break
            if(items[i+j] == None):
                break
            if(items[i+j][0] == ' '):
                items[i+j] = items[i+j][1:]
            items[i+j] = re.sub('\\\\n', '', items[i+j])
            items[i+j] = items[i+j].translate({ ord('\\'): None })
            temp.append(items[i+j])
            j += 1
        if(len(group) > 50):
            if(group[0][0] == temp[0][0]):
                group.append(temp)
        else:
            group.append(temp)
        i += 10

    page, per_page, offset = get_page_args(page_parameter='page',
                                                   per_page_parameter='per_page')
    costtime = 0
    query = ""
    total = len(group)
    groups = newList(group, offset=offset, per_page=per_page)
    pagination = Pagination(page=page,
                                    per_page=per_page,
                                    offset=offset,
                                    total=total,
                                    css_framework='foundation',
                                    record_name='groups')
    return render_template('Groups.html', results=groups, searchquery=query, costTime=round(costtime, 5),
                                   number=total, similar_query1=query, similar_query2=query,
                                   pagination=pagination, page=page, per_page=per_page)
@app.route('/results')
def resultPage():  # put application's code here
    query = request.args.get('query')
    sortby = request.args.get('order')

    if not sortby:
        query = query + " " + "rel"
    else:
        query = query + " " + sortby

    return redirect(url_for("dataPage", query=query))


if __name__ == '__main__':
    app.run()
