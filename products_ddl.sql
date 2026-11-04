begin;

CREATE DATABASE foods;

\c foods

-- creating food products

CREATE TABLE food_product (
    barcode VARCHAR(255) primary key,
    name VARCHAR(255),
    serving_size VARCHAR(255),
    ns_grade char,
    ns_point INTEGER,
    nova_group VARCHAR(255),
    ecoscore INTEGER,
    brand_owner VARCHAR(255) 
    -- more columns relating products to other tables (probably a lot of foreign keys)
);

    
-- creating vitamin

CREATE TABLE vitamin (
    name varchar primary key,
    measuring_unit varchar,
    wikidata varchar
);


-- creating ingredient

CREATE TABLE ingredient (
    name varchar primary key,
    wikidata varchar
);


-- creating additive

CREATE TABLE additive (
    name varchar,
    is_vegan BOOLEAN,
    is_vegetarian BOOLEAN,
    code VARCHAR(255) primary key -- seams to not be int
);


-- creating nutrient

CREATE TABLE nutrient (
    name varchar primary key,
    measuring_unit varchar,
    wikidata varchar
);


-- creating allergen

CREATE TABLE allergen (
    name varchar primary key,
    wikidata varchar
);


-- table to relate food_product and vitamin

CREATE TABLE food_vitamin (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    food_barcode VARCHAR(255),
    vitamin_name VARCHAR(255),

    constraint fk_product_barcode
        foreign key (food_barcode)
        references food_product(barcode),

    constraint fk_product_vitamin
        foreign key (vitamin_name)
        references vitamin(name)
);


-- table to relate food_product and ingredient

CREATE TABLE food_ingredient (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    food_barcode VARCHAR(255),
    ingredient_name VARCHAR,

    constraint fk_product_barcode
        foreign key (food_barcode)
        references food_product(barcode),

    constraint fk_product_ingredient
        foreign key (ingredient_name)
        references ingredient(name)
);


-- table to relate food_product and additive

CREATE TABLE food_additive (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    food_barcode VARCHAR(255),
    additive_code VARCHAR,

    constraint fk_product_barcode
        foreign key (food_barcode)
        references food_product(barcode),

    constraint fk_product_additive
        foreign key (additive_code)
        references additive(code)
);


-- table to relate food_product and nutrient

CREATE TABLE food_nutrient (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    food_barcode VARCHAR(255),
    nutrient_name VARCHAR,

    constraint fk_product_barcode
        foreign key (food_barcode)
        references food_product(barcode),

    constraint fk_product_nutrient
        foreign key (nutrient_name)
        references nutrient(name)
);


-- table to relate food_product and allergen

CREATE TABLE food_allergen (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    food_barcode VARCHAR(255),
    allergen_name VARCHAR,

    constraint fk_product_barcode
        foreign key (food_barcode)
        references food_product(barcode),
    constraint fk_product_allergen
        foreign key (allergen_name)
        references allergen(name)
);



-- leaving commit; for terminal in case of bad command
