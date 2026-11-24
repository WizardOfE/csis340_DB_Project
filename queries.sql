begin;
-- 1 done
select count(barcode) from food_product;
-- 2 done
select count(name) from ingredient;
-- 3 done
select name from food_product where name like '%Walker%';
-- 4 done
select * from additive where is_vegan = '1';
-- 5 done
select brand_name, count(brand_name) from food_product group by brand_name having count(brand_name) > 99;

-- 6 interpreting "average" NOVA group as "mode" TODO: unfinished
select brand_name, nova_group as mode_nova_group from (
  select brand_name, nova_group, count(nova_group) as foo from food_product group by nova_group, brand_name
)  

-- 7 done
select additive_code, count(additive_code) as count_adds from food_additive group by additive_code order by count_adds desc limit 1;

-- 8 need to change how average is found ig TODO: unfinished
select food_additive.food_barcode, avg(food_product.ns_point) from food_additive 
join food_product on food_product.barcode = food_additive.food_barcode
group by food_barcode having count(food_additive.food_barcode) > avg(food_additive.food_barcode);

-- 9 done
select ingredient_name from food_ingredient group by ingredient_name having count(ingredient_name) > 999;

-- 10 done
select avg(ns_point) from (
  select food_product.name, food_product.ns_point from food_product where food_product.barcode not in (
    select food_barcode from food_ingredient where food_ingredient.ingredient_name = 'wheat'
  )
);

-- 11 done
select allergen_name, count(allergen_name) as occurances from food_allergen group by allergen_name order by occurances desc limit 10;

-- 12 done
select f_all.allergen_name, count(f_ing.ingredient_name) as num_ingredients from food_allergen f_all
join food_product on f_all.food_barcode = food_product.barcode
join food_ingredient f_ing on food_product.barcode = f_ing.food_barcode
where f_all.allergen_name in (
  select allergen_name from food_allergen group by allergen_name order by count(allergen_name) desc limit 10
)
group by f_all.allergen_name; -- might need to aggregate based on wording of question

-- 13 done
select name from food_product where barcode in (
  select food_barcode from (select food_barcode, count(food_barcode) as num_ingredients from food_ingredient group by food_barcode) where num_ingredients > (
    select avg(fee) as average from (
      select food_barcode, count(food_barcode) as fee from food_ingredient group by food_barcode
    )
  ) and food_barcode in (
    select food_barcode from (select food_barcode, count(food_barcode) as num_allergens from food_allergen group by food_barcode) where num_allergens < (
      select avg(foo) as average from (
        select food_barcode, count(food_barcode) as foo from food_allergen group by food_barcode
      )
    )
  )
);

-- 14
-- TODO: skipped

-- 15 done
select p.name, count(f_nut) as nutrients, count(f_vit) as vitamins, count(f_all) as allergens, count(f_add) as additives from food_product p
join food_allergen f_all on p.barcode = f_all.food_barcode
join food_allergen f_add on p.barcode = f_add.food_barcode
join food_allergen f_nut on p.barcode = f_nut.food_barcode
join food_allergen f_vit on p.barcode = f_vit.food_barcode
where p.nova_group = '1'
group by p.name;

-- 16 done
select ingredient_name from food_ingredient group by ingredient_name order by count(ingredient_name) desc limit 1;

-- 17 done
select food_product.name from food_product 
join food_ingredient on food_ingredient.food_barcode = food_product.barcode
join food_allergen on food_allergen.food_barcode = food_product.barcode
where food_ingredient.ingredient_name in (
  select ingredient_name from food_ingredient group by ingredient_name order by count(ingredient_name) desc limit 1
) 
and food_allergen.allergen_name in (
  select allergen_name from food_allergen group by allergen_name order by count(allergen_name) desc limit 1
) 
group by food_product.name;

-- 18
-- TODO: skipped

-- 19
-- TODO: skipped

-- 20 done
select food_product.name from food_product 
join food_vitamin on food_vitamin.food_barcode = food_product.barcode
where food_vitamin.vitamin_name in (
  select vitamin_name from food_vitamin group by vitamin_name order by count(vitamin_name) asc limit 1
);
