begin;

-- creating food products

CREATE TABLE food_product (
    barcode int[13] primary key,
    name varchar,
    serving_size varchar,
    ns_grade char,
    ns_point int[3],
    nova_group varchar,
    ecoscore int[3],
    brand_owner varchar
    
    -- more columns relating products to other tables (probably a lot of foreign keys)
    )

    
-- creating vitamin

CREATE TABLE vitamin (
    name varchar,
    id varchar primary key
)


-- creating ingredient

CREATE TABLE ingredient (
    name varchar,
    wikidata varchar primary key,
    parent varchar,
    child varchar
)


-- creating additive

CREATE TABLE additive (
    name varchar,
    is_vegan bit,
    is_vegetarian bit,
    additive_code varchar primary key
)


-- creating nutrient

CREATE TABLE nutrient (
    name varchar,
    measuring_unit varchar,
    id varchar primary key
)


-- creating allergen

CREATE TABLE allergen (
    name varchar,
    wikidata varchar primary key
)


-- table to relate food_product and vitamin

CREATE TABLE food_vitamin (
    constraint fk_product_barcode
    foreign key (barcode)
    references food_product(barcode),
    constraint fk_product_vitamin
    foreign key (id)
    references vitamin(id)
)


-- table to relate food_product and ingredient

CREATE TABLE food_ingredient (
    constraint fk_product_barcode
    foreign key (barcode)
    references food_product(barcode),
    constraint fk_product_ingredient
    foreign key (wikidata)
    references ingredient(wikidata)
)


-- table to relate food_product and additive

CREATE TABLE food_additive (
    constraint fk_product_barcode
    foreign key (barcode)
    references food_product(barcode),
    constraint fk_product_additive
    foreign key (additive_code)
    references additive(additive_code)
)


-- table to relate food_product and nutrient

CREATE TABLE food_nutrient (
    constraint fk_product_barcode
    foreign key (barcode)
    references food_product(barcode),
    constraint fk_product_nutrient
    foreign key (id)
    references nutrient(id)
)


-- table to relate food_product and allergen

CREATE TABLE food_allergen (
    constraint fk_product_barcode
    foreign key (barcode)
    references food_product(barcode),
    constraint fk_product_allergen
    foreign key (wikidata)
    references allergen(wikidata)
)



-- leaving commit; for terminal in case of bad command
