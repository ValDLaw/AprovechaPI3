import datetime

import flask
import sqlalchemy
import flask_sqlalchemy
import hashlib
import uuid

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/aprovecha'
db = flask_sqlalchemy.SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(8), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(64))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(9))
    sex = db.Column(db.String(1))
    address = db.Column(db.String(100))
    educational_institution = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % self.id

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Voucher(db.Model):
    __tablename__ = 'voucher'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='vouchers')

    def __repr__(self):
        return '<Voucher %r>' % self.id

    def to_dict(self):
        return {c.name: getattr(self, c.name).strftime('%H:%M:%S %d-%m-%Y') if isinstance(
            getattr(self, c.name), datetime.datetime
        ) else getattr(self, c.name) for c in self.__table__.columns}


class Purchase(db.Model):
    __tablename__ = 'purchase'

    id = db.Column(db.Integer, primary_key=True)
    voucher_id = db.Column(db.Integer, db.ForeignKey('voucher.id'))
    voucher = db.relationship('Voucher', backref='purchases')
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', backref='purchases')
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return '<Purchase %r>' % self.id

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    published_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean)

    def __repr__(self):
        return '<Product %r>' % self.id

    def to_dict(self):
        return {c.name: getattr(self, c.name).strftime('%H:%M:%S %d-%m-%Y') if isinstance(
            getattr(self, c.name), datetime.datetime
        ) else getattr(self, c.name) for c in self.__table__.columns}


@app.route('/')
def index():
    return 'Hello world!'


@app.route('/users/register', methods=['POST'])
def register_user():
    try:
        data = flask.request.json
        hashed_password = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()
        user = User(
            dni=data['dni'],
            email=data['email'],
            password=hashed_password,
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            sex=data['sex'],
            address=data['address'],
            educational_institution=data['educational_institution']
        )
        db.session.add(user)
        db.session.commit()
        return flask.jsonify({'id': user.id}), 201
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return flask.jsonify({'error': 'El DNI o correo ya se encuentra registrado'}), 400
    except KeyError:
        db.session.rollback()
        return flask.jsonify({'error': 'Campos incompletos'}), 400
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = db.session.get(User, user_id)
        return flask.jsonify(user.to_dict()), 200
    except AttributeError:
        return flask.jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500


@app.route('/users/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = flask.request.json
        user = db.session.get(User, user_id)

        user.dni = data['dni']
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.phone = data['phone']
        user.sex = data['sex']
        user.address = data['address']
        user.educational_institution = data['educational_institution']

        db.session.commit()
        return flask.jsonify({'id': user.id}), 200
    except AttributeError:
        db.session.rollback()
        return flask.jsonify({'error': 'Usuario no encontrado'}), 404
    except KeyError:
        db.session.rollback()
        return flask.jsonify({'error': 'Campos incompletos'}), 400
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = db.session.get(User, user_id)
        db.session.delete(user)
        db.session.commit()
        return flask.jsonify({'id': user.id}), 200
    except AttributeError:
        db.session.rollback()
        return flask.jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/users/all', methods=['GET'])
def get_all_users():
    try:
        users = db.session.query(User).all()
        return flask.jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500


@app.route('/vouchers/create', methods=['POST'])
def create_voucher():
    try:
        data = flask.request.json
        voucher = Voucher(
            code=uuid.uuid1().hex,
            amount=data['amount'],
            date=datetime.datetime.now(),
            user_id=data['user_id']
        )
        db.session.add(voucher)
        db.session.commit()
        return flask.jsonify({'id': voucher.id}), 201
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return flask.jsonify({'error': 'El usuario no existe'}), 400
    except KeyError:
        db.session.rollback()
        return flask.jsonify({'error': 'Campos incompletos'}), 400
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/vouchers/<int:voucher_id>', methods=['GET'])
def get_voucher(voucher_id):
    try:
        voucher = db.session.get(Voucher, voucher_id)
        return flask.jsonify(voucher.to_dict()), 200
    except AttributeError:
        return flask.jsonify({'error': 'Voucher no encontrado'}), 404
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500


@app.route('/vouchers/update/<int:voucher_id>', methods=['PUT'])
def update_voucher(voucher_id):
    try:
        data = flask.request.json
        voucher = db.session.get(Voucher, voucher_id)

        voucher.amount = data['amount']
        voucher.date = datetime.datetime.strptime(data['date'], '%H:%M:%S %d-%m-%Y')
        voucher.user_id = data['user_id']

        db.session.commit()
        return flask.jsonify({'id': voucher.id}), 200
    except AttributeError:
        db.session.rollback()
        return flask.jsonify({'error': 'Voucher no encontrado'}), 404
    except KeyError:
        db.session.rollback()
        return flask.jsonify({'error': 'Campos incompletos'}), 400
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/vouchers/delete/<int:voucher_id>', methods=['DELETE'])
def delete_voucher(voucher_id):
    try:
        voucher = db.session.get(Voucher, voucher_id)
        db.session.delete(voucher)
        db.session.commit()
        return flask.jsonify({'id': voucher.id}), 200
    except AttributeError:
        db.session.rollback()
        return flask.jsonify({'error': 'Voucher no encontrado'}), 404
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/vouchers/all', methods=['GET'])
def get_all_vouchers():
    try:
        vouchers = db.session.query(Voucher).all()
        return flask.jsonify([voucher.to_dict() for voucher in vouchers]), 200
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500


@app.route('/products/create', methods=['POST'])
def create_product():
    try:
        data = flask.request.json
        product = Product(
            name=data['name'],
            price=data['price'],
            published_date=datetime.datetime.strptime(data['published_date'], '%H:%M:%S %d-%m-%Y'),
            due_date=datetime.datetime.strptime(data['due_date'], '%H:%M:%S %d-%m-%Y'),
            is_active=data['is_active'],
        )
        db.session.add(product)
        db.session.commit()
        return flask.jsonify({'id': product.id}), 201
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return flask.jsonify({'error': 'El producto ya existe'}), 400
    except KeyError:
        db.session.rollback()
        return flask.jsonify({'error': 'Campos incompletos'}), 400
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = db.session.get(Product, product_id)
        return flask.jsonify(product.to_dict()), 200
    except AttributeError:
        return flask.jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500


@app.route('/products/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = flask.request.json
        product = db.session.get(Product, product_id)

        product.name = data['name']
        product.price = data['price']
        product.published_date = datetime.datetime.strptime(data['published_date'], '%H:%M:%S %d-%m-%Y')
        product.due_date = datetime.datetime.strptime(data['due_date'], '%H:%M:%S %d-%m-%Y')
        product.is_active = data['is_active']

        db.session.commit()
        return flask.jsonify({'id': product.id}), 200
    except AttributeError:
        db.session.rollback()
        return flask.jsonify({'error': 'Producto no encontrado'}), 404
    except KeyError:
        db.session.rollback()
        return flask.jsonify({'error': 'Campos incompletos'}), 400
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = db.session.get(Product, product_id)
        db.session.delete(product)
        db.session.commit()
        return flask.jsonify({'id': product.id}), 200
    except AttributeError:
        db.session.rollback()
        return flask.jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/products/all', methods=['GET'])
def get_all_products():
    try:
        products = db.session.query(Product).all()
        return flask.jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500


@app.route('/purchase/create', methods=['POST'])
def create_purchase():
    try:
        data = flask.request.json
        purchase = Purchase(
            product_id=data['product_id'],
            voucher_id=data['voucher_id'],
            quantity=data['quantity'],
        )
        db.session.add(purchase)
        db.session.commit()
        return flask.jsonify({'id': purchase.id}), 201
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return flask.jsonify({'error': 'La compra ya existe'}), 400
    except KeyError:
        db.session.rollback()
        return flask.jsonify({'error': 'Campos incompletos'}), 400
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/purchase/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    try:
        purchase = db.session.get(Purchase, purchase_id)
        return flask.jsonify(purchase.to_dict()), 200
    except AttributeError:
        return flask.jsonify({'error': 'Compra no encontrada'}), 404
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500


@app.route('/purchase/update/<int:purchase_id>', methods=['PUT'])
def update_purchase(purchase_id):
    try:
        data = flask.request.json
        purchase = db.session.get(Purchase, purchase_id)

        purchase.product_id = data['product_id']
        purchase.voucher_id = data['voucher_id']
        purchase.quantity = data['quantity']

        db.session.commit()
        return flask.jsonify({'id': purchase.id}), 200
    except AttributeError:
        db.session.rollback()
        return flask.jsonify({'error': 'Compra no encontrada'}), 404
    except KeyError:
        db.session.rollback()
        return flask.jsonify({'error': 'Campos incompletos'}), 400
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/purchase/delete/<int:purchase_id>', methods=['DELETE'])
def delete_purchase(purchase_id):
    try:
        purchase = db.session.get(Purchase, purchase_id)
        db.session.delete(purchase)
        db.session.commit()
        return flask.jsonify({'id': purchase.id}), 200
    except AttributeError:
        db.session.rollback()
        return flask.jsonify({'error': 'Compra no encontrada'}), 404
    except Exception as e:
        db.session.rollback()
        return flask.jsonify({'error': str(e)}), 500


@app.route('/purchase/all', methods=['GET'])
def get_all_purchases():
    try:
        purchases = db.session.query(Purchase).all()
        return flask.jsonify([purchase.to_dict() for purchase in purchases]), 200
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=False)
