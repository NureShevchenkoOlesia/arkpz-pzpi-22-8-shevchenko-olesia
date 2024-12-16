//рекомендація 1: розділяти файли за функціоналом та використовувати структуру папок для модульності
//приклад:
src /
    components /
    services /
    utils /

//рекомендація 2: додавати коментарі для відділення великих секцій коду
//приклад:
// --- User API Functions ---

//рекомендація 3: для форматування коду використовувати 2 пробіли для розділення сегментів, 
//обмежуватися в 80-100 символами на рядок, відкриті дужки залишати на тому ж рядку
//приклад:
if (isValid) {
    console.log("Valid");
} else {
    console.log("Invalid");
}


//рекомендація 4: для іменування використовувати CamelCase для змінних та функцій, 
//UPPER_SNAKE_CASE для констант, і PascalCase для класів. імена обирати зрозумілі та логічні

//рекомендація 5: уникати «магічних чисел»
//приклад:
//поганий код
if (userAge > 18) {

    //гарний код 
    const ADULT_AGE = 18;
    if (userAge > ADULT_AGE) { }
}

//рекомендація 6: dикористовувати коментарі для пояснення логіки, а не очевидного синтаксису
//приклад:
//поганий код
// Цикл проходить по масиву
for (let i = 0; i < array.length; i++) {
    console.log(array[i]);
}

//гарний код 
// Перевіряємо наявність користувача у списку
const isUserPresent = users.includes(targetUser);

//рекомендація 7: використовувати JSDoc для документування функцій, класів і модулів
//приклад:
/**
* Обчислює суму двох чисел
* @param {number} a - перше число
* @param {number} b - друге число
* @returns {number} - сума чисел
*/
function add(a, b) {
    return a + b;
}

//рекомендація 8: використовувати Git Hooks для запуску перевірок перед комітом

//розбір загального прикладу:
//поганий код
async function data(id) {
    const res = await fetch(`/api/users/${id}`);
    return res.json();
}

//гарний код 
// Функція для отримання даних користувача
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) throw new Error("Failed to fetch user data");
        return await response.json();
    } catch (error) {
        console.error(error);
    }
}