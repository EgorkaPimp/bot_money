import db.database, db.serch_match
import create_graph
import os

class View():

    def view_cat(categories, user_id, type_cat, data_month=None, data_day=None, data_year=None):
        view_map = {}
        view_end = ""
        view_sum = 0
        moneys = []
        graph = None
        for category in categories:
            sum_month = db.serch_match.search_money(user_id, category[0],
                                                    data_month, data_day, data_year, type_cat)
            sum_all = 0
            for sum_cat in sum_month:
                if ',' in str(sum_cat[0]):
                    value = float(sum_cat[0].replace(',', '.'))
                else:
                    value = sum_cat[0]
                sum_all = sum_all + value
            moneys.append(sum_all)
            view_map.setdefault(category[0], sum_all)
        if type_cat == 'expenses':
            graph = create_graph.cmd_graph(categories, moneys, user_id)
        for i in view_map:
            line = f"*{i}* - {view_map[i]} \n"
            view_end = view_end + line
            view_sum = view_sum + view_map[i]
        return view_end, view_sum, graph

    def del_graph(user_id):
        os.remove(f"graph/graph_test_{user_id}.png")