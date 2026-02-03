"""Team Fortress 2 Item Search Engine - Flask Application."""

from flask import Flask, render_template, request, redirect, url_for
import re
from flask_paginate import Pagination, get_page_args

from src import search_engine, autocomplete

app = Flask(__name__)


def filter_list(items):
    """Convert tuple list to flat list and remove backslashes."""
    flat_list = [item for row in items for item in row]
    return [re.sub(r'\\', '', item) for item in flat_list]


def paginate_list(data, offset=0, per_page=10):
    """Return a slice of the list for pagination."""
    return data[offset: offset + per_page]


def get_search_type(query_parts):
    """Determine search type from query parts."""
    if 'bm25' in query_parts:
        return 0
    elif 'tfidf' in query_parts:
        return 1
    elif 'view' in query_parts:
        return 2
    else:
        return 5


@app.route('/', methods=['POST', 'GET'])
def home_page():
    """Render the home page with search form."""
    if request.method == 'POST':
        query = request.form.get('inputWords', '')
        ad1 = request.form.get('class') or 'None'
        ad2 = request.form.get('quality') or 'None'
        ad3 = request.form.get('grade') or 'None'

        query = f"{query} {ad1} {ad2} {ad3}"
        return redirect(url_for("data_page", query=query))

    elif request.method == 'GET':
        auto = autocomplete.get_suggestions()
        auto = filter_list(auto)
        return render_template('index.html', languages=auto)

    return render_template('index.html')


@app.route('/dataPage/<query>')
def data_page(query):
    """Process search query and display results."""
    query_parts = query.split()
    search_keywords = ['bm25', 'tfidf', 'view', 'rel']
    has_search_keyword = any(kw in query_parts for kw in search_keywords)

    if has_search_keyword and len(query_parts) >= 1:
        if len(query_parts) <= 4:
            search_query = " ".join(query_parts[:-1])
            ad1 = 'None'
            ad2 = 'None'
            ad3 = 'None'
        else:
            search_query = " ".join(query_parts[:-4])
            ad3 = query_parts[-2]
            ad2 = query_parts[-3]
            ad1 = query_parts[-4]
    else:
        search_query = " ".join(query_parts[:-3]) if len(query_parts) > 3 else ""
        ad3 = query_parts[-1] if len(query_parts) >= 1 else 'None'
        ad2 = query_parts[-2] if len(query_parts) >= 2 else 'None'
        ad1 = query_parts[-3] if len(query_parts) >= 3 else 'None'

    search_type = get_search_type(query_parts)

    ad_flag = 0
    if ad1 != 'None' and ad1:
        ad_flag = 1
    if ad2 != 'None' and ad2:
        ad_flag += 2
    if ad3 != 'None' and ad3:
        ad_flag += 4

    if not search_query:
        return render_template('index.html')

    if search_type == 0:
        rel, costtime = search_engine.query_bm25_search(search_query)
    elif search_type == 1:
        rel, costtime = search_engine.query_wiki_id_search(search_query)
    elif search_type == 2:
        rel, costtime = search_engine.query_frequency_search(search_query)
    else:
        rel, costtime = search_engine.query_search(search_query)

    if not rel:
        return render_template('404.html')

    groups = []
    for item in rel:
        flag = 0
        for group in groups:
            if item[0] in group[0][0]:
                group.append(item)
                flag = 1
                break

        if not flag:
            should_add = False
            if ad_flag == 0:
                should_add = True
            elif ad_flag == 1:
                should_add = ad1 in item[5]
            elif ad_flag == 2:
                should_add = ad2 in item[2]
            elif ad_flag == 3:
                should_add = ad1 in item[5] and ad2 in item[2]
            elif ad_flag == 4:
                should_add = item[3] is not None and ad3 in item[3]
            elif ad_flag == 5:
                should_add = item[3] is not None and ad1 in item[5] and ad3 in item[3]
            elif ad_flag == 6:
                should_add = item[3] is not None and ad2 in item[2] and ad3 in item[3]
            elif ad_flag == 7:
                should_add = (item[3] is not None and ad1 in item[5] and
                              ad2 in item[2] and ad3 in item[3])

            if should_add:
                groups.append([item])

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(groups)
    groups = paginate_list(groups, offset=offset, per_page=per_page)
    pagination = Pagination(page=page,
                            per_page=per_page,
                            offset=offset,
                            total=total,
                            css_framework='foundation',
                            record_name='groups')

    datas = groups[:3]
    relist = []
    for data in datas:
        biglist = []
        for items in data:
            tuplelist = []
            for item in items:
                item_str = str(item)
                clean_str = item_str.replace('<b>', '').replace('</b>', '')
                tuplelist.append(clean_str)
            biglist.append(tuple(tuplelist))
        relist.append(biglist)

    return render_template('result.html', results=groups, searchquery=search_query,
                           costTime=round(costtime, 5), number=total,
                           similar_query1=search_query, newresults=relist,
                           pagination=pagination, page=page, per_page=per_page)


@app.route('/groupPage')
def group_page():
    """Display grouped item results."""
    group = request.args.get('group', '')

    chars_to_remove = '[](){}\'\"'
    for char in chars_to_remove:
        group = group.replace(char, '')

    items = group.split(',')
    group_list = []
    i = 0

    while i < len(items):
        temp = []
        for j in range(10):
            if i + j > len(items) - 1:
                break
            if items[i + j] is None:
                break

            item = items[i + j]
            if item and item[0] == ' ':
                item = item[1:]
            item = re.sub(r'\\n', '', item)
            item = item.replace('\\', '')
            temp.append(item)

        if len(group_list) > 50:
            if temp and group_list[0][0] == temp[0][0]:
                group_list.append(temp)
        else:
            group_list.append(temp)
        i += 10

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    costtime = 0
    search_query = ""
    total = len(group_list)
    groups = paginate_list(group_list, offset=offset, per_page=per_page)
    pagination = Pagination(page=page,
                            per_page=per_page,
                            offset=offset,
                            total=total,
                            css_framework='foundation',
                            record_name='groups')

    return render_template('groups.html', results=groups, searchquery=search_query,
                           costTime=round(costtime, 5), number=total,
                           similar_query1=search_query, similar_query2=search_query,
                           pagination=pagination, page=page, per_page=per_page)


@app.route('/results')
def result_page():
    """Handle search results with sorting options."""
    query = request.args.get('query', '')
    sortby = request.args.get('order')

    if not sortby:
        query = query + " rel"
    else:
        query = query + " " + sortby

    return redirect(url_for("data_page", query=query))


if __name__ == '__main__':
    app.run(debug=True)
