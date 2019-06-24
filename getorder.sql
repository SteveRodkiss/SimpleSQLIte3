select * from pizzas inner join pizzaorders on pizzaorders.pizzaid=pizzas.id where pizzaorders.orderid=3

/*get pizzas ordered by a particular name*/
SELECT pizzas.name 
FROM pizzaorders
JOIN orders ON orders.id=pizzaorders.orderid
JOIN pizzas ON pizzas.id=pizzaorders.pizzaid
WHERE orders.ordername = "James"; 