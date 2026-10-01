"""RFM customer segmentation — reusable core."""
import pandas as pd

COLUMNS = ['customer_id', 'purchase_date', 'transaction_amount',
           'product', 'order_id', 'city']


def load(path):
    """Read the CSV and force dates into a real datetime type."""
    df = pd.read_csv(path)
    df.columns = COLUMNS
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    return df


def build_rfm(df):
    """Collapse receipts into one row per customer."""
    snapshot = df['purchase_date'].max() + pd.Timedelta(days=1)
    return df.groupby('customer_id').agg(
        recency   = ('purchase_date',      lambda s: (snapshot - s.max()).days),
        frequency = ('order_id',           'nunique'),
        monetary  = ('transaction_amount', 'sum'),
    )


def add_scores(r):
    """Score each metric 1-5 by equal-sized group."""
    r = r.copy()
    # rank() first: qcut refuses duplicate values
    # (946 customers share frequency = 1)
    r['R'] = pd.qcut(r['recency'].rank(method='first'),
                     5, labels=[5, 4, 3, 2, 1]).astype(int)   # inverted: low recency = good
    r['M'] = pd.qcut(r['monetary'].rank(method='first'),
                     5, labels=[1, 2, 3, 4, 5]).astype(int)
    # F deliberately excluded — see README "Limitations"
    r['score'] = r['R'] + r['M']
    return r


def add_segments(r):
    """Turn scores into named groups."""
    r = r.copy()

    def label(row):
        if row['score'] >= 8:                          return 'Champion'
        if row['R'] <= 2 and row['M'] >= 4:            return 'Lapsed high-value'
        if row['R'] >= 4 and row['frequency'] == 1:    return 'One-time visitor'
        return 'Average'

    r['segment'] = r.apply(label, axis=1)
    return r
