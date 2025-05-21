# GROCS Grocery Delivery Platform

## Libraries to Install

Install required libraries using `requirements.txt`:

```bash
py -m pip install -r requirements.txt
python3 -m pip install -r requirements.txt
```

## Assessment 2 Challenge

Develop GROCS, a grocery delivery web application, using IFN582 workshop techniques. Features include:

- **Landing Page**: Product listing with search (by name) and category filter, using Bootstrap 5.3.
- **Item Details**: Product details with add-to-basket option.
- **Basket**: CRUD operations (add, update, delete, clear) in session, with dynamic totals.
- **Checkout**: Validated delivery form (name, email, address, phone, delivery option), emphasizing Green Delivery ($2.00, eco-friendly).
- **Access Management**: User login, registration, and admin panel for product management, using plain-text passwords (note: insecure, for demo only).
- **Error Handling**: Custom 404 and 500 error pages.
- **Professional UI**: Responsive Bootstrap-Flask design, no form errors.
- **Sample Data**: 15 products, 6 categories, 6 users (2 admins), 3 orders.

Addresses Assessment 1 feedback:
- User stories: Search returns results in 500ms, Green Delivery highlighted.
- Schema: `Order_Items` models quantity, relationships verbalized.

## Setup Instructions

1. **Install Dependencies**: Run the commands above.
2. **Verify Images**: Ensure images (e.g., `orange.jpg`) are in `project/static/img/`.
3. **Run the Application**:
   ```bash
   python run.py
   ```
4. **Access the App**: Open `http://localhost:8888` in Google Chrome.

## Notes

- **Admin Credentials**: `admin1`/`admin1` or `admin2`/`admin2`.
- **Debug Mode**: `debug=False` for production. Use `debug=True` for development.
- **Port**: `port=8888`. Change to `5000` if needed.
- **Green Delivery**: Highlighted in checkout with $2.00 cost.
- **Demo**: Show search, basket, Green Delivery checkout, admin panel, and error pages in 4 minutes.
- **Security**: Plain-text passwords are used per workshop, but insecure. Use hashing (e.g., Bcrypt) in production.