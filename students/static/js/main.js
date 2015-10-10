
function initJournal () {
  var indicator = $('#ajax-progress-indicator');
  // var warmes = $('#ajax-progress-warmes');
  
	$('.day-box input[type="checkbox"]').click(function(event) {
		// alert('test');
    var box = $(this);
    $.ajax(box.data('url'), {
      'type': 'POST',
      'async': true,
      'dataType': 'json',
      'data': {
        'pk': box.data('student-id'),
        'date': box.data('date'),
        'present': box.is(':checked') ? '1': '',
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        // 'warmes':error
      },
      'beforeSend': function(xhr, settings){
        indicator.show();
      },
      'error': function(xhr, status, error){
        // var illia = "hello illia";
        // if (error) return illia;
        alert(gettext('There was an error on the server. Please, try again a bit later.'));
        indicator.hide();
        // warmes.text(error);
        // warmes.html(error);
        // warmes.show();
      },
      'success': function(data, status, xhr){
        indicator.hide();
        // warmes.hide();
        // alert(data['key']) ; also work
        // alert(data['status']);
      }
    });
  });
}

function initGroupSelector() {
  // look up select element with groups and attach our even handler
  // on field "change" event
  $('#group-selector select').change(function(event){
    // get value of currently selected group option
    var group = $(this).val();

    if (group) {
      // set cookie with expiration date 1 year since now;
      // cookie creation function takes period in days
      $.cookie('current_group', group, {'path': '/', 'expires': 365});
    } else {
      // otherwise we delete the cookie
      $.removeCookie('current_group', {'path': '/'});
    }

    // and reload a page
    location.reload(true);

    return true;
  });
}
function initDateFields() { 
    $('input.dateinput').datetimepicker({
      'format': 'YYYY-MM-DD',
      viewMode: 'years',
      icons: {
                    time: "fa fa-clock-o",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                },
      locale: 'uk'
  });
}
function initDateTimeFields() { 
    $('input.datetimeinput').datetimepicker({
      // viewMode: 'years',
      viewMode: 'months',
      'format': 'YYYY-MM-DD H:mm',

      locale: 'uk'
    });
    //          var inp = 'input.datetimeinput';

    // $(inp).wrap('<div class="input-group date" style="text-align:left"></div>');
    
    // $('<span class="input-group-addon">\
    //      <span class="glyphicon glyphicon-calendar"></span>\
    //    </span>').insertAfter(inp);
     
};

    // }).after("<span class='glyphicons glyphicons-bus'></span>");
  // }).after(<span class="input-group-addon"><i class="glyphicon glyphicon-th"></i></span>);
  // }).after("<span class='form-control-addon'>test</span>");


function initEditStudentPage() { 
  $('a.student-edit-form-link').click(function(event){
    var link = $(this);
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        // check if we got successfull response from the server
        if (status != 'success') {
          alert(gettext('There was an error on the server. Please, try again a bit later.'));
          // alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
          return false;
        }
        // update modal window with arrived content from the server
        var modal = $('#myModal'), 
              html = $(data), form = html.find('#content-column form');
            modal.find('.modal-title').html(html.find('#content-column h2').text());
            modal.find('.modal-body').html(form);

        // init our edit form
        initEditStudentForm(form, modal);

        // setup and show modal window finally
        modal.modal({
          'keyboard':false,
          'backdrop':false,
          'show':true
        }); 
      },
      'error': function(){
          alert(gettext('There was an error on the server. Please, try again a bit later.'));
          // alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
          return false
      }
    });
      
    return false;
  });
}

function initEditStudentForm(form, modal) {
  // attach datepicker
  initDateFields();

  // close modal window on Cancel button click
  form.find('input[name="cancel_button"]').click(function(event){
    modal.modal('hide');
    return false;
  });

  // make form work in AJAX mode
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
        alert(gettext('There was an error on the server. Please, try again a bit later.'));
        return false;
    },
    'success': function(data, status, xhr) {
      var html = $(data), newform = html.find('#content-column form');

      // copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      // copy form to modal if we found it in server response
      if (newform.length > 0) {
        modal.find('.modal-body').append(newform);

        // initialize form fields and buttons
        initEditStudentForm(newform, modal);
      } else {
        // if no form, it means success and we need to reload page
        // to get updated students list;
        // reload after 2 seconds, so that user can read success message
        setTimeout(function(){location.reload(true);}, 2000);
      }
    }
  });
}

// function initEditStudentPage() { 
//   $('a.student-edit-form-link').click(function(event){
//     var modal = $('#myModal'); 
//     modal.modal('show'); 
//     return false;
// });
// };


// functions for Groups
function initEditGroupPage() { 
//   $('a.group-edit-form-link').click(function(event){
//     var modal = $('#myModal1'); 
//     modal.modal('show'); 
//     return false;
// });
// ---------------------------------------------------------------
  var ajaxBusy = $('#ajaxBusy');

  $('a.group-edit-form-link').click(function(event){
    var link = $(this);
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
    'beforeSend': function(xhr, settings) {
       ajaxBusy.show();
    },
    'complete': function(xhr, settings){
       ajaxBusy.hide();
    },
      'success': function(data, status, xhr){
        // check if we got successfull response from the server
        if (status != 'success') {
          alert(gettext('There was an error on the server. Please, try again a bit later.'));
          return false;
        }
        // update modal window with arrived content from the server
        var modal = $('#myModal1'), 
              html = $(data), form = html.find('#content-column form');
                modal.find('.modal-title').html(html.find('#content-column h2').text());
                // modal.find('.modal-body').html(form);
                modal.find('.modal-footer').html(form);

        // init our edit form
        initEditGroupForm(form, modal);

        // setup and show modal window finally
        modal.modal({
          'keyboard':false,
          'backdrop':false,
          'show':true
        }); 
      },
      'error': function(){
          alert(gettext('There was an error on the server. Please, try again a bit later.'));
          return false
      }
    });
      
    return false;
  });

};

// functions for Groups
function initEditGroupForm(form, modal) {
  // attach datepicker
  // initDateTimeFields();
  var ajaxBusy = $('#ajaxBusy');

  // close modal window on Cancel button click
  form.find('input[name="cancel_button"]').click(function(event){
    modal.modal('hide');
    return false;
  });
  // make form work in AJAX mode
  form.ajaxForm({
    'dataType': 'html',
    // 'beforeSend': function() {
    //    ajaxBusy.show();
    // },
    // 'complete': function(){
    //    ajaxBusy.hide();
    // },
    // beforeSubmit: function(){
    //   ajaxBusy.show();
    //   return true;
    // },
    'error': function(){
        alert(gettext('There was an error on the server. Please, try again a bit later.'));
        return false;
    },
    // beforeSend: function() {
    //  $('#loader').show();
    // },
    // complete: function(){
    //    $('#loader').hide();
    // },
  // success: function() {}
    'success': function(data, status, xhr) {
      var html = $(data), newform = html.find('#content-column form');

      // copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      // copy form to modal if we found it in server response
      if (newform.length > 0) {
        modal.find('.modal-body').append(newform);

        // initialize form fields and buttons
        initEditGroupForm(newform, modal);
      } else {
        // if no form, it means success and we need to reload page
        // to get updated students list;
        // reload after 2 seconds, so that user can read success message
        setTimeout(function(){location.reload(true);}, 1500);
      }
    }
  });
}



// function from forum. I dont understand, what change after this function.
// function updatePageContext() {
//     var url = window.location.href;  
//     $.ajax({
//         'url': url,
//         'dataType': 'html',
//         'type': 'get',
//         'success': function(data, status, xhr){
//             // check if we got successfull response from the server
//             if (status != 'success') {
//                 alert('Ошибка на сервере, попробуйте пожалуйста позже.');
//                 return false;
//             }
//             // update modal window with arrived content from the server
//             var table = $('.table'), newpage = $(data), newtable = newpage.find('.table');
//             table.html(newtable);
//             initEditStudentPage();
//         },

//         'error': function(){
//             alert('Ошибка на сервере, попробуйте пожалуйста позже.');
//             return false;
//         }
//     });
//     return false;
// }

function initEditExamPage() { 
//   $('a.group-edit-form-link').click(function(event){
//     var modal = $('#myModal1'); 
//     modal.modal('show'); 
//     return false;
// });
// ---------------------------------------------------------------
  $('a.exam-edit-form-link').click(function(event){
    var link = $(this);
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        // check if we got successfull response from the server
        if (status != 'success') {
          alert(gettext('There was an error on the server. Please, try again a bit later.'));
          return false;
        }
        // update modal window with arrived content from the server
        var modal = $('#myModal1'), 
              html = $(data), form = html.find('#content-column form');
                modal.find('.modal-title').html(html.find('#content-column h2').text());
                // modal.find('.modal-body').html(form);
                modal.find('.modal-footer').html(form);

        // init our edit form
        initEditExamForm(form, modal);

        // setup and show modal window finally
        modal.modal({
          'keyboard':false,
          'backdrop':false,
          'show':true
        }); 
      },
      'error': function(){
          alert(gettext('There was an error on the server. Please, try again a bit later.'));
          return false
      }
    });
      
    return false;
  });

};

// functions for Exams
function initEditExamForm(form, modal) {
  // attach datepicker
  initDateTimeFields();

  // close modal window on Cancel button click
  form.find('input[name="cancel_button"]').click(function(event){
    modal.modal('hide');
    return false;
  });

  // make form work in AJAX mode
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
        alert(gettext('There was an error on the server. Please, try again a bit later.'));
        return false;
    },
    'success': function(data, status, xhr) {
      var html = $(data), newform = html.find('#content-column form');

      // copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      // copy form to modal if we found it in server response
      if (newform.length > 0) {
        modal.find('.modal-body').append(newform);

        // initialize form fields and buttons
        initEditExamForm(newform, modal);
      } else {
        // if no form, it means success and we need to reload page
        // to get updated students list;
        // reload after 2 seconds, so that user can read success message
        setTimeout(function(){location.reload(true);}, 1500);
      }
    }
  });
}





$(document).ready(function () {
	initJournal();
  initGroupSelector();
  initDateFields();
  initDateTimeFields();
  initEditStudentPage();
  initEditGroupPage();
  // updatePageContext();
  initEditExamPage();
});

    // Setup the ajax indicator
// $(document).ajaxStart(function(){ 
//   $('#ajaxBusy').show(); 
// }).ajaxStop(function(){ 
//   $('#ajaxBusy').hide();
// });


