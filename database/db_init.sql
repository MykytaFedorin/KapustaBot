CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE Product (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price DECIMAL(10, 2),
    image_url VARCHAR(255)
);

CREATE TABLE Order_ (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES Customer(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2),
    status VARCHAR(20)
);

CREATE TABLE OrderItems (
    item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Order_(order_id),
    product_id INT REFERENCES Product(product_id),
    quantity INT,
    subtotal DECIMAL(10, 2)
);

