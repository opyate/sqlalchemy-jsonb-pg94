# Requirements

[Fig](http://www.fig.sh/) and Docker.

If not, just ```python app.py``` with a PostgresQL database (you might need to modify the connection string in ```app.py```).

# Steps

Run with ```fig up``` or ```python app.py```.

Create the test instance in the database with:

    curl -XPUT http://0.0.0.0:5000/

Re-create the exact same instance with:

    curl -XPOST http://0.0.0.0:5000/ \
    -H 'Content-Type: application/json' \
    -d '{"eggs": 42, "obj": {"beans": "with brandy!", "ham": 43}, "spam": "but I prefer bacon!"}'

The POST handler should do a JSONB equality check in the ```filter_by```.
