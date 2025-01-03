﻿//Метод «Заміна коментаря методом» 
//Код до рефакторингу:
public class Order
{
    public double price;
    public double CalculateTotal()
    {
        // Calculate the total price with tax
        double tax = price * 0.2;
        return price + tax;
    }
}

//Код після рефакторингу:
public class Order
{
    public double price;
    public double CalculateTotal()
    {
        return CalculateTotalPriceWithTax(price);
    }
    private double CalculateTotalPriceWithTax(double price)
    {
        double tax = price * 0.2;
        return price + tax;
    }
}

//Метод «Видалення невикористовуваного коду» 
//Код до рефакторингу:
public class Order
{
    public double price;
    public double discount;
    public double CalculateTotal()
    {
        double tax = price * 0.2;
        double total = price + tax;
        // Старі обчислення, які більше не актуальні
        double unusedDiscount = discount * 0.1;
        return total;
    }
}

//Код після рефакторингу:
public class Order
{
    public double price;
    public double CalculateTotal()
    {
        double tax = price * 0.2;
        return price + tax;
    }
}

//Метод «Перейменування змінних» 
//Код до рефакторингу:
public class Order
{
    public double a;
    public double b;
    public double CalculateTotal()
    {
        double tax = a * 0.2;
        return a + tax + b;
    }
}

//Код після рефакторингу:
public class Order
{
    public double price;
    public double discount;
    public double CalculateTotal()
    {
        double tax = price * 0.2;
        return price + tax + discount;
    }
}

