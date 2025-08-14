-- create-table-purchase-orders
-- depends:

CREATE TABLE purchase_orders (
    id SERIAL PRIMARY KEY,
    po_number VARCHAR(50),
    po_date DATE,
    total_amount DECIMAL(10,2),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_po_number ON purchase_orders(po_number);
CREATE INDEX idx_po_date ON purchase_orders(po_date);


