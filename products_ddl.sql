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
    name VARCHAR(255),
    id VARCHAR(255) primary key
);


-- creating ingredient

CREATE TABLE ingredient (
    name varchar,
    wikidata varchar primary key,
    parent varchar,
    child varchar
);


-- creating additive

CREATE TABLE additive (
    name varchar,
    is_vegan bit,
    is_vegetarian bit,
    code varchar primary key
);


-- creating nutrient

CREATE TABLE nutrient (
    name varchar,
    measuring_unit varchar,
    id varchar primary key
);


-- creating allergen

CREATE TABLE allergen (
    name varchar,
    wikidata varchar primary key
);


-- table to relate food_product and vitamin

CREATE TABLE food_vitamin (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    food_barcode VARCHAR(255),
    vitamin_id VARCHAR(255),

    constraint fk_product_barcode
        foreign key (food_barcode)
        references food_product(barcode),

    constraint fk_product_vitamin
        foreign key (vitamin_id)
        references vitamin(id)
);


-- table to relate food_product and ingredient

CREATE TABLE food_ingredient (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    food_barcode VARCHAR(255),
    ingredient_wikidata VARCHAR,

    constraint fk_product_barcode
        foreign key (food_barcode)
        references food_product(barcode),

    constraint fk_product_ingredient
        foreign key (ingredient_wikidata)
        references ingredient(wikidata)
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
    nutrient_id VARCHAR,

    constraint fk_product_barcode
        foreign key (food_barcode)
        references food_product(barcode),

    constraint fk_product_nutrient
        foreign key (nutrient_id)
        references nutrient(id)
);


-- table to relate food_product and allergen

CREATE TABLE food_allergen (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    food_barcode VARCHAR(255),
    allergen_wikidata VARCHAR,

    constraint fk_product_barcode
        foreign key (food_barcode)
        references food_product(barcode),
    constraint fk_product_allergen
        foreign key (allergen_wikidata)
        references allergen(wikidata)
);



-- leaving commit; for terminal in case of bad command
