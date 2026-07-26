# Cleaning Decision Log Draft

- `geolocation` duplicates: keep for now; duplicate ZIP-prefix coordinate rows likely represent repeated geolocation reference records rather than a transactional error.
- `orders.order_approved_at` missing: flag; missing approval timestamps can indicate orders that were approved outside the captured system or not yet approved.
- `orders.order_delivered_carrier_date` missing: flag; null carrier dates are likely structural for undelivered or cancelled orders.
- `orders.order_delivered_customer_date` missing: flag; null customer delivery dates are likely structural for undelivered or partially fulfilled orders.
- `order_reviews.review_comment_title` missing: keep/flag; marketplace review comments are often optional and partially blank even when ratings exist.
- `order_reviews.review_comment_message` missing: keep/flag; review narrative fields are commonly sparse and should be treated as optional text.
- `products.product_category_name` missing: flag; product catalog labels may be incomplete for legacy or untranslated listings.
- `products` product metadata missing: flag; missing product dimensions/text fields are often catalog sparsity rather than broken records.
