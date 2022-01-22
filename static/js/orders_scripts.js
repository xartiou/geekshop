window.onload = function () {

//    нам нужны переменные
    let _quantity, _price, orderitems_num, delta_quantity, orderitems_quantity, delta_cost

    let quantity_arr = [];
    let price_arr = [];

// получаем количество строк
    let TOTAL_FORMS = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());
    console.log(TOTAL_FORMS)

// получаем общее количество и сумму
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    // console.log(order_total_quantity)
    // console.log(order_total_cost)

// считываем количество каждого продукта и его цену в quantity_arr и price_arr в цикле
    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }

// выводим в консоль
    console.info('QUANTITY', quantity_arr)
    console.info('PRICE', price_arr)


// 1 метод для получения количества, цены и суммы
    $('.order_form').on('click', 'input[type=number]', function () {
            let target = event.target;
            orderitems_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
            if (price_arr[orderitems_num]) {
                orderitems_quantity = parseInt(target.value);
                delta_quantity = orderitems_quantity - quantity_arr[orderitems_num];
                quantity_arr[orderitems_num] = orderitems_quantity;
                orderSummaryUpdate(price_arr[orderitems_num], delta_quantity);
            }
        }
    );

    // метод общий для пересчета количества, цены
    function orderSummaryUpdate(orderitems_price, delta_quantity) {
        delta_cost = orderitems_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_cost.toString() + ',00');

    };
//    function orderSummaryUpdate(orderitem_price, delta_quantity){
//        delta_cost = orderitem_price * delta_quantity;
//
//        order_total_cost = Number((order_total_cost + delta_cost). toFixed(2));
//        order_total_quantity = order_total_quantity + delta_quantity;
//
//        $('.order_total_quantity').html(order_total_quantity);
//        $('.order_total_cost').html(order_total_cost);
//
//
//    }

//2 метод для реакции на удалить
    $('.order_form').on('click', 'input[type=checkbox]', function () {
            let target = event.target
            orderitems_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
            if (target.checked) {
                delta_quantity = -quantity_arr[orderitems_num];

            } else {
                delta_quantity = quantity_arr[orderitems_num];
            }
            orderSummaryUpdate(price_arr[orderitems_num], delta_quantity);
        }
    );

// метод общий для пересчета количества, цены
    function orderSummaryUpdate(orderitems_price, delta_quantity) {
        delta_cost = orderitems_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_cost.toString() + ',00');

    };

// добавляем кнопки действий
    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'Удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });

// функция удаления
    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type="number"]').name;
        orderitems_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitems_num];
        orderSummaryUpdate(price_arr[orderitems_num], delta_quantity);
    };


};