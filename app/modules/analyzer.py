def analyze(product_id):
    if product_id == None:
        return None
    else:
        import os
        import sys
        import numpy as np
        import pandas as pd
        from opcode import opname
        from fileinput import filename
        from numpy import average, product
        from matplotlib import pyplot as plt

        
        opinions = pd.read_json(f"opinions/{product_id}.json")

        opinions_count = len(opinions)
        pros_count = opinions["pros"].map(bool).sum()
        cons_count = opinions["cons"].map(bool).sum()
        average_score = opinions["score"].mean().round(2)
        data = {
                'id': product_id,
                'n': opinions_count,
                'p': pros_count,
                'c': cons_count,
                'a': average_score
            }
        return data
