from ofxtools.Parser import OFXTree
import re
parser = OFXTree()
with open('OFXData.ofx', 'rb') as f:  # N.B. need to open file in binary mode
    parser.parse(f)
    ofx = parser.convert()
    print ( type(ofx) )
    stmts = ofx.statements
    print ( len(stmts), stmts )
    txs = stmts[0].banktranlist
    not_matched_txs = txs
    acct = stmts[0].bankacctfrom
    balances = stmts[0].ledgerbal
    petrol = [r'COLES EXPRESS']
    groceries = [r'BAKERS DELIGHT', r'WOOLWORTHS', ]
    bakery = [r'Mrs Jones The Baker', ]
    # Make a regex that matches if any of our regexes match.
    combined = "(" + ")|(".join(groceries) + ")"
    prog = re.compile(combined)
    categories = {}
    for trnx in txs:
        print ( trnx )
        print ( trnx.trntype, trnx.trnamt, trnx.memo )
        match = prog.search(trnx.memo)
        if match:
            print("Adding groceries:", trnx.memo, trnx.trnamt)
            if "groceries" not in categories:
                categories["groceries"] = trnx.trnamt
            else:
                categories["groceries"] += trnx.trnamt
            not_matched_txs[:] = [x for x in txs if x.fitid != trnx.fitid]
    print (categories)
    print (len(txs), len(not_matched_txs))
