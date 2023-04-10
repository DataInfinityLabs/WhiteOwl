// add event listener to the editcamera class form

$(document).ready(function() {

    $('.editcamera').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var camid =  form.find('[name="camid"]').val();
        var camname = form.find('[name="camname"]').val();
        var camurl = form.find('[name="camurl"]').val();

        // get the modal with the id of editcameramodal and update the values

        $('#editcameramodal').find('#id').val(camid);
        $('#editcameramodal').find('#name').val(camname);
        $('#editcameramodal').find('#url').val(camurl);
        
        $('#editcameramodal').modal('show');
    });
    
})


