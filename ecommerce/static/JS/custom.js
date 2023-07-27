$(function() {
    $(document).on('click', '.increment-btn', function(e) {
      e.preventDefault();

      var inc_value = $(this).closest('.input-group').find('.qty-input').val();
      var value = parseInt(inc_value, 10);
      value = isNaN(value) ? 0 : value;
      if (value < 10) {
        value++;
        $(this).closest('.input-group').find('.qty-input').val(value);
      }
    });

    $(document).on('click', '.decrement-btn', function(e) {
      e.preventDefault();

      var dec_value = $(this).closest('.input-group').find('.qty-input').val();
      var value = parseInt(dec_value, 10);
      value = isNaN(value) ? 0 : value;
      if (value > 1) {
        value--;
        $(this).closest('.input-group').find('.qty-input').val(value);
      }
    });

    $(document).on('click','.addtocartbtn',function (e){
      e.preventDefault();

      var product_id=$(this).closest('.product_data').find('.prod_id').val();
      var product_qty=$(this).closest('.product_data').find('.qty-input').val();
      var token =$('input[name=csrfmiddlewaretoken]').val();
      $.ajax({
        type : "POST",
        url: "/cart-to-cart",
        data:{
          'product_id':product_id,
          'product_qty':product_qty,
          csrfmiddlewaretoken:token
        },
       
       success:function(response){
          alertify.success(response.status)

        }
      });
      
    })
    $(document).on('click','.changeQuantity',function (e){
      e.preventDefault();

      var product_id=$(this).closest('.product_data').find('.prod_id').val();
      var product_qty=$(this).closest('.product_data').find('.qty-input').val();
      var token =$('input[name=csrfmiddlewaretoken]').val();
      $.ajax({
        type : "POST",
        url: "/update-cart",
        data:{
          'product_id':product_id,
          'product_qty':product_qty,
          csrfmiddlewaretoken:token
        },
       
       success:function(response){
          alertify.success(response.status)

        }
      });
      
    })

    $('.delete-cart-item').click(function (e) { 
      e.preventDefault();

      var product_id=$(this).closest('.product_data').find('.prod_id').val();
      var token =$('input[name=csrfmiddlewaretoken]').val();

      $.ajax({
        type: "Post",
        url: "delete-cart-item",
        data: {
            'product_id':product_id,
            csrfmiddlewaretoken:token
        },
        success: function (response) {
          alertify.success(response.status)
          $('.cartdata').load(location.href + " .cartdata")
          
        }
      });
      
    });


  });