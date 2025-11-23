-- Task 1

SELECT
    c.name,
    COUNT(fc.film_id) count_films
FROM category c
JOIN film_category fc
  ON c.category_id = fc.category_id
GROUP BY c.name
ORDER BY count_films DESC;

-- Task 2

SELECT
    a.first_name,
    a.last_name,
    COUNT(r.rental_id) AS total_rentals
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN inventory i ON fa.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY a.actor_id
ORDER BY total_rentals DESC
LIMIT 10;

-- Task 3

SELECT
    c.name,
    SUM(p.amount) AS payment
FROM category c
JOIN public.film_category fc on c.category_id = fc.category_id
JOIN inventory i ON fc.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY c.category_id
ORDER BY payment DESC
LIMIT 1;

-- Task 4

SELECT
    f.title
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
WHERE i.inventory_id IS NULL;

-- Task 5

WITH ActorStats AS (
    SELECT
        a.first_name,
        a.last_name,
        COUNT(f.film_id) AS film_count
    FROM actor a
    JOIN film_actor fa ON a.actor_id = fa.actor_id
    JOIN film f ON fa.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = 'Children'
    GROUP BY a.actor_id, a.first_name, a.last_name
),
RankedActors AS (
    SELECT
        *,
        DENSE_RANK() OVER (ORDER BY film_count DESC) as rank_position
    FROM ActorStats
)
SELECT first_name, last_name, film_count
FROM RankedActors
WHERE rank_position <= 3;

-- Task 6

SELECT
    ci.city,
    SUM(CASE WHEN c.active = 1 THEN 1 ELSE 0 END) AS active_customers,
    SUM(CASE WHEN c.active = 0 THEN 1 ELSE 0 END) AS inactive_customers
FROM city ci
JOIN address a ON ci.city_id = a.city_id
JOIN customer c ON a.address_id = c.address_id
GROUP BY ci.city
ORDER BY inactive_customers DESC;

-- Task 7

WITH CityRentals AS (

    SELECT
        'Starts with a' AS group_name,
        cat.name AS category_name,
        EXTRACT(EPOCH FROM (r.return_date - r.rental_date)) / 3600 AS hours
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film_category fc ON i.film_id = fc.film_id
    JOIN category cat ON fc.category_id = cat.category_id
    JOIN customer c ON r.customer_id = c.customer_id
    JOIN address a ON c.address_id = a.address_id
    JOIN city ci ON a.city_id = ci.city_id
    WHERE ci.city LIKE 'a%' OR ci.city LIKE 'A%'

    UNION ALL

    SELECT
        'Contains -' AS group_name,
        cat.name AS category_name,
        EXTRACT(EPOCH FROM (r.return_date - r.rental_date)) / 3600 AS hours
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film_category fc ON i.film_id = fc.film_id
    JOIN category cat ON fc.category_id = cat.category_id
    JOIN customer c ON r.customer_id = c.customer_id
    JOIN address a ON c.address_id = a.address_id
    JOIN city ci ON a.city_id = ci.city_id
    WHERE ci.city LIKE '%-%'
),
CategorySums AS (
    SELECT
        group_name,
        category_name,
        SUM(hours) AS total_hours
    FROM CityRentals
    WHERE hours IS NOT NULL
    GROUP BY group_name, category_name
),
RankedCategories AS (
    SELECT
        group_name,
        category_name,
        total_hours,
        RANK() OVER (PARTITION BY group_name ORDER BY total_hours DESC) as rnk
    FROM CategorySums
)
SELECT group_name, category_name, total_hours
FROM RankedCategories
WHERE rnk = 1;