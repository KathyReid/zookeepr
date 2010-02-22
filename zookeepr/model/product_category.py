"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from zookeepr.model.meta import Session

def setup(meta):
    meta.Session.add_all(
        [
            ProductCategory(name='Ticket', description='Please choose your registration type. See <a href="http://www.lca2010.org.nz/register/prices" target="_blank">the website</a> for a description of what is included in each ticket type.', display='radio', min_qty=1, max_qty=1, display_order=1),
            ProductCategory(name='T-Shirt', description='Please choose how many t-shirts you would like.', note='One t-shirt is free with your registration, and one t-shirt is free with every adult Partner Programme ticket purchased. Any additional t-shirts are $25.00 each. More details and measurements on t-shirt sizes can be found on the <a href="/register/shirts" target="_blank">registration information</a>.', display='qty', display_mode='shirt', min_qty=1, max_qty=100, display_order=10),
            ProductCategory(name='Penguin Dinner Ticket', description="Please indicate how many Penguin Dinner tickets you would like.", note="You should include yourself in this number, even if you register as a Professional.  An adult ticket includes an adult's meal, a child ticket includes a child's meal, and an infant ticket does not include any meal and the infant will need to sit on your knee.  If your child requires an adult meal, then please purchase an adult ticket for them.", display='qty', min_qty=0, max_qty=5, display_mode='grid', display_order=20),
            ProductCategory(name='Accommodation', description='Please consider where you are going to stay during the conference.', display='select', min_qty=0, max_qty=10, display_order=30),
            ProductCategory(name="Partners Programme", description="Please register your partner and children for the Partners Programme.", display='qty', min_qty=0, max_qty=50, display_mode='grid', display_order=40),
            ProductCategory(name="Speakers Dinner Ticket", description="Please indicate how many Speaker Dinner tickets you would like.', note='These are for you, your significant other, and your children. An adult ticket includes an adult's meal, a child ticket includes a child's meal, and an infant ticket does not include any meal and the infant will need to sit on your knee. If your child requires an adult meal, then purchase an adult ticket for them.", display='qty', min_qty=0, max_qty=200, display_mode='grid', display_order=25),
        ]
    )

class ProductCategory(Base):
    """Stores the product categories used for registration
    """
    __tablename__ = 'product_category'

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.Text, nullable=False, unique=True)
    description = sa.Column(sa.types.Text, nullable=False)
    note = sa.Column(sa.types.Text)
    display_order = sa.Column(sa.types.Integer, nullable=False)
    
    # display is used to determine the type of field to collect input with (see templates/registration/form.mako)
    # display is also used to validate the output (see controllers/registration.py)
    # available types so far: radio, select, checkbox, qty
    # The first three are self explanatory and act as the HTML counterpart
    # qty is an integer validated text box
    display = sa.Column(sa.types.Text, nullable=False) 

    # what display mode to use?
    # options: grid, shirt
    display_mode = sa.Column(sa.types.Text) 
    
    min_qty = sa.Column(sa.types.Integer, nullable=True)
    max_qty = sa.Column(sa.types.Integer, nullable=True)

    def __init__(self, **kwargs):
        super(ProductCategory, self).__init__(**kwargs)

    @classmethod
    def find_all(self):
        return Session.query(ProductCategory).order_by(ProductCategory.display_order).order_by(ProductCategory.name).all()

    @classmethod
    def find_by_id(cls, id):
        return Session.query(ProductCategory).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return Session.query(ProductCategory).filter_by(name=name).first()

    def available_products(self, person, stock=True):
        # bool stock: care about if the product is in stock (ie sold out?)
        products = []
        for product in self.products:
            if product.available(stock):
                products.append(product)
        return products

    def qty_person_sold(self, person):
        qty = 0
        for i in person.invoices:
            for ii in i.invoice_items:
                if ii.product.category == self:
                    qty += ii.qty
        return qty

    def can_i_sell(self, person, qty):
        if self.qty_person_sold(person) + qty <= self.max_qty:
            return True
        else:
            return False

    def clean_name(self):
        return self.name.replace('-','_')

    def __repr__(self):
        return '<ProductCategory id=%r name=%r description=%r note=%r display_order=%r display=%r min_qty=%r max_qty=%r>' % (self.id, self.name, self.description, self.note, self.display_order, self.display, self.min_qty, self.max_qty)
