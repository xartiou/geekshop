window.onload = function () {
    let _quantity, _price, orderitems_num, delta_quantity, orderitems_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];

    let TOTAL_FORMS = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());
    console.log(TOTAL_FORMS);
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for (let i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        if(_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }
    console.log(quantity_arr);
    console.log(price_arr);
    if (!order_total_quantity) {
        orderSummaryRecalc();
    }

//    события
    $('.order_form').on('click', 'input[type=number]', function() {
        let target = event.target;
        orderitems_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitems_num]) {
            orderitems_quantity = parseInt(target.value);
            delta_quantity = orderitems_quantity - quantity_arr[orderitems_num];
            quantity_arr[orderitems_num] = orderitems_quantity;
            orderSummaryUpdate(price_arr[orderitems_num], delta_quantity);
        }
    });

// событие на удаление (при нажатии на кнопку "Удаление")
    $('.order_form').on('click', 'input[type=checkbox]', function() {
        let target = event.target;
        orderitems_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (target.checked) {
            delta_quantity = - quantity_arr[orderitems_num];
        } else {
            delta_quantity = quantity_arr[orderitems_num];
        }
        orderSummaryUpdate(price_arr[orderitems_num], delta_quantity);
    });

// событие на изменение наименования товара
    $('.order_form').on('change', 'select', function() {
       let target = event.target;
       orderitems_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
       let orderitems_product_pk = target.options[target.selectedIndex].value;

       $.ajax({
           url: '/orders/products/' + orderitems_product_pk + '/price/',
           success: function(data){
           console.log(data);
           console.log(TOTAL_FORMS);
               if (data.price) {
                   price_arr[orderitems_num] = parseFloat(data.price);
                   let price_html = "<span>" + data.price.toString().replace('.', ',') + "</span>"руб.;
                   let curr_tr = $('.order_form table').find('tr:eq(' + (orderitems_num + 1) + ')');
                   curr_tr.find('td:eq(2)').html(price_html);
                   orderSummaryRecalc();
               }
           },
       });
    });
// функция для пересчета цены при смене товара
    function orderSummaryRecalc() {
        order_total_quantity = 0;
        order_total_cost = 0;
        for (let i=0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }


//    общая функция обновления данных
    function orderSummaryUpdate(orderitems_price, delta_quantity) {
        delta_cost = orderitems_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity
        $('.order_total_quantity').html(order_total_quantity);
        $('.order_total_cost').html(order_total_cost);
    }

//  подключаем formset для formset_row
    $('.formset_row').formset( {
        //    опции
        addText: 'добавить продукт',
        deleteText: 'Удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });
// функция удаления строки
    function deleteOrderItem(row) {
        delta_quantity = -quantity_arr[orderitems_num]
        orderSummaryUpdate(price_arr[orderitems_num], delta_quantity);
        let target_name = row[0].querySelector('input[type=number]').name;
        orderitems_num = target_name.replace('orderitems-', '').replace('-quantity', '');
    }

}