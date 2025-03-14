# Till database handling routines

# Various parts of the UI call on these routines to work out what the
# hell is going on.  We try to ensure the database constraints are
# never broken here, but that's not really a substitute for
# implementing them in the database itself.

import time
#from . import stock
import psycopg2 as db
import psycopg2.extensions
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import subqueryload_all,joinedload,subqueryload
from sqlalchemy.orm import undefer
from sqlalchemy.sql.expression import tuple_,func,null
from sqlalchemy.sql import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import distinct
from models import *


# psycopg converted database numeric() types into float() types.

# By default, psycopg2 converts them into decimal.Decimal() types -
# arguably more correct, but not what the rest of this package is
# expecting.

# Until the rest of the package is updated to expect Decimal()s,
# convert to float()s instead:
#DEC2FLOAT = psycopg2.extensions.new_type(
#    db._psycopg.DECIMAL.values,
#    'DEC2FLOAT',
#    lambda value, curs: float(value) if value is not None else None)
#psycopg2.extensions.register_type(DEC2FLOAT)
# If psycopg2._psycopg.DECIMAL stops working, use
# psycopg2.extensions.DECIMAL instead.

database=None

con=None
def cursor():
    con.commit()
    return con.cursor()
def commit():
    con.commit()

### Convenience functions

def execone(cur,c,*args):
    "Execute c and return the single result. Does not commit."
    cur.execute(c,*args)
    r=cur.fetchone()
    if not r: return None
    return r[0]

def ticket(cur,seq):
    "Fetch a new serial number from the named sequence"
    return execone(cur,"SELECT nextval(%s)",(seq,))

### Functions relating to the transactions,lines,payments tables

def trans_new(note=None):
    "Create a new transaction and return its number"
    # Check that there's a current session
    s=session_current()
    if not s: return None
    cur=cursor()
    t=ticket(cur,"transactions_seq")
    cur.execute("INSERT INTO transactions (transid,sessionid,notes) "
                "VALUES (%s,%s,%s)",(t,s[0],note))
    commit()
    return t

def trans_closed(trans):
    cur=cursor()
    return execone(
        cur,"SELECT closed FROM transactions WHERE transid=%s",(trans,))

def trans_getnotes(trans):
    cur=cursor()
    return execone(
        cur,"SELECT notes FROM transactions WHERE transid=%s",(trans,))

def trans_setnotes(trans,notes):
    cur=cursor()
    cur.execute("UPDATE transactions SET notes=%s WHERE transid=%s",
                (notes,trans))
    commit()

# See also stock_sell()

def trans_addline(trans,dept,items,amountper,source,transcode,text=None):
    "Insert a line into a transaction that has no associated stock record"
    cur=cursor()
    lid=ticket(cur,"translines_seq")
    cur.execute("INSERT INTO translines (translineid,transid,items,amount,"
                "dept,source,transcode,text) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (lid,trans,items,amountper,dept,source,transcode,text))
    commit()
    return lid

def trans_additems(lid,items):
    "Update an existing line with additional items"
    cur=cursor()
    # XXX check the transaction is not closed
    cur.execute("UPDATE translines SET items=items+%s "
                "WHERE translines.translineid=%s",(items,lid))
    commit()

def trans_getline(lid):
    "Retrieve information about a transaction line"
    cur=cursor()
    cur.execute("SELECT tl.transid,tl.items,"
                "tl.amount,tl.dept,d.description,"
                "tl.stockref,tl.transcode,tl.time,tl.text,d.vatband "
                "FROM translines tl "
                "INNER JOIN departments d ON tl.dept=d.dept "
                "WHERE tl.translineid=%s",(lid,))
    return cur.fetchone()

def trans_getlines(trans):
    "Retrieve lines and payments for a transaction"
    cur=cursor()
    cur.execute("SELECT translineid FROM translines WHERE transid=%s "
                "ORDER BY translineid",(trans,))
    lines=[x[0] for x in cur.fetchall()]
    cur.execute("SELECT p.amount,p.paytype,pt.description,p.ref "
                "FROM payments p "
                "LEFT JOIN paytypes pt ON p.paytype=pt.paytype "
                "WHERE transid=%s ORDER BY time ",(trans,))
    payments=cur.fetchall()
    return (lines,payments)

def trans_multiband(trans):
    "Determine whether a transaction has lines in more than one VAT band."
    cur=cursor()
    cur.execute("SELECT DISTINCT vat.band FROM translines tl "
                "LEFT JOIN departments d ON tl.dept=d.dept "
                "LEFT JOIN vat ON d.vatband=vat.band "
                "WHERE transid=%s",(trans,))
    bands=cur.fetchall()
    return len(bands)>1

def trans_age(trans):
    "Return the age of the transaction in days"
    cur=cursor()
    cur.execute("SELECT extract(days from (now()-min(time))) "
                "FROM translines WHERE transid=%s",(trans,))
    return cur.fetchone()[0]

def trans_balance(trans):
    "Return (linestotal,paymentstotal) on a transaction"
    cur=cursor()
    cur.execute("SELECT (SELECT sum(amount*items) FROM translines "
                "WHERE translines.transid=%s),(SELECT sum(amount) "
                "FROM payments WHERE payments.transid=%s)",(trans,trans));
    r=cur.fetchone()
    if not r[0]: linestotal=Decimal("0.00")
    else: linestotal=r[0]
    if not r[1]: paymentstotal=Decimal("0.00")
    else: paymentstotal=r[1]
    return (linestotal,paymentstotal)

def trans_date(trans):
    "Return the accounting date of the transaction"
    cur=cursor()
    d=execone(cur,"SELECT s.sessiondate FROM transactions t "
              "LEFT JOIN sessions s ON t.sessionid=s.sessionid "
              "WHERE t.transid=%s",(trans,))
    return d

def trans_addpayment(trans,ptype,amount,ref):
    """Add a payment to a transaction, and return the remaining balance.
    If the remaining balance is zero, mark the transaction closed."""
    cur=cursor()
    cur.execute("INSERT INTO payments (transid,amount,paytype,ref) VALUES "
                "(%s,%s,%s,%s)",(trans,amount,ptype,ref))
    (lines,payments)=trans_balance(trans)
    remain=lines-payments
    if remain==Decimal("0.00"):
        cur.execute("UPDATE transactions SET closed=true WHERE transid=%s",
                    (trans,))
    commit()
    return remain

def trans_pingapint(trans,amount,code,vid,blob):
    """Add a PingaPint voucher redemption to a transaction and return
    the remaining balance.  If the remaining balance is zero, mark the
    transaction closed.

    This is similar to trans_addpayment but it's important that it all
    execute in one database transaction."""
    cur=cursor()
    pid=ticket(cur,"payments_seq")
    cur.execute("INSERT INTO payments (paymentid,transid,amount,paytype,ref) "
                "VALUES (%s,%s,%s,'PPINT',%s)",(pid,trans,amount,code))
    cur.execute("INSERT INTO pingapint (paymentid,amount,vid,json_data) VALUES "
                "(%s,%s,%s,%s)",(pid,amount,vid,blob))
    (lines,payments)=trans_balance(trans)
    remain=lines-payments
    if remain==Decimal("0.00"):
        cur.execute("UPDATE transactions SET closed=true WHERE transid=%s",
                    (trans,))
    commit()
    return remain

def trans_cancel(trans):
    """Delete a transaction and everything that depends on it."""
    cur=cursor()
    closed=execone(cur,"SELECT closed FROM transactions WHERE transid=%s",
                   (trans,))
    if closed: return "Transaction closed"
    cur.execute("DELETE FROM stockout WHERE stockout.translineid IN "
                "(SELECT translineid FROM translines WHERE transid=%s)",(trans,))
    cur.execute("DELETE FROM payments WHERE transid=%s",(trans,))
    cur.execute("DELETE FROM translines WHERE transid=%s",(trans,))
    cur.execute("DELETE FROM transactions WHERE transid=%s",(trans,))
    commit()

def trans_deleteline(transline):
    cur=cursor()
    cur.execute("DELETE FROM stockout WHERE translineid=%s",(transline,))
    cur.execute("DELETE FROM translines WHERE translineid=%s",(transline,))
    commit()

def trans_defer(trans):
    """Defers a transaction to a later session, by setting its sessionid to
    null.

    """
    cur=cursor()
    cur.execute("UPDATE transactions SET sessionid=null WHERE transid=%s",
                (trans,))
    commit()

def trans_merge(t1,t2):
    """Merge t1 into t2, and delete t1.

    """
    cur=cursor()
    cur.execute("UPDATE translines SET transid=%s WHERE transid=%s",
                (t2,t1))
    cur.execute("DELETE FROM transactions WHERE transid=%s",(t1,))
    commit()

def trans_restore():
    """Restores all deferred transactions.

    """
    s=session_current()
    if s is None: return 0
    sessionid=s[0]
    cur=cursor()
    cur.execute("UPDATE transactions SET sessionid=%s WHERE sessionid IS NULL",
                (sessionid,))
    commit()

def trans_makefree(transid,removecode):
    """Converts all stock sold in this transaction to 'removecode', and
    deletes the transaction.  Usually used when converting an open transaction
    to 'free drinks'.

    """
    cur=cursor()
    cur.execute("UPDATE stockout SET removecode=%s,translineid=NULL "
                "WHERE translineid IN (SELECT translineid FROM translines "
                "WHERE transid=%s)",(removecode,transid))
    cur.execute("DELETE FROM translines WHERE transid=%s",(transid,))
    cur.execute("DELETE FROM transactions WHERE transid=%s",(transid,))
    commit()

def vat_info(band,date):
    cur=cursor()
    cur.execute("SELECT vatrate(%s,%s),business(%s,%s)",(band,date,band,date))
    return cur.fetchone()

def business_info(business):
    cur=cursor()
    cur.execute("SELECT name,abbrev,address,vatno FROM businesses "
                "WHERE business=%s",(business,))
    return cur.fetchone()

### Functions related to the stocktypes table

def stocktype_info(stn):
    cur=cursor()
    cur.execute("SELECT dept,manufacturer,name,shortname,abv,unit "
                "FROM stocktypes WHERE stocktype=%s",(stn,))
    return cur.fetchone()

def stocktype_completemanufacturer(m):
    session=sm()
    result=session.execute(
        select([StockType.manufacturer]).\
            where(StockType.manufacturer.ilike(m+'%'))
        )
    session.close()
    return [x[0] for x in result]

def stocktype_completename(m,n):
    session=sm()
    result=session.execute(
        select([distinct(StockType.name)]).\
            where(StockType.manufacturer==m).\
            where(StockType.name.ilike(n+'%'))
        )
    session.close()
    return [x[0] for x in result]

def stocktype_search_inconsistent_prices():
    cur=cursor()
    cur.execute("SELECT st.stocktype FROM stocktypes st "
                "INNER JOIN stock s ON s.stocktype=st.stocktype "
                "WHERE s.finished IS NULL "
                "GROUP BY st.stocktype "
                "HAVING COUNT(DISTINCT s.saleprice)>1")
    return [x[0] for x in cur.fetchall()]

### Functions related to the department table

def department_list():
    cur=cursor()
    cur.execute("SELECT dept,description FROM departments ORDER BY dept")
    return cur.fetchall()

### Functions related to finishing stock

def stockfinish_list():
    cur=cursor()
    cur.execute("SELECT finishcode,description FROM stockfinish")
    return cur.fetchall()

### Functions related to the stock,stockout,stockonsale tables

def stock_info(stockid_list):
    """Return lots of information on stock items in the list."""
    if len(stockid_list)==0: return []
    cur=cursor()
    # Q: Does psycopg2 deal with lists?
    # A: lists are turned into ARRAY types.  Tuples are turned into
    # something suitable for the IN operator.  The documentation says
    # that empty tuples are not supported so must be guarded against
    # (already done, above).  The psycopg2.extensions module MUST be
    # imported to register support for this.
    cur.execute("SELECT * FROM stockinfo WHERE stockid IN %s",
                (tuple(stockid_list),))
    r=cur.fetchall()
    # Q: This is a real candidate for returning a dict! Does pgdb support it?
    # A: not explicitly, but we can do something like:
    cn=[x[0] for x in cur.description]
    from . import stock
    def mkdict(r):
        d={}
        for i in cn:
            d[i]=r[0]
            r=r[1:]
        d['abvstr']=stock.abvstr(d['abv'])
        if d['used'] is None: d['used']=Decimal("0.0")
        d['remaining']=d['size']-d['used']
        return d
    # At this point we have a list of results, but that list is not
    # necessarily in the order of the input list.  We must sort it
    # into the appropriate order.  Note that we may have been passed
    # stockids that do not exist!
    sid={}
    for i in r:
        sid[i[0]]=mkdict(i)
    return [sid[x] for x in stockid_list if x in sid]

def stock_checkpullthru(stockid,maxtime):
    """Did this stock item require pulling through?"""
    cur=cursor()
    r=execone(cur,"SELECT now()-max(stockout.time)>%s FROM stockout "
              "WHERE stockid=%s AND removecode IN ('sold','pullthru')",
              (maxtime,stockid))
    if r is None: r=False
    return r

def stock_reprice(sn,saleprice):
    cur=cursor()
    cur.execute("UPDATE stock SET saleprice=%s WHERE stockid=%s",(saleprice,sn))
    commit()

def stock_sell(trans,dept,stockitem,items,qty,price,source,transcode):
    """Sell some stock.  Inserts a line into a transaction, and creates
    an associated stock record.

    'dept' is the department the sale will be recorded in.

    'qty' is the amount being sold as a unit, eg. 0.5 for a half pint,
    2.0 for a double, 4.0 for a 4-pint jug.

    'items' is the number of things of size 'qty' that are being sold.
    It will be negative for void transactions.

    'price' is the price of 'qty' of the stock, with discounts, etc. taken
    into account.

    'source' is a string identifying where the transaction is taking place.

    'transcode' is a letter identifying the type of transaction;
    currently 'S' for a sale, or 'V' for a void.

    """
    cur=cursor()
    # Write out a stockout line
    son=ticket(cur,"stockout_seq")
    lid=ticket(cur,"translines_seq")
    cur.execute("INSERT INTO stockout (stockoutid,stockid,qty,removecode,"
                "translineid) VALUES (%s,%s,%s,'sold',%s)",
                (son,stockitem,qty*items,lid))
    # Write out a transaction line
    cur.execute("INSERT INTO translines (translineid,transid,items,amount,"
                "dept,source,stockref,transcode) VALUES "
                "(%s,%s,%s,%s,%s,%s,%s,%s)",
                (lid,trans,items,price,dept,source,son,transcode))
    commit()
    return lid

def stock_sellmore(lid,items):
    "Update a transaction line and stock record with extra items"
    cur=cursor()
    # Fetch old number of items
    oi=execone(cur,"SELECT items FROM translines WHERE translineid=%s",(lid,))
    ni=oi+items
    # Update stockout line
    cur.execute("UPDATE stockout SET qty=(qty/%s)*%s WHERE translineid=%s",
                (oi,ni,lid))
    # Update transaction line
    cur.execute("UPDATE translines SET items=%s WHERE translineid=%s",(ni,lid))
    commit()
    return ni

def stock_fetchline(stocklineref):
    "Fetch stockout details given a line reference"
    cur=cursor()
    cur.execute("SELECT so.qty,so.removecode,"
                "so.stockid,st.manufacturer,st.name,st.shortname,"
                "st.abv,ut.name FROM stockout so "
                "INNER JOIN stock ON so.stockid=stock.stockid "
                "INNER JOIN stocktypes st ON st.stocktype=stock.stocktype "
                "INNER JOIN unittypes ut ON ut.unit=st.unit "
                "WHERE so.stockoutid=%s",(stocklineref,))
    return cur.fetchone()

def stock_search(dept=None,exclude_stock_on_sale=True,
                 finished_stock_only=False,stockline=None,stocktype=None):
    """Return a list of stock numbers that fit the criteria."""
    cur=cursor()
    if stockline is None:
        order="s.stockid"
    else:
        order="(s.stocktype IN (SELECT stocktype FROM stockline_stocktype_log stl WHERE stl.stocklineid=%d)) DESC,s.stockid"%stockline
    if dept is None:
        deptq=""
    else:
        deptq="AND st.dept=%d"%dept
    if exclude_stock_on_sale:
        sosq="AND s.stockid NOT IN (SELECT stockid FROM stockonsale)"
    else:
        sosq=""
    if finished_stock_only:
        finq="not null"
    else:
        finq="null"
    if stocktype:
        stq="AND s.stocktype=%d"%stocktype
    else:
        stq=""
    cur.execute("SELECT s.stockid FROM stock s INNER JOIN deliveries d ON "
                "s.deliveryid=d.deliveryid INNER JOIN stocktypes st ON "
                "st.stocktype=s.stocktype "
                "WHERE finishcode is %s AND "
                "d.checked=true %s %s %s ORDER BY %s"%(
            finq,sosq,deptq,stq,order))
    return [x[0] for x in cur.fetchall()]

def stock_putonsale(stockid,stocklineid):
    """Connect a stock item to a particular line.  Additionally, create
    an annotation that records the line name.

    """
    cur=cursor()
    cur.execute("UPDATE stock SET onsale=now() WHERE stockid=%s",(stockid,))
    cur.execute("INSERT INTO stockonsale (stocklineid,stockid) VALUES "
                "(%s,%s)",(stocklineid,stockid))
    cur.execute("INSERT INTO stock_annotations (stockid,atype,text) "
                "SELECT %s,'start',(SELECT name FROM stocklines "
                "WHERE stocklineid=%s)",(stockid,stocklineid))
    commit()
    return True

def stock_autoallocate_candidates(deliveryid=None):
    """
    Return a list of (stockline,stockid,displayqty) tuples, ordered
    by stockid.  List is suitable for passing to stock_allocate() once
    duplicate stockids have been resolved.

    """
    cur=cursor()
    ds="AND deliveryid=%s"%deliveryid if deliveryid is not None else ""
    cur.execute(
        "SELECT sl.stocklineid,si.stockid,si.used AS displayqty "
        "FROM (SELECT * FROM stocklines WHERE capacity IS NOT NULL) AS sl "
        "CROSS JOIN (SELECT * FROM stockinfo WHERE deliverychecked "
        "AND finished IS NULL %s AND stockid NOT IN ( "
        "SELECT stockid FROM stockonsale)) AS si "
        "WHERE si.stocktype IN "
        "(SELECT stocktype FROM stockline_stocktype_log ssl "
        "WHERE ssl.stocklineid=sl.stocklineid) "
        "ORDER BY si.stockid"%ds)
    return cur.fetchall()

def stock_allocate(aal):
    """
    Allocate stock to stocklines; expects a list of
    (stockline,stockid,displayqty) tuples, as produced by
    stock_autoallocate_candidates() and then filtered for duplicate
    stockids.

    """
    cur=cursor()
    for i in aal:
        cur.execute("INSERT INTO stockonsale VALUES (%s,%s,%s)",i)
    commit()

def stock_purge():
    cur=cursor()
    cur.execute(
        "SELECT sos.stockid INTO TEMPORARY TABLE t_stockpurge "
        "FROM stocklines sl "
        "LEFT JOIN stockonsale sos ON sos.stocklineid=sl.stocklineid "
        "LEFT JOIN stockinfo si ON si.stockid=sos.stockid "
        "WHERE sl.capacity IS NOT NULL "
        "AND si.used=si.size")
    cur.execute(
        "UPDATE stock SET finished=now(),finishcode='empty' "
        "WHERE stockid IN (SELECT stockid FROM t_stockpurge)")
    cur.execute(
        "DELETE FROM stockonsale WHERE stockid IN "
        "(SELECT stockid FROM t_stockpurge)")
    cur.execute("DROP TABLE t_stockpurge")
    commit()

def stock_recordwaste(stock,reason,amount,update_displayqty):
    """Record wastage of a stock item.  If update_displayqty is set then
    the displayqty field in the stockonsale table will be increased by the
    same amount, so that the quantity on display remains unchanged.  (If
    there is no entry for the stockid in stockonsale then nothing happens.)

    """
    cur=cursor()
    t=ticket(cur,'stockout_seq')
    cur.execute("INSERT INTO stockout (stockoutid,stockid,qty,removecode) "
                "VALUES (%s,%s,%s,%s)",(t,stock,amount,reason))
    if update_displayqty:
        cur.execute("UPDATE stockonsale SET displayqty=displayqty+%s "
                    "WHERE stockid=%s",(int(amount),stock))
    commit()
    return t

def stock_finish(stock,reason):
    "Finish with a stock item; anything left is unaccounted waste"
    cur=cursor()
    # Disconnect it from its line, if it has one
    cur.execute("DELETE FROM stockonsale WHERE stockid=%s",(stock,))
    # Record the finish time and reason
    cur.execute("UPDATE stock SET finished=now(),finishcode=%s "
                "WHERE stockid=%s",(reason,stock))
    commit()

def stock_disconnect(stock):
    "Temporarily disconnect a stock item."
    cur=cursor()
    cur.execute("DELETE FROM stockonsale WHERE stockid=%s",(stock,))
    commit()

def stock_onsale(line):
    """Find out what's on sale on a particular [beer] line.  This function
    returns a list of all the stock items allocated to the line, in order
    of best before date and then stock number, earliest dates/lowest numbers
    first.

    """
    cur=cursor()
    cur.execute(
        "SELECT sos.stockid,sos.displayqty "
        "FROM stockonsale sos "
        "LEFT JOIN stock s ON s.stockid=sos.stockid "
        "WHERE sos.stocklineid=%s "
        "ORDER BY coalesce(sos.displayqty,0) DESC,"
        "s.bestbefore,sos.stockid",(line,))
    return cur.fetchall()

def stock_annotate(stock,atype,text):
    """Create an annotation for a stock item.  This routine performs
    no checks; it is assumed the caller has already ensured the
    annotation is sensible.

    """
    cur=cursor()
    cur.execute("INSERT INTO stock_annotations (stockid,atype,text) "
                "VALUES (%s,%s,%s)",(stock,atype,text))
    commit()

def stock_annotations(stock,atype=None):
    """Return annotations for a stock item, restricted to atype if
    specified.

    """
    if atype is not None: ac=" AND sa.atype='%s'"%atype
    else: ac=""
    cur=cursor()
    cur.execute("SELECT at.description,sa.time,sa.text "
                "FROM stock_annotations sa "
                "LEFT JOIN annotation_types at ON at.atype=sa.atype "
                "WHERE sa.stockid=%%s%s ORDER BY sa.time"%ac,(stock,))
    return cur.fetchall()

def stocktake(dept=None):
    cur=cursor()
    if dept is None: deptclause=""
    else: deptclause="and st.dept=%d "%dept
    # We return:
    # Department number
    # Department name
    # Stock type name
    # Stock ID
    # Stock line (may be null)
    # Stock line display capacity (may be null)
    # displayqty (may be null)
    # used
    # size
    # unit
    
    cur.execute(
        "select st.dept,d.description,st.shortname,s.stockid,"
        "sl.name,sl.capacity,sos.displayqty,"
        "(select sum(so.qty) as sum from stockout so "
        "where so.stockid=s.stockid) as used,"
        "su.size,su.unit "
        "from stocktypes st "
        "inner join stock s on s.stocktype=st.stocktype "
        "left join stockonsale sos on s.stockid=sos.stockid "
        "left join stocklines sl on sos.stocklineid=sl.stocklineid "
        "left join stockunits su on s.stockunit=su.stockunit "
        "left join departments d on st.dept=d.dept "
        "where s.finished is null %s"
        "order by st.dept,st.manufacturer,st.shortname,s.stockid"%deptclause)
    return cur.fetchall()

### Find out what's on the stillage by checking annotations

def stillage_summary(session):
    stillage=session.query(StockAnnotation).\
        join(StockItem).\
        outerjoin(StockOnSale).\
        outerjoin(StockLine).\
        filter(tuple_(StockAnnotation.text,StockAnnotation.time).in_(
            select([StockAnnotation.text,func.max(StockAnnotation.time)],
                   StockAnnotation.atype=='location').\
                group_by(StockAnnotation.text))).\
        filter(StockItem.finished==None).\
        order_by(StockLine.name!=null(),StockAnnotation.time).\
        options(joinedload('stockitem')).\
        options(joinedload('stockitem.stocktype')).\
        options(joinedload('stockitem.stockonsale')).\
        options(joinedload('stockitem.stockonsale.stockline')).\
        all()
    return stillage

### Check stock levels

def stocklevel_check(dept=None,period='3 weeks'):
    cur=cursor()
    deptstr="" if dept==None else "AND dept=%d"%dept
    cur.execute(
        "SELECT st.stocktype,st.shortname,sum(qty) as sold,"
        "sum(qty)-coalesce((select sum(size-coalesce(used,0)) "
        "FROM stockinfo WHERE stocktype=st.stocktype "
        "AND finished is null),0) as understock "
        "FROM stocktypes st "
        "LEFT JOIN stock s ON st.stocktype=s.stocktype "
        "LEFT JOIN stockout so ON so.stockid=s.stockid "
        "WHERE (removecode='sold' or removecode is null) "
        "%s "
        "AND now()-so.time<'%s' "
        "GROUP BY st.stocktype,st.shortname "
        "ORDER BY understock DESC"%(deptstr,period))
    return cur.fetchall()

### Functions related to the stocktype/stockline log table

def stockline_stocktype_log(stocklines=None):
    cur=cursor()
    if stocklines is None:
        slt=""
    else:
        slt="WHERE ssl.stocklineid IN (%s) "%(
            ",".join(["%d"%x for x in stocklines]))
    cur.execute(
        "SELECT ssl.stocklineid,ssl.stocktype,sl.name,st.shortname "
        "FROM stockline_stocktype_log ssl "
        "LEFT JOIN stocklines sl ON ssl.stocklineid=sl.stocklineid "
        "LEFT JOIN stocktypes st ON ssl.stocktype=st.stocktype "
        "%s"
        "ORDER BY sl.dept,sl.name,st.shortname"%slt)
    return cur.fetchall()

def stockline_stocktype_log_del(stockline,stocktype):
    cur=cursor()
    cur.execute(
        "DELETE FROM stockline_stocktype_log "
        "WHERE stocklineid=%s AND stocktype=%s",(stockline,stocktype))
    commit()
    return

### Functions related to food order numbers

def foodorder_reset():
    cur=cursor()
    cur.execute("DROP SEQUENCE foodorder_seq")
    cur.execute("CREATE SEQUENCE foodorder_seq")
    commit()

def foodorder_ticket():
    cur=cursor()
    n=ticket(cur,"foodorder_seq")
    commit()
    return n

### Functions related to stock lines

def stockline_restock(stocklineid,changes):
    cur=cursor()
    for sd,move,newdisplayqty,stockqty_after_move in changes:
        cur.execute("UPDATE stockonsale SET displayqty=%s WHERE "
                    "stocklineid=%s AND stockid=%s",(
            newdisplayqty,stocklineid,sd['stockid']))
    commit()

def stockline_summary(session,locations):
    s=session.query(StockLine).\
        filter(StockLine.location.in_(locations)).\
        filter(StockLine.capacity==None).\
        order_by(StockLine.name).\
        options(joinedload('stockonsale')).\
        options(joinedload('stockonsale.stockitem')).\
        options(joinedload('stockonsale.stockitem.stocktype')).\
        all()
    return s

### Functions relating to till keyboards

def keyboard_checklines(layout,keycode):
    """keycode is a string.  Returns a list of (linename,qty,dept,
    pullthru,menukey,stocklineid,location,capacity) tuples (possibly
    empty).  The list may be in any order; it's up to the caller to
    sort it (eg. by menukey numeric keycode).

    """
    cur=cursor()
    cur.execute("SELECT sl.name,k.qty,sl.dept,sl.pullthru,"
                "k.menukey,k.stocklineid,sl.location,sl.capacity "
                "FROM keyboard k "
                "LEFT JOIN stocklines sl ON sl.stocklineid=k.stocklineid "
                "WHERE k.layout=%s AND k.keycode=%s",(layout,keycode))
    return cur.fetchall()

def keyboard_checkstockline(layout,stocklineid):
    """Return all the key bindings in this keyboard layout for the
    specified stock line.

    """
    cur=cursor()
    cur.execute("SELECT keycode,menukey,qty FROM keyboard "
                "WHERE layout=%s AND stocklineid=%s",(layout,stocklineid))
    return cur.fetchall()

def keyboard_addbinding(layout,keycode,menukey,stocklineid,qty):
    cur=cursor()
    cur.execute("INSERT INTO keyboard (layout,keycode,menukey,stocklineid,qty) "
                "VALUES (%s,%s,%s,%s,%s)",(layout,keycode,menukey,stocklineid,qty))
    commit()

def keyboard_delbinding(layout,keycode,menukey):
    cur=cursor()
    cur.execute("DELETE FROM keyboard WHERE layout=%s AND keycode=%s AND menukey=%s",
                (layout,keycode,menukey))
    commit()

def keyboard_setcap(layout,keycode,cap):
    """keycode is a string.  Stores a new keycap for the specified keyboard layout."""
    cur=cursor()
    cur.execute("DELETE FROM keycaps WHERE layout=%s AND keycode=%s",(layout,keycode))
    cur.execute("INSERT INTO keycaps (layout,keycode,keycap) VALUES (%s,%s,%s)",
                (layout,keycode,cap))
    commit()

def keyboard_delcap(layout,keycode):
    cur=cursor()
    cur.execute("DELETE FROM keycaps WHERE layout=%s AND keycode=%s",(layout,keycode))
    commit()

def keyboard_getcaps(layout):
    """Returns all the keycaps for a particular layout."""
    cur=cursor()
    cur.execute("SELECT keycode,keycap FROM keycaps WHERE layout=%s",(layout,))
    return cur.fetchall()

### Functions relating to the sessions,sessiontotals tables

def session_current():
    "Return the current session number and the time it started."
    cur=cursor()
    cur.execute("SELECT sessionid,starttime,sessiondate FROM sessions WHERE "
                "endtime IS NULL");
    r=cur.fetchall()
    if len(r)==1:
        return r[0]
    return None

def session_list(session,unpaidonly,closedonly):
    """Return the list of sessions.  Explicitly undefers loading of
    the total column property so that we don't have to make a
    round-trip to the database for each object returned.

    """
    q=session.query(Session).\
        order_by(desc(Session.id)).\
        options(undefer('total'))
    if unpaidonly:
        q=q.filter(select([func.count(SessionTotal.sessionid)],
                          whereclause=SessionTotal.sessionid==Session.id).\
                       correlate(Session.__table__).as_scalar()==0)
    if closedonly:
        q=q.filter(Session.endtime!=None)
    return q.all()

def session_translist(session,onlyopen=False):
    """Returns the list of transactions in a session; transaction number,
    closed status, total charge.

    """
    cur=cursor()
    oos=""
    if onlyopen:
        oos="AND t.closed=FALSE "
    cur.execute("SELECT t.transid,t.notes,t.closed,sum(tl.items*tl.amount) "
                "FROM transactions t LEFT JOIN translines tl "
                "ON t.transid=tl.transid "
                "WHERE t.sessionid=%%s %s"
                "GROUP BY t.transid,t.notes,t.closed "
                "ORDER BY t.closed,t.transid DESC"%oos,(session,))
    return cur.fetchall()

def db_version():
    cur=cursor()
    return execone(cur,"SELECT version()")

def init():
    global con,database,engine,sm
    if database is None:
        raise Exception("No database defined")
    if database[0]==":":
        database="dbname=%s"%database[1:]
    # Conversion to sqlalchemy: create sqlalchemy engine URL from
    # libpq connection string
    csdict=dict([x.split('=',1) for x in database.split(' ')])
    estring="postgresql+psycopg2://"
    if 'user' in csdict:
        estring+=csdict[user]
        if 'password' in csdict:
            estring+=":%s"%(csdict['password'],)
        estring+='@'
    if 'host' in csdict:
        estring+=csdict['host']
    if 'port' in csdict:
        estring+=":%s"%(csdict['port'],)
    estring+="/%s"%(csdict['dbname'],)
    engine=create_engine(estring)
    # We might like to consider adding expire_on_commit=False to the
    # sessionmaker at some point; let's not do that for now so we can
    # spot potentially expired objects more easily while we're
    # converting the code.
    sm=sessionmaker(bind=engine)
    con=db.connect(database)
